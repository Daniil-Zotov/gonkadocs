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


def yaml_str(text):
    """Escape for YAML double-quoted string value."""
    if not text:
        return '""'
    s = str(text).replace("\\", "\\\\").replace('"', '\\"')
    return f'"{s}"'


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


def parse_amounts(text):
    """Extract GNK and USDT amounts from proposal text body."""
    if not text:
        return (0, 0)
    text = str(text)

    gnk_total = 0
    gnk_pattern = re.compile(r"([\d,]+(?:\.\d+)?)\s*(K?)\s*GNK", re.IGNORECASE)
    for match in gnk_pattern.finditer(text):
        num_str = match.group(1).replace(",", "")
        k_suffix = match.group(2).upper()
        try:
            val = float(num_str)
            if k_suffix == "K":
                val *= 1000
            gnk_total += int(val)
        except ValueError:
            pass

    usdt_total = 0
    usdt_pattern = re.compile(r"\$([\d,]+(?:\.\d+)?)\s*(K?)|([\d,]+(?:\.\d+)?)\s*(K?)\s*USDT", re.IGNORECASE)
    for match in usdt_pattern.finditer(text):
        if match.group(1):
            num_str = match.group(1).replace(",", "")
            k_suffix = match.group(2).upper()
            try:
                val = float(num_str)
                if k_suffix == "K":
                    val *= 1000
                usdt_total += int(val)
            except ValueError:
                pass
        else:
            num_str = match.group(3).replace(",", "")
            k_suffix = match.group(4).upper()
            try:
                val = float(num_str)
                if k_suffix == "K":
                    val *= 1000
                usdt_total += int(val)
            except ValueError:
                pass

    return (gnk_total, usdt_total)


def categorize_type(msg_type):
    """Categorize proposal types into high-level buckets."""
    s = (msg_type or "").lower()
    if "upgrade" in s:
        return "Software Upgrade"
    elif "update params" in s or "allow list" in s:
        return "Governance Parameters"
    elif "community pool spend" in s or "execute contract" in s:
        return "Funding / Grants"
    elif "batch transfer" in s or "grc" in s or "restitution" in s or "compensation" in s:
        return "GRC / Restitution"
    elif "register model" in s or "register ibc" in s or "ibc" in s:
        return "Models / IBC"
    else:
        return "Other"


def parse_amounts_from_messages(messages):
    """Extract GNK and USDT amounts from proposal messages directly."""
    USDT_IBC_DENOM = "ibc/115F68FBA220A028C6F6ED08EA0C1A9C8C52798B14FB66E6C89D5D8C06A524D4"
    gnk_total = 0
    usdt_total = 0

    def coin_amount(coins, denom_suffix):
        total = 0
        for c in coins:
            denom = c.get("denom", "")
            try:
                amt = int(c.get("amount", "0"))
            except (ValueError, TypeError):
                amt = 0
            if denom == "ngonka":
                total += amt / 1_000_000_000
            elif denom == "ugonka":
                total += amt / 1_000_000
            elif denom == USDT_IBC_DENOM:
                usdt_total_local = amt / 1_000_000
                return total, usdt_total_local
            elif denom.endswith(denom_suffix):
                total += amt
        return total, 0

    for m in messages:
        t = m.get("@type", "")
        if "MsgCommunityPoolSpend" in t:
            for c in m.get("amount", []):
                denom = c.get("denom", "")
                try:
                    amt = int(c.get("amount", "0"))
                except (ValueError, TypeError):
                    continue
                if denom == "ngonka":
                    gnk_total += amt / 1_000_000_000
                elif denom == USDT_IBC_DENOM:
                    usdt_total += amt / 1_000_000

        elif "MsgExecuteContract" in t:
            wi = m.get("msg", {}).get("withdraw_ibc", {})
            if wi and wi.get("denom") == USDT_IBC_DENOM:
                try:
                    usdt_total += int(wi.get("amount", "0")) / 1_000_000
                except (ValueError, TypeError):
                    pass
            for c in m.get("funds", []):
                denom = c.get("denom", "")
                try:
                    amt = int(c.get("amount", "0"))
                except (ValueError, TypeError):
                    continue
                if denom == "ngonka":
                    gnk_total += amt / 1_000_000_000

        elif "MsgBatchTransferWithVesting" in t:
            for o in m.get("outputs", []):
                try:
                    gnk_total += int(o.get("amount", "0")) / 1_000_000_000
                except (ValueError, TypeError):
                    pass

        elif "MsgTransferWithVesting" in t:
            for c in m.get("amount", []):
                denom = c.get("denom", "")
                try:
                    amt = int(c.get("amount", "0"))
                except (ValueError, TypeError):
                    continue
                if denom == "ngonka":
                    gnk_total += amt / 1_000_000_000

        elif "MsgMultiSend" in t:
            for inp in m.get("inputs", []):
                for c in inp.get("coins", []):
                    denom = c.get("denom", "")
                    try:
                        amt = int(c.get("amount", "0"))
                    except (ValueError, TypeError):
                        continue
                    if denom == "ngonka":
                        gnk_total += amt / 1_000_000_000

    return int(gnk_total), int(usdt_total)


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

def generate_proposal_page(proposal, prop_dir):
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

    # Save messages as JSON
    msg_json = json.dumps(messages, indent=2, ensure_ascii=False)
    (prop_dir / "messages.json").write_text(msg_json, encoding="utf-8")

    tally = proposal.get("final_tally_result", {})
    yes_count = int(tally.get("yes_count", 0))
    no_count = int(tally.get("no_count", 0))
    abstain_count = int(tally.get("abstain_count", 0))
    no_with_veto_count = int(tally.get("no_with_veto_count", 0))
    total_votes = yes_count + no_count + abstain_count + no_with_veto_count

    # Extract funding from messages
    gnk_fund, usdt_fund = parse_amounts_from_messages(messages)

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

    # Funding line
    funding_parts = []
    if gnk_fund > 0:
        funding_parts.append(f'{gnk_fund:,} GNK')
    if usdt_fund > 0:
        funding_parts.append(f'${usdt_fund:,}')
    funding_html = ""
    if funding_parts:
        funding_html = f'<div class="prop-funding-line">{" · ".join(funding_parts)}</div>\n'

    summary_short = summary[:200] if summary else ""
    md = f"""---
title: {yaml_str(f"#{pid} – {title}")}
description: {yaml_str(summary_short if summary_short else f"Proposal #{pid}")}
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
        if metadata_url.startswith("http://") or metadata_url.startswith("https://"):
            md += f"**Metadata:** [{metadata_url}]({metadata_url})\n\n"
        else:
            md += f"**Metadata:** `{metadata_url}`\n\n"
    if failed_reason:
        md += f"**Failed reason:** {failed_reason}\n\n"
    if funding_html:
        md += funding_html

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

    # Contract spoiler
    md += f"""
<details class="prop-contracts">
<summary>Contract Details</summary>

```json
{msg_json}
```

</details>

---

<div class="prop-footer" markdown="1">

[View on gonka.gg](https://gonka.gg/network/proposals/{pid}){{:target="_blank"}}

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
<span class="prop-filter-count"></span>

</div>

"""

    # Compute overall stats
    total = 0
    all_props = []
    for q in sorted_quarters:
        props = proposals_by_quarter[q]
        all_props.extend(props)
        total += len(props)
    all_passed = sum(1 for p in all_props if p.get("status", "").lower() == "proposal_status_passed")
    all_rejected = sum(1 for p in all_props if p.get("status", "").lower() == "proposal_status_rejected")
    all_failed = sum(1 for p in all_props if p.get("status", "").lower() == "proposal_status_failed")
    all_pct_passed = (all_passed / total * 100) if total else 0
    all_pct_rejected = (all_rejected / total * 100) if total else 0
    all_pct_failed = (all_failed / total * 100) if total else 0

    all_cat_counts = {}
    for p in all_props:
        msg_types = get_message_types(p.get("messages", []))
        cat = categorize_type(msg_types)
        all_cat_counts[cat] = all_cat_counts.get(cat, 0) + 1
    all_cat_rows = ""
    if all_cat_counts:
        for cat, cnt in sorted(all_cat_counts.items(), key=lambda x: x[1], reverse=True):
            pct = (cnt / total * 100) if total else 0
            all_cat_rows += f'<div class="qs-row"><span class="qs-label">{cat}</span><span class="qs-bar-wrap"><span class="qs-bar" style="width:{pct:.0f}%"></span></span><span class="qs-value">{cnt}</span></div>\n'

    o_gnk = 0
    o_usdt = 0
    for p in all_props:
        if p.get("status", "").lower() == "proposal_status_passed":
            _g, _u = parse_amounts_from_messages(p.get("messages", []))
            o_gnk += _g
            o_usdt += _u
    o_funding_parts = []
    if o_gnk > 0:
        o_funding_parts.append(f'{o_gnk:,} GNK')
    if o_usdt > 0:
        o_funding_parts.append(f'${o_usdt:,}')
    o_funding_line = f'<div class="qs-funding-line">{" · ".join(o_funding_parts)}</div>\n' if o_funding_parts else ""

    md += f'''<div class="quarter-summary" markdown="1">

## Overview

<div class="qs-stats">
<div class="qs-stat total"><span class="qs-num">{total}</span><span class="qs-desc">Total Proposals</span></div>
<div class="qs-stat passed"><span class="qs-num">{all_passed}</span><span class="qs-desc">Passed ({all_pct_passed:.0f}%)</span></div>
<div class="qs-stat rejected"><span class="qs-num">{all_rejected}</span><span class="qs-desc">Rejected ({all_pct_rejected:.0f}%)</span></div>
{f'<div class="qs-stat failed"><span class="qs-num">{all_failed}</span><span class="qs-desc">Failed ({all_pct_failed:.0f}%)</span></div>' if all_failed > 0 else ''}
</div>

<div class="qs-categories">
{all_cat_rows}</div>

{o_funding_line}

</div>

'''

    for q in sorted_quarters:
        props = proposals_by_quarter[q]
        md += f'<div class="prop-quarter" id="{q.lower()}" markdown="1">\n'
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
    <a href="{q.lower()}/{pid}/" class="prop-card-title">#{pid} – {title}</a>
    <span class="prop-badge {status_css_cls}">{status_label}</span>
  </div>
  <div class="prop-card-meta">
    <span>Submitted {submit_time}</span>
    <span>Voting ends {voting_end}</span>
  </div>
"""
            if short_summary:
                md += f'  <div class="prop-card-desc">{escape_md(short_summary)}</div>\n'

            if yes_c + no_c > 0 or status_css_cls == "prop-passed":
                veto_c = int(tally.get("no_with_veto_count", 0))
                abstain_c = int(tally.get("abstain_count", 0))
                total_t = yes_c + no_c + veto_c + abstain_c
                _pct = lambda v: f"({v / total_t * 100:.1f}%)" if total_t > 0 else "(0.0%)"
                _tally_line = f'<span class="prop-tally-yes-text">Yes {yes_c:,} {_pct(yes_c)}</span> · <span class="prop-tally-no-text">No {no_c:,} {_pct(no_c)}</span> · <span class="prop-tally-veto-text">Veto {veto_c:,} {_pct(veto_c)}</span> · <span class="prop-tally-abstain-text">Abstain {abstain_c:,} {_pct(abstain_c)}</span>'

                _funding_html = ""
                if status_css_cls == "prop-passed":
                    _gnk, _usdt = parse_amounts_from_messages(p.get("messages", []))
                    _funding_parts = []
                    if _gnk > 0:
                        _funding_parts.append(f'{_gnk:,} GNK')
                    if _usdt > 0:
                        _funding_parts.append(f'${_usdt:,}')
                    if _funding_parts:
                        _funding_html = f'<span class="prop-card-funding">{" · ".join(_funding_parts)}</span>'

                md += f'  <div class="prop-card-tally">{_tally_line}{_funding_html}</div>\n'

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
    total = len(props)
    passed = sum(1 for p in props if p.get("status", "").lower() == "proposal_status_passed")
    rejected = sum(1 for p in props if p.get("status", "").lower() == "proposal_status_rejected")
    failed = sum(1 for p in props if p.get("status", "").lower() == "proposal_status_failed")
    pct_passed = (passed / total * 100) if total else 0
    pct_rejected = (rejected / total * 100) if total else 0
    pct_failed = (failed / total * 100) if total else 0

    # Categories
    cat_counts = {}
    for p in props:
        msg_types = get_message_types(p.get("messages", []))
        cat = categorize_type(msg_types)
        cat_counts[cat] = cat_counts.get(cat, 0) + 1

    cat_rows = ""
    if cat_counts:
        for cat, cnt in sorted(cat_counts.items(), key=lambda x: x[1], reverse=True):
            pct = (cnt / total * 100) if total else 0
            cat_rows += f'<div class="qs-row"><span class="qs-label">{cat}</span><span class="qs-bar-wrap"><span class="qs-bar" style="width:{pct:.0f}%"></span></span><span class="qs-value">{cnt}</span></div>\n'
    else:
        cat_rows = '<div class="qs-row"><span class="qs-label">Other</span><span class="qs-bar-wrap"><span class="qs-bar" style="width:100%"></span></span><span class="qs-value">{total}</span></div>\n'

    # Funding totals from passed proposals
    q_gnk = 0
    q_usdt = 0
    for p in props:
        if p.get("status", "").lower() == "proposal_status_passed":
            _g, _u = parse_amounts_from_messages(p.get("messages", []))
            q_gnk += _g
            q_usdt += _u
    q_funding_parts = []
    if q_gnk > 0:
        q_funding_parts.append(f'{q_gnk:,} GNK')
    if q_usdt > 0:
        q_funding_parts.append(f'${q_usdt:,}')
    q_funding_line = f'<div class="qs-funding-line">{" · ".join(q_funding_parts)}</div>\n' if q_funding_parts else ""

    md = f'''---
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
<span class="prop-filter-count"></span>

</div>

<div class="quarter-summary" markdown="1">

## {quarter} Summary

<div class="qs-stats">
<div class="qs-stat total"><span class="qs-num">{total}</span><span class="qs-desc">Total Proposals</span></div>
<div class="qs-stat passed"><span class="qs-num">{passed}</span><span class="qs-desc">Passed ({pct_passed:.0f}%)</span></div>
<div class="qs-stat rejected"><span class="qs-num">{rejected}</span><span class="qs-desc">Rejected ({pct_rejected:.0f}%)</span></div>
{f'<div class="qs-stat failed"><span class="qs-num">{failed}</span><span class="qs-desc">Failed ({pct_failed:.0f}%)</span></div>' if failed > 0 else ''}
</div>

<div class="qs-categories">
{cat_rows}</div>

{q_funding_line}

</div>

<div class="prop-quarter">
<h2>{quarter}</h2>
<p>{len(props)} proposals</p>
'''

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

        md += f'''<div class="prop-card" data-status="{status_css_cls}">
  <div class="prop-card-header">
    <a href="{pid}/" class="prop-card-title">#{pid} – {title}</a>
    <span class="prop-badge {status_css_cls}">{status_label}</span>
  </div>
  <div class="prop-card-meta">
    <span>Submitted {submit_time}</span>
    <span>Voting ends {voting_end}</span>
  </div>
'''
        if short_summary:
            md += f'  <div class="prop-card-desc">{escape_md(short_summary)}</div>\n'
        if yes_c + no_c > 0 or status_css_cls == "prop-passed":
            veto_c = int(tally.get("no_with_veto_count", 0))
            abstain_c = int(tally.get("abstain_count", 0))
            total_t = yes_c + no_c + veto_c + abstain_c
            _pct = lambda v: f"({v / total_t * 100:.1f}%)" if total_t > 0 else "(0.0%)"
            _tally_line = f'<span class="prop-tally-yes-text">Yes {yes_c:,} {_pct(yes_c)}</span> · <span class="prop-tally-no-text">No {no_c:,} {_pct(no_c)}</span> · <span class="prop-tally-veto-text">Veto {veto_c:,} {_pct(veto_c)}</span> · <span class="prop-tally-abstain-text">Abstain {abstain_c:,} {_pct(abstain_c)}</span>'

            _funding_html = ""
            if status_css_cls == "prop-passed":
                _gnk, _usdt = parse_amounts_from_messages(p.get("messages", []))
                _funding_parts = []
                if _gnk > 0:
                    _funding_parts.append(f'{_gnk:,} GNK')
                if _usdt > 0:
                    _funding_parts.append(f'${_usdt:,}')
                if _funding_parts:
                    _funding_html = f'<span class="prop-card-funding">{" · ".join(_funding_parts)}</span>'

            md += f'  <div class="prop-card-tally">{_tally_line}{_funding_html}</div>\n'
        md += "</div>\n\n"

    md += '''</div>

<p><a href="../"><em>← Back to all proposals</em></a></p>

<script>
function initProposalsPage() {
  var checkboxes = document.querySelectorAll(\'.prop-oview-filter input[type=checkbox]\');
  var cards = document.querySelectorAll(\'.prop-card\');
  var countEl = document.querySelector(\'.prop-filter-count\');
  function apply() {
    var filters = {};
    checkboxes.forEach(function(cb) {
      filters[cb.id.replace(\'prop-filter-\', \'\')] = cb.checked;
    });
    var visible = 0;
    cards.forEach(function(card) {
      var status = card.getAttribute(\'data-status\');
      var show = false;
      if (status === \'prop-passed\' && filters.passed) show = true;
      else if (status === \'prop-rejected\' && filters.rejected) show = true;
      else if (status === \'prop-voting\' && filters.voting) show = true;
      else if (status === \'prop-failed\' && filters.rejected) show = true;
      card.style.display = show ? \'\' : \'none\';
      if (show) visible++;
    });
    countEl.textContent = visible + \' of \' + cards.length + \' proposals\';
  }
  checkboxes.forEach(function(cb) { cb.addEventListener(\'change\', apply); });
  apply();
}
document$.subscribe(initProposalsPage);
</script>
'''

    return md


# ── update mkdocs.yml nav ──────────────────────────────────────

def update_mkdocs_nav(sorted_quarters, proposals_by_quarter):
    if not MKDOCS_YML.exists():
        print(f"mkdocs.yml not found at {MKDOCS_YML}, skipping nav update")
        return

    content = MKDOCS_YML.read_text(encoding="utf-8")

    nav_lines = []
    nav_lines.append("    - On-Chain Governance Proposals:")
    nav_lines.append("      - On-Chain Governance: proposals/proposals/index.md")
    for q in sorted_quarters:
        q_lower = q.lower()
        props = proposals_by_quarter.get(q, [])
        # Sort by descending ID
        props_sorted = sorted(props, key=lambda x: int(x["id"]), reverse=True)
        nav_lines.append(f"      - {q}:")
        nav_lines.append(f'        - Overview: proposals/proposals/{q_lower}/index.md')
        for p in props_sorted:
            pid = p["id"]
            title = p.get("title", f"Proposal #{pid}").strip()
            title_esc = title.replace('"', '\\"')
            nav_lines.append(f'        - "#{pid} – {title_esc}": proposals/proposals/{q_lower}/{pid}/index.md')

    new_nav = "\n".join(nav_lines)

    # Replace existing On-Chain Governance nav block
    # On-Chain Governance is the last nav item before `theme:` top-level key
    pattern = r"    - On-Chain Governance Proposals:.*?(?=\ntheme:)"
    replacement = new_nav

    # Check if pattern exists before attempting replacement
    if not re.search(pattern, content, re.DOTALL):
        print("Warning: could not find On-Chain Governance nav block in mkdocs.yml")
        return

    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    if new_content == content:
        print("On-chain governance nav is already up to date")
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

    # Generate individual proposal pages (organized by quarter)
    print(f"\nGenerating {len(proposals)} proposal pages...")
    for p in proposals:
        pid = p["id"]
        submit = p.get("submit_time", "")
        if submit:
            try:
                dt = datetime.fromisoformat(submit.replace("Z", "+00:00"))
                q_lower = get_quarter(dt).lower()
            except (ValueError, TypeError):
                q_lower = "unknown"
        else:
            q_lower = "unknown"
        prop_dir = OUTPUT_DIR / q_lower / pid
        prop_dir.mkdir(parents=True, exist_ok=True)
        page_md = generate_proposal_page(p, prop_dir)
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
