#!/usr/bin/env python3
"""Generate calendar events from the /gonka/docs/network-updates/ page.

The network-updates.md file (synced hourly from gonka-ai/gonka-docs) organises
announcements as dated sections:

    ## August 13, 2026
    **Migrate community-sale and wrapped-token contracts**
    <body...>

Each dated section becomes an all-day calendar event (category
"network_updates") with a link to the exact anchor on the network-updates page,
so new updates automatically land in the community calendar and its .ics export
(which is generated from docs/community/calendar/*.json).

Output is written to docs/community/calendar/network-updates.json and is picked
up automatically by the calendar manifest, events.md, enrich and iCal steps.
"""
import datetime
import json
import re
import sys
from pathlib import Path

NETWORK_PAGE = "network-updates.md"
OUT_FILENAME = "network-updates.json"
NETWORK_UPDATES_BASE = "/gonka/docs/network-updates/"

_HEADING_RE = re.compile(r"^##\s+([A-Za-z]+)\s+(\d{1,2}),\s+(\d{4})$")


def _clean_text(text):
    """Reduce markdown to readable plain text while keeping bare URLs."""
    if not text:
        return text
    text = text.replace("`", "").replace("**", "")
    # [label](url) -> url  (keep the link target)
    segments = text.split("](")
    parts = []
    for idx, seg in enumerate(segments):
        if idx == 0:
            parts.append(seg)
        else:
            close = seg.find(")")
            if close != -1:
                parts.append(seg[:close])
                parts.append(seg[close + 1:])
            else:
                parts.append(seg)
    text = "".join(parts)
    lines = [ln.strip() for ln in text.split(chr(10)) if ln.strip()]
    return " ".join(lines)


def _anchor(date_text, occurrence):
    """MkDocs Material anchor for a \"## August 13, 2026\" heading.

    Base anchor is lowercased with spaces hyphens and punctuation removed; the
    Nth duplicate on the same date gets a _N-1 numeric suffix.
    """
    base = date_text.lower().replace(",", "").replace(" ", "-")
    return base if occurrence == 0 else f"{base}_{occurrence}"


def parse_network_updates(md_text):
    events = []
    cur = None
    # occurrence counter per date string (=== per yyyy-mm-dd)
    seen = {}

    def flush(current):
        if current is None:
            return
        heading, date_str, body = current
        # first bold line is the update title
        title = ""
        paragraphs = []
        for line in body:
            stripped = line.strip()
            if not stripped:
                continue
            if not title and stripped.startswith("**") and stripped.endswith("**"):
                title = stripped.strip("**").strip()
            elif not title and stripped.startswith("**"):
                title = stripped.strip("**").strip()
            if stripped and not stripped.startswith(("**How to vote", "**Deadline")):
                paragraphs.append(stripped)
        if not title:
            title = "Network update"
        occurrence = seen.get(date_str, 0)
        seen[date_str] = occurrence + 1
        url = NETWORK_UPDATES_BASE + "#" + _anchor(heading, occurrence)
        body_text = _clean_text("\n".join(p for p in paragraphs if p))[:400]
        events.append({
            "date": date_str,
            "category": "network_updates",
            "type": "network_update",
            "title": title,
            "url": url,
            "time": "",
            "description": body_text if body_text else title,
            "tags": ["network"],
        })

    for line in md_text.split("\n"):
        m = _HEADING_RE.match(line.strip())
        if m:
            if cur:
                flush(cur)
            month = datetime.datetime.strptime(m.group(1), "%B").month
            date_str = f"{int(m.group(3)):04d}-{month:02d}-{int(m.group(2)):02d}"
            heading = f"{m.group(1)} {m.group(2)}, {m.group(3)}"
            cur = (heading, date_str, [])
        elif cur is not None:
            cur[2].append(line)
    if cur:
        flush(cur)

    return events


def generate(docs_dir="docs"):
    doc_path = Path(docs_dir) / "gonka" / "docs" / "docs" / NETWORK_PAGE
    if not doc_path.exists():
        print(f"  [network-updates] source not found: {doc_path} (skipping)")
        return None
    events = parse_network_updates(doc_path.read_text(encoding="utf-8"))
    out_path = Path(docs_dir) / "community" / "calendar" / OUT_FILENAME
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(events, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(f"  [network-updates] Generated {len(events)} events -> {out_path}")
    return out_path


def main():
    docs_dir = sys.argv[1] if len(sys.argv) > 1 else "docs"
    generate(docs_dir)


if __name__ == "__main__":
    main()
