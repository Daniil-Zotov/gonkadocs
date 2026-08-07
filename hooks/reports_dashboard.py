"""MkDocs hook: injects a full-year proposal-reports calendar into the template context.

The reports dashboard page (docs/overrides/reports-dashboard.html) renders a full-year
calendar (all 12 months, grouped into 4 collapsible quarters) drawn with thin gray
lines. Each day cell shows a small day number plus color-coded events:

  * light blue  — upcoming call (a scheduled report call for a proposal that has no
                  report yet);
                 blue   — past call that was followed by a published report;
                 gray   — expected report (upcoming call for a proposal that already
                  has recurring reports, i.e. the next one is expected);
                 green  — a published report (report*.md);
                 red    — overdue: a past report call that was not followed by a
                  published report.

Every published report shows: proposal number + proposal name (both link to the
proposal page) and, below, the report title linking to the report page.
"""

import datetime as dt
import glob
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
_QUARTERS = ["Q1", "Q2", "Q3", "Q4"]
_WEEKDAYS = ["MO", "TU", "WE", "TH", "FR", "SA", "SU"]

_CALL_TYPES = {"committee_call", "community_call", "network_event"}

STATUS_UPCOMING = "upcoming"  # light blue
STATUS_PAST = "past"          # blue
STATUS_EXPECTED = "expected"  # gray
STATUS_PUBLISHED = "published"  # green
STATUS_OVERDUE = "overdue"    # red


def _strip_frontmatter(text):
    return re.sub(r"\A---\s*\n.*?^---\s*\n", "", text, flags=re.DOTALL | re.MULTILINE).strip()


def _load_reports(proposals_dir):
    """Scan report*.md → list of {date, proposal, title, name_url, report_url}."""
    out = []
    for path in sorted(glob.glob(os.path.join(proposals_dir, "**", "report*.md"), recursive=True)):
        try:
            content = _strip_frontmatter(open(path, encoding="utf-8").read())
        except OSError:
            continue
        m = re.search(r"\*\*Дата публикации:\*\*\s*([\d-]+)", content)
        if not m:
            continue
        date = m.group(1)
        title = ""
        h1 = re.search(r"^#\s+(.+)$", content, flags=re.MULTILINE)
        title = h1.group(1).strip() if h1 else os.path.basename(path)
        proposal = ""
        for p in path.split(os.sep):
            if p.isdigit():
                proposal = p
        rel = os.path.relpath(path, os.path.join(_ROOT, "docs")).replace(os.sep, "/")
        out.append(
            {
                "date": date,
                "proposal": proposal,
                "title": title,
                "url": "/" + rel[:-3] + "/",
                "proposal_title": "",
            }
        )
    try:
        out.sort(key=lambda r: r["date"])
    except Exception:
        pass
    return out


def _proposal_map(proposals_dir):
    """id -> {name, url} from proposals.json descriptions."""
    mp = {}
    json_path = os.path.join(os.path.dirname(proposals_dir), "calendar", "proposals.json")
    if os.path.isfile(json_path):
        try:
            data = json.load(open(json_path, encoding="utf-8"))
        except Exception:
            data = []
        if not isinstance(data, list):
            data = data.get("events", [])
        for it in data:
            if it.get("type") != "proposal_report":
                continue
            mm = re.match(r"^(?:Passed|Rejected|Failed|Voting):\s*#(\d+)\s*[–—-]\s*(.+)$", it.get("title", ""))
            if mm:
                mp[int(mm.group(1))] = {"name": mm.group(2).strip()}
    # add urls by scanning proposal dirs
    for qdir in sorted(glob.glob(os.path.join(proposals_dir, "*"))):
        if not os.path.isdir(qdir):
            continue
        for pdir in sorted(glob.glob(os.path.join(qdir, "*"))):
            pid = os.path.basename(pdir)
            if not pid.isdigit():
                continue
            rel = os.path.relpath(pdir, os.path.join(_ROOT, "docs")).replace(os.sep, "/")
            entry = mp.setdefault(int(pid), {"name": f"#{pid}"})
            entry["url"] = "/" + rel + "/"
    return mp


def _is_call(e):
    return (e.get("type") or "").lower() in _CALL_TYPES


def _call_proposal_id(e, pmap):
    u = (e.get("url") or "")
    mm = re.search(r"/(\d+)/?$", u)
    if mm and int(mm.group(1)) in pmap:
        return int(mm.group(1))
    mm = re.search(r"#(\d+)", e.get("title") or "")
    return int(mm.group(1)) if mm else None


def _today():
    return dt.date.today()


def _build_events(reports, all_events, pmap, today):
    """Return events dict: date(str) -> list of {status, ...}."""
    by_date = {}

    def add(dstr, item):
        by_date.setdefault(dstr, []).append(item)

    # 1) published reports -> green
    for r in reports:
        try:
            d = dt.date.fromisoformat(r["date"])
        except (ValueError, TypeError):
            continue
        add(r["date"], {
            "status": STATUS_PUBLISHED,
            "proposal": r["proposal"],
            "title": r["title"],
            "url": r["url"],
            "date": r["date"],
        })

    # 2) report calls from calendar -> classify
    pmap_ids = set(pmap.keys())
    for e in all_events:
        if not _is_call(e):
            continue
        dstr = e.get("date", "")
        try:
            d = dt.date.fromisoformat(dstr)
        except (ValueError, TypeError):
            continue
        pid = _parse_proposal_id(e, pmap)
        # reports published for this proposal
        pid_str = str(pid) if pid else None
        prop_reports = [r for r in reports if r["proposal"] == pid_str]
        has_any = len(prop_reports) > 0
        if d > today:
            status = STATUS_EXPECTED if has_any else STATUS_UPCOMING
        else:
            # past call: delivered if a report exists on/after this call date
            after = [r for r in prop_reports if r["date"] >= dstr]
            status = STATUS_PAST if after else STATUS_OVERDUE
        add(dstr, {
            "status": status,
            "proposal": pid,
            "title": e.get("title", ""),
            "url": pmap.get(pid, {}).get("url", ""),
            "date": dstr,
            "time": e.get("time", ""),
        })

    return by_date


def on_env(env, config, **kwargs):
    docs_dir = config["docs_dir"]
    today = _today()
    proposals_dir = os.path.join(docs_dir, "proposals", "proposals")

    reports = _load_reports(proposals_dir)
    pmap = _proposal_map(proposals_dir)
    all_events = []
    cal_dir = os.path.join(docs_dir, "community", "calendar")
    if os.path.isdir(cal_dir):
        try:
            all_events = load_events(cal_dir)
        except Exception:
            all_events = []
    all_events = [e for e in all_events if e.get("date", "")]

    by_date = _build_events(reports, all_events, pmap, today)

    # enrich published reports with proposal name
    for dstr, items in by_date.items():
        for it in items:
            if it["status"] == STATUS_PUBLISHED:
                ent = pmap.get(int(it["proposal"]), {}) if it["proposal"] else {}
                it["proposal_name"] = ent.get("name", f"#{it['proposal']}")
                it["proposal_url"] = ent.get("url", "")

    # Build calendar months for the span of data (min year .. max year), default current year.
    dates = [dt.date.fromisoformat(d) for d in by_date if d]
    if dates:
        span_years = range(min(d.year for d in dates), max(d.year for d in dates) + 1)
    else:
        span_years = range(today.year, today.year + 1)

    quarters_out = []
    for year in span_years:
        buckets = {q: [] for q in _QUARTERS}
        for mi in range(12):
            month = {
                "label": _MONTHS[mi],
                "year": year,
                "num": mi + 1,
                "weeks": [],
            }
            buckets[_QUARTERS[mi // 3]].append(month)
        for q in _QUARTERS:
            for month in buckets[q]:
                _fill_month(month, by_date, today)
            quarters_out.append({"label": f"{year}-{q}", "ym": f"{year}-{buckets[q][0]['num']:02d}", "months": buckets[q]})

    env.globals["reports_quarters"] = quarters_out
    env.globals["reports_today"] = today.isoformat()
    return env


def _fill_month(month, by_date, today):
    from calendar import monthcalendar
    year, num = month["year"], month["num"]
    weeks = []
    for wk in monthcalendar(year, num):
        days = []
        for dd in wk:
            if dd == 0:
                days.append({"empty": True})
                continue
            d = dt.date(year, num, dd)
            dstr = d.isoformat()
            evs = sorted(by_date.get(dstr, []), key=lambda it: _status_rank(it["status"]))
            days.append({
                "empty": False,
                "day": dd,
                "col": d.weekday() + 1,
                "date": dstr,
                "is_today": d == today,
                "is_weekend": d.weekday() >= 5,
                "events": evs,
            })
        weeks.append(days)
    month["weeks"] = weeks


_status_rank_map = {
    STATUS_PUBLISHED: 0,
    STATUS_OVERDUE: 1,
    STATUS_EXPECTED: 2,
    STATUS_UPCOMING: 3,
    STATUS_PAST: 4,
}


def _status_rank(s):
    return _status_rank_map.get(s, 5)


def _parse_proposal_id(e, pmap):
    u = (e.get("url") or "")
    mm = re.search(r"/(\d+)/?$", u)
    if mm and int(mm.group(1)) in pmap:
        return int(mm.group(1))
    mm = re.search(r"#(\d+)", e.get("title") or "")
    return int(mm.group(1)) if mm else None