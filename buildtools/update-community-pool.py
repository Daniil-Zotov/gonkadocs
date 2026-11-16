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

import base64
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
COMMUNITY_POOL_ADDR = "gonka1jv65s3grqf6v6jl3dp4t6c9t9rk99cd8h2rzwa"
GOV_MODULE_ADDR = "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33"
USDT_IBC_DENOM = "ibc/115F68FBA220A028C6F6ED08EA0C1A9C8C52798B14FB66E6C89D5D8C06A524D4"
# Bridged CW20 USDT — "Tether USD", 6 decimals (Ethereum 0xdAC17f958D2ee523a2206206994597C13d831ec7)
USDT_CW20_ADDR = "gonka15ggwj9un6qrmu4nj5ev6l7kpdcr00td03ff2mmj4cyhl8u8vjd2qnl3hgk"
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
        "version": "v0.2.16",
        "pr": None,
        "link": f"{SITE_URL}{PROPOSALS_PREFIX}2026-q4/113/",
        "link_label": "Proposal #113",
        "pr_status": "Passed",
        "date": "2026-10",
        "denom": "USDT",
        "total": 104150,
        # v0.2.16 bounties were distributed via governance proposal #113
        # (the upgrade handler defines distributeBountyRewards but never calls it)
        "gov_proposal": True,
        "source": "Community Sale",
        "recipients": [
            ("kaitaku.ai (@baychak, @clanster)", "gonka1x45hruazmcqxslj3g8a08988hr5fr3wx33drhp", 12000, "ML-node observability: metrics exporter, DAPI federation endpoint, Grafana dashboards (gonka-grafana) + hosting monitoring.kaitaku.ai"),
            ("@qdanik", "gonka1j3f2xkapx8cmczpjqcsrh7cc3peyj3ngkjv4p8", 500, "Contribution to the ML-node observability track"),
            ("kaitaku.ai (@baychak, @clanster)", "gonka1x45hruazmcqxslj3g8a08988hr5fr3wx33drhp", 20000, "decode-PoC: vLLM port and experiments with reevaluation on all hardware schemes and models"),
            ("Axel-t", "gonka1yhdhp4vwsvdsplv4acksntx0zxh8saueq6lj9m", 18000, "CUDA Graph Support for Decode PoC"),
            ("kaitaku.ai (@baychak, @clanster)", "gonka1x45hruazmcqxslj3g8a08988hr5fr3wx33drhp", 5000, "gonka-poc as plugin: removes re-porting PoC on every vLLM release"),
            ("kaitaku.ai (@baychak, @clanster)", "gonka1x45hruazmcqxslj3g8a08988hr5fr3wx33drhp", 5000, "DeepSeek-V4-Flash: experiments and new model proposal"),
            ("kaitaku.ai (@baychak, @clanster)", "gonka1x45hruazmcqxslj3g8a08988hr5fr3wx33drhp", 4000, "GLM-5.3-Flash: experiments and new model proposal"),
            ("kaitaku.ai (@baychak, @clanster)", "gonka1x45hruazmcqxslj3g8a08988hr5fr3wx33drhp", 2000, "GLM-5.2: experiments, images for B300/B200/H200"),
            ("kaitaku.ai (@baychak, @clanster)", "gonka1x45hruazmcqxslj3g8a08988hr5fr3wx33drhp", 2000, "Hy3 evaluation experiments"),
            ("kaitaku.ai (@baychak, @clanster)", "gonka1x45hruazmcqxslj3g8a08988hr5fr3wx33drhp", 9600, "GPU rental reimbursement for model and PoC experiments since 2026-06-01 (Verda, Vast, Dataoorts, Nebius), at cost"),
            ("@x0152", "gonka18enyz7h6hh5zjveee5wnhkhrcexamfz0zdxxqe", 8000, "Release management: PR reviews, HackerOne report reviews, Trainshards v0 (PR #1350, #1618)"),
            ("@vitaly-andr", "gonka1uqt4hue8tljwwgdkvtthyl3n8kkkqtydyns4cm", 5000, "Chain-halt bug report (Issue #1205) + fix (cosmos-sdk PR #16)"),
            ("@vitaly-andr", "gonka1uqt4hue8tljwwgdkvtthyl3n8kkkqtydyns4cm", 1000, "v0.2.16 upgrade review"),
            ("@bonujel", "gonka1zqss46r6jf6dhhyaa777kc2ppvjhn0ufkx4y57", 1000, "v0.2.16 upgrade review"),
            ("@staaason / @zpoken", "gonka1s8zggm642e3kncy48c7vxwmeclt2wxyyd8qtdt", 8050, "HackerOne report reviews + PR #1767, #1552 (landed as PR #1623)"),
            ("@cyberdelamain", "gonka15u0r3mf6t7zsfuslusnyt7hsjrq357yumpe8st", 3000, "v0.2.16 review and fixes: PR #1828, #1846, #1845, #1859"),
        ],
    },
    {
        "version": "v0.2.15",
        "pr": 1503,
        "pr_status": "Merged",
        "date": "2026-07",
        "denom": "USDT",
        "total": 39825,
        "source": "Community Sale",
        "recipients": [
            ("@akup", "gonka1ejkupq3cy6p8xd64ew2wlzveml86ckpzn9dl56", 22000, "RM: devshard v4 release management"),
            ("@Ryanchen911", "gonka1zqss46r6jf6dhhyaa777kc2ppvjhn0ufkx4y57", 1000, "RM: devshard v4 upgrade review"),
            ("@redstartechno", "gonka105ce4495mj0mwkxqeasgdzqfq5jjrfq32eza5l", 200, "PR #1308: devshard contribution"),
            ("@0xMayoor", "gonka1s8szs7n43jxgz4a4xaxmzm5emh7fmjxhach7w8", 3000, "PR #1283: report and fix of medium severity vulnerability"),
            ("@0xMayoor", "gonka1s8szs7n43jxgz4a4xaxmzm5emh7fmjxhach7w8", 500, "PR #1311: report and fix of low severity vulnerability"),
            ("@pixelplex", "gonka1vu28c7w5zxqe28lakrrfdrkvscft326rxur3dv", 7000, "PR #1144, #1152, #1126, #1154: devshard contribution"),
            ("@aikuznetsov", "gonka1frlfyz2wtltdy47dq3w9pwc8ruvjvlthp2lh53", 3125, "PR #1332, #1295: testing proposal and implementation"),
            ("@snevolin", "gonka1vnupswg7qz2w5k5ax6zrp02mxmln6arnvjc87h", 3000, "PR #1437, #1490: devshard contribution"),
        ],
    },
    {
        "version": "v0.2.14",
        "pr": 1446,
        "pr_status": "Merged",
        "date": "2026-07",
        "denom": "USDT",
        "total": 50250,
        "source": "Community Sale",
        "recipients": [
            ("@akup", "gonka1ejkupq3cy6p8xd64ew2wlzveml86ckpzn9dl56", 5000, "devshards v3 RM, upgrade review, HackerOne reviews"),
            ("@x0152", "gonka18enyz7h6hh5zjveee5wnhkhrcexamfz0zdxxqe", 6000, "RM, HackerOne reviews"),
            ("@qdanik", "gonka1j3f2xkapx8cmczpjqcsrh7cc3peyj3ngkjv4p8", 11500, "RM, HackerOne reviews, MiniMax M2.7 R&D, PoC (incl. GPU), SMST optimization (PR #1432)"),
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
            ("@maksimenkoff", "gonka1gmuxdcxlsxn5z72elx77w9zym7yrgfxqgzg6ry", 3000, "Vulnerability report and fix #1415"),
            ("@blizko", "gonka12jaf7m4eysyqt32mrgarum6z96vt55tckvcleq", 1000, "v0.2.13 upgrade review"),
        ],
    },
    {
        "version": "v0.2.13",
        "pr": 1168,
        "pr_status": "Merged",
        "date": "2026-05",
        "denom": "USDT",
        "total": 18875,
        "source": "Community Sale",
        "recipients": [
            ("@blizko", "gonka12jaf7m4eysyqt32mrgarum6z96vt55tckvcleq", 8000, "Prompt of death: vLLM crash via structured outputs"),
            ("kaitaku.ai", "gonka1x45hruazmcqxslj3g8a08988hr5fr3wx33drhp", 10000, "Kimi experiments report"),
            ("@ouicate", "gonka1f0elpwnx7ezytdlck35003nz6qk8kzvurvnj4a", 500, "PR #826: Partial Payment on Claim Failure Causes Permanent Reward Loss"),
            ("@ouicate", "gonka1f0elpwnx7ezytdlck35003nz6qk8kzvurvnj4a", 375, "PR #826: Underfunded Work Payout Still Removes Settle Amount"),
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
        amt = int(str(amount_str).split(".")[0])
        if denom == "ngonka":
            return f"{amt / 1_000_000_000:,.0f}"
        elif denom == USDT_IBC_DENOM:
            return f"${amt / 1_000_000:,.0f}"
        return f"{amt} {denom}"
    except (ValueError, TypeError, ZeroDivisionError):
        return str(amount_str)


def format_balance_line(gnk_val, usdt_val, show_gnk=True, show_usdt=True, gnk_equiv_usdt=None, gnk_color=None, extra_parts=None):
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
    for extra in (extra_parts or []):
        parts.append(extra)
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


def fetch_cw20_balance(token_addr, holder_addr):
    """Query CW20 token balance via wasm smart query. Returns raw amount string."""
    query = {"balance": {"address": holder_addr}}
    b64 = base64.b64encode(json.dumps(query).encode()).decode()
    data = fetch_json(f"{{BASE}}/cosmwasm/wasm/v1/contract/{token_addr}/smart/{b64}")
    if not data:
        return "0"
    try:
        return data.get("data", {}).get("balance", "0")
    except (AttributeError, TypeError):
        return "0"


# ── Fetch funding history ──────────────────────────────────────

def iter_messages(messages):
    """Yield effective messages, unwrapping cosmos.authz MsgExec envelopes (e.g. #117)."""
    for m in (messages or []):
        t = m.get("@type", "")
        if t.endswith(".MsgExec") and m.get("msgs"):
            yield from iter_messages(m.get("msgs", []))
        else:
            yield m


def parse_funding_from_messages(messages):
    """Extract GNK and USDT amounts from all message types in a proposal, per source.

    Sources:
    - "Community Pool" — MsgCommunityPoolSpend (real distribution-module spends)
    - "Community Sale" — MsgExecuteContract withdraw_ibc / withdraw_cw20
      (gov-module-authorized USDT payouts from the Community Sale contract)
    - "Gov Module" — vesting distributions (GNK)

    Inflows (CW20 send/transfer INTO community-controlled addresses, e.g. the
    #117 Bitfury tranche) are reported GROSS and never netted against outflows,
    so both legs of deposit-then-payout proposals stay visible.

    Returns (sources, inflow_sources): both map source name to (gnk, usdt)
    non-negative ints (zero entries dropped).
    """
    outflows = {}
    inflows = {}

    def _add(bucket, source, gnk=0.0, usdt=0.0):
        b = bucket.setdefault(source, [0.0, 0.0])
        b[0] += gnk
        b[1] += usdt

    for m in iter_messages(messages):
        t = m.get("@type", "")

        if "MsgCommunityPoolSpend" in t:
            for c in m.get("amount", []):
                denom = c.get("denom", "")
                try:
                    amt = int(c.get("amount", "0"))
                except (ValueError, TypeError):
                    continue
                if denom == "ngonka":
                    _add(outflows, "Community Pool", gnk=amt / 1_000_000_000)
                elif denom == USDT_IBC_DENOM:
                    _add(outflows, "Community Pool", usdt=amt / 1_000_000)

        elif "MsgExecuteContract" in t:
            # All on-chain MsgExecuteContract calls in governance proposals target
            # the Community Sale contract — its USDT payouts are a separate source,
            # not Community Pool spending
            wi = m.get("msg", {}).get("withdraw_ibc", {})
            if wi and wi.get("denom") == USDT_IBC_DENOM:
                try:
                    _add(outflows, "Community Sale", usdt=int(wi.get("amount", "0")) / 1_000_000)
                except (ValueError, TypeError):
                    pass
            # withdraw_cw20 pays out bridged CW20 USDT from the Community Sale
            # contract (#117 reimbursement, #118 MillCreek fee)
            wc = m.get("msg", {}).get("withdraw_cw20", {})
            if wc and wc.get("contract_addr") == USDT_CW20_ADDR:
                try:
                    _add(outflows, "Community Sale", usdt=int(wc.get("amount", "0")) / 1_000_000)
                except (ValueError, TypeError):
                    pass
            for c in m.get("funds", []):
                denom = c.get("denom", "")
                try:
                    amt = int(c.get("amount", "0"))
                except (ValueError, TypeError):
                    continue
                if denom == "ngonka":
                    _add(outflows, "Community Sale", gnk=amt / 1_000_000_000)
            # CW20 send/transfer INTO a pool-controlled address = USDT inflow (#117)
            inner = m.get("msg", {})
            if m.get("contract") == USDT_CW20_ADDR:
                cw_payload = inner.get("send") or inner.get("transfer") or {}
                recipient = cw_payload.get("contract") or cw_payload.get("recipient") or ""
                if recipient in (COMMUNITY_SALE_ADDR, COMMUNITY_POOL_ADDR):
                    try:
                        _add(inflows, "Community Sale", usdt=int(cw_payload.get("amount", "0")) / 1_000_000)
                    except (ValueError, TypeError):
                        pass

        elif "MsgBatchTransferWithVesting" in t:
            for o in m.get("outputs", []):
                for c in o.get("amount") or []:
                    denom = c.get("denom", "")
                    try:
                        amt = int(c.get("amount", "0"))
                    except (ValueError, TypeError):
                        continue
                    if denom == "ngonka":
                        _add(outflows, "Gov Module", gnk=amt / 1_000_000_000)
                    elif denom == USDT_IBC_DENOM:
                        _add(outflows, "Gov Module", usdt=amt / 1_000_000)

        elif "MsgTransferWithVesting" in t:
            for c in m.get("amount", []):
                denom = c.get("denom", "")
                try:
                    amt = int(c.get("amount", "0"))
                except (ValueError, TypeError):
                    continue
                if denom == "ngonka":
                    _add(outflows, "Gov Module", gnk=amt / 1_000_000_000)

        elif "MsgMultiSend" in t:
            for inp in m.get("inputs", []):
                for c in inp.get("coins", []):
                    denom = c.get("denom", "")
                    try:
                        amt = int(c.get("amount", "0"))
                    except (ValueError, TypeError):
                        continue
                    if denom == "ngonka":
                        _add(outflows, "Gov Module", gnk=amt / 1_000_000_000)

    # Report inflows and outflows GROSS per source (not netted), so both legs
    # of deposit-then-payout proposals stay visible (e.g. #117: +1,750,000 in,
    # 607,250 immediately reimbursed to Bitfury, net +1,142,750).
    sources = {}
    for s, (g_out, u_out) in outflows.items():
        if g_out > 0 or u_out > 0:
            sources[s] = (int(g_out), int(u_out))
    inflow_sources = {}
    for s, (g_in, u_in) in inflows.items():
        if g_in > 0 or u_in > 0:
            inflow_sources[s] = (int(g_in), int(u_in))

    return sources, inflow_sources


def determine_source(sources):
    """Build a combined source label from the per-source breakdown."""
    names = [s for s in ("Community Pool", "Community Sale", "Gov Module") if sources.get(s)]
    return " + ".join(names) if names else "—"


def fetch_funding_history():
    """Fetch all passed proposals and aggregate funding amounts.

    Returns (funding, source_totals, net_totals). source_totals maps each
    source name (inflow keys keep an "(inflow)" suffix) to (gnk, usdt) summed
    over per-message attribution; net_totals maps inflow source names to the
    proposal-level net (deposit − same-source payout).
    """
    data = fetch_json("{BASE}/cosmos/gov/v1/proposals?pagination.limit=200")
    if not data:
        return [], {}, {}

    funding = []
    source_totals = {}
    net_totals = {}
    for p in data.get("proposals", []):
        if p.get("status") not in PASSED_STATUSES:
            continue

        pid = p["id"]
        title = p.get("title", "")
        msgs = p.get("messages", [])
        ts = fmt_time_short(p.get("voting_end_time", ""))

        sources, inflow_sources = parse_funding_from_messages(msgs)
        gnk_spend = sum(g for g, _ in sources.values())
        usdt_spend = sum(u for _, u in sources.values())
        gnk_in = sum(g for g, _ in inflow_sources.values())
        usdt_in = sum(u for _, u in inflow_sources.values())

        if gnk_spend == 0 and usdt_spend == 0 and gnk_in == 0 and usdt_in == 0:
            continue

        submit = p.get("submit_time", "")
        q = "unknown"
        if submit:
            try:
                dt = datetime.fromisoformat(submit.replace("Z", "+00:00"))
                q = get_quarter(dt).lower()
            except (ValueError, TypeError):
                pass

        base = {
            "pid": pid,
            "quarter": q,
            "date": ts,
            "title": short_title(title),
        }

        # Deposit legs first (chronological: money in, then paid out — e.g. #117)
        for s, (g, u) in inflow_sources.items():
            funding.append({**base, "source": f"{s} (inflow)", "gnk": g, "usdt": u, "inflow": True})

        if gnk_spend > 0 or usdt_spend > 0:
            funding.append({**base, "source": determine_source(sources), "gnk": gnk_spend, "usdt": usdt_spend, "inflow": False})

        # Accumulate per-source totals for the summary; inflow keys keep the
        # "(inflow)" suffix so gross deposits and gross payouts stay separate
        for s, (g, u) in sources.items():
            pg, pu = source_totals.get(s, (0, 0))
            source_totals[s] = (pg + g, pu + u)
        for s, (g, u) in inflow_sources.items():
            key = f"{s} (inflow)"
            pg, pu = source_totals.get(key, (0, 0))
            source_totals[key] = (pg + g, pu + u)
        # Proposal-level net per source (deposit minus same-source payout, e.g.
        # #117: 1,750,000 − 607,250 = +1,142,750)
        for s, (g_in, u_in) in inflow_sources.items():
            g_out, u_out = sources.get(s, (0, 0))
            net_g, net_u = g_in - g_out, u_in - u_out
            if net_g > 0 or net_u > 0:
                pg, pu = net_totals.get(s, (0, 0))
                net_totals[s] = (pg + net_g, pu + net_u)

    return funding, source_totals, net_totals


# ── Generate content ───────────────────────────────────────────

def _cw20_span(cw20_raw):
    """HTML span with the CW20 bridged-USDT part of a balance, or None if zero."""
    try:
        cw_usdt = int(str(cw20_raw).split(".")[0]) / 1_000_000
    except (ValueError, TypeError, ZeroDivisionError):
        return None
    if cw_usdt <= 0:
        return None
    BLUE = 'color:var(--md-accent-fg-color,#5468ff);font-size:0.95rem;font-weight:600'
    return f'<span style="{BLUE}">${cw_usdt:,.0f} USDT (CW20 bridged)</span>'


def generate_balance_line(gnk_raw, usdt_raw, extra_parts=None):
    gnk_val = format_balance(gnk_raw, "ngonka") if gnk_raw else ""
    usdt_val = format_balance(usdt_raw, USDT_IBC_DENOM) if usdt_raw else ""
    return format_balance_line(gnk_val, usdt_val, extra_parts=extra_parts)


def generate_sale_balance_line(sale_balances, sale_cw20_raw="0"):
    gnk = sale_balances.get("ngonka", "0")
    usdt = sale_balances.get(USDT_IBC_DENOM, "0")
    gnk_val = format_balance(gnk, "ngonka")
    usdt_val = format_balance(usdt, USDT_IBC_DENOM)
    try:
        gnk_raw = int(str(gnk).split(".")[0]) / 1_000_000_000
        equiv = gnk_raw * 0.6
        equiv_str = f"{equiv:,.0f}"
    except (ValueError, TypeError):
        equiv_str = None
    cw20_span = _cw20_span(sale_cw20_raw)
    return format_balance_line(gnk_val, usdt_val, gnk_equiv_usdt=equiv_str, gnk_color="grey",
                               extra_parts=[cw20_span] if cw20_span else None)


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
        sign = "+" if f.get("inflow") else ""
        gnk_str = f"{sign}{f['gnk']:,}" if f["gnk"] > 0 else "—"
        usdt_str = f"{sign}${f['usdt']:,}" if f["usdt"] > 0 else "—"
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
        # Distributions made via governance proposals (e.g. v0.2.16 via #113) are
        # already listed as proposal rows above — skip to avoid double counting.
        if b.get("gov_proposal"):
            continue
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


def _amount_label(f):
    """Format a funding entry as "X GNK + $Y USDT" (with "+" for inflows)."""
    parts = []
    if f["gnk"] > 0:
        parts.append(f"{f['gnk']:,} GNK")
    if f["usdt"] > 0:
        sign = "+" if f.get("inflow") else ""
        parts.append(f"{sign}${f['usdt']:,} USDT")
    return " + ".join(parts) if parts else "—"


def generate_summary(funding, source_totals, net_totals):
    spends = [f for f in funding if not f.get("inflow")]
    inflows = [f for f in funding if f.get("inflow")]
    total_gnk = sum(f["gnk"] for f in spends)
    total_usdt = sum(f["usdt"] for f in spends)
    # Per-source totals use per-message attribution (accurate for mixed proposals
    # like #116 = Community Pool + Community Sale + Gov Module). Inflow keys keep
    # the "(inflow)" suffix — e.g. "Community Sale (inflow)" = gross deposits (#117).
    pool_gnk, pool_usdt = source_totals.get("Community Pool", (0, 0))
    sale_gnk, sale_usdt = source_totals.get("Community Sale", (0, 0))
    gov_gnk, _ = source_totals.get("Gov Module", (0, 0))

    # Gross inflows (e.g. #117 Bitfury tranche into the Community Sale contract)
    inflow_gnk = sum(f["gnk"] for f in inflows)
    inflow_usdt = sum(f["usdt"] for f in inflows)
    # Proposal-level net per inflow source (deposit minus same-source payout)
    net_gnk = sum(g for g, _ in net_totals.values())
    net_usdt = sum(u for _, u in net_totals.values())

    # Bounty totals
    bounty_gnk = sum(b["total"] for b in BOUNTY_DISTRIBUTIONS if b["denom"] == "GNK")
    bounty_usdt = sum(b["total"] for b in BOUNTY_DISTRIBUTIONS if b["denom"] == "USDT")
    bounty_sale = sum(b["total"] for b in BOUNTY_DISTRIBUTIONS if b["source"] == "Community Sale")
    bounty_gov = sum(b["total"] for b in BOUNTY_DISTRIBUTIONS if b["source"] == "Gov Module")

    largest = max(spends, key=lambda f: f["gnk"]) if spends else None
    largest_label = f"#{largest['pid']} — {_amount_label(largest)}" if largest else "—"

    recent = max(funding, key=lambda f: int(f["pid"])) if funding else None
    recent_label = f"#{recent['pid']} — {_amount_label(recent)}" if recent else "—"

    n_proposals = len({f["pid"] for f in funding})
    inflow_row = ""
    if inflow_gnk > 0 or inflow_usdt > 0:
        parts = []
        if inflow_gnk > 0:
            parts.append(f"+{inflow_gnk:,} GNK")
        if inflow_usdt > 0:
            parts.append(f"+${inflow_usdt:,}")
        inflow_row = f"\n| Community Sale inflows (proposals) | {' + '.join(parts)} |"
    net_row = ""
    if net_gnk > 0 or net_usdt > 0:
        parts = []
        if net_gnk > 0:
            parts.append(f"+{net_gnk:,} GNK")
        if net_usdt > 0:
            parts.append(f"+${net_usdt:,}")
        net_row = f"\n| Community Sale net (deposits − same-source payouts) | {' + '.join(parts)} |"

    return f"""| Metric | Value |
| :----- | :---- |
| Total governance proposals | {n_proposals} |
| Total GNK approved (proposals) | {total_gnk:,} GNK |
| Total USDT approved (proposals) | ${total_usdt:,} |
| From Community Pool | {pool_gnk:,} GNK + ${pool_usdt:,} |
| From Community Sale (proposals) | {sale_gnk:,} GNK + ${sale_usdt:,} |
| From Gov Module | {gov_gnk:,} GNK |{inflow_row}{net_row}
| Largest funding | {largest_label} |
| Most recent | {recent_label} |
| **Bounty distributions** | **{len(BOUNTY_DISTRIBUTIONS)}** |
| Total GNK distributed (bounties) | {bounty_gnk:,} GNK |
| Total USDT distributed (bounties) | ${bounty_usdt:,} |
| From Community Sale contract | ${bounty_sale:,} USDT |
| From Gov Module | {bounty_gov:,} GNK |"""


def generate_bounty_table():
    rows = [
        "| Version | PR | Status | Date | Recipients | Total GNK | Total USDT | Source",
        "| :------ | :- | :----- | :--- | :--------- | --------: | --------: | :----",
    ]
    for b in BOUNTY_DISTRIBUTIONS:
        link_url = b.get("link") or f"https://github.com/gonka-ai/gonka/pull/{b['pr']}"
        link_label = b.get("link_label") or f"PR #{b['pr']}"
        n = len(b["recipients"])
        gnk_str = f"{b['total']:,}" if b['denom'] == 'GNK' else "—"
        usdt_str = f"${b['total']:,}" if b['denom'] == 'USDT' else "—"
        rows.append(
            f"| {b['version']} "
            f"| [{link_label}]({link_url}) "
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
        link_url = b.get("link") or f"https://github.com/gonka-ai/gonka/pull/{b['pr']}"
        link_label = b.get("link_label") or f"PR #{b['pr']}"
        parts.append(f"\n### {b['version']} — [{link_label}]({link_url}) ({b['pr_status']})\n")
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
    sale_cw20 = fetch_cw20_balance(USDT_CW20_ADDR, COMMUNITY_SALE_ADDR)

    print("Fetching Gov Module balance...")
    gov_balances = fetch_account_balance(GOV_MODULE_ADDR)

    print("Fetching funding history from proposals...")
    funding, source_totals, net_totals = fetch_funding_history()

    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    pool_cw20 = fetch_cw20_balance(USDT_CW20_ADDR, COMMUNITY_POOL_ADDR)
    pool_cw20_span = _cw20_span(pool_cw20)
    pool_line = generate_balance_line(gnk_pool, usdt_pool,
                                      extra_parts=[pool_cw20_span] if pool_cw20_span else None)
    sale_line = generate_sale_balance_line(sale_balances, sale_cw20)
    gov_line = generate_gov_balance_line(gov_balances)
    fund_table = generate_funding_table(funding)
    summary = generate_summary(funding, source_totals, net_totals) if funding else ""

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
    cw20_fmt = "{:,.0f}".format(int(sale_cw20) / 1_000_000)
    print(f"  Community Sale: {format_balance(gnk_sale, 'ngonka')} GNK, {format_balance(usdt_s, USDT_IBC_DENOM)} USDT (IBC), ${cw20_fmt} USDT (CW20 bridged)")
    print(f"  Gov Module: {format_balance(gnk_gov, 'ngonka')} GNK")
    print(f"  Funding: {len(funding)} proposals")


if __name__ == "__main__":
    update_file()
