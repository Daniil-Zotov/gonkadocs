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

CONTENT_PREVIEW_LEN = 800  # max chars stored for AI context

_FRONTMATTER_RE = re.compile(r'^---\s*\n.*?^---\s*\n', re.DOTALL | re.MULTILINE)


def content_preview(content: str, max_len: int = CONTENT_PREVIEW_LEN) -> str:
    """Strip frontmatter and return first max_len chars of meaningful content."""
    cleaned = _FRONTMATTER_RE.sub('', content, count=1)
    # remove excessive blank lines
    cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
    return cleaned.strip()[:max_len]


# ── helpers ────────────────────────────────────────────────────

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()


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
}

ACTION_LABELS = {
    'new':             'Added',
    'deleted':         'Removed',
    'updated':         'Updated',
    'status_changed':  'Status Changed',
}


# ── metadata extraction ────────────────────────────────────────

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
        meta['status'] = _extract_proposal_status(content)

    elif section == 'preproposals':
        if '🟢 Active' in content:
            meta['status'] = 'active'
        elif '🔴 Expired' in content:
            meta['status'] = 'expired'

    elif section == 'issues':
        if re.search(r'\bstate:\s*open\b', content, re.IGNORECASE):
            meta['status'] = 'open'
        elif re.search(r'\bstate:\s*closed\b', content, re.IGNORECASE):
            meta['status'] = 'closed'

    return meta


# ── directory scanning ─────────────────────────────────────────

def scan_directory(dir_path: Path, section: str) -> dict:
    files = {}
    if not dir_path.exists():
        return files
    for fpath in sorted(dir_path.rglob('*.md')):
        rel = str(fpath.relative_to(dir_path))
        try:
            content = fpath.read_text(encoding='utf-8')
            meta = extract_metadata(section, fpath, content)
            meta['checksum'] = sha256_file(fpath)
            files[rel] = meta
        except Exception as e:
            print(f'  Warning: could not read {fpath}: {e}', file=sys.stderr)
    return files


# ── URL construction ────────────────────────────────────────────

def make_url(section: str, file_path: str) -> str:
    p = Path(file_path)
    # Strip .md extension first (handles both INDEX.MD and OTHER.MD)
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
    }.get(section, section)

    suffix = '/'.join(parts)
    suffix = suffix + '/' if suffix else ''
    return f'/{url_section}/{suffix}'


# ── AI enrichment ──────────────────────────────────────────────

AI_SYSTEM_PROMPT = """Ты — редактор ленты событий сообщества Gonka, децентрализованной AI-сети для инференса.
Напиши короткий пост об изменении, описанном ниже.

Правила:
- Максимум 2–3 предложения
- Дружелюбный, но профессиональный тон
- Только обычный текст (без markdown, без **, без ##)
- Внимательно прочитай содержимое ДО и ПОСЛЕ изменений, чтобы понять суть
- Расскажи, что именно изменилось и почему это важно для сообщества
- Если указаны статусы до/после (например, голосование → принят), объясни значение
- Не пересказывай содержимое дословно — объясни смысл изменений"""


def enrich_with_ai(events: list, section: str):
    try:
        import requests
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

    section_label = SECTION_LABELS.get(section, section)

    for event in events:
        action_label = ACTION_LABELS.get(event['action'], event['action'])
        details = event.get('details', {})
        title = event['item'].get('title', '')

        user_prompt = (
            f'Раздел: {section_label}\n'
            f'Действие: {action_label}\n'
            f'Название: {title}\n'
        )

        # Add before/after content for meaningful AI analysis
        if details.get('content_before'):
            user_prompt += '--- Содержимое ДО ---\n' + details['content_before'] + '\n'
        if details.get('content_after'):
            user_prompt += '--- Содержимое ПОСЛЕ ---\n' + details['content_after'] + '\n'
        if details.get('content'):
            user_prompt += '--- Содержимое ---\n' + details['content'] + '\n'

        # Status changes
        status_info = []
        if details.get('status_before'):
            status_info.append(f"статус до: {details['status_before']}")
        if details.get('status_after'):
            status_info.append(f"статус после: {details['status_after']}")
        if details.get('status'):
            status_info.append(f"статус: {details['status']}")
        if status_info:
            user_prompt += 'Статусы: ' + ', '.join(status_info) + '\n'

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
                        {'role': 'system', 'content': AI_SYSTEM_PROMPT},
                        {'role': 'user', 'content': user_prompt},
                    ],
                    'max_tokens': 350,
                    'temperature': 0.7,
                },
                timeout=15,
            )
            resp.raise_for_status()
            data = resp.json()
            ai_text = data['choices'][0]['message']['content'].strip()
            event['ai_description'] = ai_text
            print(f'  AI: [{event["action"]}] {ai_text[:100]}...')
        except Exception as e:
            print(f'  AI enrichment failed for {event["id"]}: {e}', file=sys.stderr)


# ── commands ───────────────────────────────────────────────────

def cmd_snapshot(args):
    dir_path = Path(args.dir)
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
    new_files = scan_directory(dir_path, args.section)

    new_keys = set(new_files.keys())
    old_keys = set(old_files.keys())

    events = []

    def _content_preview_from_meta(meta: dict) -> str:
        return (meta.get('content_preview') or '')[:CONTENT_PREVIEW_LEN]

    # new files
    for key in sorted(new_keys - old_keys):
        f = new_files[key]
        events.append({
            'id': make_event_id(),
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'section': args.section,
            'action': 'new',
            'item': {
                'title': f.get('title', key),
                'url': make_url(args.section, key),
                'file': key,
            },
            'details': {
                'status': f.get('status'),
                'content': _content_preview_from_meta(f),
            },
            'ai_description': None,
        })

    # deleted files
    for key in sorted(old_keys - new_keys):
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
            'details': {
                'content': _content_preview_from_meta(f),
            },
            'ai_description': None,
        })

    # modified files (including status changes)
    for key in sorted(new_keys & old_keys):
        old = old_files[key]
        new = new_files[key]
        if old.get('checksum') == new.get('checksum'):
            continue

        old_status = old.get('status')
        new_status = new.get('status')

        action = 'updated'
        details = {
            'content_before': _content_preview_from_meta(old),
            'content_after': _content_preview_from_meta(new),
        }

        if old_status and new_status and old_status != new_status:
            action = 'status_changed'
            details['status_before'] = old_status
            details['status_after'] = new_status

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
        print('No changes detected')
        cmd_snapshot(args)
        return

    # AI enrichment
    if args.ai:
        enrich_with_ai(events, args.section)

    # Append to events.json (newest first)
    events_path = Path(args.events)
    events_path.parent.mkdir(parents=True, exist_ok=True)

    existing = []
    if events_path.exists():
        try:
            existing = json.loads(events_path.read_text(encoding='utf-8'))
        except (json.JSONDecodeError, IOError):
            pass

    all_events = events + existing  # newest first

    MAX_EVENTS = 500
    if len(all_events) > MAX_EVENTS:
        all_events = all_events[:MAX_EVENTS]

    events_path.write_text(
        json.dumps(all_events, indent=2, ensure_ascii=False), encoding='utf-8'
    )
    print(f'Detected {len(events)} changes -> {args.events}')

    # Save new manifest for next comparison
    cmd_snapshot(args)


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

    args = parser.parse_args()

    if args.command == 'snapshot':
        cmd_snapshot(args)
    elif args.command == 'detect':
        cmd_detect(args)


if __name__ == '__main__':
    main()
