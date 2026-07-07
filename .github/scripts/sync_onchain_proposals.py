#!/usr/bin/env python3
"""Sync on-chain governance proposals from Gonka mainnet into proposals/proposals/.

Fetches all proposals from rpc.gonka.gg, generates:
- Individual proposal pages (proposals/proposals/{id}/index.md)
- Quarter-grouped index (proposals/proposals/index.md)
- Per-quarter sub-pages (proposals/proposals/{quarter}/index.md)
- Auto-updates mkdocs.yml nav section
"""

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

RPC_BASE = "https://rpc.gonka.gg"
OUTPUT_DIR = Path(os.environ.get("OUTPUT_DIR", "docs/proposals/proposals"))
MKDOCS_YML = Path(os.environ.get("MKDOCS_YML", "mkdocs.yml"))


# ── helpers ────────────────────────────────────────────────────

def escape_md(text):
    if not text:
        return ""
    return str(text).replace("|", "\\|").replace("\n", " ").replace("\r", "")


def escape_md_block(text):
    """Escape for markdown block content (not inline)."""
    if not text:
        return ""
    return str(text)


def get_quarter(dt):
    return f"{dt.year}-Q{(dt.month - 1) // 3 + 1}"


def format_status_label(status):
    return {
        "PROPOSAL_STATUS_PASSED": "Passed",
        "PROPOSAL_STATUS_REJECTED": "Rejected",
        "PROPOSAL_STATUS_VOTING_PERIOD": "Voting",
        "PROPOSAL_STATUS_DEPOSIT_PERIOD": "Deposit",
        "PROPOSAL_STATUS_FAILED": "Failed",
        "PROPOSAL_STATUS_UNSPECIFIED": "Unspecified",
    }.get(status, status)


def status_css(status):
    s = status.lower()
    if "passed" in s:
        return "prop-passed"
    elif "rejected" in s or "failed" in s:
        return "prop-rejected"
    elif "voting" in s:
        return "prop-voting"
    elif "deposit" in s:
        return "prop-deposit"
    return ""


def format_amount(amount_str, denom="ngonka"):
    try:
        amt = int(amount_str)
        if denom == "ngonka" or denom == "ugonka":
            factor = {"ngonka": 1_000_000_000, "ugonka": 1_000_000}.get(denom, 1_000_000_000)
            val = amt / factor
            if val >= 1_000_000:
                return f"{val/1_000_000:.1f}M GNK"
            elif val >= 1_000:
                return f"{val/1_000:.1f}K GNK"
            else:
                return f"{val:.2f} GNK"
        return f"{amt} {denom}"
    except (ValueError, TypeError):
        return str(amount_str)


def fmt_time(iso_str):
    if not iso_str:
        return ""
    try:
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d %H:%M UTC")
    except (ValueError, TypeError):
        return iso_str


def fmt_time_short(iso_str):
    if not iso_str:
        return ""
    try:
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d")
    except (ValueError, TypeError):
        return iso_str


def get_message_types(messages):
    """Extract human-readable message types from proposal messages."""
    types = set()
    for m in (messages or []):
        t = m.get("@type", "")
        name = t.rsplit(".", 1)[-1] if t else "Unknown"
        name = re.sub(r'^Msg', '', name)
        # convert CamelCase to spaced
        name = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', name)
        types.add(name)
    return ", ".join(sorted(types)) if types else "—"


# ── fetch proposals ────────────────────────────────────────────

def fetch_proposals():
    url = f"{RPC_BASE}/cosmos/gov/v1/proposals?pagination.limit=200"
    print(f"Fetching {url}...")
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    proposals = data.get("proposals", [])
    print(f"Got {len(proposals)} proposals")
    return proposals


# ── generate individual proposal page ──────────────────────────

def generate_proposal_page(proposal):
    pid = proposal["id"]
    title = proposal.get("title", f"Proposal #{pid}").strip()
    status = proposal.get("status", "PROPOSAL_STATUS_UNSPECIFIED")
    status_label = format_status_label(status)
    status_css_cls = status_css(status)

    submit_time = fmt_time(proposal.get("submit_time", ""))
    voting_start = fmt_time(proposal.get("voting_start_time", ""))
    voting_end = fmt_time(proposal.get("voting_end_time", ""))
    deposit_end = fmt_time(proposal.get("deposit_end_time", ""))
    proposer = proposal.get("proposer", "")
    metadata_url = proposal.get("metadata", "")
    summary = proposal.get("summary", "")
    expedited = proposal.get("expedited", False)
    failed_reason = proposal.get("failed_reason", "")

    messages = proposal.get("messages", [])
    msg_types = get_message_types(messages)

    tally = proposal.get("final_tally_result", {})
    yes_count = int(tally.get("yes_count", 0))
    no_count = int(tally.get("no_count", 0))
    abstain_count = int(tally.get("abstain_count", 0))
    no_with_veto_count = int(tally.get("no_with_veto_count", 0))
    total_votes = yes_count + no_count + abstain_count + no_with_veto_count

    # Generate description from summary
    description = summary

    # Status badge HTML
    badge_html = f'<span class="prop-badge {status_css_cls}">{status_label}</span>'

    # Tally section if voting period ended
    tally_html = ""
    if total_votes > 0:
        pct = lambda v: f"{(v / total_votes * 100):.1f}%" if total_votes > 0 else "0%"
        tally_html = f"""
<div class="prop-tally">
  <div class="prop-tally-bar">
    <div class="prop-tally-yes" style="width:{pct(yes_count)}"></div>
    <div class="prop-tally-no" style="width:{pct(no_count)}"></div>
    <div class="prop-tally-veto" style="width:{pct(no_with_veto_count)}"></div>
    <div class="prop-tally-abstain" style="width:{pct(abstain_count)}"></div>
  </div>
  <div class="prop-tally-stats">
    <span class="prop-tally-yes-text">Yes {yes_count:,} ({pct(yes_count)})</span>
    <span class="prop-tally-no-text">No {no_count:,} ({pct(no_count)})</span>
    <span class="prop-tally-veto-text">Veto {no_with_veto_count:,} ({pct(no_with_veto_count)})</span>
    <span class="prop-tally-abstain-text">Abstain {abstain_count:,} ({pct(abstain_count)})</span>
  </div>
</div>
"""

    md = f"""---
title: "#{pid} – {escape_md(title)}"
description: "{escape_md(summary[:200]) if summary else f'Proposal #{pid}'}"
template: proposals-proposals-main.html
---

# #{pid} – {title}

<div class="prop-detail-header" markdown="1">

{badge_html}

**Proposal ID:** `{pid}`

**Type:** {msg_types}

**Submit:** {submit_time}

**Voting:** {voting_start} → {voting_end}

"""
    if expedited:
        md += "**Expedited:** Yes\n\n"
    if proposer:
        md += f"**Proposer:** `{proposer}`\n\n"
    if metadata_url:
        md += f"**Metadata:** [{metadata_url}]({metadata_url})\n\n"
    if failed_reason:
        md += f"**Failed reason:** {failed_reason}\n\n"

    md += """</div>

"""

    if summary:
        md += f"{summary}\n\n---\n\n"

    if tally_html:
        md += f"""## Final Tally

{tally_html}

---

"""

    md += f"""## Messages

| # | Type |
| :- | :--- |
"""
    for i, m in enumerate(messages, 1):
        mt = m.get("@type", "Unknown")
        md += f"| {i} | `{mt}` |\n"

    md += f"""
---

<div class="prop-footer" markdown="1">

[View on Mintscan](https://www.mintscan.io/gonka/proposals/{pid}) · [View on Ping](https://ping.pub/gonka/gov/{pid}) · Data synced from [rpc.gonka.gg]({RPC_BASE})

</div>
"""

    return md


# ── generate overview index ────────────────────────────────────

def generate_overview(proposals_by_quarter):
    sorted_quarters = sorted(proposals_by_quarter.keys(), reverse=True)

    md = """---
title: On-Chain Governance Proposals
template: proposals-oview.html
---

# On-Chain Governance Proposals

<div class="prop-oview-filter" markdown="1">

<label class="prop-filter-cb">
  <input type="checkbox" id="prop-filter-passed" checked>
  <span class="prop-filter-label">Passed</span>
</label>
<label class="prop-filter-cb">
  <input type="checkbox" id="prop-filter-rejected" checked>
  <span class="prop-filter-label">Rejected</span>
</label>
<label class="prop-filter-cb">
  <input type="checkbox" id="prop-filter-voting" checked>
  <span class="prop-filter-label">Voting</span>
</label>
<label class="prop-filter-cb">
  <input type="checkbox" id="prop-filter-deposit" checked>
  <span class="prop-filter-label">Deposit</span>
</label>
<span class="prop-filter-count"></span>

</div>

"""

    total = 0
    for q in sorted_quarters:
        props = proposals_by_quarter[q]
        total += len(props)
        md += f'<div class="prop-quarter" id="{q.lower()}">\n'
        md += f"## {q}\n\n"
        md += f"*{len(props)} proposals*\n\n"

        for p in props:
            pid = p["id"]
            title = p.get("title", f"Proposal #{pid}").strip()
            status = p.get("status", "PROPOSAL_STATUS_UNSPECIFIED")
            status_label = format_status_label(status)
            status_css_cls = status_css(status)
            tally = p.get("final_tally_result", {})
            yes_c = int(tally.get("yes_count", 0))
            no_c = int(tally.get("no_count", 0))
            voting_end = fmt_time_short(p.get("voting_end_time", ""))
            submit_time = fmt_time_short(p.get("submit_time", ""))
            summary = p.get("summary", "")

            # Short summary (truncate)
            short_summary = summary[:200] + "…" if summary and len(summary) > 200 else (summary or "")

            md += f"""<div class="prop-card" data-status="{status_css_cls}">
  <div class="prop-card-header">
    <a href="{pid}/" class="prop-card-title">#{pid} – {title}</a>
    <span class="prop-badge {status_css_cls}">{status_label}</span>
  </div>
  <div class="prop-card-meta">
    <span>Submitted {submit_time}</span>
    <span>Voting ends {voting_end}</span>
  </div>
"""
            if short_summary:
                md += f'  <div class="prop-card-desc">{escape_md(short_summary)}</div>\n'

            if yes_c + no_c > 0:
                veto_c = int(tally.get("no_with_veto_count", 0))
                abstain_c = int(tally.get("abstain_count", 0))
                total_t = yes_c + no_c + veto_c + abstain_c
                _pct = lambda v: f"({v / total_t * 100:.1f}%)" if total_t > 0 else "(0.0%)"
                md += f'  <div class="prop-card-tally"><span class="prop-tally-yes-text">Yes {yes_c:,} {_pct(yes_c)}</span> · <span class="prop-tally-no-text">No {no_c:,} {_pct(no_c)}</span> · <span class="prop-tally-veto-text">Veto {veto_c:,} {_pct(veto_c)}</span> · <span class="prop-tally-abstain-text">Abstain {abstain_c:,} {_pct(abstain_c)}</span></div>\n'

            md += "</div>\n\n"

        md += "</div>\n"

    # stats bar
    md += f"""<div class="prop-oview-stats">
<em>{total} proposals across {len(sorted_quarters)} quarters. Last updated: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")}</em>
</div>

<script>
function initProposalsPage() {{
  var checkboxes = document.querySelectorAll('.prop-oview-filter input[type=checkbox]');
  var cards = document.querySelectorAll('.prop-card');
  var countEl = document.querySelector('.prop-filter-count');

  function apply() {{
    var filters = {{}};
    checkboxes.forEach(function(cb) {{
      filters[cb.id.replace('prop-filter-', '')] = cb.checked;
    }});
    var visible = 0;
    cards.forEach(function(card) {{
      var status = card.getAttribute('data-status');
      var show = false;
      if (status === 'prop-passed' && filters.passed) show = true;
      else if (status === 'prop-rejected' && filters.rejected) show = true;
      else if (status === 'prop-voting' && filters.voting) show = true;
      else if (status === 'prop-deposit' && filters.deposit) show = true;
      else if (status === 'prop-failed' && filters.rejected) show = true;
      card.style.display = show ? '' : 'none';
      if (show) visible++;
    }});
    countEl.textContent = visible + ' of ' + cards.length + ' proposals';
  }}

  checkboxes.forEach(function(cb) {{ cb.addEventListener('change', apply); }});
  apply();
}}

document$.subscribe(initProposalsPage);
</script>
"""

    return md


# ── generate quarter page ──────────────────────────────────────

def generate_quarter_page(quarter, proposals):
    props = proposals
    md = f"""---
title: "{quarter} Proposals"
template: proposals-oview.html
---

# {quarter} Proposals

<div class="prop-oview-filter" markdown="1">

<label class="prop-filter-cb">
  <input type="checkbox" id="prop-filter-passed" checked>
  <span class="prop-filter-label">Passed</span>
</label>
<label class="prop-filter-cb">
  <input type="checkbox" id="prop-filter-rejected" checked>
  <span class="prop-filter-label">Rejected</span>
</label>
<label class="prop-filter-cb">
  <input type="checkbox" id="prop-filter-voting" checked>
  <span class="prop-filter-label">Voting</span>
</label>
<label class="prop-filter-cb">
  <input type="checkbox" id="prop-filter-deposit" checked>
  <span class="prop-filter-label">Deposit</span>
</label>
<span class="prop-filter-count"></span>

</div>

<div class="prop-quarter">
<h2>{quarter}</h2>
<p>{len(props)} proposals</p>
"""

    for p in props:
        pid = p["id"]
        title = p.get("title", f"Proposal #{pid}").strip()
        status = p.get("status", "PROPOSAL_STATUS_UNSPECIFIED")
        status_label = format_status_label(status)
        status_css_cls = status_css(status)
        tally = p.get("final_tally_result", {})
        yes_c = int(tally.get("yes_count", 0))
        no_c = int(tally.get("no_count", 0))
        voting_end = fmt_time_short(p.get("voting_end_time", ""))
        submit_time = fmt_time_short(p.get("submit_time", ""))
        summary = p.get("summary", "")
        short_summary = summary[:200] + "…" if summary and len(summary) > 200 else (summary or "")

        md += f"""<div class="prop-card" data-status="{status_css_cls}">
  <div class="prop-card-header">
    <a href="../{pid}/" class="prop-card-title">#{pid} – {title}</a>
    <span class="prop-badge {status_css_cls}">{status_label}</span>
  </div>
  <div class="prop-card-meta">
    <span>Submitted {submit_time}</span>
    <span>Voting ends {voting_end}</span>
  </div>
"""
        if short_summary:
            md += f'  <div class="prop-card-desc">{escape_md(short_summary)}</div>\n'
        if yes_c + no_c > 0:
            veto_c = int(tally.get("no_with_veto_count", 0))
            abstain_c = int(tally.get("abstain_count", 0))
            total_t = yes_c + no_c + veto_c + abstain_c
            _pct = lambda v: f"({v / total_t * 100:.1f}%)" if total_t > 0 else "(0.0%)"
            md += f'  <div class="prop-card-tally"><span class="prop-tally-yes-text">Yes {yes_c:,} {_pct(yes_c)}</span> · <span class="prop-tally-no-text">No {no_c:,} {_pct(no_c)}</span> · <span class="prop-tally-veto-text">Veto {veto_c:,} {_pct(veto_c)}</span> · <span class="prop-tally-abstain-text">Abstain {abstain_c:,} {_pct(abstain_c)}</span></div>\n'
        md += "</div>\n\n"

    md += """</div>

<p><a href="../"><em>← Back to all proposals</em></a></p>

<script>
function initProposalsPage() {
  var checkboxes = document.querySelectorAll('.prop-oview-filter input[type=checkbox]');
  var cards = document.querySelectorAll('.prop-card');
  var countEl = document.querySelector('.prop-filter-count');
  function apply() {
    var filters = {};
    checkboxes.forEach(function(cb) {
      filters[cb.id.replace('prop-filter-', '')] = cb.checked;
    });
    var visible = 0;
    cards.forEach(function(card) {
      var status = card.getAttribute('data-status');
      var show = false;
      if (status === 'prop-passed' && filters.passed) show = true;
      else if (status === 'prop-rejected' && filters.rejected) show = true;
      else if (status === 'prop-voting' && filters.voting) show = true;
      else if (status === 'prop-deposit' && filters.deposit) show = true;
      else if (status === 'prop-failed' && filters.rejected) show = true;
      card.style.display = show ? '' : 'none';
      if (show) visible++;
    });
    countEl.textContent = visible + ' of ' + cards.length + ' proposals';
  }
  checkboxes.forEach(function(cb) { cb.addEventListener('change', apply); });
  apply();
}
document$.subscribe(initProposalsPage);
</script>
"""

    return md


# ── update mkdocs.yml nav ──────────────────────────────────────

def update_mkdocs_nav(sorted_quarters, proposals_by_quarter):
    if not MKDOCS_YML.exists():
        print(f"mkdocs.yml not found at {MKDOCS_YML}, skipping nav update")
        return

    content = MKDOCS_YML.read_text(encoding="utf-8")

    nav_lines = []
    nav_lines.append("    - On-Chain Governance: proposals/proposals/index.md")
    for q in sorted_quarters:
        q_lower = q.lower()
        props = proposals_by_quarter.get(q, [])
        # Sort by descending ID
        props_sorted = sorted(props, key=lambda x: int(x["id"]), reverse=True)
        nav_lines.append(f"    - {q}:")
        nav_lines.append(f'      - Overview: proposals/proposals/{q_lower}/index.md')
        for p in props_sorted:
            pid = p["id"]
            title = p.get("title", f"Proposal #{pid}").strip()
            title_esc = title.replace('"', '\\"')
            nav_lines.append(f'      - "#{pid} – {title_esc}": proposals/proposals/{pid}/index.md')

    new_nav = "\n".join(nav_lines)

    # Replace existing On-Chain Governance nav block
    pattern = r"    - On-Chain Governance:.*?(?=\n    - Pre-Proposals:)"
    replacement = new_nav

    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    if new_content == content:
        print("Warning: nav replacement failed, mkdocs.yml unchanged")
        print("Make sure 'On-Chain Governance:' exists before 'Pre-Proposals:' in nav")
        return

    MKDOCS_YML.write_text(new_content, encoding="utf-8")
    print(f"Updated mkdocs.yml nav with {len(sorted_quarters)} quarters and {sum(len(v) for v in proposals_by_quarter.values())} proposals")


# ── main ────────────────────────────────────────────────────────

def main():
    print("=== Sync On-Chain Proposals ===")
    proposals = fetch_proposals()

    # Parse and organize
    proposals_by_quarter = {}
    for p in proposals:
        submit = p.get("submit_time", "")
        if submit:
            try:
                dt = datetime.fromisoformat(submit.replace("Z", "+00:00"))
                q = get_quarter(dt)
            except (ValueError, TypeError):
                q = "Unknown"
        else:
            q = "Unknown"
        proposals_by_quarter.setdefault(q, []).append(p)

    # Sort within each quarter by descending proposal ID
    for q in proposals_by_quarter:
        proposals_by_quarter[q].sort(key=lambda x: int(x["id"]), reverse=True)

    sorted_quarters = sorted(proposals_by_quarter.keys(), reverse=True)

    # Ensure output dir exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Generate individual proposal pages
    print(f"\nGenerating {len(proposals)} proposal pages...")
    for p in proposals:
        pid = p["id"]
        prop_dir = OUTPUT_DIR / pid
        prop_dir.mkdir(exist_ok=True)
        page_md = generate_proposal_page(p)
        (prop_dir / "index.md").write_text(page_md, encoding="utf-8")

    # Generate quarter subpages
    print(f"Generating {len(sorted_quarters)} quarter pages...")
    for q in sorted_quarters:
        q_lower = q.lower()
        q_dir = OUTPUT_DIR / q_lower
        q_dir.mkdir(exist_ok=True)
        q_md = generate_quarter_page(q, proposals_by_quarter[q])
        (q_dir / "index.md").write_text(q_md, encoding="utf-8")

    # Generate overview
    print("Generating overview index...")
    overview_md = generate_overview(proposals_by_quarter)
    (OUTPUT_DIR / "index.md").write_text(overview_md, encoding="utf-8")

    # Update nav
    update_mkdocs_nav(sorted_quarters, proposals_by_quarter)

    print(f"\nDone. {len(proposals)} proposals in {len(sorted_quarters)} quarters → {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
