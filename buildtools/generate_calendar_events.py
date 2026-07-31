#!/usr/bin/env python3
"""Generate community/calendar/events.md from calendar JSON sources.

The interactive calendar page (index.md) is rendered client-side via JS, so
events are invisible to AI agents and the MkDocs search index. This script
writes a static markdown listing of every event so that:

  1. generate-llms-full.py includes events in llms-full.txt
  2. generate-llms.py lists upcoming events in llms.txt
  3. MkDocs indexes the page -> searchable via search_index.json
  4. /community/calendar/events/ is a human-readable text version

It is called both from buildtools/build.sh (step 0, before llms generation)
and from hooks/calendar_events.py (on_pre_build, for `mkdocs serve`).

Usage:
    python3 buildtools/generate_calendar_events.py [docs_dir]
"""
import datetime as dt
import json
import os
import sys
from glob import glob
from pathlib import Path

_MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]

_TYPE_LABELS = {
    "proposal_report": "Proposal",
    "committee_call": "Committee call",
    "ama": "AMA",
    "livestream": "Livestream",
    "network_update": "Network update",
    "community": "Community",
}

_SOURCE_LABELS = {
    "community.json": "Community",
    "proposals.json": "On-chain proposals",
    "proposal-77.json": "Proposal #77",
    "committees.json": "Committees",
    "network.json": "Network",
}

SITE_URL = "https://gonkadocs.com"


def load_events(calendar_dir: str) -> list[dict]:
    """Load all events from calendar JSON files (excluding manifest.json)."""
    events = []
    for path in sorted(glob(os.path.join(calendar_dir, "*.json"))):
        base = os.path.basename(path)
        if base == "manifest.json":
            continue
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError):
            continue

        items = data if isinstance(data, list) else data.get("events", [])
        source = _SOURCE_LABELS.get(base, base.replace(".json", "").replace("-", " ").title())
        for item in items:
            if not isinstance(item, dict) or not item.get("date"):
                continue
            item = dict(item)
            item["_source"] = source
            events.append(item)
    return events


def format_date(date_str: str) -> str:
    """2026-08-03 -> 2026-08-03 (August 3, Monday)."""
    try:
        year, month, day = date_str.split("-")
        d = dt.date(int(year), int(month), int(day))
        return f"{date_str} ({_MONTHS[int(month) - 1]} {int(day)}, {d.strftime('%A')})"
    except (ValueError, IndexError):
        return date_str


def today_iso() -> str:
    return dt.date.today().isoformat()


def event_to_md(event: dict) -> str:
    title = str(event.get("title", "Untitled")).replace("\n", " ").strip()
    date_str = str(event.get("date", ""))
    time_str = str(event.get("time", "")).strip()
    url = event.get("url", "")
    event_type = event.get("type", "")
    source = event.get("_source", "")

    lines = [f"### {title}"]

    meta = []
    if date_str:
        meta.append(format_date(date_str))
    if time_str:
        meta.append(time_str)
    if event_type and event_type != "proposal_report":
        meta.append(_TYPE_LABELS.get(event_type, event_type.replace("_", " ").title()))
    if source:
        meta.append(f"Source: {source}")
    if meta:
        lines.append("")
        lines.append("**" + "** · **".join(meta) + "**")

    desc = str(event.get("description", "")).strip()
    if desc:
        lines.append("")
        lines.append(desc)

    if url:
        lines.append("")
        if url.startswith("http"):
            lines.append(f"Link: {url}")
        else:
            lines.append(f"Link: {SITE_URL}{url}")

    return "\n".join(lines)


def build_events_md(events: list[dict]) -> str:
    upcoming = sorted(
        [e for e in events if e.get("date", "") >= today_iso()],
        key=lambda e: (e.get("date", ""), e.get("time", "")),
    )
    past = sorted(
        [e for e in events if e.get("date", "") < today_iso()],
        key=lambda e: (e.get("date", ""), e.get("time", "")),
        reverse=True,
    )

    out = [
        "---",
        "title: Community Calendar (all events)",
        "description: Machine-readable listing of all community calendar events — AMAs, committee calls, proposal milestones, network updates.",
        "---",
        "",
        "# Community Calendar — All Events",
        "",
        "This is the machine-readable version of the community calendar. The interactive",
        "calendar UI is at [/community/calendar/](/community/calendar/).",
        "",
    ]

    out.append(f"- **Total events:** {len(events)}")
    out.append(f"- **Upcoming:** {len(upcoming)}")
    out.append(f"- **Past:** {len(past)}")
    out.append("")

    if upcoming:
        out.append("## Upcoming Events")
        out.append("")
        for e in upcoming:
            out.append(event_to_md(e))
            out.append("")

    if past:
        out.append("## Past Events")
        out.append("")
        for e in past:
            out.append(event_to_md(e))
            out.append("")

    return "\n".join(out)


def generate(docs_dir: str) -> str | None:
    """Write events.md into docs/community/calendar/. Returns out path or None."""
    calendar_dir = os.path.join(docs_dir, "community", "calendar")
    if not os.path.isdir(calendar_dir):
        return None

    events = load_events(calendar_dir)
    out_path = os.path.join(calendar_dir, "events.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(build_events_md(events))
    return out_path


if __name__ == "__main__":
    docs_dir_arg = sys.argv[1] if len(sys.argv) > 1 else "docs"
    root = Path(__file__).resolve().parent.parent
    target = docs_dir_arg if os.path.isabs(docs_dir_arg) else os.path.join(str(root), docs_dir_arg)
    result = generate(target)
    if result:
        n_events = len(load_events(os.path.join(target, "community", "calendar")))
        print(f"  [calendar] Generated events.md with {n_events} events -> {result}")
