#!/usr/bin/env python3
"""
Generate llms.txt — AI agent entry point for gonkadocs.com.

Dynamically scans the docs directory to build an up-to-date index
of all documentation sections and pages.

Usage:
    python3 buildtools/generate-llms.py

Output:
    docs/llms.txt  (included in MkDocs build -> _site/llms.txt)
"""
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
SITE_URL = os.environ.get("GONKA_SITE_URL", "https://gonkadocs.com").rstrip("/")

# Section scan configurations
# (scan_dir, section_heading, url_prefix, description)
SECTIONS = [
    {
        "dir": "gonka/docs/docs",
        "heading": "## Protocol Documentation",
        "url_prefix": "/gonka/docs/",
        "desc": "Official protocol documentation (auto-synced from gonka-ai/gonka-docs)",
        "entries": [
            ("introduction.md", "Introduction", "What Gonka is, roles (Developers, Hosts)"),
            ("architecture.md", "Architecture", "Inference flow diagrams, Proof of Compute, epoch mechanics"),
        ],
        "subdirs": [
            ("developer", "Developer", {
                "quickstart.md": ("Developer Quickstart", "Send inference via brokers, OpenAI-compatible API, tool calling"),
                "gateway-developer-quickstart.md": ("Gateway Developer Quickstart", "Run your own gateway (Docker), devshard escrow"),
            }),
            ("host", "Host", {
                "quickstart.md": ("Host Quickstart", "Join as GPU provider, hardware requirements"),
                "hardware-specifications.md": ("Hardware Specifications", "GPU/CPU/RAM requirements per model"),
                "key-management.md": ("Key Management", "Validator, consensus, and node keys"),
                "collateral.md": ("Collateral", "Staking, slashing, collateral parameters"),
                "mlnode-validation.md": ("ML Node Validation", "PoC validation mechanics, sprint execution"),
                "mlnode-management.md": ("ML Node Management", "Deploy and manage inference nodes"),
                "multi_model_poc.md": ("Multi-Model PoC", "Run multiple models on one host"),
                "network-node-api.md": ("Network Node API", "Chain node and API node endpoints"),
                "rewards.md": ("Rewards", "Epoch rewards distribution"),
            }),
            ("wallet", "Wallet", {
                "create-account.md": ("Create Account", "Create a Gonka account on-chain"),
                "dashboard.md": ("Dashboard", "Web dashboard for account management"),
                "pricing.md": ("Pricing", "Per-token pricing, settlement mechanics"),
            }),
            ("governance", "Governance", {
                "transactions-and-governance.md": ("Transactions & Governance", "Submit proposals, vote"),
                "voting-power-eligibility.md": ("Voting Power", "How voting power is calculated"),
                "creating-proposals.md": ("Creating Proposals", "How to create governance proposals"),
                "voting-on-proposals.md": ("Voting on Proposals", "How to vote on proposals"),
            }),
            ("cross-chain-transfers", "Cross-Chain", {
                "ethereum-bridge/deposit-usdt.md": ("Deposit USDT (Ethereum)", "Deposit USDT via Ethereum bridge"),
                "ethereum-bridge/withdraw-usdt.md": ("Withdraw USDT (Ethereum)", "Withdraw USDT via Ethereum bridge"),
                "ethereum-bridge/deposit-gnk.md": ("Deposit GNK (Ethereum)", "Deposit GNK via Ethereum bridge"),
                "ethereum-bridge/withdraw-gnk.md": ("Withdraw GNK (Ethereum)", "Withdraw GNK via Ethereum bridge"),
                "ibc/withdraw-usdt-via-kava.md": ("IBC USDT via Kava", "Transfer USDT via IBC through Kava"),
                "widget-integration.md": ("Widget Integration", "Cross-chain widget for websites"),
            }),
        ],
        "entries": [
            ("model-licenses.md", "Model Licenses", "Supported models and licensing terms"),
            ("errors.md", "Error Reference", "Common errors and troubleshooting"),
        ],
    },
    {
        "dir": "community",
        "heading": "## Community Documentation",
        "url_prefix": "/community/",
        "desc": "Community governance and planning",
        "entries": [
            ("roadmap/gonka-network-development-roadmap.md", "Roadmap", "Three-horizon development strategy"),
            ("grc/README.md", "GRC (Restitution Committee)", "Compensation framework for protocol bugs"),
            ("gsc/regulation.md", "GSC (Self-Governance Committee)", "Community governance charter"),
        ],
    },
    {
        "dir": "proposals",
        "heading": "## On-Chain Proposals",
        "url_prefix": "/proposals/",
        "desc": "Governance proposals dashboard",
        "entries": [
            ("README.md", "Proposals Dashboard", "Full table of on-chain governance proposals"),
        ],
    },
    {
        "dir": "proposals/preproposals",
        "heading": "## Pre-Proposals (auto-synced)",
        "url_prefix": "/proposals/preproposals/",
        "desc": "Community proposals from gonka.vote — off-chain indicative polls",
        "entries": [
            ("index.md", "Pre-Proposals Overview", "Active and expired community proposals with vote tallies and comments"),
        ],
    },
    {
        "dir": "docs",
        "heading": "## AI Agent Resources",
        "url_prefix": "/",
        "desc": "Machine-readable files and setup guides for AI agents",
        "entries": [
            ("agents.md", "For AI Agents", "How AI agents discover and use Gonka documentation — llms.txt, MCP server, setup guides"),
        ],
    },
]


# Directories whose individual pages should NOT be auto-discovered
# (they are already represented by overview/index links)
SKIP_SUBDIRS = {
    "community/issues",
    "community/discussion",
    "gonka/docs/docs/zh",
    "gonka/docs/docs/participant",
    "proposals/preproposals",  # Already covered by explicit entries
}


def find_extra_pages(section_dir: str, known_files: set) -> list[tuple[str, str, str]]:
    """Find any .md files in a directory that aren't in the known_files set.
    Returns list of (rel_path, title, auto_description)."""
    scan_path = DOCS / section_dir
    if not scan_path.exists():
        return []

    extra = []
    for root, dirs, files in os.walk(scan_path):
        for fn in sorted(files):
            if not fn.endswith(".md"):
                continue
            abs_path = Path(root) / fn
            rel_path = str(abs_path.relative_to(DOCS))

            if rel_path in known_files:
                continue

            # Skip index/README at section root
            if fn in ("README.md", "CNAME", ".gitignore"):
                continue
            if rel_path.startswith(".") or "images/" in rel_path:
                continue

            # Skip auto-sync subdirs (duplicates, translations, too granular)
            skip = False
            for skip_prefix in SKIP_SUBDIRS:
                if rel_path.startswith(skip_prefix):
                    skip = True
                    break
            if skip:
                continue

            # Extract title from file
            content = abs_path.read_text(encoding="utf-8", errors="replace")
            title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            title = title_match.group(1).strip() if title_match else fn.replace(".md", "").replace("-", " ").title()
            extra.append((rel_path, title, "Auto-synced content"))

    return extra


def build_section_entries(section: dict) -> list[str]:
    """Build markdown lines for a section."""
    lines = []
    lines.append(section["heading"])
    lines.append("")

    url_prefix = section["url_prefix"]
    known_files = set()

    # Static entries
    for entry in section.get("entries", []):
        if isinstance(entry, tuple) and len(entry) == 3:
            # Simple entry: (filename, title, description)
            filename, title, desc = entry
            url = f"{url_prefix}{filename.replace('.md', '/')}"
            if filename.endswith("index.md"):
                url = f"{url_prefix}"
            lines.append(f"- [{title}]({url}): {desc}")
            known_files.add(f"{section['dir']}/{filename}")

    # Subdirectory entries
    for subdir_entry in section.get("subdirs", []):
        if len(subdir_entry) == 3:
            subdir, subdir_title, files = subdir_entry
            lines.append(f"\n### {subdir_title}\n")
            for filename, (title, desc) in files.items():
                # Build URL
                if filename.endswith("index.md"):
                    url = f"{url_prefix}{subdir}/"
                else:
                    url = f"{url_prefix}{subdir}/{filename.replace('.md', '/')}"
                lines.append(f"- [{title}]({url}): {desc}")
                known_files.add(f"{section['dir']}/{subdir}/{filename}")

    # Auto-discover any remaining .md files not in the known set
    extra = find_extra_pages(section["dir"], known_files)
    if extra:
        lines.append(f"\n### Additional Pages (auto-synced)\n")
        for rel_path, title, desc in extra:
            # Convert file path to URL
            url_path = rel_path.replace(".md", "/").replace("index/", "")
            lines.append(f"- [{title}]({url_prefix}{url_path[len(section['dir'])+1:]}): {desc}")

    return lines


def main():
    parts = []
    parts.append("# Gonka Docs\n")
    parts.append(f"> Gonka is a decentralized AI inference network with Proof of Compute consensus. This portal unifies official protocol documentation, GitHub Discussions, community governance docs, and on-chain proposals into a single searchable site at gonkadocs.com.\n")
    parts.append("Key facts: Gonka uses Proof of Compute (PoC) consensus where ~100% of compute goes to useful LLM inference. Hosts contribute GPU resources and earn GNK tokens. Developers access inference through OpenAI-compatible APIs via community brokers or self-hosted gateways. The network runs epochs (~24h) with on-chain governance.\n")

    # GitHub discussions section (always included)
    parts.append("## GitHub Discussions (auto-synced)")
    parts.append("")
    parts.append("- [All Discussions](/community/discussion/): Index of all discussions from gonka-ai/gonka")
    parts.append("- [Proposals](/community/discussion/proposals/): Technical and funding proposals")
    parts.append("- [Show and Tell](/community/discussion/show-and-tell/): Community projects")
    parts.append("- [Q&A](/community/discussion/q-a/): Best practices, technical questions")
    parts.append("- [General](/community/discussion/general/): Network reliability, governance")
    parts.append("")

    # GitHub issues section (always included)
    parts.append("## GitHub Issues (auto-synced)")
    parts.append("")
    parts.append("- [All Issues](/community/issues/): Index of all issues from gonka-ai/gonka")
    parts.append("- [By Label](/community/issues/labels/): Issues grouped by label")
    parts.append("")

    # Dynamic sections
    for section in SECTIONS:
        entries = build_section_entries(section)
        parts.extend(entries)
        parts.append("")

    # Machine-readable resources
    parts.append("## Machine-Readable Resources")
    parts.append("")
    parts.append("- [Full Documentation](/llms-full.txt): All pages combined in a single file")
    parts.append("- [OpenAPI Specification](/openapi.yaml): OpenAPI 3.0 spec for the inference API")
    parts.append("- [Search Index](/search/search_index.json): Lunr.js search index, queryable programmatically")
    parts.append("- [Sitemap](/sitemap.xml): Full sitemap of all pages")
    parts.append("")

    # Key concepts
    parts.append("## Key Concepts")
    parts.append("")
    parts.append("- **Proof of Compute (PoC)**: Novel consensus where compute time is used for useful LLM inference, not wasteful hashing. Sprints are short proof windows; rest of epoch is productive inference.")
    parts.append("- **Epochs**: ~24 hour cycles (17280 blocks). Each epoch: Sprint -> weight assignment -> inference work -> reward settlement.")
    parts.append("- **Devshards**: Short-lived sessions with on-chain escrow for per-request billing. Gateways open devshards; brokers resell access.")
    parts.append("- **Transfer Agent (TA)**: Randomly selected host that routes inference requests. Any host can be TA, Validator, or Executor.")
    parts.append("- **GNK Token**: Native token. Hosts earn GNK for providing compute. Used for staking, governance, and payments.")
    parts.append("- **OpenAI-Compatible API**: Gonka inference is accessible via standard `/v1/chat/completions` endpoint through brokers.")

    output = "\n".join(parts)

    out_path = DOCS / "llms.txt"
    out_path.write_text(output, encoding="utf-8")
    print(f"Generated: {out_path} ({len(output)} bytes)", file=sys.stderr)


if __name__ == "__main__":
    main()
