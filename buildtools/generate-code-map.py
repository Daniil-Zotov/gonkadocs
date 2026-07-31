#!/usr/bin/env python3
"""Generate gonka-code-map.txt — an index of the gonka-ai/gonka source mirror.

Scans gonka-code/ (repo root) and produces a structured map of modules, key
files, and design docs with full URLs, optimized for AI agents.

Usage:
    python3 buildtools/generate-code-map.py

Output:
    docs/gonka-code-map.txt  (served at /gonka-code-map.txt)
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CODE_DIR = ROOT / "gonka-code"
OUT = ROOT / "docs" / "gonka-code-map.txt"
SITE_URL = "https://gonkadocs.com"

# Generated/vendor files never surfaced in the map
HIDDEN_FILE_SUFFIXES = (".pb.go", ".pulsar.go", ".pb.gw.go", ".pb.goc.go")
HIDDEN_DIRS = {"api", "types", "simulation", "testutil", ".github", ".clinerules", ".junie"}

# (dir, heading, description)
MODULES = [
    ("inference-chain", "## Inference Chain (Cosmos SDK blockchain)\n",
     "Core blockchain node (Go). Contains app/, x/ modules, proto/, contracts/."),
    ("inference-chain/x/inference", "### x/inference — core inference module\n",
     "Proof of Compute, inference lifecycle, validation. keeper/ holds the business logic."),
    ("inference-chain/x/bls", "### x/bls — BLS threshold signing\n",
     "Distributed key generation, threshold signatures for PoC and cross-chain bridge."),
    ("inference-chain/x/collateral", "### x/collateral — collateral & slashing\n",
     "Host collateral, weight, slashing rules."),
    ("inference-chain/x/restrictions", "### x/restrictions — transfer restrictions\n",
     "Allowlists, transfer restrictions."),
    ("inference-chain/x/streamvesting", "### x/streamvesting — vesting\n",
     "Streamed vesting accounts, batch transfers with vesting."),
    ("inference-chain/x/bookkeeper", "### x/bookkeeper\n",
     "Accounting/settlement keeper module."),
    ("inference-chain/x/genesistransfer", "### x/genesistransfer\n",
     "Genesis account transfers."),
    ("inference-chain/app", "### app — node wiring\n",
     "app.go, ante handlers, upgrade_tracking, upgrades registry."),
    ("inference-chain/app/upgrades", "### app/upgrades — upgrade handlers\n",
     "One dir per protocol version (v0_2_2 .. v0_2_15). Each upgrades.go contains the on-chain bountyRewards array (bounty payouts)."),
    ("inference-chain/proto", "### proto — protobuf definitions\n",
     "Source .proto files for all modules."),
    ("inference-chain/contracts", "### contracts\n",
     "Solidity/Wasm contracts (community-sale, wrapped-token)."),
    ("devshard", "## Devshards\n",
     "Devshard protocol: short-lived escrow sessions for per-request inference billing. e2e/, testenv/."),
    ("decentralized-api", "## Decentralized API\n",
     "OpenAI-compatible API layer, broker, event listener, node manager."),
    ("mlnode", "## ML Node\n",
     "Inference node stack (Python): model serving, PoC validation scripts, benchmarks, training experiments."),
    ("testermint", "## TesterMint\n",
     "Kotlin testing framework for the chain (consensus, PoC)."),
    ("common", "## Common libraries\n",
     "Shared Go libraries: chain, completionapi, logging, nodemanager, observability, queryapi, storage, utils, validation."),
    ("genesis", "## Genesis\n",
     "Mainnet genesis files and validator configs."),
    ("bridge", "## Bridge\n",
     "Ethereum bridge related code."),
    ("proxy", "## Proxy\n",
     "RPC/API proxy components."),
    ("proxy-ssl", "## Proxy SSL\n",
     "SSL/TLS proxy for nodes."),
    ("tmkms", "## tmkms\n",
     "TM KMS: remote key management / signing for validators."),
    ("edge-api", "## Edge API\n",
     "Edge API gateway components."),
    ("edge-api-router", "## Edge API Router\n",
     "Edge API routing components."),
    ("versioned", "## Versioned\n",
     "Versioned module/API handling."),
    ("versiond-router", "## versiond-router\n",
     "Versioned router."),
    ("deploy", "## Deploy\n",
     "Deployment scripts and configs."),
    ("local-test-net", "## Local Test Net\n",
     "Local testnet bootstrap scripts."),
    ("test-net-cloud", "## Test Net Cloud\n",
     "Cloud testnet deployment (k8s, devshard-testing)."),
    ("docs", "## Docs\n",
     "Additional design docs and papers (whitepaper, tokenomics)."),
    ("proposals", "## Design Docs (proposals/)\n",
     "Protocol design docs and governance artifacts — one dir per feature/upgrade. Great context for understanding why code works the way it does."),
]

# (path, title, description)
KEY_FILES = [
    ("inference-chain/app/app.go", "app.go", "Node wiring, module registration, ante handlers"),
    ("inference-chain/app/upgrades.go", "upgrades.go", "Upgrade registry (which versions are enabled)"),
    ("inference-chain/x/inference/permissions.go", "x/inference/permissions.go", "Permission model for inference"),
]


def url(path: str) -> str:
    return f"{SITE_URL}/gonka-code/{path}"


def is_hidden(rel_path: str) -> bool:
    parts = Path(rel_path).parts
    if any(part in HIDDEN_DIRS for part in parts[:-1]):
        return True
    return rel_path.lower().endswith(HIDDEN_FILE_SUFFIXES)


def list_dir(rel_dir: str) -> list[str]:
    """List source files in a mirror dir (excluding generated)."""
    lines = []
    root = CODE_DIR / rel_dir
    if not root.is_dir():
        return lines
    for p in sorted(root.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(CODE_DIR)
        rel_str = str(rel)
        if is_hidden(rel_str):
            continue
        lines.append(f"- `{rel_str}` → {url(rel_str)}")
    return lines


def main() -> None:
    if not CODE_DIR.is_dir():
        print(f"ERROR: {CODE_DIR} not found. Run sync-gonka-code.py first.", file=sys.stderr)
        sys.exit(1)

    parts = []
    parts.append("# Gonka Source Code Map\n")
    parts.append("> Mirrored from github.com/gonka-ai/gonka (main branch), synced hourly.")
    parts.append("> This file is an index. Raw source files are served under /gonka-code/.\n")
    parts.append("When answering questions about Gonka internals, use this map to find the relevant")
    parts.append("files, then fetch the raw source from the /gonka-code/ URLs below.\n")

    n_go = sum(1 for p in CODE_DIR.rglob("*") if p.is_file() and p.suffix in {".go", ".proto"})
    n_md = sum(1 for p in CODE_DIR.rglob("*") if p.is_file() and p.suffix == ".md")
    total = sum(1 for p in CODE_DIR.rglob("*") if p.is_file())
    parts.append(f"- Source files: {total} (Go/proto: {n_go}, markdown design docs: {n_md})\n")

    for root, heading, desc in MODULES:
        lines = list_dir(root)
        if not lines:
            continue
        parts.append(heading)
        parts.append(f"{desc}\n")
        parts.extend(lines)
        parts.append("")

    parts.append("## Key files\n")
    for rel, title, desc in KEY_FILES:
        if (CODE_DIR / rel).exists():
            parts.append(f"- **{title}**: {desc} — {url(rel)}")
    parts.append("")

    parts.append("## Bounty rewards\n")
    parts.append("On-chain bounty distributions live in `app/upgrades/v0_2_*/upgrades.go` as")
    parts.append("`bountyRewards` arrays (with recipient addresses, amounts, and PR references):\n")
    for p in sorted((CODE_DIR / "inference-chain/app/upgrades").rglob("upgrades.go")):
        rel = p.relative_to(CODE_DIR)
        parts.append(f"- `{rel}` → {url(str(rel))}")
    parts.append("")

    parts.append("## Design docs (proposals/)\n")
    parts.append("One README per feature. Fetch these for rationale before reading code:\n")
    for p in sorted((CODE_DIR / "proposals").glob("*")):
        if p.is_file() and p.suffix == ".md":
            rel = p.relative_to(CODE_DIR)
            parts.append(f"- `{rel}` → {url(str(rel))}")
        elif p.is_dir():
            for f in sorted(p.glob("*.md")):
                rel = f.relative_to(CODE_DIR)
                parts.append(f"- `{rel}` → {url(str(rel))}")
    parts.append("")

    output = "\n".join(parts)
    OUT.write_text(output, encoding="utf-8")
    print(f"Generated: {OUT} ({len(output)} bytes)", file=sys.stderr)


if __name__ == "__main__":
    main()
