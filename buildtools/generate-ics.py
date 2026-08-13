#!/usr/bin/env python3
"""Generate gonka-events.ics from calendar JSON sources."""
import hashlib
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ICS_FILENAME = "gonka-events.ics"

def _escape_ics(text):
    if text is None:
        return ""
    text = str(text)
    text = text.replace("\\", "\\\\")
    text = text.replace(";", "\\;")
    text = text.replace(",", "\\,")
    text = text.replace("\r\n", "\\n")
    text = text.replace("\n", "\\n")
    text = text.replace("\r", "")
    return text

def _fold_line(line):
    result = []
    remaining = line
    while len(remaining.encode("utf-8")) > 75:
        low, high = 0, len(remaining)
        while low < high:
            mid = (low + high + 1) // 2
            if len(remaining[:mid].encode("utf-8")) <= 75:
                low = mid
            else:
                high = mid - 1
        result.append(remaining[:low])
        remaining = " " + remaining[low:]
    result.append(remaining)
    return "\r\n".join(result)

def _ics_line(name, value):
    if not value:
        return _fold_line(f"{name}:")
    return _fold_line(f"{name}:{value}")

def _parse_time(date_str, time_str):
    m = re.match(r"(\d{1,2}):(\d{2})\s*UTC", str(time_str).strip(), re.I)
    if not m:
        raise ValueError(f"Cannot parse time: {time_str!r}")
    hour, minute = int(m.group(1)), int(m.group(2))
    d = datetime.strptime(date_str, "%Y-%m-%d").replace(
        hour=hour, minute=minute, second=0, tzinfo=timezone.utc
    )
    return d

def _load_events(calendar_dir):
    events = []
    for path in sorted(calendar_dir.glob("*.json")):
        if path.name == "manifest.json":
            continue
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        items = data if isinstance(data, list) else data.get("events", [])
        for item in items:
            if isinstance(item, dict) and item.get("date"):
                events.append(item)
    return events

def generate(docs_dir):
    calendar_dir = docs_dir / "community" / "calendar"
    events = _load_events(calendar_dir)
    dtstamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Gonka Docs//Gonka Community Calendar//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        _ics_line("X-WR-CALNAME", "Gonka Community Calendar"),
        _ics_line("X-WR-TIMEZONE", "UTC"),
        _ics_line("X-WR-CALDESC", "Community events for the Gonka decentralized AI inference network: AMAs, committee calls, proposals, livestreams, and network updates."),
    ]
    for ev in sorted(events, key=lambda e: (e.get("date", ""), e.get("time", ""))):
        title = ev.get("title", "Untitled")
        desc = ev.get("description", "")
        url = ev.get("url", "")
        event_type = ev.get("type", "")
        has_time = bool(str(ev.get("time", "")).strip())
        if "is_all_day" in ev:
            is_all_day = ev["is_all_day"]
        elif event_type == "proposal_report":
            is_all_day = True
        else:
            is_all_day = not has_time
        duration_minutes = ev.get("duration_minutes")
        uid = ev.get("uid", "")
        if not uid:
            base = f"{ev.get('date', '')}|{title}|{event_type}"
            h = hashlib.sha256(base.encode()).hexdigest()[:12]
            uid = f"gonka-{ev.get('date', '')}-{h}@gonkadocs.com"
        location = ev.get("location")
        if not location:
            if url and re.search(r"zoom\.us|meet\.google\.com", url, re.I):
                location = url
            elif desc:
                m = re.search(
                    r"(https?://(?:meet\.google\.com/[a-zA-Z0-9\-]+"
                    r"|(?:us\d+\.)?zoom\.us/j/\d+(?:\?[^\s<>\"']*)?"
                    r"|zoom\.us/j/\d+(?:\?[^\s<>\"']*)?"
                    r"|t\.me/\+?[a-zA-Z0-9_\-]+))",
                    str(desc), re.I,
                )
                if m:
                    location = m.group(1)
        tags = ev.get("tags", [])
        lines.append("BEGIN:VEVENT")
        lines.append(_ics_line("UID", uid))
        lines.append(_ics_line("DTSTAMP", dtstamp))
        if is_all_day:
            dt = ev["date"].replace("-", "")
            lines.append(_ics_line("DTSTART;VALUE=DATE", dt))
        else:
            try:
                start = _parse_time(ev["date"], ev.get("time", ""))
                start_str = start.strftime("%Y%m%dT%H%M%SZ")
                lines.append(_ics_line("DTSTART", start_str))
                if duration_minutes:
                    end = start + timedelta(minutes=int(duration_minutes))
                else:
                    end = start + timedelta(hours=1)
                end_str = end.strftime("%Y%m%dT%H%M%SZ")
                lines.append(_ics_line("DTEND", end_str))
            except ValueError:
                dt = ev["date"].replace("-", "")
                lines.append(_ics_line("DTSTART;VALUE=DATE", dt))
        lines.append(_ics_line("SUMMARY", _escape_ics(title)))
        parts = []
        if desc:
            parts.append(str(desc))
        if url:
            parts.append(f"\nURL: {url}")
        if tags:
            parts.append(f"\nTags: {', '.join(str(t) for t in tags)}")
        full_desc = "\n".join(parts)
        if full_desc.strip():
            lines.append(_ics_line("DESCRIPTION", _escape_ics(full_desc.strip())))
        if location:
            lines.append(_ics_line("LOCATION", _escape_ics(location)))
        if url:
            lines.append(_ics_line("URL", url))
        if event_type:
            lines.append(_ics_line("CATEGORIES", _escape_ics(event_type)))
        lines.append("END:VEVENT")
    lines.append("END:VCALENDAR")
    lines.append("")
    out_path = calendar_dir / ICS_FILENAME
    out_path.write_text("\r\n".join(lines), encoding="utf-8")
    print(f"Generated {len(events)} events -> {out_path}")
    return out_path

def main():
    docs_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("docs")
    generate(docs_dir)

if __name__ == "__main__":
    main()
