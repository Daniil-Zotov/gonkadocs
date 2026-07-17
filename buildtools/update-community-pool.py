#!/usr/bin/env python3
"""Update Community Pool balances and spend history in docs/proposals/community pool.md.

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

# ── Configuration ──────────────────────────────────────────────

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


# ── Helpers ────────────────────────────────────────────────────

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
            val = amt / 1_000_000_000
            if val >= 1_000_000:
                return f"{val/1_000_000:.1f}M GNK"
            elif val >= 1_000:
                return f"{val/1_000:.1f}K GNK"
            else:
                return f"{val:,.2f} GNK"
        elif denom == USDT_IBC_DENOM:
            return f"${amt / 1_000_000:,.2f}"
        return f"{amt} {denom}"
    except (ValueError, TypeError, ZeroDivisionError):
        return str(amount_str)


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


# ── Fetch spend history ────────────────────────────────────────

def fetch_spend_history():
    """Fetch all proposals and extract passed MsgCommunityPoolSpend messages."""
    data = fetch_json("{BASE}/cosmos/gov/v1/proposals?pagination.limit=200")
    if not data:
        return []

    spends = []
    for p in data.get("proposals", []):
        if p.get("status") not in PASSED_STATUSES:
            continue

        pid = p["id"]
        msgs = p.get("messages", [])
        ts = fmt_time_short(p.get("voting_end_time", ""))

        submit = p.get("submit_time", "")
        q = "unknown"
        if submit:
            try:
                dt = datetime.fromisoformat(submit.replace("Z", "+00:00"))
                q = get_quarter(dt).lower()
            except (ValueError, TypeError):
                pass

        for m in msgs:
            if "/cosmos.distribution.v1beta1.MsgCommunityPoolSpend" not in m.get("@type", ""):
                continue

            recv = m.get("recipient", "")
            for a in m.get("amount", []):
                denom = a.get("denom", "")
                try:
                    amt = int(a.get("amount", "0"))
                except (ValueError, TypeError):
                    continue

                gnk_val = 0
                usdt_val = 0
                if denom == "ngonka":
                    gnk_val = amt / 1_000_000_000
                elif denom == USDT_IBC_DENOM:
                    usdt_val = amt / 1_000_000

                spends.append({
                    "pid": pid,
                    "quarter": q,
                    "date": ts,
                    "recipient": recv,
                    "gnk": gnk_val,
                    "usdt": usdt_val,
                })

    return spends


# ── Generate tables ────────────────────────────────────────────

def generate_pool_balance_table(gnk_pool, usdt_pool):
    rows = [
        "| Address | Asset | Balance |",
        "| :------ | :---- | :------ |",
        f"| Community Pool | GNK | {format_balance(gnk_pool, 'ngonka')} |",
        f"| Community Pool | USDT | {format_balance(usdt_pool, USDT_IBC_DENOM)} |",
    ]
    return "\n".join(rows) + "\n"


def generate_sale_balance_table(sale_balances):
    gnk = sale_balances.get("ngonka", "0")
    usdt = sale_balances.get(USDT_IBC_DENOM, "0")
    rows = [
        "| Asset | Balance |",
        "| :---- | :------ |",
        f"| GNK | {format_balance(gnk, 'ngonka')} |",
        f"| USDT | {format_balance(usdt, USDT_IBC_DENOM)} |",
    ]
    return "\n".join(rows) + "\n"


def generate_gov_balance_table(gov_balances):
    gnk = gov_balances.get("ngonka", "0")
    rows = [
        "| Asset | Balance |",
        "| :---- | :------ |",
        f"| GNK | {format_balance(gnk, 'ngonka')} |",
    ]
    return "\n".join(rows) + "\n"


def generate_spend_table(spends):
    rows = [
        "| # | Proposal | Date | Recipient | Amount GNK | Amount USDT |",
        "| :-: | :------ | :--: | :-------- | ---------: | ---------: |",
    ]
    if not spends:
        return "\n".join(rows) + "\n| — | — | — | — | — | — |\n"

    # Sort by descending proposal ID
    spends_sorted = sorted(spends, key=lambda s: int(s["pid"]), reverse=True)
    for i, s in enumerate(spends_sorted, 1):
        pid = s["pid"]
        q = s["quarter"]
        gnk_str = f"{s['gnk']:,.1f}" if s["gnk"] > 0 else "—"
        usdt_str = f"${s['usdt']:,.0f}" if s["usdt"] > 0 else "—"
        rows.append(
            f"| {i} "
            f"| [#{pid}]({SITE_URL}{PROPOSALS_PREFIX}{q}/{pid}/) "
            f"| {s['date']} "
            f"| [`{short_addr(s['recipient'])}`](https://gonka.gg/address/{s['recipient']}) "
            f"| {gnk_str} "
            f"| {usdt_str} |"
        )

    return "\n".join(rows) + "\n"


def generate_summary(spends):
    total_gnk = sum(s["gnk"] for s in spends)
    total_usdt = sum(s["usdt"] for s in spends)
    prop_count = len(set(s["pid"] for s in spends))

    largest = max(spends, key=lambda s: s["gnk"]) if spends else None
    largest_label = f"#{largest['pid']} — {largest['gnk']:,.0f} GNK" if largest else "—"
    if largest and largest["usdt"] > 0:
        largest_label += f" + ${largest['usdt']:,.0f} USDT"

    # Most recent by highest proposal number
    recent = max(spends, key=lambda s: int(s["pid"])) if spends else None
    recent_label = f"#{recent['pid']} — {recent['gnk']:,.0f} GNK" if recent else "—"
    if recent and recent["usdt"] > 0:
        recent_label += f" + ${recent['usdt']:,.0f} USDT"

    return f"""| Metric | Value |
| :----- | :---- |
| Total `MsgCommunityPoolSpend` messages | {len(spends)} |
| Proposals with `MsgCommunityPoolSpend` | {prop_count} |
| Total GNK spent | {total_gnk:,.0f} GNK |
| Total USDT spent | ${total_usdt:,.0f} |
| Largest spend | {largest_label} |
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

    # Fetch fresh data
    print("Fetching Community Pool balance...")
    gnk_pool, usdt_pool = fetch_community_pool()
    if not gnk_pool and not usdt_pool:
        print("ERROR: could not fetch community pool balance")
        sys.exit(1)

    print("Fetching Community Sale balance...")
    sale_balances = fetch_account_balance(COMMUNITY_SALE_ADDR)

    print("Fetching Gov Module balance...")
    gov_balances = fetch_account_balance(GOV_MODULE_ADDR)

    print("Fetching spend history from proposals...")
    spends = fetch_spend_history()

    # Generate sections
    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    pool_table = generate_pool_balance_table(gnk_pool, usdt_pool)
    sale_table = generate_sale_balance_table(sale_balances)
    gov_table = generate_gov_balance_table(gov_balances)
    spend_table = generate_spend_table(spends)
    summary = generate_summary(spends) if spends else ""

    # Replace markers
    content = replace_between_markers(
        content, "<!-- UPDATE_TIMESTAMP -->", "<!-- /UPDATE_TIMESTAMP -->", now_utc
    )
    content = replace_between_markers(
        content, "<!-- BALANCES_START -->", "<!-- BALANCES_END -->", pool_table
    )
    content = replace_between_markers(
        content, "<!-- SALE_BALANCE_START -->", "<!-- SALE_BALANCE_END -->", sale_table
    )
    content = replace_between_markers(
        content, "<!-- GOV_BALANCE_START -->", "<!-- GOV_BALANCE_END -->", gov_table
    )
    content = replace_between_markers(
        content, "<!-- SPENT_HISTORY_START -->", "<!-- SPENT_HISTORY_END -->",
        spend_table + "\n" + summary
    )

    with open(FILE_PATH, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Updated {FILE_PATH}")
    print(f"  Community Pool: {format_balance(gnk_pool, 'ngonka')}, "
          f"{format_balance(usdt_pool, USDT_IBC_DENOM)}")
    gnk_sale = sale_balances.get("ngonka", "0")
    usdt_s = sale_balances.get(USDT_IBC_DENOM, "0")
    gnk_gov = gov_balances.get("ngonka", "0")
    print(f"  Community Sale: {format_balance(gnk_sale, 'ngonka')}, {format_balance(usdt_s, USDT_IBC_DENOM)}")
    print(f"  Gov Module: {format_balance(gnk_gov, 'ngonka')}")
    print(f"  Spends: {len(spends)} messages (passed only)")


if __name__ == "__main__":
    update_file()
