#!/usr/bin/env python3
"""Sync all GitHub Issues from gonka-ai/gonka into community/issues/.

Generates GitHub-style issue pages with:
- Main index: all issues listed (no pagination) in GitHub design
- Label pages: issues filtered by label (no pagination)
- Individual issue pages: full issue with comments
"""

import os
import re
import sys
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import requests

OWNER = os.environ.get("REPO_OWNER", "gonka-ai")
REPO = os.environ.get("REPO_NAME", "gonka")
OUTPUT_DIR = Path(os.environ.get("OUTPUT_DIR", "docs/community/issues"))
GH_TOKEN = os.environ.get("GH_TOKEN", "")

API_BASE = "https://api.github.com"
HEADERS = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}
if GH_TOKEN:
    HEADERS["Authorization"] = f"Bearer {GH_TOKEN}"

# SVG icons for open/closed issues
ICON_OPEN = '<svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg>'
ICON_CLOSED = '<svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg>'
ICON_COMMENT = '<svg viewBox="0 0 16 16"><path d="M1 2.75C1 1.784 1.784 1 2.75 1h10.5c.966 0 1.75.784 1.75 1.75v7.5A1.75 1.75 0 0 1 13.25 12H9.06l-2.573 2.573A1.458 1.458 0 0 1 4 13.543V12H2.75A1.75 1.75 0 0 1 1 10.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h4.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"/></svg>'


def gh_get(path, params=None, retries=3):
    url = f"{API_BASE}{path}"
    for attempt in range(retries):
        r = requests.get(url, headers=HEADERS, params=params, timeout=60)
        if r.status_code in (502, 503) and attempt < retries - 1:
            time.sleep(2 ** attempt)
            continue
        if r.status_code == 403 and "rate limit" in r.text.lower():
            reset = int(r.headers.get("X-RateLimit-Reset", 0))
            wait = max(reset - int(time.time()), 10)
            print(f"  Rate limited, waiting {wait}s...")
            time.sleep(min(wait, 300))
            continue
        if r.status_code == 422:
            return None
        r.raise_for_status()
        return r.json()
    return None


def list_all_issues():
    issues = []
    page = 1
    while True:
        data = gh_get(f"/repos/{OWNER}/{REPO}/issues", {
            "state": "all",
            "per_page": 100,
            "page": page,
            "sort": "updated",
            "direction": "desc",
        })
        if not data:
            break
        for item in data:
            if "pull_request" in item:
                continue
            issues.append(item)
        if len(data) < 100:
            break
        page += 1
    return issues


def fetch_issue(number):
    issue = gh_get(f"/repos/{OWNER}/{REPO}/issues/{number}")
    if not issue:
        return None, []
    comments = []
    page = 1
    while True:
        cdata = gh_get(f"/repos/{OWNER}/{REPO}/issues/{number}/comments", {
            "per_page": 100,
            "page": page,
        })
        if not cdata:
            break
        comments.extend(cdata)
        if len(cdata) < 100:
            break
        page += 1
    return issue, comments


def slugify(text, max_len=60):
    text = (text or "").strip().lower()
    text = re.sub(r"[^\w\s\-а-яё]", "", text, flags=re.UNICODE)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text[:max_len] or "untitled"


def fmt_date(iso):
    try:
        return datetime.fromisoformat(iso.replace("Z", "+00:00")).strftime("%Y-%m-%d %H:%M UTC")
    except Exception:
        return iso or "unknown"


def fmt_date_short(iso):
    try:
        return datetime.fromisoformat(iso.replace("Z", "+00:00")).strftime("%Y-%m-%d")
    except Exception:
        return (iso or "")[:10]


def user_link(user):
    if not user:
        return "deleted user"
    return f'[@{user["login"]}]({user["html_url"]})'


def label_html(label):
    """Generate HTML for a single label badge."""
    name = label["name"]
    color = label.get("color", "ededed")
    # Determine text color based on background brightness
    r, g, b = int(color[:2], 16), int(color[2:4], 16), int(color[4:], 16)
    brightness = (r * 299 + g * 587 + b * 114) / 1000
    text_color = "#24292f" if brightness > 128 else "#ffffff"
    return (
        f'<span class="issues-label" style="background-color: #{color}; '
        f'color: {text_color}; border-color: #{color};">{name}</span>'
    )


def labels_html(labels):
    if not labels:
        return ""
    return " ".join(label_html(l) for l in labels)


def time_ago(iso):
    """Human-readable time ago."""
    try:
        dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        diff = now - dt
        seconds = int(diff.total_seconds())
        if seconds < 60:
            return "just now"
        elif seconds < 3600:
            m = seconds // 60
            return f"{m} minute{'s' if m != 1 else ''} ago"
        elif seconds < 86400:
            h = seconds // 3600
            return f"{h} hour{'s' if h != 1 else ''} ago"
        elif seconds < 2592000:
            d = seconds // 86400
            return f"{d} day{'s' if d != 1 else ''} ago"
        else:
            return fmt_date_short(iso)
    except Exception:
        return fmt_date_short(iso)


def issue_list_item_html(issue, base_path=""):
    """Generate HTML for a single issue in the list.
    
    Args:
        issue: GitHub issue data
        base_path: Relative path prefix (e.g. "../../" for label subdirectories)
    """
    number = issue["number"]
    title = issue["title"]
    state = issue.get("state", "open")
    user = issue.get("user")
    labels = issue.get("labels", [])
    body = issue.get("body", "") or ""
    comments_count = issue.get("comments", 0)
    updated_at = issue.get("updated_at", "")
    created_at = issue.get("created_at", "")

    # Truncate body for preview
    body_preview = body[:200].replace("\n", " ").strip()
    if len(body) > 200:
        body_preview += "..."

    status_html = (
        f'<span class="issues-status issues-status-{state}">'
        f'{ICON_OPEN if state == "open" else ICON_CLOSED}</span>'
    )

    labels_part = ""
    if labels:
        labels_part = f'<span class="issues-labels">{labels_html(labels)}</span>'

    comments_part = ""
    if comments_count > 0:
        comments_part = (
            f'<span class="issues-meta-item">'
            f'{ICON_COMMENT} {comments_count}</span>'
        )

    # Calculate relative time
    rel_time = time_ago(updated_at) if updated_at else ""

    return f'''<li class="issues-list-item">
  {status_html}
  <div class="issues-body">
    <div class="issues-title">
      <a href="{base_path}{number:05d}-{slugify(title)}/">{title}</a>
      <span class="issues-number">#{number}</span>
    </div>
    {f'<p class="issues-desc">{body_preview}</p>' if body_preview else ''}
    <div class="issues-labels">{labels_html(labels)}</div>
    <div class="issues-meta">
      <span class="issues-meta-item">{user_link(user)} opened {rel_time}</span>
      {comments_part}
    </div>
  </div>
</li>'''


def build_global_index(issues, by_label, by_state, total):
    sync_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    open_count = by_state.get("open", 0)
    closed_count = by_state.get("closed", 0)

    # Sort by updated_at descending
    sorted_issues = sorted(issues, key=lambda x: x.get("updated_at", ""), reverse=True)

    items_html = "\n".join(issue_list_item_html(it, base_path="") for it in sorted_issues)

    out = f"""---
title: "GitHub Issues"
template: issues-main.html
---

# GitHub Issues — `{OWNER}/{REPO}`

All issues from [{OWNER}/{REPO}](https://github.com/{OWNER}/{REPO}/issues).
Total: **{total}** (🟢 open: **{open_count}**, 🔴 closed: **{closed_count}**).
Updated: `{sync_time}`.

<ul class="issues-list">
{items_html}
</ul>
"""
    return out


def build_label_index(label_name, label_slug, items):
    sync_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    items_sorted = sorted(items, key=lambda x: x["updated_at"], reverse=True)

    items_html = "\n".join(issue_list_item_html(it, base_path="../../") for it in items_sorted)

    out = f"""---
title: "Issues: {label_name}"
template: issues-main.html
---

# Issues: {label_name}

Issues with label **{label_name}**. Total: **{len(items_sorted)}**.
Updated: `{sync_time}`.

[← All Issues](../../index.md)

<ul class="issues-list">
{items_html}
</ul>
"""
    return out


def build_issue_page(issue, comments):
    sync_time = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    number = issue["number"]
    title = issue["title"]
    state = issue.get("state", "open")
    user = issue.get("user")
    labels = issue.get("labels", [])
    body = issue.get("body") or "*(empty)*"

    state_html = "Open" if state == "open" else "Closed"
    status_cls = f"issues-status-{state}"
    icon = ICON_OPEN if state == "open" else ICON_CLOSED

    out = f"""---
title: "#{number} — {title}"
source: {issue['html_url']}
issue_number: {number}
synced_at: {sync_time}
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status {status_cls}">{icon}</span>
    {title}
    <span class="issues-number">#{number}</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">{state_html}</span>
    <span class="issues-meta-item">{user_link(user)} opened {fmt_date(issue['created_at'])}</span>
    <span class="issues-meta-item">{len(comments)} comment{'s' if len(comments) != 1 else ''}</span>
    <span class="issues-meta-item">Updated {fmt_date(issue['updated_at'])}</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;">{labels_html(labels)}</div>
</div>

<div class="issues-content" markdown="1">
{body}
</div>
"""

    if comments:
        out += f"\n---\n\n## 💬 Comments ({len(comments)})\n\n"
        for i, c in enumerate(comments, 1):
            cu = c.get("user")
            out += f'''<div class="issues-comment">
  <div class="issues-comment-header">
    <span>{user_link(cu)}</span>
    <span class="issues-meta-item">commented {fmt_date(c['created_at'])}</span>
  </div>
  <div class="issues-comment-body issues-content" markdown="1">
    {c.get("body") or "*(empty)*"}
  </div>
</div>
'''

    # Auto-sync notice
    out += f"""
---

> 🔄 **Auto-synced** from [Issue #{number}]({issue['html_url']}) every hour.
"""
    return out


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Listing issues in {OWNER}/{REPO}...")
    listing = list_all_issues()
    print(f"Found {len(listing)} issues.")

    by_label = defaultdict(list)
    by_state = defaultdict(int)
    seen_paths = {Path("index.md")}

    labels_dir = OUTPUT_DIR / "labels"
    labels_dir.mkdir(parents=True, exist_ok=True)

    # First pass: collect metadata for all issues
    issue_metas = []
    for meta in listing:
        number = meta["number"]
        print(f"  → #{number} {meta['title'][:60]}")
        issue, comments = fetch_issue(number)
        if issue is None:
            continue

        labels = issue.get("labels", [])
        state = issue.get("state", "open")
        by_state[state] += 1

        slug = slugify(issue["title"])
        filename = f"{number:05d}-{slug}.md"

        # Write individual issue page
        (OUTPUT_DIR / filename).write_text(
            build_issue_page(issue, comments), encoding="utf-8"
        )
        seen_paths.add(Path(filename))

        # Collect label info
        label_names = [l["name"] for l in labels] if labels else ["no-label"]
        for label_name in label_names:
            label_slug = slugify(label_name, max_len=40)
            by_label[label_name].append({
                "number": issue["number"],
                "title": issue["title"],
                "user": issue.get("user"),
                "state": state,
                "updated_at": issue["updated_at"],
                "labels": labels,
                "_filename": filename,
                "_label_slug": label_slug,
            })

    # Generate label index pages
    for label_name, items in by_label.items():
        label_slug = items[0]["_label_slug"]
        label_dir = labels_dir / label_slug
        label_dir.mkdir(parents=True, exist_ok=True)
        (label_dir / "index.md").write_text(
            build_label_index(label_name, label_slug, items), encoding="utf-8"
        )
        seen_paths.add(Path("labels") / label_slug / "index.md")

    # Generate global index page (all issues, no pagination)
    (OUTPUT_DIR / "index.md").write_text(
        build_global_index(listing, by_label, by_state, len(listing)), encoding="utf-8"
    )

    # Generate issues-labels-nav.html for sidebar navigation
    labels_items = []
    for label_name in sorted(by_label.keys()):
        items = by_label[label_name]
        label_slug = items[0]["_label_slug"]
        labels_items.append((label_name, label_slug, len(items)))
    # Sort by count descending
    labels_items.sort(key=lambda x: -x[2])

    nav_html = ""
    for name, slug, count in labels_items:
        nav_html += f'''          <li class="md-nav__item">
            <a href="/community/issues/labels/{slug}/" class="md-nav__link">
              <span class="md-ellipsis">
                <span class="issues-label" style="display:inline-flex; font-size:11px; padding:1px 6px;">{name}</span>
                <span class="issues-label-count">{count}</span>
              </span>
            </a>
          </li>
'''
    nav_path = Path("docs/overrides/partials/issues-labels-nav.html")
    nav_path.parent.mkdir(parents=True, exist_ok=True)
    nav_path.write_text(nav_html, encoding="utf-8")

    # Remove stale files
    for path in OUTPUT_DIR.rglob("*.md"):
        rel = path.relative_to(OUTPUT_DIR)
        if rel not in seen_paths:
            print(f"  ✗ removing stale {rel}")
            path.unlink()
    for p in sorted(OUTPUT_DIR.glob("*"), reverse=True):
        if p.is_dir() and not any(p.iterdir()):
            p.rmdir()

    print(f"Done. {len(listing)} issues, {len(by_label)} labels.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
