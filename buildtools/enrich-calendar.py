#!/usr/bin/env python3
"""Enrich calendar JSON files with iCal-ready fields."""
import hashlib
import json
import re
import sys
from pathlib import Path

def _make_uid(event):
    base = f"{event.get('date', '')}|{event.get('title', '')}|{event.get('type', '')}"
    h = hashlib.sha256(base.encode("utf-8")).hexdigest()[:12]
    return f"gonka-{event.get('date', '')}-{h}@gonkadocs.com"

_VIDEO_RE = re.compile(
    r"(https?://(?:meet\.google\.com/[a-zA-Z0-9\-]+"
    r"|(?:us\d+\.)?zoom\.us/j/\d+(?:\?[^\s<>\"']*)?"
    r"|zoom\.us/j/\d+(?:\?[^\s<>\"']*)?"
    r"|t\.me/\+?[a-zA-Z0-9_\-]+))",
    re.IGNORECASE,
)

def _extract_location(event):
    url = event.get("url", "")
    if url and re.search(r"zoom\.us|meet\.google\.com", url, re.I):
        return url
    desc = event.get("description", "")
    if desc:
        m = _VIDEO_RE.search(str(desc))
        if m:
            return m.group(1)
    return None

def _enrich_event(event):
    ev = dict(event)
    event_type = ev.get("type", "")
    has_time = bool(str(ev.get("time", "")).strip())
    if event_type == "proposal_report":
        ev["is_all_day"] = True
        ev["duration_minutes"] = None
    elif has_time:
        ev["is_all_day"] = False
        ev["duration_minutes"] = 60
    else:
        ev["is_all_day"] = True
        ev["duration_minutes"] = None
    ev["location"] = _extract_location(ev)
    ev["uid"] = _make_uid(ev)
    return ev

def _process_file(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        enriched = [_enrich_event(ev) for ev in data]
        count = len(enriched)
    elif isinstance(data, dict) and "events" in data:
        enriched = [_enrich_event(ev) for ev in data["events"]]
        data["events"] = enriched
        count = len(enriched)
    else:
        return 0
    with open(path, "w", encoding="utf-8") as f:
        json.dump(enriched if isinstance(data, list) else data, f, indent=1, ensure_ascii=False)
        f.write("\n")
    return count

def main():
    docs_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("docs")
    calendar_dir = docs_dir / "community" / "calendar"
    total = 0
    for json_path in sorted(calendar_dir.glob("*.json")):
        if json_path.name == "manifest.json":
            continue
        n = _process_file(json_path)
        print(f"  enriched {n:4d} events  ->  {json_path.name}")
        total += n
    print(f"\nTotal enriched: {total} events")

if __name__ == "__main__":
    main()
