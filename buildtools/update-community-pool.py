#!/usr/bin/env python3
"""Update Community Pool data in docs/proposals/community pool.md.

Fetches fresh data from chain API and replaces content between markers:
- <!-- UPDATE_TIMESTAMP --> ... <!-- /UPDATE_TIMESTAMP -->
- <!-- BALANCES_START --> ... <!-- BALANCES_END -->
- <!-- SALE_BALANCE_START --> ... <!-- SALE_BALANCE_END -->
- <!-- GOV_BALANCE_START --> ... <!-- GOV_BALANCE_END -->
- <!-- SPENT_HISTORY_START --> ... <!-- SPENT_HISTORY_END -->

Usage:
    python3 buildtools/update-community-pool.py
"""

import json
import re
import sys
from datetime import datetime, timezone

import requests

RPC_ENDPOINTS = [
    "https://node3.gonka.ai/chain-api",
    "https://rpc.gonka.gg",
    "http://node1.gonka.ai:8000/chain-api",
]

COMMUNITY_SALE_ADDR = "gonka18pkq9mwxxlmyq7kr5txhm060wemg2s4u94wvsfd9w2kdc0u99d6spk8pz2"
GOV_MODULE_ADDR = "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33"
USDT_IBC_DENOM = "ibc/115F68FBA220A028C6F6ED08EA0C1A9C8C52798B14FB66E6C89D5D8C06A524D4"
FILE_PATH = "docs/proposals/community pool.md"

MAX_RETRIES = 3
RETRY_DELAY = 5

SITE_URL = "https://gonkadocs.com"
PROPOSALS_PREFIX = "/proposals/proposals/"

PASSED_STATUSES = {"PROPOSAL_STATUS_PASSED"}


def fetch_json(url, timeout=30):
    last_error = None
    for endpoint in RPC_ENDPOINTS:
        full_url = url.replace("{BASE}", endpoint.rstrip("/"))
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                resp = requests.get(full_url, timeout=timeout)
                resp.raise_for_status()
                if not resp.text.strip():
                    raise ValueError("empty response")
                return resp.json()
            except Exception as e:
                last_error = e
                if attempt < MAX_RETRIES:
                    import time
                    time.sleep(RETRY_DELAY * attempt)
    print(f"ERROR: all endpoints exhausted for {url}: {last_error}", file=sys.stderr)
    return None


def format_balance(amount_str, denom):
    try:
        amt = int(amount_str.split(".")[0])
        if denom == "ngonka":
            return f"{amt / 1_000_000_000:,.0f}"
        elif denom == USDT_IBC_DENOM:
            return f"${amt / 1_000_000:,.0f}"
        return f"{amt} {denom}"
    except (ValueError, TypeError, ZeroDivisionError):
        return str(amount_str)


def format_balance_line(gnk_val, usdt_val, show_gnk=True, show_usdt=True, gnk_equiv_usdt=None, gnk_color=None):
    COMMON = 'font-size:0.95rem;font-weight:600'
    BLUE = f'color:var(--md-accent-fg-color,#5468ff);{COMMON}'
    gnk_style = f'color:{gnk_color};{COMMON}' if gnk_color else BLUE
    parts = []
    if show_gnk and gnk_val:
        gnk_html = f'<span style="{gnk_style}">{gnk_val} GNK'
        if gnk_equiv_usdt:
            gnk_html += f' (~${gnk_equiv_usdt} USDT)'
        gnk_html += '</span>'
        parts.append(gnk_html)
    if show_usdt and usdt_val:
        parts.append(f'<span style="{BLUE}">{usdt_val} USDT</span>')
    return (
        '<p style="margin:0.2rem 0">\n'
        + "<strong>Current balance:</strong> "
        + " · ".join(parts)
        + "\n</p>"
    )


def short_addr(addr):
    if len(addr) > 20:
        return addr[:10] + "…" + addr[-6:]
    return addr


def get_quarter(dt):
    return f"{dt.year}-Q{(dt.month - 1) // 3 + 1}"


def fmt_time_short(iso_str):
    if not iso_str:
        return ""
    try:
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d")
    except (ValueError, TypeError):
        return iso_str[:10]


def short_title(title, max_len=60):
    if not title:
        return ""
    if len(title) <= max_len:
        return title
    return title[:max_len - 1] + "…"


# ── Fetch balances ─────────────────────────────────────────────

def fetch_community_pool():
    data = fetch_json("{BASE}/cosmos/distribution/v1beta1/community_pool")
    if not data:
        return {}, {}
    gnk = 0
    usdt = 0
    for coin in data.get("pool", []):
        d = coin.get("denom", "")
        if d == "ngonka":
            gnk = coin.get("amount", "0")
        elif d == USDT_IBC_DENOM:
            usdt = coin.get("amount", "0")
    return gnk, usdt


def fetch_account_balance(address):
    data = fetch_json(f"{{BASE}}/cosmos/bank/v1beta1/balances/{address}")
    if not data:
        return {}
    balances = {}
    for coin in data.get("balances", []):
        balances[coin["denom"]] = coin["amount"]
    return balances


# ── Fetch funding history ──────────────────────────────────────

def parse_funding_from_messages(messages):
    """Extract total GNK and USDT from all message types in a proposal.
    
    Returns (gnk_total, usdt_total) as floats.
    """
    gnk_total = 0.0
    usdt_total = 0.0

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
                for c in o.get("amount") or []:
                    denom = c.get("denom", "")
                    try:
                        amt = int(c.get("amount", "0"))
                    except (ValueError, TypeError):
                        continue
                    if denom == "ngonka":
                        gnk_total += amt / 1_000_000_000
                    elif denom == USDT_IBC_DENOM:
                        usdt_total += amt / 1_000_000

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


def determine_source(messages):
    """Determine funding source for a proposal based on message types."""
    has_pool_spend = False
    has_gov_vesting = False
    for m in messages:
        t = m.get("@type", "")
        if "MsgCommunityPoolSpend" in t or "MsgExecuteContract" in t:
            has_pool_spend = True
        if "MsgBatchTransferWithVesting" in t or "MsgTransferWithVesting" in t or "MsgMultiSend" in t:
            has_gov_vesting = True
    if has_pool_spend and has_gov_vesting:
        return "Community Pool + Gov Module"
    elif has_pool_spend:
        return "Community Pool"
    elif has_gov_vesting:
        return "Gov Module"
    return "—"


def fetch_funding_history():
    """Fetch all passed proposals and aggregate funding amounts."""
    data = fetch_json("{BASE}/cosmos/gov/v1/proposals?pagination.limit=200")
    if not data:
        return []

    funding = []
    for p in data.get("proposals", []):
        if p.get("status") not in PASSED_STATUSES:
            continue

        pid = p["id"]
        title = p.get("title", "")
        msgs = p.get("messages", [])
        ts = fmt_time_short(p.get("voting_end_time", ""))

        gnk_total, usdt_total = parse_funding_from_messages(msgs)

        if gnk_total == 0 and usdt_total == 0:
            continue

        submit = p.get("submit_time", "")
        q = "unknown"
        if submit:
            try:
                dt = datetime.fromisoformat(submit.replace("Z", "+00:00"))
                q = get_quarter(dt).lower()
            except (ValueError, TypeError):
                pass

        source = determine_source(msgs)

        funding.append({
            "pid": pid,
            "quarter": q,
            "date": ts,
            "title": short_title(title),
            "source": source,
            "gnk": gnk_total,
            "usdt": usdt_total,
        })

    return funding


# ── Generate content ───────────────────────────────────────────

def generate_balance_line(gnk_raw, usdt_raw):
    gnk_val = format_balance(gnk_raw, "ngonka") if gnk_raw else ""
    usdt_val = format_balance(usdt_raw, USDT_IBC_DENOM) if usdt_raw else ""
    return format_balance_line(gnk_val, usdt_val)


def generate_sale_balance_line(sale_balances):
    gnk = sale_balances.get("ngonka", "0")
    usdt = sale_balances.get(USDT_IBC_DENOM, "0")
    gnk_val = format_balance(gnk, "ngonka")
    usdt_val = format_balance(usdt, USDT_IBC_DENOM)
    try:
        gnk_raw = int(gnk.split(".")[0]) / 1_000_000_000
        equiv = gnk_raw * 0.6
        equiv_str = f"{equiv:,.0f}"
    except (ValueError, TypeError):
        equiv_str = None
    return format_balance_line(gnk_val, usdt_val, gnk_equiv_usdt=equiv_str, gnk_color="grey")


def generate_gov_balance_line(gov_balances):
    gnk = gov_balances.get("ngonka", "0")
    gnk_val = format_balance(gnk, "ngonka")
    return format_balance_line(gnk_val, None, show_usdt=False)


def generate_funding_table(funding):
    rows = [
        "| Proposal | Date | Description | Source | Amount GNK | Amount USDT |",
        "| :------ | :--: | :---------- | :---- | ---------: | ---------: |",
    ]
    if not funding:
        return "\n".join(rows) + "\n| — | — | — | — | — | — |\n"

    funding_sorted = sorted(funding, key=lambda s: int(s["pid"]), reverse=True)
    for f in funding_sorted:
        pid = f["pid"]
        q = f["quarter"]
        gnk_str = f"{f['gnk']:,}" if f["gnk"] > 0 else "—"
        usdt_str = f"${f['usdt']:,}" if f["usdt"] > 0 else "—"
        rows.append(
            f"| [#{pid}]({SITE_URL}{PROPOSALS_PREFIX}{q}/{pid}/) "
            f"| {f['date']} "
            f"| {f['title']} "
            f"| {f['source']} "
            f"| {gnk_str} "
            f"| {usdt_str} |"
        )

    return "\n".join(rows) + "\n"


def generate_summary(funding):
    total_gnk = sum(f["gnk"] for f in funding)
    total_usdt = sum(f["usdt"] for f in funding)
    pool_gnk = sum(f["gnk"] for f in funding if "Community Pool" in f["source"])
    pool_usdt = sum(f["usdt"] for f in funding if "Community Pool" in f["source"])
    gov_gnk = sum(f["gnk"] for f in funding if "Gov Module" in f["source"])

    largest = max(funding, key=lambda f: f["gnk"]) if funding else None
    largest_label = f"#{largest['pid']} — {largest['gnk']:,} GNK" if largest else "—"
    if largest and largest["usdt"] > 0:
        largest_label += f" + ${largest['usdt']:,} USDT"

    recent = max(funding, key=lambda f: int(f["pid"])) if funding else None
    recent_label = f"#{recent['pid']} — {recent['gnk']:,} GNK" if recent else "—"
    if recent and recent["usdt"] > 0:
        recent_label += f" + ${recent['usdt']:,} USDT"

    return f"""| Metric | Value |
| :----- | :---- |
| Total funded proposals | {len(funding)} |
| Total GNK approved | {total_gnk:,} GNK |
| Total USDT approved | ${total_usdt:,} |
| From Community Pool | {pool_gnk:,} GNK + ${pool_usdt:,} |
| From Gov Module | {gov_gnk:,} GNK |
| Largest funding | {largest_label} |
| Most recent | {recent_label} |"""


# ── Update file ────────────────────────────────────────────────

def replace_between_markers(content, start_marker, end_marker, new_content):
    pattern = re.escape(start_marker) + r".*?" + re.escape(end_marker)
    replacement = start_marker + "\n" + new_content.strip() + "\n" + end_marker
    if not re.search(pattern, content, re.DOTALL):
        print(f"WARNING: markers {start_marker}...{end_marker} not found in file")
        return content
    return re.sub(pattern, replacement, content, flags=re.DOTALL)


def update_file():
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    print("Fetching Community Pool balance...")
    gnk_pool, usdt_pool = fetch_community_pool()
    if not gnk_pool and not usdt_pool:
        print("ERROR: could not fetch community pool balance")
        sys.exit(1)

    print("Fetching Community Sale balance...")
    sale_balances = fetch_account_balance(COMMUNITY_SALE_ADDR)

    print("Fetching Gov Module balance...")
    gov_balances = fetch_account_balance(GOV_MODULE_ADDR)

    print("Fetching funding history from proposals...")
    funding = fetch_funding_history()

    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    pool_line = generate_balance_line(gnk_pool, usdt_pool)
    sale_line = generate_sale_balance_line(sale_balances)
    gov_line = generate_gov_balance_line(gov_balances)
    fund_table = generate_funding_table(funding)
    summary = generate_summary(funding) if funding else ""

    content = replace_between_markers(
        content, "<!-- UPDATE_TIMESTAMP -->", "<!-- /UPDATE_TIMESTAMP -->", now_utc
    )
    content = replace_between_markers(
        content, "<!-- BALANCES_START -->", "<!-- BALANCES_END -->", pool_line
    )
    content = replace_between_markers(
        content, "<!-- SALE_BALANCE_START -->", "<!-- SALE_BALANCE_END -->", sale_line
    )
    content = replace_between_markers(
        content, "<!-- GOV_BALANCE_START -->", "<!-- GOV_BALANCE_END -->", gov_line
    )
    content = replace_between_markers(
        content, "<!-- SPENT_HISTORY_START -->", "<!-- SPENT_HISTORY_END -->",
        fund_table + "\n" + summary
    )

    with open(FILE_PATH, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Updated {FILE_PATH}")
    print(f"  Community Pool: {format_balance(gnk_pool, 'ngonka')} GNK, "
          f"{format_balance(usdt_pool, USDT_IBC_DENOM)} USDT")
    gnk_sale = sale_balances.get("ngonka", "0")
    usdt_s = sale_balances.get(USDT_IBC_DENOM, "0")
    gnk_gov = gov_balances.get("ngonka", "0")
    print(f"  Community Sale: {format_balance(gnk_sale, 'ngonka')} GNK, {format_balance(usdt_s, USDT_IBC_DENOM)} USDT")
    print(f"  Gov Module: {format_balance(gnk_gov, 'ngonka')} GNK")
    print(f"  Funding: {len(funding)} proposals")


if __name__ == "__main__":
    update_file()
