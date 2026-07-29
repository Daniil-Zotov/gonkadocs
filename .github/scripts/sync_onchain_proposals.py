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
import time
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

import requests

# ── Bounty reward distributions by upgrade version ──────────────
# Mirrors BOUNTY_DISTRIBUTIONS in buildtools/update-community-pool.py.
# Maps version → bounty info shown on upgrade proposal pages.
BOUNTY_BY_VERSION = {
    "v0.2.6":  {"total": 30000, "denom": "GNK",   "source": "Gov Module",      "pr": 497,  "pr_status": "Merged"},
    "v0.2.10": {"total": 23000, "denom": "GNK",   "source": "Gov Module",      "pr": 733,  "pr_status": "Merged"},
    "v0.2.11": {"total": 150750,"denom": "GNK",   "source": "Gov Module",      "pr": 919,  "pr_status": "Merged"},
    "v0.2.12": {"total": 35200, "denom": "USDT",  "source": "Community Sale",  "pr": 1113, "pr_status": "Merged"},
    "v0.2.13": {"total": 18000, "denom": "USDT",  "source": "Community Sale",  "pr": 1168, "pr_status": "Merged"},
    "v0.2.14": {"total": 45250, "denom": "USDT",  "source": "Community Sale",  "pr": 1446, "pr_status": "Merged"},
    "v0.2.15": {"total": 39825, "denom": "USDT",  "source": "Community Sale",  "pr": 1503, "pr_status": "Merged"},
}

RPC_ENDPOINTS = [
    "https://rpc.gonka.gg",
    "https://node3.gonka.ai/chain-api",
    "http://node1.gonka.ai:8000/chain-api",
]
OUTPUT_DIR = Path(os.environ.get("OUTPUT_DIR", "docs/proposals/proposals"))
MKDOCS_YML = Path(os.environ.get("MKDOCS_YML", "mkdocs.yml"))
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds


def fetch_with_retry(url, timeout=30):
    """Try fetching URL across all RPC endpoints with retries."""
    last_error = None
    for endpoint in RPC_ENDPOINTS:
        full_url = url.replace("{BASE}", endpoint.rstrip("/"))
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                print(f"  [{endpoint}] attempt {attempt}/{MAX_RETRIES}...")
                resp = requests.get(full_url, timeout=timeout)
                resp.raise_for_status()
                if not resp.text.strip():
                    print("  empty response, will retry")
                    raise ValueError("empty response")
                return resp.json()
            except Exception as e:
                last_error = e
                print(f"  failed: {e}")
                if attempt < MAX_RETRIES:
                    time.sleep(RETRY_DELAY * attempt)
    print(f"ERROR: all endpoints exhausted, last error: {last_error}")
    sys.exit(1)


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


def linkify(text):
    """Convert URLs and gonka1 addresses to clickable HTML links."""
    if not text:
        return ""
    import re
    s = str(text)
    s = re.sub(r'https?://[^\s<>"\'()]+', lambda m: f'<a href="{m.group(0)}" target="_blank">{m.group(0)}</a>', s)
    s = re.sub(r'\b(gonka1[ac-hj-np-z02-9]{38,})\b', lambda m: f'<a href="https://gonka.gg/address/{m.group(1)}" target="_blank">{m.group(1)}</a>', s)
    return s


def linkify_md(text):
    """Convert URLs and gonka1 addresses to Markdown links."""
    if not text:
        return ""
    import re
    s = str(text)
    s = re.sub(r'(?<!<)(https?://[^\s<>"\'()]+)(?!>)', lambda m: f'<{m.group(1)}>', s)
    s = re.sub(r'\b(gonka1[ac-hj-np-z02-9]{38,})\b', lambda m: f'[{m.group(1)}](https://gonka.gg/address/{m.group(1)})', s)
    return s


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


def get_upgrade_version(messages):
    """Extract the software upgrade plan name from proposal messages."""
    for m in (messages or []):
        if "MsgSoftwareUpgrade" in m.get("@type", ""):
            return m.get("plan", {}).get("name", "")
    return ""


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


def _vote_option_display(opts):
    """Convert vote options to display HTML."""
    parts = []
    for o in opts:
        opt = o.get("option", "")
        w = float(o.get("weight", "0"))
        label = opt.replace("VOTE_OPTION_", "").title()
        cls = opt.lower().replace("vote_option_", "")
        if cls == "yes":
            cls = "prop-vote-yes"
        elif cls == "no":
            cls = "prop-vote-no"
        elif cls == "no_with_veto":
            cls = "prop-vote-veto"
        elif cls == "abstain":
            cls = "prop-vote-abstain"
        pct = f"{w * 100:.1f}%" if w else ""
        parts.append(f'<span class="prop-voter-option {cls}">{label} {pct}</span>')
    return " ".join(parts)


def _format_voter_row(v):
    voter = v.get("voter", "")
    opts = v.get("options", [])
    addr_link = f'<a href="https://gonka.gg/address/{voter}" target="_blank" class="prop-voter-addr">{voter[:12]}…{voter[-6:]}</a>'
    return f"<tr><td>{addr_link}</td><td>{_vote_option_display(opts)}</td></tr>"


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


def parse_amounts_by_source(messages):
    """Extract GNK and USDT amounts grouped by funding source.

    Returns dict[str, tuple[int, int]] mapping source name to (gnk, usdt).
    Sources: "Community Pool" (MsgCommunityPoolSpend, MsgExecuteContract)
             "Gov Module" (MsgBatchTransferWithVesting, MsgTransferWithVesting, MsgMultiSend)
    """
    USDT_IBC_DENOM = "ibc/115F68FBA220A028C6F6ED08EA0C1A9C8C52798B14FB66E6C89D5D8C06A524D4"
    raw = {}

    for m in messages:
        t = m.get("@type", "")

        if "MsgCommunityPoolSpend" in t or "MsgExecuteContract" in t:
            source = "Community Pool"
        elif "MsgBatchTransferWithVesting" in t or "MsgTransferWithVesting" in t or "MsgMultiSend" in t:
            source = "Gov Module"
        else:
            continue

        gnk_raw, usdt_raw = raw.get(source, (0, 0))

        if "MsgCommunityPoolSpend" in t:
            for c in m.get("amount", []):
                denom = c.get("denom", "")
                try:
                    amt = int(c.get("amount", "0"))
                except (ValueError, TypeError):
                    continue
                if denom == "ngonka":
                    gnk_raw += amt
                elif denom == USDT_IBC_DENOM:
                    usdt_raw += amt

        elif "MsgExecuteContract" in t:
            wi = m.get("msg", {}).get("withdraw_ibc", {})
            if wi and wi.get("denom") == USDT_IBC_DENOM:
                try:
                    usdt_raw += int(wi.get("amount", "0"))
                except (ValueError, TypeError):
                    pass
            for c in m.get("funds", []):
                denom = c.get("denom", "")
                try:
                    amt = int(c.get("amount", "0"))
                except (ValueError, TypeError):
                    continue
                if denom == "ngonka":
                    gnk_raw += amt

        elif "MsgBatchTransferWithVesting" in t:
            for o in m.get("outputs", []):
                for c in (o.get("amount") or []):
                    denom = c.get("denom", "")
                    try:
                        amt = int(c.get("amount", "0"))
                    except (ValueError, TypeError):
                        continue
                    if denom == "ngonka":
                        gnk_raw += amt
                    elif denom == USDT_IBC_DENOM:
                        usdt_raw += amt

        elif "MsgTransferWithVesting" in t:
            for c in m.get("amount", []):
                denom = c.get("denom", "")
                try:
                    amt = int(c.get("amount", "0"))
                except (ValueError, TypeError):
                    continue
                if denom == "ngonka":
                    gnk_raw += amt

        elif "MsgMultiSend" in t:
            for inp in m.get("inputs", []):
                for c in inp.get("coins", []):
                    denom = c.get("denom", "")
                    try:
                        amt = int(c.get("amount", "0"))
                    except (ValueError, TypeError):
                        continue
                    if denom == "ngonka":
                        gnk_raw += amt

        raw[source] = (gnk_raw, usdt_raw)

    return {src: (int(gnk / 1_000_000_000), int(usdt / 1_000_000)) for src, (gnk, usdt) in raw.items()}


def funding_parts_by_source(amt_by_source):
    """Convert parse_amounts_by_source result to display strings.

    Returns list of strings like "100,000 GNK · Community Pool".
    """
    parts = []
    for source in sorted(amt_by_source.keys()):
        gnk, usdt = amt_by_source[source]
        sub = []
        if gnk > 0:
            sub.append(f"{gnk:,} GNK")
        if usdt > 0:
            sub.append(f"${usdt:,}")
        if sub:
            sub.append(source)
            parts.append(" · ".join(sub))
    return parts


# ── fetch proposals ────────────────────────────────────────────

def fetch_proposals():
    url = "{BASE}/cosmos/gov/v1/proposals?pagination.limit=200"
    print(f"Fetching proposals...")
    data = fetch_with_retry(url)
    proposals = data.get("proposals", [])
    print(f"Got {len(proposals)} proposals")
    return proposals


# ── generate individual proposal page ──────────────────────────

def generate_proposal_page(proposal, prop_dir, total_voting_power=0):
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
    amt_by_source = parse_amounts_by_source(messages)

    # Status badge HTML
    voting_end_iso = proposal.get("voting_end_time", "")
    if status_css_cls == "prop-voting" and voting_end_iso:
        badge_html = f'<div class="prop-badge-row"><span class="prop-badge {status_css_cls}">{status_label}</span><span class="prop-vote-countdown prop-vote-countdown-detail" data-deadline="{voting_end_iso}"></span></div>'
    else:
        badge_html = f'<span class="prop-badge {status_css_cls}">{status_label}</span>'

    # Tally section if voting period ended
    tally_html = ""
    if total_votes > 0:
        stat_pct = lambda v: f"{(v / total_votes * 100):.1f}%" if total_votes > 0 else "0%"
        if total_voting_power > 0:
            _vp = total_voting_power
            bar_pct = lambda v: f"{v / _vp * 100:.1f}%"
        else:
            bar_pct = lambda v: f"{v / total_votes * 100:.1f}%" if total_votes > 0 else "0%"
        _turnout_line = ""
        if total_voting_power > 0 and voting_end_iso and voting_end_iso[:10] >= QUORUM_CUTOFF:
            turnout_pct = total_votes / total_voting_power * 100
            quorum_needed = int(total_voting_power * QUORUM)
            quorum_met = total_votes >= quorum_needed
            _turnout_cls = "prop-tally-yes-text" if quorum_met else "prop-tally-veto-text"
            _turnout_line = f'<span class="{_turnout_cls}">{"✓" if quorum_met else "✗"} Turnout {total_votes:,} / {total_voting_power:,} ({turnout_pct:.1f}%) · Quorum {QUORUM*100:.0f}% ({quorum_needed:,})</span>'
        tally_html = f"""
<div class="prop-tally">
  <div class="prop-tally-bar">
    <div class="prop-tally-yes" style="width:{bar_pct(yes_count)}"></div>
    <div class="prop-tally-no" style="width:{bar_pct(no_count)}"></div>
    <div class="prop-tally-veto" style="width:{bar_pct(no_with_veto_count)}"></div>
    <div class="prop-tally-abstain" style="width:{bar_pct(abstain_count)}"></div>
  </div>
  <div class="prop-tally-stats">
    <span class="prop-tally-yes-text">Yes {yes_count:,} ({stat_pct(yes_count)})</span>
    <span class="prop-tally-no-text">No {no_count:,} ({stat_pct(no_count)})</span>
    <span class="prop-tally-veto-text">Veto {no_with_veto_count:,} ({stat_pct(no_with_veto_count)})</span>
    <span class="prop-tally-abstain-text">Abstain {abstain_count:,} ({stat_pct(abstain_count)})</span>
    <span class="prop-tally-total-text">Total {total_votes:,} votes</span>
    {_turnout_line}
  </div>
</div>
"""

    # Funding line
    funding_parts = funding_parts_by_source(amt_by_source)
    funding_html = ""
    if funding_parts:
        if status_css_cls == "prop-passed":
            _funding_cls = "prop-funding-line"
        elif status_css_cls == "prop-voting":
            _funding_cls = "prop-funding-line prop-funding-line-voting"
        else:
            _funding_cls = "prop-funding-line prop-funding-line-rejected"
        funding_html = f'<div class="{_funding_cls}">{" · ".join(funding_parts)}</div>\n'

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
        md += f"**Proposer:** [`{proposer}`](https://gonka.gg/address/{proposer}){{:target=\"_blank\"}}\n\n"
    if metadata_url:
        if metadata_url.startswith("http://") or metadata_url.startswith("https://"):
            md += f"**Metadata:** [{metadata_url}]({metadata_url})\n\n"
        else:
            md += f"**Metadata:** `{metadata_url}`\n\n"
    if failed_reason:
        md += f"**Failed reason:** {failed_reason}\n\n"
    if funding_html:
        md += funding_html

    # Bounty reward line (upgrade proposals only)
    bounty_html = ""
    if messages:
        v = get_upgrade_version(messages)
        b = BOUNTY_BY_VERSION.get(v)
        if b:
            total_str = f"${b['total']:,}" if b["denom"] == "USDT" else f"{b['total']:,}"
            bounty_html = (
                f'<div class="prop-bounty-line">'
                f'Bounty Reward из Community Pool: {total_str} {b["denom"]} · '
                f'{b["source"]} · '
                f'<a href="https://github.com/gonka-ai/gonka/pull/{b["pr"]}" target="_blank">PR #{b["pr"]}</a>'
                f'</div>\n'
            )
    if bounty_html:
        md += bounty_html

    md += f"""

[View on gonka.gg](https://gonka.gg/network/proposals/{pid}){{:target="_blank"}}

</div>

"""

    if summary:
        md += f"{linkify_md(summary)}\n\n---\n\n"

    if tally_html:
        md += f"""## Final Tally

{tally_html}

"""

    # Voter table (only for active proposals with individual votes available)
    voters_html = ""
    votes_data = None
    if status == "PROPOSAL_STATUS_VOTING_PERIOD":
        votes_data = fetch_votes(pid)
        if votes_data:
            (prop_dir / "votes.json").write_text(json.dumps(votes_data, indent=2, ensure_ascii=False), encoding="utf-8")
            print(f"  #{pid}: fetched {len(votes_data)} votes")

    if not votes_data and (prop_dir / "votes.json").exists():
        try:
            votes_data = json.loads((prop_dir / "votes.json").read_text(encoding="utf-8"))
            if votes_data:
                print(f"  #{pid}: loaded {len(votes_data)} saved votes")
        except (json.JSONDecodeError, OSError):
            votes_data = None

    if votes_data:
        rows = "\n".join(
            _format_voter_row(v) for v in votes_data
        )
        voters_html = f"""
<h2 id="voters">Voters</h2>

<div class="prop-voters-wrap">
<table class="prop-voters">
<thead><tr><th>Voter</th><th>Vote</th></tr></thead>
<tbody>
{rows}
</tbody>
</table>
</div>

---
"""

    if voters_html:
        md += voters_html

    md += f"""## Messages

| # | Type |
| :- | :--- |
"""
    for i, m in enumerate(messages, 1):
        mt = m.get("@type", "Unknown")
        md += f"| {i} | `{mt}` |\n"

    # Contract spoiler
    md += f"""
<details class="prop-contracts" markdown="1">
<summary markdown="1">Contract Details</summary>

```json
{msg_json}
```

</details>
"""

    return md


# ── generate overview index ────────────────────────────────────

def generate_overview(proposals_by_quarter, proposal_voting_power=None):
    if proposal_voting_power is None:
        proposal_voting_power = {}
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
  <input type="checkbox" id="prop-filter-funding">
  <span class="prop-filter-label">With Funding</span>
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

    o_amt_by_source = {}
    for p in all_props:
        if p.get("status", "").lower() == "proposal_status_passed":
            _src_amt = parse_amounts_by_source(p.get("messages", []))
            for src, (_g, _u) in _src_amt.items():
                pg, pu = o_amt_by_source.get(src, (0, 0))
                o_amt_by_source[src] = (pg + _g, pu + _u)
    o_funding_parts = funding_parts_by_source(o_amt_by_source)
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

            voting_end_iso = p.get("voting_end_time", "")
            is_voting = status_css_cls == "prop-voting"
            card_data_attrs = f'data-status="{status_css_cls}"'
            countdown_html = ""
            if is_voting and voting_end_iso:
                card_data_attrs += f' data-voting-end="{voting_end_iso}"'
                countdown_html = f'    <span class="prop-vote-countdown" data-deadline="{voting_end_iso}"></span>\n'

            md += f"""<div class="prop-card" {card_data_attrs}>
  <div class="prop-card-header">
    <a href="{q.lower()}/{pid}/" class="prop-card-title">#{pid} – {title}</a>
{countdown_html}    <span class="prop-badge {status_css_cls}">{status_label}</span>
  </div>
  <div class="prop-card-meta">
    <span>Submitted {submit_time}</span>
    <span>Voting ends {voting_end}</span>
  </div>
"""
            if short_summary:
                md += f'  <div class="prop-card-desc">{linkify(escape_md(short_summary))}</div>\n'

            if yes_c + no_c > 0 or status_css_cls in ("prop-passed", "prop-voting"):
                veto_c = int(tally.get("no_with_veto_count", 0))
                abstain_c = int(tally.get("abstain_count", 0))
                total_t = yes_c + no_c + veto_c + abstain_c
                _pct = lambda v: f"({v / total_t * 100:.1f}%)" if total_t > 0 else "(0.0%)"
                _tally_line = f'<span class="prop-tally-yes-text">Yes {yes_c:,} {_pct(yes_c)}</span> · <span class="prop-tally-no-text">No {no_c:,} {_pct(no_c)}</span> · <span class="prop-tally-veto-text">Veto {veto_c:,} {_pct(veto_c)}</span> · <span class="prop-tally-abstain-text">Abstain {abstain_c:,} {_pct(abstain_c)}</span>'

                _vp = proposal_voting_power.get(pid, 0)
                _turnout_line = ""
                if _vp > 0 and total_t > 0 and voting_end_iso[:10] >= QUORUM_CUTOFF:
                    _turnout_pct = total_t / _vp * 100
                    _quorum_needed = int(_vp * QUORUM)
                    _quorum_met = total_t >= _quorum_needed
                    _turnout_cls = "prop-tally-yes-text" if _quorum_met else "prop-tally-veto-text"
                    _turnout_line = f'<span class="{_turnout_cls}">{"✓" if _quorum_met else "✗"} Turnout {total_t:,} / {_vp:,} ({_turnout_pct:.1f}%) · Quorum {QUORUM*100:.0f}% ({_quorum_needed:,})</span>'

                _funding_html = ""
                _amt_by_source = parse_amounts_by_source(p.get("messages", []))
                _funding_parts = funding_parts_by_source(_amt_by_source)
                if _funding_parts:
                    if status_css_cls == "prop-passed":
                        _funding_cls = "prop-card-funding"
                    elif status_css_cls == "prop-voting":
                        _funding_cls = "prop-card-funding prop-card-funding-voting"
                    else:
                        _funding_cls = "prop-card-funding prop-card-funding-rejected"
                    _funding_html = f'<span class="{_funding_cls}">{" · ".join(_funding_parts)}</span>'

                md += f'  <div class="prop-card-tally">{_tally_line}{_funding_html}</div>\n'
                if _turnout_line:
                    md += f'  <div class="prop-card-tally">{_turnout_line}</div>\n'

            md += "</div>\n\n"

        md += "</div>\n"

    # stats bar
    md += f"""<div class="prop-oview-stats">
<em>{total} proposals across {len(sorted_quarters)} quarters. Last updated: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")}</em>
</div>

<script>
function _ovInit() {{
  document.querySelectorAll('.prop-vote-countdown').forEach(function(el) {{
    var deadline = new Date(el.getAttribute('data-deadline'));
    function update() {{
      var diff = deadline - new Date();
      if (diff <= 0) {{ el.textContent = 'Ended'; el.classList.add('ended'); return; }}
      var d = Math.floor(diff / 86400000);
      var h = Math.floor((diff % 86400000) / 3600000);
      var m = Math.floor((diff % 3600000) / 60000);
      if (d > 0) el.textContent = d + 'd ' + h + 'h ' + m + 'm';
      else if (h > 0) el.textContent = h + 'h ' + m + 'm';
      else el.textContent = m + 'm';
    }}
    update();
    setInterval(update, 60000);
  }});
}}
_ovInit();
</script>
"""

    return md


# ── generate quarter page ──────────────────────────────────────

def generate_quarter_page(quarter, proposals, proposal_voting_power=None):
    if proposal_voting_power is None:
        proposal_voting_power = {}
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
    q_amt_by_source = {}
    for p in props:
        if p.get("status", "").lower() == "proposal_status_passed":
            _src_amt = parse_amounts_by_source(p.get("messages", []))
            for src, (_g, _u) in _src_amt.items():
                pg, pu = q_amt_by_source.get(src, (0, 0))
                q_amt_by_source[src] = (pg + _g, pu + _u)
    q_funding_parts = funding_parts_by_source(q_amt_by_source)
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
<label class="prop-filter-cb">
  <input type="checkbox" id="prop-filter-funding">
  <span class="prop-filter-label">With Funding</span>
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

        voting_end_iso = p.get("voting_end_time", "")
        is_voting = status_css_cls == "prop-voting"
        card_data_attrs = f'data-status="{status_css_cls}"'
        countdown_html = ""
        if is_voting and voting_end_iso:
            card_data_attrs += f' data-voting-end="{voting_end_iso}"'
            countdown_html = f'    <span class="prop-vote-countdown" data-deadline="{voting_end_iso}"></span>\n'

        md += f'''<div class="prop-card" {card_data_attrs}>
  <div class="prop-card-header">
    <a href="{pid}/" class="prop-card-title">#{pid} – {title}</a>
{countdown_html}    <span class="prop-badge {status_css_cls}">{status_label}</span>
  </div>
  <div class="prop-card-meta">
    <span>Submitted {submit_time}</span>
    <span>Voting ends {voting_end}</span>
  </div>
'''
        if short_summary:
            md += f'  <div class="prop-card-desc">{linkify(escape_md(short_summary))}</div>\n'
        if yes_c + no_c > 0 or status_css_cls in ("prop-passed", "prop-voting"):
            veto_c = int(tally.get("no_with_veto_count", 0))
            abstain_c = int(tally.get("abstain_count", 0))
            total_t = yes_c + no_c + veto_c + abstain_c
            _pct = lambda v: f"({v / total_t * 100:.1f}%)" if total_t > 0 else "(0.0%)"
            _tally_line = f'<span class="prop-tally-yes-text">Yes {yes_c:,} {_pct(yes_c)}</span> · <span class="prop-tally-no-text">No {no_c:,} {_pct(no_c)}</span> · <span class="prop-tally-veto-text">Veto {veto_c:,} {_pct(veto_c)}</span> · <span class="prop-tally-abstain-text">Abstain {abstain_c:,} {_pct(abstain_c)}</span>'

            _vp = proposal_voting_power.get(pid, 0)
            _turnout_line = ""
            if _vp > 0 and total_t > 0 and voting_end_iso[:10] >= QUORUM_CUTOFF:
                _turnout_pct = total_t / _vp * 100
                _quorum_needed = int(_vp * QUORUM)
                _quorum_met = total_t >= _quorum_needed
                _turnout_cls = "prop-tally-yes-text" if _quorum_met else "prop-tally-veto-text"
                _turnout_line = f'<span class="{_turnout_cls}">{"✓" if _quorum_met else "✗"} Turnout {total_t:,} / {_vp:,} ({_turnout_pct:.1f}%) · Quorum {QUORUM*100:.0f}% ({_quorum_needed:,})</span>'

            _funding_html = ""
            _amt_by_source = parse_amounts_by_source(p.get("messages", []))
            _funding_parts = funding_parts_by_source(_amt_by_source)
            if _funding_parts:
                if status_css_cls == "prop-passed":
                    _funding_cls = "prop-card-funding"
                elif status_css_cls == "prop-voting":
                    _funding_cls = "prop-card-funding prop-card-funding-voting"
                else:
                    _funding_cls = "prop-card-funding prop-card-funding-rejected"
                _funding_html = f'<span class="{_funding_cls}">{" · ".join(_funding_parts)}</span>'

            md += f'  <div class="prop-card-tally">{_tally_line}{_funding_html}</div>\n'
            if _turnout_line:
                md += f'  <div class="prop-card-tally">{_turnout_line}</div>\n'
        md += "</div>\n\n"

    md += '''</div>

<p><a href="../"><em>← Back to all proposals</em></a></p>
'''

    return md


# ── calendar events ────────────────────────────────────────────

CALENDAR_FILE = Path("docs/community/calendar/proposals.json")


def generate_proposal_calendar(proposals_by_quarter):
    """Generate calendar events for proposals in docs/community/calendar/proposals.json.

    Active voting proposals → type: proposal_vote_end on voting_end_time.
    Passed/rejected/failed proposals → type: proposal_report with outcome tag.
    """
    events = []
    for q, props in proposals_by_quarter.items():
        for p in props:
            pid = p["id"]
            title = p.get("title", f"Proposal #{pid}").strip()
            status = p.get("status", "")
            voting_end = p.get("voting_end_time", "")
            summary = p.get("summary", "")

            if not voting_end or status in (
                "PROPOSAL_STATUS_UNSPECIFIED",
                "PROPOSAL_STATUS_DEPOSIT_PERIOD",
            ):
                continue

            try:
                dt = datetime.fromisoformat(voting_end.replace("Z", "+00:00"))
                date_str = dt.strftime("%Y-%m-%d")
                time_str = dt.strftime("%H:%M UTC")
            except (ValueError, TypeError):
                continue

            q_lower = q.lower()
            url = f"/proposals/proposals/{q_lower}/{pid}/"
            status_label = format_status_label(status)
            desc = (summary[:200] + "…") if summary and len(summary) > 200 else (summary or "")

            if status == "PROPOSAL_STATUS_VOTING_PERIOD":
                events.append({
                    "date": date_str,
                    "category": "governance",
                    "type": "proposal_vote_end",
                    "title": f"Voting ends: #{pid} – {title}",
                    "url": url,
                    "time": time_str,
                    "description": desc,
                    "tags": ["voting"],
                })
            else:
                # Passed / Rejected / Failed
                events.append({
                    "date": date_str,
                    "category": "governance",
                    "type": "proposal_report",
                    "title": f"{status_label}: #{pid} – {title}",
                    "url": url,
                    "time": time_str,
                    "description": desc,
                    "tags": [status_label.lower()],
                })

    events.sort(key=lambda e: e["date"])

    CALENDAR_FILE.parent.mkdir(parents=True, exist_ok=True)
    CALENDAR_FILE.write_text(json.dumps(events, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Generated {len(events)} proposal calendar events → {CALENDAR_FILE}")


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

def generate_rss_feed(sorted_quarters, proposals_by_quarter):
    """Generate an RSS 2.0 feed for proposals."""
    from xml.sax.saxutils import escape
    SITE_URL = "https://gonkadocs.com"

    items = []
    for q in sorted_quarters:
        for p in proposals_by_quarter.get(q, []):
            pid = p["id"]
            title = escape(p.get("title", f"Proposal #{pid}").strip())
            status = format_status_label(p.get("status", ""))
            summary = p.get("summary", "")
            summary_esc = escape(summary[:500]) if summary else ""
            submit = p.get("submit_time", "")
            pub_date = ""
            if submit:
                try:
                    dt = datetime.fromisoformat(submit.replace("Z", "+00:00"))
                    pub_date = dt.strftime("%a, %d %b %Y %H:%M:%S +0000")
                except (ValueError, TypeError):
                    pass
            link = f"{SITE_URL}/proposals/proposals/{q.lower()}/{pid}/"
            items.append(f"""    <item>
      <title>#{pid} – {title}</title>
      <link>{link}</link>
      <guid isPermaLink="true">{link}</guid>
      <pubDate>{pub_date}</pubDate>
      <category>{escape(status)}</category>
      <description>{summary_esc}</description>
    </item>""")

    rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>Gonka On-Chain Governance Proposals</title>
    <link>{SITE_URL}/proposals/proposals/</link>
    <description>On-chain governance proposals for the Gonka decentralized AI inference network</description>
    <language>en</language>
    <atom:link href="{SITE_URL}/proposals/proposals/proposals.xml" rel="self" type="application/rss+xml"/>
{chr(10).join(items)}
  </channel>
</rss>"""

    rss_path = OUTPUT_DIR / "proposals.xml"
    rss_path.write_text(rss, encoding="utf-8")
    print(f"Generated RSS feed: {rss_path} ({len(items)} items)")


def generate_proposals_sitemap(sorted_quarters, proposals_by_quarter):
    """Generate a sitemap.xml for proposals (browsers/crawlers look for this)."""
    from xml.sax.saxutils import escape
    SITE_URL = "https://gonkadocs.com"
    today = datetime.now(timezone.utc).date().isoformat()

    urls = []

    # Root proposals page
    urls.append(f"""  <url>
    <loc>{SITE_URL}/proposals/proposals/</loc>
    <lastmod>{today}</lastmod>
    <changefreq>hourly</changefreq>
    <priority>0.8</priority>
  </url>""")

    for q in sorted_quarters:
        q_lower = q.lower()
        # Quarter overview
        urls.append(f"""  <url>
    <loc>{SITE_URL}/proposals/proposals/{q_lower}/</loc>
    <lastmod>{today}</lastmod>
    <changefreq>hourly</changefreq>
    <priority>0.7</priority>
  </url>""")

        for p in proposals_by_quarter.get(q, []):
            pid = p["id"]
            submit = p.get("submit_time", "")
            lastmod = today
            if submit:
                try:
                    dt = datetime.fromisoformat(submit.replace("Z", "+00:00"))
                    lastmod = dt.date().isoformat()
                except (ValueError, TypeError):
                    pass
            status = p.get("status", "")
            # Voting proposals change more often
            changefreq = "hourly" if status == "PROPOSAL_STATUS_VOTING_PERIOD" else "weekly"
            priority = "0.6" if status == "PROPOSAL_STATUS_VOTING_PERIOD" else "0.5"
            urls.append(f"""  <url>
    <loc>{SITE_URL}/proposals/proposals/{q_lower}/{pid}/</loc>
    <lastmod>{lastmod}</lastmod>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
  </url>""")

    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(urls)}
</urlset>"""

    sitemap_path = OUTPUT_DIR / "sitemap.xml"
    sitemap_path.write_text(sitemap, encoding="utf-8")
    print(f"Generated proposals sitemap: {sitemap_path} ({len(urls)} URLs)")


def fetch_live_tally(proposal_id):
    """Fetch the live tally for a voting proposal (the list endpoint returns zeros)."""
    try:
        data = fetch_with_retry(f"{{BASE}}/cosmos/gov/v1/proposals/{proposal_id}/tally", timeout=10)
        return data.get("tally", {})
    except Exception as e:
        print(f"  Warning: could not fetch tally for #{proposal_id}: {e}")
        return {}


def fetch_votes(proposal_id):
    """Fetch individual votes for a proposal (only available for active voting proposals)."""
    votes = []
    key = ""
    page = 0
    while True:
        page += 1
        url = f"{{BASE}}/cosmos/gov/v1/proposals/{proposal_id}/votes?pagination.limit=500"
        if key:
            url += f"&pagination.key={urllib.parse.quote(key, safe='')}"
        try:
            data = fetch_with_retry(url, timeout=15)
        except Exception as e:
            print(f"  Warning: could not fetch votes for #{proposal_id} page {page}: {e}")
            break
        page_votes = data.get("votes", [])
        if not page_votes:
            break
        votes.extend(page_votes)
        key = data.get("pagination", {}).get("next_key", "") or ""
        if not key:
            break
    return votes


QUORUM = 0.25  # 25% from chain params
QUORUM_CUTOFF = "2026-07-01"  # Only show quorum/turnout for proposals with voting_end >= this date


def get_snapshot_voting_power(prop_dir):
    """Load saved voting power snapshot for a proposal, or 0 if not yet saved."""
    snap_path = prop_dir / "voting_power.json"
    if snap_path.exists():
        try:
            return json.loads(snap_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return 0
    return 0


def save_snapshot_voting_power(prop_dir, total_voting_power):
    """Save voting power snapshot for a proposal that has ended voting."""
    snap_path = prop_dir / "voting_power.json"
    if not snap_path.exists():
        snap_path.write_text(json.dumps(total_voting_power), encoding="utf-8")
        print(f"  Saved voting power snapshot: {total_voting_power}")


def fetch_total_voting_power():
    """Fetch total voting power from all bonded validators (sum of tokens field)."""
    print("Fetching total voting power...")
    total = 0
    key = ""
    page = 0
    while True:
        page += 1
        url = f"{{BASE}}/cosmos/staking/v1beta1/validators?pagination.limit=500&status=BOND_STATUS_BONDED"
        if key:
            url += f"&pagination.key={urllib.parse.quote(key, safe='')}"
        try:
            data = fetch_with_retry(url, timeout=15)
        except Exception as e:
            print(f"  Error fetching validators page {page}: {e}")
            break
        vals = data.get("validators", [])
        for v in vals:
            try:
                total += int(v.get("tokens", "0"))
            except (ValueError, TypeError):
                pass
        key = data.get("pagination", {}).get("next_key", "") or ""
        if not key:
            break
    print(f"Total voting power: {total}")
    return total


def main():
    print("=== Sync On-Chain Proposals ===")
    proposals = fetch_proposals()

    # Patch tally for voting proposals (list endpoint returns all zeros)
    print("Fetching live tallies for voting proposals...")
    for p in proposals:
        if p.get("status") == "PROPOSAL_STATUS_VOTING_PERIOD":
            pid = p["id"]
            live = fetch_live_tally(pid)
            if live:
                p["final_tally_result"] = live
                print(f"  #{pid}: patched tally → {live}")

    # Fetch total voting power for turnout/quorum
    total_voting_power = fetch_total_voting_power()

    # Save voting power snapshots for ended proposals (so historical values never change)
    print("Saving voting power snapshots...")
    for p in proposals:
        if p.get("status") != "PROPOSAL_STATUS_VOTING_PERIOD":
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
            save_snapshot_voting_power(prop_dir, total_voting_power)

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

    # Pre-load snapshot voting power for each proposal (for card display)
    proposal_voting_power = {}
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
        saved = get_snapshot_voting_power(prop_dir)
        if p.get("status") == "PROPOSAL_STATUS_VOTING_PERIOD":
            proposal_voting_power[pid] = total_voting_power
        else:
            proposal_voting_power[pid] = saved if saved else total_voting_power

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
        page_md = generate_proposal_page(p, prop_dir, proposal_voting_power[pid])
        (prop_dir / "index.md").write_text(page_md, encoding="utf-8")

    # Generate quarter subpages
    print(f"Generating {len(sorted_quarters)} quarter pages...")
    for q in sorted_quarters:
        q_lower = q.lower()
        q_dir = OUTPUT_DIR / q_lower
        q_dir.mkdir(exist_ok=True)
        q_md = generate_quarter_page(q, proposals_by_quarter[q], proposal_voting_power)
        (q_dir / "index.md").write_text(q_md, encoding="utf-8")

    # Generate overview
    print("Generating overview index...")
    overview_md = generate_overview(proposals_by_quarter, proposal_voting_power)
    (OUTPUT_DIR / "index.md").write_text(overview_md, encoding="utf-8")

    # Generate RSS feed
    print("Generating RSS feed...")
    generate_rss_feed(sorted_quarters, proposals_by_quarter)

    # Generate proposals sitemap.xml (browsers/crawlers check this path)
    print("Generating proposals sitemap...")
    generate_proposals_sitemap(sorted_quarters, proposals_by_quarter)

    # Generate calendar events for proposals
    print("Generating proposal calendar events...")
    generate_proposal_calendar(proposals_by_quarter)

    # Update nav
    update_mkdocs_nav(sorted_quarters, proposals_by_quarter)

    print(f"\nDone. {len(proposals)} proposals in {len(sorted_quarters)} quarters → {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
