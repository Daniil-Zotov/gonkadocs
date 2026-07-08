---
title: For AI Agents
description: How AI agents discover and use Gonka documentation
hide:
  - navigation
---

<style>
.agents-wrap{max-width:820px;margin:0 auto;padding:2.5rem 2rem 4rem}
.agents-title{font-size:2rem;font-weight:700;margin:0 0 0.5rem;letter-spacing:-0.02em}
.agents-lead{color:var(--md-default-fg-color--light);font-size:1.05rem;line-height:1.6;margin:0 0 2.5rem}
.agents-lead a{color:var(--md-accent-fg-color);text-decoration:underline}
.agents-section{margin-bottom:2.5rem}
.agents-section h2{font-size:1.25rem;font-weight:600;margin:0 0 0.75rem;color:var(--md-default-fg-color);letter-spacing:-0.01em}
.agents-section h3{font-size:1.05rem;font-weight:600;margin:1.5rem 0 0.5rem;color:var(--md-default-fg-color)}
.agents-section p,.agents-section li{font-size:0.95rem;line-height:1.65;color:var(--md-default-fg-color)}
.agents-section ul{padding-left:1.25rem;margin:0.5rem 0}
.agents-section li{margin-bottom:0.35rem}
.agents-pre{background:var(--md-code-bg-color);border:1px solid var(--md-default-fg-color--lightest);border-radius:8px;padding:1rem 1.25rem;font-family:var(--md-code-font-family);font-size:0.85rem;line-height:1.55;color:var(--md-default-fg-color);overflow-x:auto;margin:0.75rem 0 1rem;white-space:pre-wrap;word-break:break-all}
.agents-pre .hl-comment{color:var(--md-default-fg-color--light)}
.agents-pre .hl-key{color:var(--md-accent-fg-color)}
.agents-pre .hl-url{color:var(--md-accent-fg-color)}
.agents-note{background:rgba(9,105,218,0.06);border:1px solid rgba(9,105,218,0.18);border-radius:8px;padding:0.85rem 1.1rem;font-size:0.9rem;line-height:1.55;color:var(--md-default-fg-color);margin:1rem 0}
.agents-note strong{color:var(--md-accent-fg-color)}
.agents-example{background:var(--md-code-bg-color);border:1px solid var(--md-default-fg-color--lightest);border-radius:8px;padding:1.1rem 1.25rem;margin:1rem 0}
.agents-example-q{color:var(--md-default-fg-color--light);font-size:0.85rem;margin:0 0 0.35rem;font-style:italic}
.agents-example-a{font-size:0.9rem;color:var(--md-default-fg-color);line-height:1.55;margin:0}
.agents-example-a code{font-family:var(--md-code-font-family);background:var(--md-code-bg-color);padding:0.15em 0.35em;border-radius:3px;font-size:0.82rem}
.agents-links{display:flex;flex-wrap:wrap;gap:0.75rem;margin:1.5rem 0}
.agents-link{display:inline-flex;align-items:center;gap:0.4rem;background:var(--md-code-bg-color);border:1px solid var(--md-default-fg-color--lightest);border-radius:6px;padding:0.55rem 1rem;font-family:var(--md-code-font-family);font-size:0.82rem;color:var(--md-default-fg-color);transition:border-color 0.15s;text-decoration:none}
.agents-link:hover{border-color:var(--md-accent-fg-color);color:var(--md-default-fg-color)}
.agents-link-dot{width:8px;height:8px;border-radius:50%;flex-shrink:0}
.agents-divider{border:none;border-top:1px solid var(--md-default-fg-color--lightest);margin:2.5rem 0}
</style>

# For AI Agents

**Gonka Docs** is designed as a single source of truth for AI agents. Your coding assistant, custom GPT, or autonomous agent can discover and use all documentation without you copying content by hand.

---

## Machine-readable discovery files

We serve standard `llms.txt` files that AI agents check automatically when they need to understand a service.

<div class="agents-links">
  <a href="/llms.txt" class="agents-link" target="_blank">
    <span class="agents-link-dot" style="background:var(--md-accent-fg-color)"></span>
    /llms.txt — Quick overview
  </a>
  <a href="/llms-full.txt" class="agents-link" target="_blank">
    <span class="agents-link-dot" style="background:#7b8aff"></span>
    /llms-full.txt — Full documentation
  </a>
  <a href="/openapi.yaml" class="agents-link" target="_blank">
    <span class="agents-link-dot" style="background:#8250df"></span>
    /openapi.yaml — OpenAPI 3.0 spec
  </a>
  <a href="/sitemap.xml" class="agents-link" target="_blank">
    <span class="agents-link-dot" style="background:#1a7f37"></span>
    /sitemap.xml — Sitemap
  </a>
</div>

---

## Cursor / Windsurf / Cline

Add this to your project's rules file (`.cursorrules`, `.windsurfrules`, or `AGENTS.md`):

```
# Gonka Documentation

When working with Gonka (decentralized AI inference network), use these resources:
- Quick overview: https://gonkadocs.com/llms.txt
- Full docs: https://gonkadocs.com/llms-full.txt
- API spec: https://gonkadocs.com/openapi.yaml

Key sections:
  /gonka/docs/           → Protocol documentation (architecture, quickstart, wallet)
  /community/            → Roadmap, Gonka Product Committee, GSC
  /community/discussion/ → GitHub Discussions (proposals, Q&A, show-and-tell)
  /community/issues/     → GitHub Issues (bugs, features, enhancements)
  /proposals/proposals/  → On-chain governance proposals by quarter with funding amounts and source (Community Pool / Gov Module)
  /proposals/preproposals/ → Community pre-proposals (off-chain indicative polls)

Fetch /llms-full.txt for complete documentation before writing code.
```

<div class="agents-note">
  <strong>Tip:</strong> With this rule in place, you can just say "explain Gonka architecture" or "how to run a node" — the agent will know where to find the information.
</div>

---

## MCP Server

For AI agents that support MCP (Model Context Protocol), we provide a server with tools:

```json
{
  "mcpServers": {
    "gonka-docs": {
      "command": "python3",
      "args": ["buildtools/mcp-server.py"]
    }
  }
}
```

Available tools:
- `search_gonka_docs(query)` — search across all documentation
- `read_gonka_page(url)` — read a specific documentation page
- `list_gonka_sections()` — list all available sections
- `read_gonka_llms_full()` — get the full documentation context
- `read_gonka_proposal(id)` — read a governance proposal

---

## Custom GPTs / OpenAI Assistants

Add this to the system prompt of your GPT or Assistant:

```
# System prompt addition:

You can access Gonka documentation via gonkadocs.com.
To discover information, fetch:
  https://gonkadocs.com/llms.txt (quick overview)
  https://gonkadocs.com/llms-full.txt (complete docs)

Key topics:
- Architecture: Proof of Compute consensus, inference flows, epochs
- Developer: OpenAI-compatible API, inference via brokers
- Host: GPU resource connection, node management
- Wallet: Accounts, collateral, cross-chain (USDT/GNK)
- Governance: Proposals, voting, GRC, GSC
- On-Chain Proposals: /proposals/proposals/ — quarterly overviews with status, funding amounts, and source (Community Pool / Gov Module)
- Pre-Proposals: /proposals/preproposals/ — community grant requests and polls
- Issues: Bugs, feature requests, enhancements from gonka-ai/gonka
```

---

## Autonomous agents

For fully autonomous agents (LangChain, AutoGPT, custom bots), the recommended flow is:

1. Fetch `https://gonkadocs.com/llms.txt` for quick context (project overview, key concepts)
2. If more detail is needed, fetch `https://gonkadocs.com/llms-full.txt` for complete documentation
3. For proposals: fetch `/proposals/proposals/` for the overview page, then drill into a specific quarter (e.g., `/proposals/proposals/2026-q2/`) and individual proposal pages (e.g., `/proposals/proposals/2026-q2/74/`) — each page includes funding amounts with source labels
4. Or use the MCP server for structured access with tools

```python
# Example: Python agent discovering Gonka docs
import requests

# 1. Get quick overview
overview = requests.get("https://gonkadocs.com/llms.txt").text
print(overview[:500])

# 2. Search for specific topic
# Use the search index to find relevant pages
search_index = requests.get("https://gonkadocs.com/search/search_index.json").json()

# 3. Find docs about architecture
for doc in search_index["docs"]:
    if "architecture" in doc.get("location", "").lower():
        print(f"Found: {doc['location']}")
```

---

## What your agent can do

- **Understand the protocol** — architecture, Proof of Compute, inference flows, epochs
- **Get started quickly** — developer quickstart, gateway setup, host GPU resources
- **Manage wallets** — accounts, collateral, cross-chain bridges (USDT/GNK via Ethereum/IBC)
- **Participate in governance** — read and submit proposals, vote, understand Gonka Product Committee / GSC
- **Track on-chain funding** — each proposal shows the funding amount and source (`Community Pool` or `Gov Module`), organized by quarter with per-quarter summaries and totals
- **Explore community** — discussions, show-and-tell projects, Q&A, roadmap
- **Use the API** — OpenAI-compatible inference endpoint, node management APIs

---

## Example conversations

<div class="agents-example">
  <p class="agents-example-q">User: "Explain Gonka architecture"</p>
  <p class="agents-example-a">
    Agent fetches <code>/llms.txt</code>, finds the Architecture section, then reads
    <code>/gonka/docs/architecture/</code> for detailed explanation of Proof of Compute
    consensus and inference flows.
  </p>
</div>

<div class="agents-example">
  <p class="agents-example-q">User: "How do I run a Gonka node?"</p>
  <p class="agents-example-a">
    Agent fetches <code>/llms-full.txt</code>, locates the Host Quickstart section,
    and provides step-by-step instructions for connecting GPU resources.
  </p>
</div>

<div class="agents-example">
  <p class="agents-example-q">User: "What governance proposals are active?"</p>
  <p class="agents-example-a">
    Agent fetches <code>/proposals/proposals/</code> page, identifies active proposals
    by status badge, and lists them with their descriptions, tally results, and
    funding amounts with sources (<code>Community Pool</code> / <code>Gov Module</code>).
  </p>
</div>

<div class="agents-example">
  <p class="agents-example-q">User: "How much funding has been approved this quarter and where does it come from?"</p>
  <p class="agents-example-a">
    Agent fetches <code>/proposals/proposals/</code>, reads the current quarter's summary
    section which includes the total approved GNK/USDT broken down by funding source
    (<code>Community Pool</code> and <code>Gov Module</code>).
  </p>
</div>

<div class="agents-example">
  <p class="agents-example-q">User: "How do I call the inference API?"</p>
  <p class="agents-example-a">
    Agent fetches <code>/openapi.yaml</code> for the API spec, then provides
    code examples for calling the OpenAI-compatible <code>/v1/chat/completions</code> endpoint.
  </p>
</div>

<div class="agents-example">
  <p class="agents-example-q">User: "What's the roadmap for Gonka?"</p>
  <p class="agents-example-a">
    Agent fetches <code>/community/roadmap/</code> and summarizes the three-horizon
    development strategy.
  </p>
</div>

<div class="agents-example">
  <p class="agents-example-q">User: "What open issues exist for the Gonka project?"</p>
  <p class="agents-example-a">
    Agent fetches <code>/community/issues/</code> and lists recent open issues with
    their titles, labels, and authors from the gonka-ai/gonka repository.
  </p>
</div>

---

<p style="text-align:center;color:var(--md-default-fg-color--light);font-size:0.9rem">
  Full documentation: <a href="/llms-full.txt" style="color:var(--md-accent-fg-color);text-decoration:underline">llms-full.txt</a>
  &nbsp;·&nbsp;
  API spec: <a href="/openapi.yaml" style="color:var(--md-accent-fg-color);text-decoration:underline">openapi.yaml</a>
  &nbsp;·&nbsp;
  GitHub: <a href="https://github.com/Daniil-Zotov/gonkadocs" style="color:var(--md-accent-fg-color);text-decoration:underline">Daniil-Zotov/gonkadocs</a>
</p>
