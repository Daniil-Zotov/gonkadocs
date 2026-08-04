#!/usr/bin/env python3
"""
Activity Feed — change detection engine for Gonka Docs.

Tracks changes in synced data directories (proposals, pre-proposals,
discussions, issues, protocol docs) and generates structured events
for the community activity feed.

Usage:
    activity-feed.py snapshot --dir PATH --section NAME --manifest PATH
    activity-feed.py detect   --dir PATH --section NAME --manifest PATH
                              --events PATH [--ai]
    activity-feed.py backfill --events PATH
    activity-feed.py daily-reminder --dir PATH --events PATH
"""

import argparse
import hashlib
import json
import os
import re
import secrets
import sys
from datetime import datetime, timezone
from pathlib import Path


# ── constants ─────────────────────────────────────────────────

CONTENT_PREVIEW_LEN = 800

_FRONTMATTER_RE = re.compile(r'^---\s*\n.*?^---\s*\n', re.DOTALL | re.MULTILINE)

# ── helpers ────────────────────────────────────────────────────


def _strip_timestamps(text: str) -> str:
    """Remove sync timestamps that change on every update, so that
    timestamp-only changes don't alter the checksum."""
    # Issues: ``Updated: `2026-07-11 03:49 UTC`.``
    text = re.sub(r'(?m)^Updated:\s*`\d{4}-\d{2}-\d{2} \d{2}:\d{2} UTC`\.?\s*$', '', text)
    # Issues detail: `<span ...>Updated 2026-07-11 03:49 UTC</span>`
    text = re.sub(r'Updated \d{4}-\d{2}-\d{2} \d{2}:\d{2} UTC', '', text)
    # Discussions: ``Обновлено: `2026-07-13 11:25 UTC`.``
    text = re.sub(r'Обновлено:\s*`\d{4}-\d{2}-\d{2} \d{2}:\d{2} UTC`\.?\s*', '', text)
    # Discussions detail: `**Обновлено:** 2026-07-13 11:25 UTC`
    text = re.sub(r'\*\*Обновлено:\*\*\s*\d{4}-\d{2}-\d{2} \d{2}:\d{2} UTC', '', text)
    # Discussion frontmatter: `synced_at: 2026-07-13T11:25:00Z`
    text = re.sub(r'(?m)^synced_at:\s*\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z\s*$', '', text)
    # Proposals/preproposals: `Last updated: 2026-07-13 12:00 UTC`
    text = re.sub(r'Last updated:\s*\d{4}-\d{2}-\d{2} \d{2}:\d{2} UTC', '', text)
    return text


def content_preview(content: str, max_len: int = CONTENT_PREVIEW_LEN) -> str:
    cleaned = _FRONTMATTER_RE.sub('', content, count=1)
    cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
    return cleaned.strip()[:max_len]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()


def sha256_str(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def make_event_id() -> str:
    ts = datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')
    rand = secrets.token_hex(4)
    return f'evt_{ts}_{rand}'


SECTION_LABELS = {
    'proposals':    'On-Chain Proposals',
    'preproposals': 'Pre-Proposals',
    'discussions':  'Discussions',
    'issues':       'Issues',
    'gonka_docs':   'Protocol Docs',
    'calendar':     'Calendar',
}

ACTION_LABELS = {
    'new':             'Added',
    'deleted':         'Removed',
    'updated':         'Updated',
    'status_changed':  'Status Changed',
    'quorum_reached':  'Quorum Reached',
    'daily_reminder':  'Today',
}


# ── proposal-specific extraction ──────────────────────────────

def _extract_funding(content: str) -> str:
    lines = []
    for m in re.finditer(r'prop-funding-line[^>]*>([^<]+)', content):
        lines.append(m.group(1).strip())
    if lines:
        return ' · '.join(lines)
    return ''


def _extract_quorum(content: str) -> bool | None:
    m = re.search(r'class="prop-tally-(yes|veto)-text">([✓✗]) Turnout', content)
    if m:
        return m.group(2) == '✓'
    return None


def _extract_voting_end(content: str) -> str:
    m = re.search(r'\*\*Voting:\*\*.*?→\s*(.+?)\n', content)
    if m:
        return m.group(1).strip()
    return ''


def _extract_description(content: str) -> str:
    m = re.search(r'^description:\s*"?(.+?)"?\s*$', content, re.MULTILINE)
    if m:
        return m.group(1).strip()
    return ''


# ── metadata extraction ────────────────────────────────────────

def _is_detail_page(rel_path: Path, section: str) -> bool:
    """Check if the file is a detail page (not an overview/index/label page).

    Proposals: 2026-q3/85/index.md → detail (3+ parts)
               index.md, 2026-q3/index.md → overview (1-2 parts)
    Preproposals: {uuid}/index.md → detail (2+ parts)
                  index.md → overview (1 part)
    Issues: 01466-something.md → detail
            index.md, labels/no-label/index.md → skip (overview/label page)
    Discussions: proposals/1464-something.md → detail
                 index.md, proposals/index.md → skip (overview/category page)
    Gonka docs: network-updates.md → detail
                index.md → skip (overview page)
    """
    parts = rel_path.parts
    # Skip index pages for all sections
    if parts[-1] == 'index.md':
        return False
    if section == 'proposals':
        return len(parts) >= 3
    elif section == 'preproposals':
        return len(parts) >= 2
    elif section == 'issues':
        # Only track individual issue files (not label overviews in subdirs)
        return len(parts) == 1
    elif section == 'discussions':
        # Only track individual discussion files (not category/index pages)
        return len(parts) >= 2
    return True

def _extract_title(content: str, fallback: str) -> str:
    m = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if m:
        t = m.group(1).strip()
        if len(t) < 300:
            return t
    m = re.search(r'^title:\s*"?(.+?)"?\s*$', content, re.MULTILINE)
    if m:
        return m.group(1).strip()
    return fallback


def _extract_comment_bodies(content: str) -> list[str]:
    """Extract all comment body texts from an issue page."""
    bodies = []
    for m in re.finditer(
        r'<div class="issues-comment-body[^"]* issues-content">(.*?)</div>\s*</div>',
        content, re.DOTALL
    ):
        text = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        if text:
            lines = [l.strip() for l in text.split('\n') if l.strip()]
            bodies.append(' '.join(lines)[:400])
    return bodies


def _comment_checksum(content: str) -> str:
    """Hash of all comment texts for change detection."""
    bodies = _extract_comment_bodies(content)
    return sha256_str('|'.join(bodies))


def _extract_proposal_status(content: str):
    m = re.search(r'prop-badge\s+prop-(\w+)', content)
    if m:
        return m.group(1)
    m = re.search(r'(PROPOSAL_STATUS_\w+)', content)
    if m:
        return m.group(1)
    return None


def extract_metadata(section: str, rel_path: Path, content: str) -> dict:
    meta = {
        'title': _extract_title(content, rel_path.stem),
        'status': None,
        'content_preview': content_preview(content),
    }

    if section == 'proposals':
        if _is_detail_page(rel_path, section):
            meta['status'] = _extract_proposal_status(content)
            meta['funding'] = _extract_funding(content)
            meta['quorum_met'] = _extract_quorum(content)
            meta['voting_end'] = _extract_voting_end(content)
            meta['description'] = _extract_description(content)

    elif section == 'preproposals':
        if _is_detail_page(rel_path, section):
            if '🟢 Active' in content:
                meta['status'] = 'active'
            elif '🔴 Expired' in content:
                meta['status'] = 'expired'

    elif section == 'issues':
        if re.search(r'\bstate:\s*open\b', content, re.IGNORECASE):
            meta['status'] = 'open'
        elif re.search(r'\bstate:\s*closed\b', content, re.IGNORECASE):
            meta['status'] = 'closed'
        meta['comment_checksum'] = _comment_checksum(content)
        meta['comment_bodies'] = _extract_comment_bodies(content)

    return meta


# ── directory scanning ─────────────────────────────────────────

def scan_directory(dir_path: Path, section: str) -> dict:
    files = {}
    if not dir_path.exists():
        return files
    for fpath in sorted(dir_path.rglob('*.md')):
        rel = fpath.relative_to(dir_path)
        # skip overview/index pages for proposals and preproposals
        if not _is_detail_page(rel, section):
            continue
        # skip Chinese documentation translations
        if str(rel).startswith('zh/'):
            continue
        rel = str(rel)
        try:
            content = fpath.read_text(encoding='utf-8')
            content = _strip_timestamps(content)
            meta = extract_metadata(section, fpath, content)
            meta['checksum'] = sha256_str(content)
            files[rel] = meta
        except Exception as e:
            print(f'  Warning: could not read {fpath}: {e}', file=sys.stderr)
    return files


# ── calendar scanning ─────────────────────────────────────────

def _calendar_fingerprint(event: dict) -> str:
    """Stable identity for a calendar event across syncs."""
    return sha256_str(
        '|'.join([
            str(event.get('date', '')),
            str(event.get('title', '')),
            str(event.get('url', '')),
        ])
    )


def scan_calendar(dir_path: Path) -> dict:
    """Scan calendar JSON files (excluding manifest.json).

    Returns {fingerprint: meta} so new events are detected by identity,
    not by whole-file checksum (files hold many events).
    """
    files = {}
    if not dir_path.exists():
        return files

    for json_path in sorted(dir_path.glob('*.json')):
        if json_path.name == 'manifest.json':
            continue
        try:
            data = json.loads(json_path.read_text(encoding='utf-8'))
        except (json.JSONDecodeError, OSError):
            continue

        items = data if isinstance(data, list) else data.get('events', [])
        for ev in items:
            if not isinstance(ev, dict) or not ev.get('date') or not ev.get('title'):
                continue
            fp = _calendar_fingerprint(ev)
            meta = {
                'title': str(ev.get('title', '')).strip(),
                'date': str(ev.get('date', '')),
                'time': str(ev.get('time', '')).strip(),
                'event_type': str(ev.get('type', '')),
                'url': str(ev.get('url', '')),
                'content_preview': str(ev.get('description', '')).strip()[:CONTENT_PREVIEW_LEN],
                'checksum': sha256_str(json.dumps(ev, ensure_ascii=False, sort_keys=True)),
            }
            files[fp] = meta
    return files


# ── URL construction ────────────────────────────────────────────

def make_url(section: str, file_path: str) -> str:
    p = Path(file_path)
    if p.suffix == '.md':
        p = p.with_suffix('')
    if p.name == 'index':
        p = p.parent

    parts = [part for part in p.parts if part != '.']

    url_section = {
        'proposals':    'proposals/proposals',
        'preproposals': 'proposals/preproposals',
        'discussions':  'community/discussion',
        'issues':       'community/issues',
        'gonka_docs':   'gonka/docs',
        'calendar':     'community/calendar',
    }.get(section, section)

    suffix = '/'.join(parts)
    suffix = suffix + '/' if suffix else ''
    return f'/{url_section}/{suffix}'


# ── AI enrichment ──────────────────────────────────────────────

AI_SYSTEM_PROMPT = """You are an editor of the Gonka community activity feed, a decentralized AI inference network.
Write a short post about the change described below.

Rules:
- Always reply in English
- Maximum 2-3 sentences
- Friendly but professional tone
- Plain text only (no markdown, no **, no ##, no HTML tags)
- Carefully read the content BEFORE and AFTER the change to understand the essence
- Tell what exactly changed and why it matters to the community
- If statuses before/after are given (e.g. voting -> passed), explain what that means
- If funding amounts are given, be sure to mention them
- If a new comment on an issue is given — briefly summarize the comment (who wrote it, what about)
- Do not retell the content verbatim — explain the meaning of the changes
- Reply only with the finished post, without reasoning, analysis or explanations"""

AI_TRANSLATE_PROMPT = """Translate the following community post from Russian into English.
Output only the translated English post. Do not include any commentary, markdown, formatting, or the original text.

The post to translate:
"""


def _has_cyrillic(text: str) -> bool:
    return any('\u0400' <= c <= '\u04ff' for c in text)


def _call_ai(api_key: str, api_endpoint: str, model: str,
             system_prompt: str, user_prompt: str,
             attempts: int = 3, timeout: int = 60) -> str:
    import requests
    import time as _time

    last_err = None
    for attempt in range(1, attempts + 1):
        try:
            resp = requests.post(
                f'{api_endpoint}/chat/completions',
                headers={
                    'Authorization': f'Bearer {api_key}',
                    'Content-Type': 'application/json',
                },
                json={
                    'model': model,
                    'messages': [
                        {'role': 'system', 'content': system_prompt},
                        {'role': 'user', 'content': user_prompt},
                    ],
                    'max_tokens': 350,
                    'temperature': 0.7,
                    'reasoning_effort': 'none',
                },
                timeout=timeout,
            )
            resp.raise_for_status()
            data = resp.json()
            raw = data['choices'][0]['message'].get('content')
            if not raw:
                raise ValueError('AI returned empty content')
            break
        except Exception as e:
            last_err = e
            if attempt < attempts:
                _time.sleep(attempt * 5)
    else:
        raise last_err

    ai_text = raw.strip()
    ai_text = re.sub(r'<think>.*?</think>', '', ai_text, flags=re.DOTALL | re.IGNORECASE).strip()
    ai_text = re.sub(r'<[^>]+>', '', ai_text).strip()
    ai_text = re.sub(
        r'\[@(\w+(?:-\w+)*)\]\(((?:https?://)?[^\s)]+)\)',
        r'<a href="\2">@\1</a>',
        ai_text,
    )
    return ai_text


def _build_user_prompt(section: str, event: dict) -> str:
    """Build the AI user prompt (in English) from an event."""
    section_label = SECTION_LABELS.get(section, section)
    action_label = ACTION_LABELS.get(event['action'], event['action'])
    details = event.get('details', {})
    title = event['item'].get('title', '')

    user_prompt = (
        f'Section: {section_label}\n'
        f'Action: {action_label}\n'
        f'Title: {title}\n'
    )

    if details.get('content_before'):
        user_prompt += '--- Content BEFORE ---\n' + details['content_before'] + '\n'
    if details.get('content_after'):
        user_prompt += '--- Content AFTER ---\n' + details['content_after'] + '\n'
    if details.get('content'):
        user_prompt += '--- Content ---\n' + details['content'] + '\n'

    status_info = []
    if details.get('status_before'):
        status_info.append(f"status before: {details['status_before']}")
    if details.get('status_after'):
        status_info.append(f"status after: {details['status_after']}")
    if details.get('status'):
        status_info.append(f"status: {details['status']}")
    if status_info:
        user_prompt += 'Statuses: ' + ', '.join(status_info) + '\n'

    if details.get('funding'):
        user_prompt += f'Funding amounts: {details["funding"]}\n'

    if details.get('voting_end'):
        user_prompt += f'Voting ends: {details["voting_end"]}\n'

    if details.get('description'):
        user_prompt += f'Proposal summary: {details["description"]}\n'

    new_comments = details.get('new_comments', [])
    if new_comments:
        user_prompt += 'New comments:\n'
        for i, c in enumerate(new_comments, 1):
            user_prompt += f'  {i}. {c}\n'

    if details.get('comment_count'):
        user_prompt += f'Total comments: {details["comment_count"]}\n'

    return user_prompt


def enrich_with_ai(events: list, section: str):
    try:
        import requests  # noqa: F401
    except ImportError:
        print('  AI enrichment: requests library not installed, skipping')
        return

    api_key = os.environ.get('AI_API_KEY', '')
    api_endpoint = os.environ.get(
        'AI_API_ENDPOINT', 'https://api.proxy.gonka.gg/v1'
    ).rstrip('/')
    model = os.environ.get('AI_MODEL', 'moonshotai/Kimi-K2.6')

    if not api_key:
        print('  AI enrichment: AI_API_KEY not set, skipping')
        return

    for event in events:
        user_prompt = _build_user_prompt(section, event)

        try:
            ai_text = _call_ai(api_key, api_endpoint, model,
                               AI_SYSTEM_PROMPT, user_prompt)
            event['ai_description'] = ai_text
            print(f'  AI: [{event["action"]}] {ai_text[:100]}...')
        except Exception as e:
            print(f'  AI enrichment failed for {event["id"]}: {e}', file=sys.stderr)


def backfill_enrichments(events_path: Path):
    """Enrich or translate events already stored in events.json.

    - Events without an ai_description get one generated from their details.
    - Events whose ai_description is in Russian are translated to English.
    """
    if not events_path.exists():
        return

    api_key = os.environ.get('AI_API_KEY', '')
    api_endpoint = os.environ.get(
        'AI_API_ENDPOINT', 'https://api.proxy.gonka.gg/v1'
    ).rstrip('/')
    model = os.environ.get('AI_MODEL', 'moonshotai/Kimi-K2.6')

    if not api_key:
        print('  AI backfill: AI_API_KEY not set, skipping')
        return

    try:
        import requests  # noqa: F401
    except ImportError:
        print('  AI backfill: requests library not installed, skipping')
        return

    try:
        events = json.loads(events_path.read_text(encoding='utf-8'))
    except (json.JSONDecodeError, IOError):
        print('  AI backfill: could not read events file, skipping')
        return

    changed = 0
    for event in events:
        ai = event.get('ai_description') or ''
        section = event.get('section', '')

        # Skip events that are already enriched in English, unless the text
        # looks like a failed output (empty, still Cyrillic, or echoed prompt).
        if ai and not _has_cyrillic(ai) and 'Post to translate' not in ai:
            continue

        try:
            if not ai:
                user_prompt = _build_user_prompt(section, event)
                ai_text = _call_ai(api_key, api_endpoint, model,
                                   AI_SYSTEM_PROMPT, user_prompt)
                mode = 'generate'
            else:
                ai_text = _call_ai(api_key, api_endpoint, model,
                                   AI_TRANSLATE_PROMPT, ai)
                if _has_cyrillic(ai_text) or 'Post to translate' in ai_text:
                    raise ValueError('AI translation still contains Cyrillic or echoed the prompt')
                mode = 'translate'

            if not ai_text or _has_cyrillic(ai_text):
                raise ValueError('AI output is empty or not English')
            event['ai_description'] = ai_text
            changed += 1
            print(f'  AI backfill ({mode}): [{event.get("action")}] {ai_text[:100]}...')
        except Exception as e:
            print(f'  AI backfill failed for {event.get("id")}: {e}', file=sys.stderr)

    if changed:
        events_path.write_text(
            json.dumps(events, indent=2, ensure_ascii=False), encoding='utf-8'
        )
        print(f'AI backfill: {changed} events enriched/translated -> {events_path}')


# ── commands ───────────────────────────────────────────────────

def cmd_snapshot(args):
    dir_path = Path(args.dir)
    if args.section == 'calendar':
        files = scan_calendar(dir_path)
    else:
        files = scan_directory(dir_path, args.section)

    manifest = {
        'section': args.section,
        'snapshot_time': datetime.now(timezone.utc).isoformat(),
        'files': files,
    }
    manifest_path = Path(args.manifest)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding='utf-8'
    )
    print(f'Snapshot: {len(files)} files -> {args.manifest}')
    return files


def cmd_detect(args):
    manifest_path = Path(args.manifest)

    if not manifest_path.exists():
        print('No prior manifest — creating baseline (no events)')
        cmd_snapshot(args)
        return

    old_manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    old_files = old_manifest.get('files', {})

    dir_path = Path(args.dir)
    if args.section == 'calendar':
        new_files = scan_calendar(dir_path)
    else:
        new_files = scan_directory(dir_path, args.section)

    new_keys = set(new_files.keys())
    old_keys = set(old_files.keys())

    events = []

    def _cp(meta: dict) -> str:
        return (meta.get('content_preview') or '')[:CONTENT_PREVIEW_LEN]

    # ── new files / events ─────────────────────────────────
    for key in sorted(new_keys - old_keys):
        f = new_files[key]
        details = {
            'status': f.get('status'),
            'content': _cp(f),
        }
        if args.section == 'proposals':
            details['funding'] = (f.get('funding') or '')
            details['voting_end'] = (f.get('voting_end') or '')
            details['description'] = (f.get('description') or '')
        elif args.section == 'calendar':
            details['date'] = f.get('date') or ''
            details['time'] = f.get('time') or ''
            details['event_type'] = f.get('event_type') or ''
            details['url'] = f.get('url') or ''

        item = {
            'title': f.get('title', key),
            'url': make_url(args.section, key),
            'file': key,
        }
        if args.section == 'calendar' and f.get('url'):
            item['url'] = f.get('url')

        events.append({
            'id': make_event_id(),
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'section': args.section,
            'action': 'new',
            'item': item,
            'details': details,
            'ai_description': None,
        })

    # ── deleted files / events ─────────────────────────────
    for key in sorted(old_keys - new_keys):
        # Calendar: only surface new events, not removals
        if args.section == 'calendar':
            continue
        f = old_files[key]
        events.append({
            'id': make_event_id(),
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'section': args.section,
            'action': 'deleted',
            'item': {
                'title': f.get('title', key),
                'url': None,
                'file': key,
            },
            'details': {'content': _cp(f)},
            'ai_description': None,
        })

    # ── modified files (including status / quorum changes) ─
    for key in sorted(new_keys & old_keys):
        # Calendar: only surface new events, not edits
        if args.section == 'calendar':
            continue
        old = old_files[key]
        new = new_files[key]
        if old.get('checksum') == new.get('checksum'):
            continue

        old_status = old.get('status')
        new_status = new.get('status')

        action = 'updated'
        details = {
            'content_before': _cp(old),
            'content_after': _cp(new),
        }

        # status change takes priority
        if old_status and new_status and old_status != new_status:
            action = 'status_changed'
            details['status_before'] = old_status
            details['status_after'] = new_status

        # skip if the visible content didn't actually change
        if action == 'updated' and _cp(old) == _cp(new):
            # For issues: check if new comments appeared
            if args.section == 'issues':
                old_cc = old.get('comment_checksum', '')
                new_cc = new.get('comment_checksum', '')
                if old_cc and new_cc and old_cc != new_cc:
                    old_bodies = old.get('comment_bodies', [])
                    new_bodies = new.get('comment_bodies', [])
                    added = [c for c in new_bodies if c not in old_bodies]
                    if added:
                        details['new_comments'] = added
                        details['comment_count'] = len(new_bodies)
                        print(f"  New comment(s) on {key}: {added[0][:80]}...")
                    else:
                        continue
                else:
                    continue
            else:
                continue

        # proposals: skip plain updated, check quorum
        if args.section == 'proposals':
            old_quorum = old.get('quorum_met')
            new_quorum = new.get('quorum_met')
            quorum_just_met = (
                old_quorum is not None
                and new_quorum is not None
                and not old_quorum
                and new_quorum
            )

            if action == 'updated':
                if quorum_just_met:
                    action = 'quorum_reached'
                    details['quorum_reached'] = True
                else:
                    continue  # skip meaningless updates

            if action in ('status_changed', 'quorum_reached', 'new'):
                details['funding'] = (new.get('funding') or '')
                details['voting_end'] = (new.get('voting_end') or '')
                details['description'] = (new.get('description') or '')

        events.append({
            'id': make_event_id(),
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'section': args.section,
            'action': action,
            'item': {
                'title': new.get('title', key),
                'url': make_url(args.section, key),
                'file': key,
            },
            'details': details,
            'ai_description': None,
        })

    if not events:
        print('No relevant changes detected')
        if args.ai:
            backfill_enrichments(Path(args.events))
        cmd_snapshot(args)
        return

    # AI enrichment
    if args.ai:
        enrich_with_ai(events, args.section)
        backfill_enrichments(Path(args.events))

    # Append to events.json (newest first)
    events_path = Path(args.events)
    events_path.parent.mkdir(parents=True, exist_ok=True)

    existing = []
    if events_path.exists():
        try:
            existing = json.loads(events_path.read_text(encoding='utf-8'))
        except (json.JSONDecodeError, IOError):
            pass

    all_events = events + existing

    MAX_EVENTS = 500
    if len(all_events) > MAX_EVENTS:
        all_events = all_events[:MAX_EVENTS]

    events_path.write_text(
        json.dumps(all_events, indent=2, ensure_ascii=False), encoding='utf-8'
    )
    print(f'Detected {len(events)} relevant changes -> {args.events}')

    cmd_snapshot(args)


# ── daily reminder ─────────────────────────────────────────────

def cmd_daily_reminder(args):
    """Post one reminder event about today's upcoming calendar events.

    Idempotent: posts at most one reminder per calendar day (UTC). The
    reminder is a single event whose details.today lists all events that
    happen today, so the feed shows 'Today' in the morning without spamming
    one entry per event.
    """
    today = datetime.now(timezone.utc).date().isoformat()

    events_path = Path(args.events)
    existing = []
    if events_path.exists():
        try:
            existing = json.loads(events_path.read_text(encoding='utf-8'))
        except (json.JSONDecodeError, IOError):
            existing = []

    # Idempotency: skip if a reminder for today already exists
    for ev in existing:
        if ev.get('section') == 'calendar' and ev.get('action') == 'daily_reminder':
            ts = (ev.get('timestamp') or '')[:10]
            if ts == today:
                print(f'Daily reminder already posted for {today}, skipping')
                return

    events = scan_calendar(Path(args.dir))
    todays = sorted(
        [m for m in events.values() if m.get('date') == today],
        key=lambda m: m.get('time', ''),
    )

    if not todays:
        print(f'No calendar events on {today}, no reminder')
        return

    today_items = [
        {
            'title': m.get('title', ''),
            'date': m.get('date', ''),
            'time': m.get('time', ''),
            'event_type': m.get('event_type', ''),
            'url': m.get('url', ''),
        }
        for m in todays
    ]

    reminder = {
        'id': make_event_id(),
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'section': 'calendar',
        'action': 'daily_reminder',
        'item': {
            'title': f"Today: {len(today_items)} events — {', '.join(t.get('title', '') for t in today_items[:3])}{'…' if len(today_items) > 3 else ''}",
            'url': '/community/calendar/',
            'file': None,
        },
        'details': {
            'today': today_items,
            'count': len(today_items),
        },
        'ai_description': None,
    }

    all_events = [reminder] + existing
    MAX_EVENTS = 500
    if len(all_events) > MAX_EVENTS:
        all_events = all_events[:MAX_EVENTS]

    events_path.parent.mkdir(parents=True, exist_ok=True)
    events_path.write_text(
        json.dumps(all_events, indent=2, ensure_ascii=False), encoding='utf-8'
    )
    print(f'Daily reminder posted for {today}: {len(today_items)} events')


# ── CLI ─────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='Activity Feed — change detection')
    sub = parser.add_subparsers(dest='command', required=True)

    snap = sub.add_parser('snapshot', help='Save current state as baseline')
    snap.add_argument('--dir', required=True, help='Directory to scan')
    snap.add_argument('--section', required=True,
                      choices=list(SECTION_LABELS.keys()),
                      help='Section identifier')
    snap.add_argument('--manifest', required=True, help='Manifest file path')

    det = sub.add_parser('detect', help='Detect changes and generate events')
    det.add_argument('--dir', required=True, help='Directory to scan')
    det.add_argument('--section', required=True,
                     choices=list(SECTION_LABELS.keys()),
                     help='Section identifier')
    det.add_argument('--manifest', required=True, help='Manifest file path')
    det.add_argument('--events', required=True, help='Events JSON file path')
    det.add_argument('--ai', action='store_true',
                     help='Enrich events with AI descriptions')

    rem = sub.add_parser('daily-reminder',
                         help='Post a reminder about today\'s calendar events')
    rem.add_argument('--dir', required=True, help='Calendar directory to scan')
    rem.add_argument('--events', required=True, help='Events JSON file path')

    bf = sub.add_parser('backfill',
                        help='Enrich/translate existing events in events.json')
    bf.add_argument('--events', required=True, help='Events JSON file path')

    args = parser.parse_args()

    if args.command == 'snapshot':
        cmd_snapshot(args)
    elif args.command == 'detect':
        cmd_detect(args)
    elif args.command == 'daily-reminder':
        cmd_daily_reminder(args)
    elif args.command == 'backfill':
        backfill_enrichments(Path(args.events))


if __name__ == '__main__':
    main()
