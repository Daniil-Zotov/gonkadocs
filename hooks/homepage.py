"""MkDocs hook: injects live homepage data into the home template context.

The homepage (docs/overrides/home.html) shows dynamic blocks: the next 3 days of
calendar events, the last 3 days of activity feed events, and the current
community pool balances. These are rendered server-side (not via JS) so the data
is stable, indexable, and available to AI agents reading the rendered page.

Runs on_env so the Jinja globals are available to the home template only.
"""

import datetime as dt
import json
import os
import re
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ROOT / "buildtools"))

from generate_calendar_events import load_events  # noqa: E402

_MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]

_SECTION_LABELS = {
    "proposals": "Proposals",
    "preproposals": "Pre-Proposals",
    "discussions": "Discussions",
    "issues": "Issues",
    "gonka_docs": "Docs",
    "calendar": "Calendar",
}

_ACTION_LABELS = {
    "new": "Added",
    "deleted": "Deleted",
    "updated": "Updated",
    "status_changed": "Status changed",
    "quorum_reached": "Quorum reached",
    "daily_reminder": "Today",
}

_POOL_ADDRESSES = {
    "community": ("Community Pool (distribution module)", "gonka1jv65s3grqf6v6jl3dp4t6c9t9rk99cd8h2rzwa"),
    "sale": ("Community Sale", "gonka18pkq9mwxxlmyq7kr5txhm060wemg2s4u94wvsfd9w2kdc0u99d6spk8pz2"),
    "gov": ("Gov Module (authority)", "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33"),
}


def _cal_when(e):
    d = e.get("date", "")
    try:
        dobj = dt.date.fromisoformat(d)
        return f"{dobj.strftime('%A')}, {_MONTHS[dobj.month - 1]} {dobj.day}"
    except (ValueError, TypeError):
        return d


def _ago(ts_str, now):
    try:
        ts = dt.datetime.fromisoformat(ts_str)
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=dt.timezone.utc)
        diff = now - ts
        secs = int(diff.total_seconds())
        if secs < 0:
            return "just now"
        if secs < 60:
            return "just now"
        if secs < 3600:
            return f"{secs // 60} min ago"
        if secs < 86400:
            return f"{secs // 3600} h ago"
        if secs < 604800:
            return f"{secs // 86400} d ago"
        return ts.strftime("%B %d, %Y")
    except (ValueError, TypeError):
        return ts_str


def _linkify(text):
    """Mirror calendar.html `linkify()`: escape, auto-link URLs, mini-markdown."""
    if not text:
        return ""
    escaped = str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    def _wrap(m):
        url = m.group(0)
        clean = re.sub(r"[.,);:]+$", "", url)
        suffix = url[len(clean):]
        return f'<a href="{clean}" target="_blank" rel="noopener">{clean}</a>{suffix}'

    escaped = re.sub(r"(https?://[^\s<]+)", _wrap, escaped)
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"\n-{3,}\n", '<hr class="cal-event-hr">', escaped)
    escaped = re.sub(r"\n{2,}", "<br><br>", escaped)
    escaped = escaped.replace("\n", "<br>")
    return escaped


def _block(md, start, end):
    m = re.search(re.escape(start) + r"(.*?)" + re.escape(end), md, re.S)
    return m.group(1) if m else ""


def _spans(block):
    return [s.strip() for s in re.findall(r"<span[^>]*>(.*?)</span>", block, re.S) if s.strip()]


def _parse_pool(path):
    if not os.path.isfile(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        md = f.read()
    out = {}
    for key, (name, address) in _POOL_ADDRESSES.items():
        marker = {
            "community": ("<!-- BALANCES_START -->", "<!-- BALANCES_END -->"),
            "sale": ("<!-- SALE_BALANCE_START -->", "<!-- SALE_BALANCE_END -->"),
            "gov": ("<!-- GOV_BALANCE_START -->", "<!-- GOV_BALANCE_END -->"),
        }[key]
        spans = _spans(_block(md, marker[0], marker[1]))
        out[key] = {"name": name, "address": address, "balances": spans}
    return out


def on_env(env, config, **kwargs):
    docs_dir = config["docs_dir"]

    # Calendar events: next 3 days (today .. today+2)
    calendar_dir = os.path.join(docs_dir, "community", "calendar")
    upcoming = []
    if os.path.isdir(calendar_dir):
        all_events = load_events(calendar_dir)
        today = dt.date.today()
        end = today + dt.timedelta(days=2)
        for e in all_events:
            try:
                d = dt.date.fromisoformat(e.get("date", ""))
            except (ValueError, TypeError):
                continue
            if today <= d <= end:
                item = dict(e)
                item["_when"] = _cal_when(e)
                upcoming.append(item)
        upcoming.sort(key=lambda e: (e.get("date", ""), e.get("time", "")))
    env.globals["home_calendar"] = upcoming

    # Activity feed: last 3 days, newest first
    ev_path = os.path.join(docs_dir, "community", "activity", "events.json")
    now = dt.datetime.now(dt.timezone.utc)
    cutoff = now - dt.timedelta(days=3)
    recent = []
    if os.path.isfile(ev_path):
        try:
            with open(ev_path, "r", encoding="utf-8") as f:
                feed = json.load(f)
        except (json.JSONDecodeError, OSError):
            feed = []
        for e in feed:
            try:
                ts = dt.datetime.fromisoformat(e.get("timestamp", ""))
            except (ValueError, TypeError):
                continue
            if ts.tzinfo is None:
                ts = ts.replace(tzinfo=dt.timezone.utc)
            if ts < cutoff:
                continue
            item = dict(e)
            item["_ago"] = _ago(e.get("timestamp", ""), now)
            item["_section_label"] = _SECTION_LABELS.get(e.get("section", ""), e.get("section", ""))
            item["_action_label"] = _ACTION_LABELS.get(e.get("action", ""), e.get("action", ""))
            recent.append(item)
        recent.sort(key=lambda e: e.get("timestamp", ""), reverse=True)
    env.globals["home_activity"] = recent

    # Community pool balances (3 addresses)
    pool_md = os.path.join(docs_dir, "proposals", "community pool.md")
    env.globals["home_pool"] = _parse_pool(pool_md)

    env.globals["home_linkify"] = _linkify

    return env
