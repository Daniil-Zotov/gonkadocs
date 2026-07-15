#!/usr/bin/env python3
"""
Gonka Docs MCP Server

Model Context Protocol server for gonkadocs.com.
AI agents (Cline, opencode, Claude, etc.) can connect to this server
to search and read Gonka documentation programmatically.

Usage:
    python3 buildtools/mcp-server.py                    # stdio mode (for Cline/opencode)
    python3 buildtools/mcp-server.py --transport sse    # SSE mode

Requires: pip install "mcp[cli]"
"""
import json
import os
import re
import sys
from pathlib import Path
from typing import Optional

from mcp.server.fastmcp import FastMCP

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SITE_URL = os.environ.get("GONKA_DOCS_URL", "https://gonkadocs.com")
DOCS_DIR = Path(os.environ.get("GONKA_DOCS_DIR", Path(__file__).resolve().parent.parent / "docs"))

mcp = FastMCP(
    "gonka-docs",
    instructions="""Gonka Docs MCP server provides access to all documentation
for the Gonka decentralized AI inference network.

Use these tools when the user asks about:
- Gonka protocol, architecture, or how it works
- Running a host/node or becoming a validator
- Using inference APIs (OpenAI-compatible)
- Governance proposals and voting
- Community roadmap and committees
- Cross-chain transfers (Ethereum bridge, IBC)
- Wallet management and pricing

Always start with search_gonka_docs to find relevant pages, then use
read_gonka_page to get full content.""",
)

# ---------------------------------------------------------------------------
# Index: load search data and page registry
# ---------------------------------------------------------------------------

_search_index: dict | None = None
_page_registry: list[dict] | None = None


def _load_search_index() -> dict:
    """Load the Lunr.js search index from the built site."""
    global _search_index
    if _search_index is not None:
        return _search_index

    # Try built site first, then docs dir
    candidates = [
        DOCS_DIR.parent / "_site" / "search" / "search_index.json",
        DOCS_DIR / "search" / "search_index.json",
    ]
    for path in candidates:
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                _search_index = json.load(f)
            return _search_index

    _search_index = {"docs": [], "config": {}}
    return _search_index


def _build_page_registry() -> list[dict]:
    """Build a flat registry of all known pages from search index + llms.txt."""
    global _page_registry
    if _page_registry is not None:
        return _page_registry

    _page_registry = []

    # From search index
    idx = _load_search_index()
    for doc in idx.get("docs", []):
        _page_registry.append({
            "title": doc.get("title", ""),
            "url": doc.get("location", ""),
            "text": doc.get("text", "")[:2000],
        })

    # If no search index, populate from llms.txt
    if not _page_registry:
        llms_path = DOCS_DIR / "llms.txt"
        if llms_path.exists():
            content = llms_path.read_text(encoding="utf-8")
            import re
            for match in re.finditer(r'\[([^\]]+)\]\(([^)]+)\)', content):
                title, url = match.group(1), match.group(2)
                if url.startswith("/") and not url.startswith("//"):
                    _page_registry.append({
                        "title": title,
                        "url": url,
                        "text": "",
                    })

    return _page_registry


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------

@mcp.tool()
def search_gonka_docs(query: str, max_results: int = 10) -> str:
    """Search Gonka documentation by keyword.

    Use this tool first when looking for information about Gonka.
    Returns matching pages with titles, URLs, and text snippets.

    Args:
        query: Search query (e.g. "proof of compute", "how to stake", "API")
        max_results: Maximum number of results to return (default 10)
    """
    idx = _load_search_index()
    docs = idx.get("docs", [])

    query_lower = query.lower()
    scored = []

    for doc in docs:
        title = doc.get("title", "").lower()
        text = doc.get("text", "").lower()
        location = doc.get("location", "").lower()

        score = 0
        # Title match is weighted higher
        if query_lower in title:
            score += 10
        elif any(w in title for w in query_lower.split()):
            score += 5

        # Text match
        if query_lower in text:
            score += 3
        elif any(w in text for w in query_lower.split()):
            score += 1

        # URL match
        if query_lower in location:
            score += 2

        if score > 0:
            scored.append((score, doc))

    scored.sort(key=lambda x: x[0], reverse=True)
    results = scored[:max_results]

    if not results:
        return f"No results found for '{query}'. Try different keywords."

    lines = [f"Found {len(results)} results for '{query}':\n"]
    for _, doc in results:
        title = doc.get("title", "Untitled")
        url = doc.get("location", "")
        text = doc.get("text", "")[:300].replace("\n", " ").strip()
        lines.append(f"### {title}")
        lines.append(f"URL: {SITE_URL}{url}")
        if text:
            lines.append(f"Snippet: {text}...")
        lines.append("")

    return "\n".join(lines)


@mcp.tool()
def read_gonka_page(url_path: str) -> str:
    """Read the full content of a Gonka documentation page.

    Args:
        url_path: Page path, e.g. "/gonka/docs/architecture/" or "architecture"
    """
    # Normalize path
    path = url_path.strip("/")
    if not path:
        path = "index"

    # Build the file path
    candidates = [
        DOCS_DIR / f"{path}.md",
        DOCS_DIR / path / "index.md",
    ]

    # Also try in gonka/docs/docs/ for upstream docs
    if path.startswith("gonka/docs/"):
        inner = path[len("gonka/docs/"):]
        candidates.append(DOCS_DIR / "gonka" / "docs" / "docs" / f"{inner}.md")
        candidates.append(DOCS_DIR / "gonka" / "docs" / "docs" / inner / "index.md")

    for candidate in candidates:
        if candidate.exists() and candidate.is_file():
            content = candidate.read_text(encoding="utf-8")
            # Strip frontmatter
            import re
            content = re.sub(r'^---\n.*?\n---\n', '', content, count=1, flags=re.DOTALL)
            # Truncate if too long
            if len(content) > 50000:
                content = content[:50000] + "\n\n[... truncated, full content at " + SITE_URL + "/" + path + "/]"
            return f"# {path}\n\nSource: {SITE_URL}/{path}/\n\n{content}"

    return f"Page not found: {url_path}. Use search_gonka_docs to find the correct path or check /proposals/ for on-chain proposals and pre-proposals."


@mcp.tool()
def list_gonka_sections() -> str:
    """List all major sections of Gonka documentation with descriptions."""
    return """# Gonka Docs Sections

## Protocol Documentation (/gonka/docs/)
Official technical documentation for the Gonka protocol.
- Architecture — Inference flow, Proof of Compute, epoch mechanics
- Developer Quickstart — Send inference via brokers (OpenAI-compatible API)
- Gateway Quickstart — Run your own gateway (Docker)
- Host Quickstart — Join as GPU provider
- Host Hardware Specs — GPU/CPU/RAM requirements
- Host Key Management — Validator/consensus/node keys
- Host Collateral — Staking, slashing
- Host Validation — PoC validation mechanics
- ML Node Management — Deploy inference nodes
- Wallet — Create account, dashboard, pricing
- Cross-Chain — Ethereum bridge (USDT/GNK), IBC via Kava
- Governance — Transactions, voting power, proposals
- Model Licenses — Supported models

## GitHub Discussions (/community/discussion/)
71 discussions from gonka-ai/gonka repository.
- Proposals (42) — Technical and funding proposals
- Show and Tell (20) — Community projects
- Q&A (3) — Best practices, technical questions
- General (5) — Network reliability, governance
- Announcements (1) — Welcome post

## Community (/community/)
Community governance and planning documents.
- Roadmap — Three-horizon development strategy
- GRC — Restitution Committee (compensation framework)
- GSC — Self-Governance Committee (charter)

## On-Chain Proposals (/proposals/)
Full table of governance proposals with statuses and summaries, plus pre-proposals (community grant requests and polls).

## Machine-Readable
- /llms.txt — AI agent entry point
- /llms-full.txt — All docs in one file (392 KB)
- /openapi.yaml — OpenAPI 3.0 spec for inference API
- /search/search_index.json — Search index (queryable)
- /sitemap.xml — Full sitemap
"""


@mcp.tool()
def read_gonka_llms_full(max_chars: int = 100000) -> str:
    """Read the full consolidated documentation file (llms-full.txt).

    Contains all protocol, community, and governance docs in a single file.
    Best for getting comprehensive context about Gonka.

    Args:
        max_chars: Maximum characters to return (default 100000, full file is ~392KB)
    """
    llms_full = DOCS_DIR / "llms-full.txt"
    if llms_full.exists():
        content = llms_full.read_text(encoding="utf-8")
        if len(content) > max_chars:
            content = content[:max_chars] + f"\n\n[... truncated, full file at {SITE_URL}/llms-full.txt]"
        return content
    return f"llms-full.txt not found. Generate it with: python3 buildtools/generate-llms-full.py"


@mcp.tool()
def read_gonka_proposal(proposal_id: str) -> str:
    """Read details of a specific on-chain governance proposal.

    Args:
        proposal_id: Proposal number (e.g. "74", "57", "44")
    """
    proposals_root = DOCS_DIR / "proposals" / "proposals"
    if not proposals_root.exists():
        return "Proposals directory not found."

    # Scan quarter directories for the proposal
    for quarter_dir in sorted(proposals_root.iterdir()):
        if not quarter_dir.is_dir() or not quarter_dir.name.startswith("20"):
            continue
        prop_dir = quarter_dir / proposal_id
        if prop_dir.is_dir():
            index_md = prop_dir / "index.md"
            if index_md.exists():
                content = index_md.read_text(encoding="utf-8")
                content = re.sub(r'^---\n.*?\n---\n', '', content, count=1, flags=re.DOTALL)
                if len(content) > 50000:
                    content = content[:50000] + "\n\n[... truncated]"
                return f"# Proposal #{proposal_id}\n\nSource: {SITE_URL}/proposals/proposals/{quarter_dir.name}/{proposal_id}/\n\n{content}"
            return f"Proposal #{proposal_id} found but has no content."

    return f"Proposal #{proposal_id} not found. See {SITE_URL}/proposals/ for available proposals."


# ---------------------------------------------------------------------------
# Resources (optional, for agents that support MCP resources)
# ---------------------------------------------------------------------------

@mcp.resource("gonka://docs/llms.txt")
def get_llms_txt() -> str:
    """Return the raw llms.txt file content."""
    llms_path = DOCS_DIR / "llms.txt"
    if llms_path.exists():
        return llms_path.read_text(encoding="utf-8")
    return "llms.txt not found"


@mcp.resource("gonka://docs/sitemap")
def get_sitemap() -> str:
    """Return the sitemap.xml content."""
    sitemap_path = DOCS_DIR.parent / "_site" / "sitemap.xml"
    if sitemap_path.exists():
        return sitemap_path.read_text(encoding="utf-8")
    return "sitemap.xml not found (run build first)"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Gonka Docs MCP Server")
    parser.add_argument("--transport", choices=["stdio", "sse"], default="stdio",
                        help="Transport mode (default: stdio)")
    args = parser.parse_args()

    if args.transport == "sse":
        mcp.run(transport="sse")
    else:
        mcp.run(transport="stdio")
