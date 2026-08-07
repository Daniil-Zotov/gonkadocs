"""MkDocs hook: injects a weekly proposal-reports dashboard into the template context.

The reports dashboard page (docs/overrides/reports-dashboard.html) shows a 7-column
calendar (the current Mon–Sun week) with thin gray grid lines. In each day cell it
displays:

  * uploaded proposal reports — parsed from report*.md files (published-date front
    note) on their publication date;
  * upcoming report calls — calendar events (TheSoul / INPUT weekly report calls and
    other committee/community calls) that fall on an upcoming day.

Runs on_env so the Jinja globals are available to the reports-dashboard template only.
"""

import datetime as dt
import glob
import os
import re
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ROOT / "buildtools"))

from generate_calendar_events import load_events  # noqa: E402

_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# Calendar event types that represent an upcoming report deliverable.
_REPORT_EVENT_TYPES = {"committee_call", "community_call", "network_event"}

_REPORT_KEYWORDS = ("report", "отчет", "отчёт")


def _is_upcoming_report_event(e):
    et = (e.get("type") or "").lower()
    title = (e.get("title") or "").lower()
    if et in _REPORT_EVENT_TYPES and ("report" in title or "call" in title or "встреч" in title):
        return True
    return False


def _strip_frontmatter(text):
    return re.sub(r"\A---\s*\n.*?^---\s*\n", "", text, flags=re.DOTALL | re.MULTILINE).strip()


def _load_reports(proposals_dir):
    """Scan report*.md files → [{date, title, url, proposal}]."""
    reports = {}
    for path in sorted(glob.glob(os.path.join(proposals_dir, "**", "report*.md"), recursive=True)):
        try:
            text = _strip_frontmatter(open(path, encoding="utf-8").read())
        except OSError:
            continue
        m = re.search(r"\*\*Дата публикации:\*\*\s*([\d-]+)", text)
        if not m:
            continue
        date = m.group(1)
        title = ""
        h1 = re.search(r"^#\s+(.+)$", text, flags=re.MULTILINE)
        if h1:
            title = h1.group(1).strip()
        if not title:
            title = os.path.basename(path)
        # derive proposal id + url from path .../2026-q2/N/reportX.md
        parts = path.split(os.sep)
        proposal = ""
        for p in parts:
            if p.isdigit():
                proposal = p
        rel = os.path.relpath(path, os.path.join(_ROOT, "docs")).replace(os.sep, "/")
        reports.setdefault(date, []).append(
            {
                "title": title,
                "proposal": proposal,
                "url": "/" + rel[:-3] + "/",
            }
        )
    return reports


def on_env(env, config, **kwargs):
    docs_dir = config["docs_dir"]
    today = dt.date.today()
    monday = today - dt.timedelta(days=today.weekday())
    week_days = [monday + dt.timedelta(days=i) for i in range(7)]

    # Load calendar events (for upcoming report events) once.
    calendar_dir = os.path.join(docs_dir, "community", "calendar")
    all_events = []
    if os.path.isdir(calendar_dir):
        try:
            all_events = load_events(calendar_dir)
        except Exception:
            all_events = []

    reports = _load_reports(os.path.join(docs_dir, "proposals", "proposals"))

    cells = []
    for day in week_days:
        iso = day.isoformat()
        uploaded = []
        for r in reports.get(iso, []):
            uploaded.append(r)
        upcoming = []
        for e in all_events:
            if _is_upcoming_report_event(e):
                if e.get("date") == iso and iso >= today.isoformat():
                    upcoming.append(
                        {
                            "title": e.get("title", ""),
                            "type": e.get("type", ""),
                            "category": e.get("category", ""),
                            "time": e.get("time", ""),
                            "url": e.get("url", ""),
                        }
                    )
        cells.append(
            {
                "date": iso,
                "weekday": _DAYS[day.weekday()],
                "day": day.day,
                "is_today": day == today,
                "is_past": iso < today.isoformat(),
                "uploaded": uploaded,
                "upcoming": upcoming,
            }
        )
    env.globals["reports_week"] = cells

    # Nearest upcoming report calls (any future date, beyond the shown week).
    upcoming_all = []
    for e in all_events:
        if _is_upcoming_report_event(e) and e.get("date", "") >= today.isoformat():
            upcoming_all.append(e)
    upcoming_all.sort(key=lambda e: (e.get("date", ""), e.get("time", "")))
    upcoming_next = []
    for e in upcoming_all[:10]:
        upcoming_next.append(
            {
                "date": e.get("date", ""),
                "title": e.get("title", ""),
                "type": e.get("type", ""),
                "time": e.get("time", ""),
                "url": e.get("url", ""),
            }
        )
    env.globals["reports_upcoming_next"] = upcoming_next
    return env