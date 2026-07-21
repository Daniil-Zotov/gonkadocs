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

# ── Bounty distributions via upgrade handlers ───────────────────
# Data sourced from gonka-ai/gonka PR diffs (upgrades.go bountyRewards vars).
# Format: (version, pr_num, pr_status, approx_date, denom, total, source, recipients_list)
#   denom: "USDT" or "GNK"
#   source: "Community Sale" or "Gov Module"
#   recipients_list: list of (alias_or_name, address, amount, description)

BOUNTY_DISTRIBUTIONS = [
    {
        "version": "v0.2.14",
        "pr": 1446,
        "pr_status": "Open",
        "date": "2026-07",
        "denom": "USDT",
        "total": 45250,
        "source": "Community Sale",
        "recipients": [
            ("@akup", "gonka1ejkupq3cy6p8xd64ew2wlzveml86ckpzn9dl56", 5000, "devshards v3 RM, upgrade review, HackerOne reviews"),
            ("@x0152", "gonka18enyz7h6hh5zjveee5wnhkhrcexamfz0zdxxqe", 6000, "RM, HackerOne reviews"),
            ("@qdanik", "gonka1j3f2xkapx8cmczpjqcsrh7cc3peyj3ngkjv4p8", 10000, "RM, HackerOne reviews, MiniMax R&D, PoC (incl. GPU)"),
            ("@ouicate", "gonka1f0elpwnx7ezytdlck35003nz6qk8kzvurvnj4a", 1000, "PR #1253: stop stale PoC validation"),
            ("@ouicate", "gonka1f0elpwnx7ezytdlck35003nz6qk8kzvurvnj4a", 1000, "PR #1255: settle before releasing unbonding"),
            ("@ouicate", "gonka1f0elpwnx7ezytdlck35003nz6qk8kzvurvnj4a", 1000, "PR #1278: bound event-listener tx queue"),
            ("@0xMayoor", "gonka1s8szs7n43jxgz4a4xaxmzm5emh7fmjxhach7w8", 500, "PR #1100: prevent uint64 wrap in settle"),
            ("@0xMayoor", "gonka1s8szs7n43jxgz4a4xaxmzm5emh7fmjxhach7w8", 750, "PR #1101: widen ShouldValidate to uint64"),
            ("@0xMayoor", "gonka1s8szs7n43jxgz4a4xaxmzm5emh7fmjxhach7w8", 500, "PR #1347: distribute unsettled escrow per slot"),
            ("@0xMayoor", "gonka1s8szs7n43jxgz4a4xaxmzm5emh7fmjxhach7w8", 2000, "PR #1376: bridge block sync vulnerability"),
            ("@alancapex", "gonka10mmdjau4dnj8krs7sh7t7635ttnmq9u3vqgz09", 3000, "PR #889: on-chain configurable reward recipients"),
            ("@Ryanchen911", "gonka1zqss46r6jf6dhhyaa777kc2ppvjhn0ufkx4y57", 7500, "PR #998: implementing maintenance windows"),
            ("@redstartechno", "gonka105ce4495mj0mwkxqeasgdzqfq5jjrfq32eza5l", 500, "PR #1307: avoid query-gas-limit on grant check"),
            ("@Lelouch33", "gonka128nd36m2pz5qcs4q6rd69622flyls05nleazqq", 5000, "Vulnerability report 1"),
            ("@Lelouch33", "gonka128nd36m2pz5qcs4q6rd69622flyls05nleazqq", 1000, "Vulnerability report 2"),
            ("@blizko", "gonka12jaf7m4eysyqt32mrgarum6z96vt55tckvcleq", 1000, "v0.2.13 upgrade review"),
        ],
    },
    {
        "version": "v0.2.13",
        "pr": 1168,
        "pr_status": "Merged",
        "date": "2026-05",
        "denom": "USDT",
        "total": 18000,
        "source": "Community Sale",
        "recipients": [
            ("@blizko", "gonka12jaf7m4eysyqt32mrgarum6z96vt55tckvcleq", 8000, "Prompt of death: vLLM crash via structured outputs"),
            ("kaitaku.ai", "gonka1x45hruazmcqxslj3g8a08988hr5fr3wx33drhp", 10000, "Kimi experiments report"),
        ],
    },
    {
        "version": "v0.2.12",
        "pr": 1113,
        "pr_status": "Merged",
        "date": "2026-04",
        "denom": "USDT",
        "total": 35200,
        "source": "Community Sale",
        "recipients": [
            ("@x0152", "gonka18enyz7h6hh5zjveee5wnhkhrcexamfz0zdxxqe", 6000, "CertiK audit fixes (GEB-29, GEB-35, …)"),
            ("@x0152", "gonka18enyz7h6hh5zjveee5wnhkhrcexamfz0zdxxqe", 3000, "DKG dealer consensus — PR #825"),
            ("@x0152", "gonka18enyz7h6hh5zjveee5wnhkhrcexamfz0zdxxqe", 1000, "Developer inference access / account API"),
            ("@x0152", "gonka18enyz7h6hh5zjveee5wnhkhrcexamfz0zdxxqe", 500, "OpenAI compatibility and API error handling"),
            ("@x0152", "gonka18enyz7h6hh5zjveee5wnhkhrcexamfz0zdxxqe", 2500, "v0.2.12 release management"),
            ("@akup", "gonka1ejkupq3cy6p8xd64ew2wlzveml86ckpzn9dl56", 5000, "v0.2.12 release management"),
            ("—", "gonka1yhdhp4vwsvdsplv4acksntx0zxh8saueq6lj9m", 9000, "Inference validation optimization — Issue #929"),
            ("—", "gonka1vu28c7w5zxqe28lakrrfdrkvscft326rxur3dv", 3000, "Acquire node gRPC — PR #945"),
            ("@0xMayoor", "gonka1s8szs7n43jxgz4a4xaxmzm5emh7fmjxhach7w8", 2000, "Fund atomicity error safety — PR #789"),
            ("@qdanik", "gonka1j3f2xkapx8cmczpjqcsrh7cc3peyj3ngkjv4p8", 1500, "Align validator slashing — PR #940"),
            ("—", "gonka1c34w3r45f0uftjckt2yy4k22vnc3zqjnp0umyz", 500, "Free inference vulnerability report"),
            ("—", "gonka139f7x4gur2yuyty64dkqxep8jk3d7ku8ayjaqg", 200, "Chat completions fix — Issue #499"),
            ("@blizko", "gonka12jaf7m4eysyqt32mrgarum6z96vt55tckvcleq", 1000, "Review of upgrade v0.2.11"),
        ],
    },
    {
        "version": "v0.2.11",
        "pr": 919,
        "pr_status": "Merged",
        "date": "2026-03",
        "denom": "GNK",
        "total": 150750,
        "source": "Gov Module",
        "recipients": [
            ("@x0152", "gonka18enyz7h6hh5zjveee5wnhkhrcexamfz0zdxxqe", 2500, "Data race conditions fix review — PR #543"),
            ("—", "gonka1yhdhp4vwsvdsplv4acksntx0zxh8saueq6lj9m", 25000, "PoC Integration into vLLM v0.11.1 — Issue #628"),
            ("@blizko", "gonka12jaf7m4eysyqt32mrgarum6z96vt55tckvcleq", 10000, "vLLM HTTP 502 via prompt series"),
            ("@blizko", "gonka12jaf7m4eysyqt32mrgarum6z96vt55tckvcleq", 1000, "Dust transaction vulnerability report"),
            ("@ouicate", "gonka1f0elpwnx7ezytdlck35003nz6qk8kzvurvnj4a", 5000, "Remote DoS of Validator PoC"),
            ("@ouicate", "gonka1f0elpwnx7ezytdlck35003nz6qk8kzvurvnj4a", 5000, "State Bloat PoC / End-Block DoS"),
            ("@ouicate", "gonka1f0elpwnx7ezytdlck35003nz6qk8kzvurvnj4a", 750, "Bridge ETH address parsing vuln"),
            ("@x0152", "gonka18enyz7h6hh5zjveee5wnhkhrcexamfz0zdxxqe", 1000, "Planned task — PR #775"),
            ("@x0152", "gonka18enyz7h6hh5zjveee5wnhkhrcexamfz0zdxxqe", 1250, "Planned task — PR #773"),
            ("@qdanik", "gonka1j3f2xkapx8cmczpjqcsrh7cc3peyj3ngkjv4p8", 12000, "vLLM 0.15.1 compatibility experiments"),
            ("@qdanik", "gonka1j3f2xkapx8cmczpjqcsrh7cc3peyj3ngkjv4p8", 15000, "vLLM simultaneous PoC + inference"),
            ("@qdanik", "gonka1j3f2xkapx8cmczpjqcsrh7cc3peyj3ngkjv4p8", 5000, "Wind down window vulnerability — PR #767"),
            ("@akup", "gonka1ejkupq3cy6p8xd64ew2wlzveml86ckpzn9dl56", 1000, "Nodes unable to join from snapshots"),
            ("@x0152", "gonka18enyz7h6hh5zjveee5wnhkhrcexamfz0zdxxqe", 3000, "Nodes unable to join (source problem)"),
            ("—", "gonka17kmfwzthep3alxt57vqcqr48uv7swp0u63gcnj", 750, "StartInference/FinishInference — Issue #780"),
            ("@x0152", "gonka18enyz7h6hh5zjveee5wnhkhrcexamfz0zdxxqe", 5000, "StartInference/FinishInference — Issue #781"),
            ("@akup", "gonka1ejkupq3cy6p8xd64ew2wlzveml86ckpzn9dl56", 5000, "StartInference/FinishInference — Issue #782"),
            ("@Lelouch33", "gonka128nd36m2pz5qcs4q6rd69622flyls05nleazqq", 7500, "Important issue + testing with fix — PR #867"),
            ("kaitaku.ai", "gonka1x45hruazmcqxslj3g8a08988hr5fr3wx33drhp", 22500, "vLLM 0.15.1 compatibility — Issue #730"),
            ("—", "gonka100s7x2t0npruu9ta02306qfmaened3vg3a9dn6", 5000, "Batch Transfer With Vesting — PR #835"),
            ("@qdanik", "gonka1j3f2xkapx8cmczpjqcsrh7cc3peyj3ngkjv4p8", 5000, "Collateral slashing vulnerability — PR #868"),
            ("@akup", "gonka1ejkupq3cy6p8xd64ew2wlzveml86ckpzn9dl56", 7500, "v0.2.11 release management"),
            ("@x0152", "gonka18enyz7h6hh5zjveee5wnhkhrcexamfz0zdxxqe", 7500, "v0.2.11 release management"),
            ("@0xMayoor", "gonka1s8szs7n43jxgz4a4xaxmzm5emh7fmjxhach7w8", 2500, "v0.2.10 upgrade review"),
            ("@blizko", "gonka12jaf7m4eysyqt32mrgarum6z96vt55tckvcleq", 2500, "v0.2.10 upgrade review"),
            ("@x0152", "gonka18enyz7h6hh5zjveee5wnhkhrcexamfz0zdxxqe", 2500, "v0.2.10 upgrade review"),
        ],
    },
    {
        "version": "v0.2.10",
        "pr": 733,
        "pr_status": "Merged",
        "date": "2026-02",
        "denom": "GNK",
        "total": 23000,
        "source": "Gov Module",
        "recipients": [
            ("@x0152", "gonka18enyz7h6hh5zjveee5wnhkhrcexamfz0zdxxqe", 500, "Minor vulnerability fix — PR #661"),
            ("@x0152", "gonka18enyz7h6hh5zjveee5wnhkhrcexamfz0zdxxqe", 700, "Planned task — PR #644"),
            ("@akup", "gonka1ejkupq3cy6p8xd64ew2wlzveml86ckpzn9dl56", 10000, "Medium risk vulnerability report + fix — PR #659"),
            ("—", "gonka1c34w3r45f0uftjckt2yy4k22vnc3zqjnp0umyz", 5000, "First report of vulnerability fixed in #659"),
            ("@x0152", "gonka18enyz7h6hh5zjveee5wnhkhrcexamfz0zdxxqe", 1000, "Low risk vulnerability — PR #545"),
            ("—", "gonka1jkydytz99gkh0t42gjj4lz0mmdeumqp7mtzke3", 100, "Minor bug fix — PR #640"),
            ("—", "gonka123khww9elhtj49zumz0daleaudl6jn9y87tf23", 500, "First report + suggested fix — Issue #422"),
            ("—", "gonka1jkydytz99gkh0t42gjj4lz0mmdeumqp7mtzke3", 100, "Minor bug fix — PR #638"),
            ("—", "gonka1jkydytz99gkh0t42gjj4lz0mmdeumqp7mtzke3", 100, "Minor bug fix — PR #634"),
            ("@ouicate", "gonka1f0elpwnx7ezytdlck35003nz6qk8kzvurvnj4a", 5000, "Independent report on issue in PR #710"),
            ("@x0152", "gonka18enyz7h6hh5zjveee5wnhkhrcexamfz0zdxxqe", 500, "Low risk vulnerability — PR #643"),
        ],
    },
    {
        "version": "v0.2.6",
        "pr": 497,
        "pr_status": "Merged",
        "date": "2026-01",
        "denom": "GNK",
        "total": 30000,
        "source": "Gov Module",
        "recipients": [
            ("—", "gonka1gmuxdcxlsxn5z72elx77w9zym7yrgfxqgzg6ry", 20000, "Vulnerability in Confirmation PoC — PR #459"),
            ("@0xMayoor", "gonka1s8szs7n43jxgz4a4xaxmzm5emh7fmjxhach7w8", 10000, "Bridge Exchange Double Vote Case Bypass"),
        ],
    },
]


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
        gnk_html = f'<span style="{gnk_style}">{gnk_val} GNK</span>'
        if gnk_equiv_usdt:
            gnk_html += f' <span style="{BLUE}">(~${gnk_equiv_usdt} USDT)</span>'
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

    # Append upgrade-handler bounty distributions
    for b in sorted(BOUNTY_DISTRIBUTIONS, key=lambda x: x["total"], reverse=True):
        src = f"Upgrade Handler ({b['source']})"
        gnk_str = f"{b['total']:,}" if b['denom'] == 'GNK' else "—"
        usdt_str = f"${b['total']:,}" if b['denom'] == 'USDT' else "—"
        pr_url = f"https://github.com/gonka-ai/gonka/pull/{b['pr']}"
        rows.append(
            f"| [PR #{b['pr']}]({pr_url}) "
            f"| {b['date']} "
            f"| {b['version']} bounty distribution "
            f"| {src} "
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

    # Bounty totals
    bounty_gnk = sum(b["total"] for b in BOUNTY_DISTRIBUTIONS if b["denom"] == "GNK")
    bounty_usdt = sum(b["total"] for b in BOUNTY_DISTRIBUTIONS if b["denom"] == "USDT")
    bounty_sale = sum(b["total"] for b in BOUNTY_DISTRIBUTIONS if b["source"] == "Community Sale")
    bounty_gov = sum(b["total"] for b in BOUNTY_DISTRIBUTIONS if b["source"] == "Gov Module")

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
| Total governance proposals | {len(funding)} |
| Total GNK approved (proposals) | {total_gnk:,} GNK |
| Total USDT approved (proposals) | ${total_usdt:,} |
| From Community Pool | {pool_gnk:,} GNK + ${pool_usdt:,} |
| From Gov Module | {gov_gnk:,} GNK |
| Largest funding | {largest_label} |
| Most recent | {recent_label} |
| **Upgrade distributions** | **{len(BOUNTY_DISTRIBUTIONS)}** |
| Total GNK distributed (upgrades) | {bounty_gnk:,} GNK |
| Total USDT distributed (upgrades) | ${bounty_usdt:,} |
| From Community Sale contract | ${bounty_sale:,} USDT |
| From Gov Module | {bounty_gov:,} GNK |"""


def generate_bounty_table():
    rows = [
        "| Version | PR | Status | Date | Recipients | Total GNK | Total USDT | Source",
        "| :------ | :- | :----- | :--- | :--------- | --------: | --------: | :----",
    ]
    for b in BOUNTY_DISTRIBUTIONS:
        pr_url = f"https://github.com/gonka-ai/gonka/pull/{b['pr']}"
        n = len(b["recipients"])
        gnk_str = f"{b['total']:,}" if b['denom'] == 'GNK' else "—"
        usdt_str = f"${b['total']:,}" if b['denom'] == 'USDT' else "—"
        rows.append(
            f"| {b['version']} "
            f"| [PR #{b['pr']}]({pr_url}) "
            f"| {b['pr_status']} "
            f"| {b['date']} "
            f"| {n} recipients "
            f"| {gnk_str} "
            f"| {usdt_str} "
            f"| {b['source']} |"
        )
    return "\n".join(rows) + "\n"


def generate_bounty_detail_table():
    """Detailed breakdown of each bounty recipient."""
    parts = []
    for b in BOUNTY_DISTRIBUTIONS:
        pr_url = f"https://github.com/gonka-ai/gonka/pull/{b['pr']}"
        parts.append(f"\n### {b['version']} — [PR #{b['pr']}]({pr_url}) ({b['pr_status']})\n")
        parts.append("| Recipient | Address | Amount | Description |")
        parts.append("| :------- | :------ | ----: | :---------- |")
        for alias, addr, amt, desc in b["recipients"]:
            denom_sym = "$" if b["denom"] == "USDT" else ""
            denom_name = " USDT" if b["denom"] == "USDT" else " GNK"
            addr_link = f"[`{addr}`](https://gonka.gg/address/{addr})"
            parts.append(f"| {alias} | {addr_link} | {denom_sym}{amt:,}{denom_name} | {desc} |")
        # total row
        gnk_str = f"{b['total']:,} GNK" if b['denom'] == 'GNK' else ""
        usdt_str = f"${b['total']:,} USDT" if b['denom'] == 'USDT' else ""
        total_label = f"{gnk_str}{usdt_str}"
        parts.append(f"| **Total** | | **{total_label}** | |")
        parts.append("")

    return "\n".join(parts) + "\n"


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

    bounty_table = generate_bounty_table()
    bounty_detail = generate_bounty_detail_table()
    content = replace_between_markers(
        content, "<!-- BOUNTY_TABLE_START -->", "<!-- BOUNTY_TABLE_END -->",
        bounty_table
    )
    content = replace_between_markers(
        content, "<!-- BOUNTY_DETAIL_START -->", "<!-- BOUNTY_DETAIL_END -->",
        bounty_detail
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
