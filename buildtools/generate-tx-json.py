#!/usr/bin/env python3
"""Find submit tx hashes for on-chain governance proposals via ClickHouse API."""

import json
import os
import re
import subprocess
import sys
import time
from collections import defaultdict
from pathlib import Path

CLICKHOUSE_API = "https://rpc.gonka.gg/api/ch"
PROPOSALS_DIR = Path(os.environ.get("PROPOSALS_DIR", "docs/proposals/proposals"))


def curl_json(url, timeout=10):
    try:
        r = subprocess.run(
            ["curl", "-s", "--max-time", str(timeout), url],
            capture_output=True, text=True, timeout=timeout + 5
        )
        if r.returncode != 0 or not r.stdout.strip():
            return None
        return json.loads(r.stdout)
    except Exception as e:
        return None


def fetch_all_txs(address):
    txs = []
    offset = 0
    limit = 100
    while True:
        url = f"{CLICKHOUSE_API}/address/{address}?limit={limit}&offset={offset}"
        data = curl_json(url)
        if not data:
            break
        batch = data.get("txs", [])
        if not batch:
            break
        txs.extend(batch)
        has_more = data.get("has_more", False)
        if not has_more:
            break
        offset += limit
    return txs


def extract_submit_events(txs):
    results = []
    for tx in txs:
        ev = tx.get("events", "")
        if "submit_proposal" not in ev:
            continue
        m = re.search(r'"proposal_id"[^"]*"(\d+)"', ev)
        pid = m.group(1) if m else None
        if pid:
            results.append({
                "proposal_id": int(pid),
                "tx_hash": tx.get("tx_hash", ""),
                "block_time": tx.get("block_time", ""),
            })
    return results


def load_proposals():
    proposals = {}
    for qdir in sorted(PROPOSALS_DIR.iterdir()):
        if not qdir.is_dir() or not qdir.name.startswith("2"):
            continue
        for pdir in sorted(qdir.iterdir()):
            if not pdir.is_dir():
                continue
            idx = pdir / "index.md"
            if not idx.exists():
                continue
            pid = pdir.name
            content = idx.read_text()
            m = re.search(r'\*\*Proposer:\*\*.*?`(gonka1[^`]+)`', content)
            proposer = m.group(1) if m else None
            m = re.search(r'\*\*Submit:\*\*\s*(.*?UTC)', content)
            submit_time = m.group(1) if m else None
            proposals[pid] = {
                "proposer": proposer, "submit_time": submit_time, "quarter": qdir.name
            }
    return proposals


def main():
    print("=== Generate tx.json ===")
    proposals = load_proposals()
    print(f"Loaded {len(proposals)} proposals")

    by_proposer = defaultdict(list)
    for pid, p in proposals.items():
        if p["proposer"]:
            by_proposer[p["proposer"]].append(pid)

    print(f"Unique proposers: {len(by_proposer)}")

    submit_tx_map = {}

    for i, (proposer, pids) in enumerate(sorted(by_proposer.items()), 1):
        pids_sorted = sorted(pids, key=int)
        print(f"[{i}/{len(by_proposer)}] {proposer[:20]}... ({len(pids)} props: {','.join(pids_sorted)})")

        txs = fetch_all_txs(proposer)
        if not txs:
            print(f"  -> no txs or error")
            continue
        print(f"  -> {len(txs)} txs")

        events = extract_submit_events(txs)
        for ev in events:
            ps = str(ev["proposal_id"])
            if ps in proposals:
                submit_tx_map[ps] = ev
                print(f"  <- #{ps} tx={ev['tx_hash'][:16]}...")

    # Generate tx.json files
    found = 0
    nf = 0
    for pid in sorted(proposals.keys(), key=int):
        p = proposals[pid]
        pd = PROPOSALS_DIR / p["quarter"].lower() / pid
        pd.mkdir(parents=True, exist_ok=True)

        if pid in submit_tx_map:
            ev = submit_tx_map[pid]
            tj = {
                "submit_tx": ev["tx_hash"],
                "funding_tx": None,
                "note": "Funding transfer occurs in governance EndBlocker, not as a separate transaction",
            }
            found += 1
        else:
            tj = {
                "submit_tx": None,
                "funding_tx": None,
                "note": "Submit tx not found in ClickHouse index",
            }
            nf += 1

        (pd / "tx.json").write_text(json.dumps(tj, indent=2) + "\n")
        print(f"  {'OK' if pid in submit_tx_map else '--'} #{pid}: {pd / 'tx.json'}")

    print(f"\nDone: {found} found, {nf} not found")


if __name__ == "__main__":
    main()
