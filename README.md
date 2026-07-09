# gonkadocs.com

Unified documentation portal for [Gonka](https://gonka.ai) — a decentralized AI inference network with Proof of Compute consensus.

**URL:** [gonkadocs.com](https://gonkadocs.com)

---

## Portal Structure

### Protocol Documentation (`/gonka/docs/`)
Auto-synced from [gonka-ai/gonka-docs](https://github.com/gonka-ai/gonka-docs) every hour.

- **Architecture** — inference flows, Proof of Compute, epochs
- **Developer Quickstart** — inference via brokers (OpenAI-compatible API)
- **Gateway Quickstart** — custom gateway (Docker)
- **Host Quickstart** — GPU resource connection
- **Wallet** — accounts, dashboard, pricing
- **Cross-Chain** — Ethereum bridge (USDT/GNK), IBC via Kava
- **Governance** — voting, proposals, transactions
- Languages: English, 中文

### GitHub Discussions (`/community/discussion/`)
Auto-synced from [gonka-ai/gonka](https://github.com/gonka-ai/gonka/discussions) every hour.

- **Proposals** — technical and funding proposals
- **Show and Tell** — community projects
- **Q&A** — best practices, technical questions
- **General** — network reliability, governance

### GitHub Issues (`/community/issues/`)
Auto-synced from [gonka-ai/gonka](https://github.com/gonka-ai/gonka/issues) every hour.

- Full issue tracker with labels, status filters, and comments
- Label-based navigation

### On-Chain Proposals (`/proposals/proposals/`)
Auto-synced from [rpc.gonka.gg](https://rpc.gonka.gg) every hour. Proposals are organized by quarter:

- **Quarterly overviews** — per-quarter summaries with pass/reject/fail rates, category breakdowns, and approved funding totals by source
- **Individual proposal pages** — detailed view with status, tally results, funding amount and source (Community Pool / Gov Module), and on-chain contract messages
- **Funding source tracking** — each proposal shows where funding originates: `Community Pool` (community pool spend, execute contract) or `Gov Module` (batch vesting, multi-send)
- **Status filters** — filter by Passed / Rejected / Voting
- **Tally results** — Yes/No/Veto/Abstain counts and percentages on every card

### Pre-Proposals (`/proposals/preproposals/`)
Auto-synced from [gonka.vote](https://gonka.vote) every hour.

- Community proposals with vote tallies and comments
- Active and expired proposal tracking

### Community (`/community/`)
- **Roadmap** — three-horizon development strategy
- **GRC** — restitution committee (bug compensation) at `/community/gonka restitution committee/`
- **GSC** — governance support committee at `/community/governance support committee/`

---

## AI Integration

Portal designed as a single source of truth for AI agents.

### Standard Files

| URL | Description |
|-----|-------------|
| [`/llms.txt`](https://gonkadocs.com/llms.txt) | AI entry point: project overview, section links, key concepts |
| [`/llms-full.txt`](https://gonkadocs.com/llms-full.txt) | All docs in one file (~392 KB), optimized for context window |
| [`/robots.txt`](https://gonkadocs.com/robots.txt) | Permissions for AI crawlers (GPTBot, ClaudeBot, PerplexityBot, Google-Extended, etc.) |
| [`/openapi.yaml`](https://gonkadocs.com/openapi.yaml) | OpenAPI 3.0 specification for inference API |
| [`/sitemap.xml`](https://gonkadocs.com/sitemap.xml) | Full sitemap (main + gonka/docs merged) |
| [`/gonka/docs/zh/sitemap.xml`](https://gonkadocs.com/gonka/docs/zh/sitemap.xml) | Chinese-language sitemap for gonka docs |
| [`/search/search_index.json`](https://gonkadocs.com/search/search_index.json) | Lunr.js search index, queryable programmatically |
| [`/proposals/proposals/proposals.xml`](https://gonkadocs.com/proposals/proposals/proposals.xml) | RSS feed for on-chain governance proposals |
| [`/humans.txt`](https://gonkadocs.com/humans.txt) | Credits and team info |
| [`/.well-known/security.txt`](https://gonkadocs.com/.well-known/security.txt) | Security policy for responsible disclosure |
| [`/manifest.json`](https://gonkadocs.com/manifest.json) | PWA manifest |

### MCP Server

Available for AI agents (Cline, opencode, Claude):

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

Tools:
- `search_gonka_docs(query)` — search documentation
- `read_gonka_page(url)` — read specific page
- `list_gonka_sections()` — list all sections
- `read_gonka_llms_full()` — full context
- `read_gonka_proposal(id)` — read governance proposal

### Page-MD Versions

Each page available as markdown via `.html.md` URL:
```
/gonka/docs/architecture/index.html  →  /gonka/docs/architecture/index.html.md
```

---

## Build Architecture

Site consists of two independent MkDocs builds merged into `_site/`:

```
buildtools/build.sh
    │
    ├──► [0] generate-llms.py + generate-llms-full.py
    │       Dynamic scanning of docs/ → llms.txt + llms-full.txt
    │
    ├──► [1] mkdocs build (main site)
    │       Homepage + Community + Proposals
    │
    ├──► [2] mkdocs build (Gonka section)
    │       Original mkdocs.yml from gonka-ai/gonka-docs
    │       i18n: en + zh, custom overrides
    │
    ├──► [3] Post-processing: fix image paths
    │       /images/ → relative paths per page depth
    │
    ├──► [4] Merge search indexes
    │       Main + gonka/docs → unified search index
    │
    ├──► [5] Generate .html.md page copies
    │       For AI agents (llms.txt standard)
    │
    ├──► [5.5] Generate zh/sitemap.xml
    │       Filter gonka URLs containing /zh/
    │
    ├──► [6] Merge sitemaps
    │       Main + gonka/docs → unified sitemap.xml
    │
    └──► [7] Copy service files
            robots.txt, llms.txt, llms-full.txt, openapi.yaml → _site/
```

---

## Auto-Sync

6 GitHub Actions workflows automatically update content:

| Workflow | Source | Syncs | Triggers Deploy |
|----------|--------|-------|:---:|
| `sync-gonka-ai-docs.yml` | gonka-ai/gonka-docs | Protocol documentation | via push |
| `sync-onchain-proposals.yml` | rpc.gonka.gg | On-chain governance proposals | via API |
| `sync-discussions.yml` | gonka-ai/gonka (GraphQL) | GitHub Discussions | via push |
| `sync-issues.yml` | gonka-ai/gonka (REST) | GitHub Issues | via push |
| `sync-preproposals.yml` | gonka.vote (REST) | Pre-Proposals | via push |

Every sync triggers the `deploy-docs.yml` workflow, which regenerates `llms.txt` and `llms-full.txt` and deploys the updated site to GitHub Pages.

---

## Local Development

```bash
# Install dependencies
pip install mkdocs mkdocs-material pymdown-extensions

# Build site
bash buildtools/build.sh

# Local preview
bash buildtools/serve.sh
```

---

## Repository Structure

```
gonkadocs/
├── mkdocs.yml                    # MkDocs config (main site)
├── buildtools/
│   ├── build.sh                  # Build script
│   ├── serve.sh                  # Local server
│   ├── generate-llms.py          # Generate llms.txt
│   ├── generate-llms-full.py     # Generate llms-full.txt
│   ├── generate-page-md.py       # Generate .html.md copies
│   ├── mcp-server.py             # MCP server for AI agents
│   └── gonka-overrides/          # Shared header for Gonka section
├── docs/
│   ├── llms.txt                  # AI entry point
│   ├── llms-full.txt             # Full documentation
│   ├── robots.txt                # AI crawler permissions
│   ├── openapi.yaml              # API specification
│   ├── index.md                  # Homepage
│   ├── 404.md                    # Custom 404 page
│   ├── manifest.json             # PWA manifest
│   ├── humans.txt                # Credits
│   ├── agents.md                 # AI agent setup guide
│   ├── .well-known/
│   │   └── security.txt          # Security policy
│   ├── overrides/                # MkDocs Material overrides
│   │   ├── partials/tabs.html    # Navigation tabs
│   │   ├── proposals-main.html   # Proposal detail template
│   │   ├── proposals-oview.html  # Proposal overview template
│   │   └── proposals-proposals-main.html
│   ├── stylesheets/
│   │   ├── github.css            # GitHub Primer theme
│   │   ├── proposals.css         # Proposal card, filter, and quarter summary styles
│   │   └── issues.css            # GitHub-style issues layout
│   ├── gonka/
│   │   └── docs/                 # Protocol documentation (synced)
│   ├── community/
│   │   ├── discussion/           # GitHub Discussions (synced)
│   │   ├── issues/               # GitHub Issues (synced)
│   │   ├── roadmap/              # Roadmap (synced)
│   │   ├── gonka restitution committee/  # GRC
│   │   ├── governance support committee/ # GSC
│   │   ├── gonka product committee/
│   │   └── go-to-market committee/
│   └── proposals/
│       ├── proposals/            # On-chain proposals by quarter
│       │   ├── index.md          # Overview with filter + summary
│       │   ├── 2025-q3/         # Per-quarter pages
│       │   ├── 2025-q4/
│       │   ├── 2026-q1/
│       │   ├── 2026-q2/
│       │   └── 2026-q3/
│       └── preproposals/         # Pre-Proposals (synced)
├── hooks/
│   ├── full_proposal.py          # MkDocs hook: inject full proposal into detail pages
│   ├── issues_nav.py             # MkDocs hook for issue page navigation
│   └── proposals_nav.py          # MkDocs hook: auto-expand Proposals nav
├── mcp.json                      # MCP server config
├── AGENTS.md                     # AI agent guide for this repo
├── .opencode/
│   └── opencode.json             # opencode config (commands, permissions, MCP)
├── .github/scripts/
│   ├── sync_all_discussions.py   # Fetch GitHub Discussions via GraphQL
│   ├── sync_gonka_issues.py      # Fetch GitHub Issues via REST
│   ├── sync_onchain_proposals.py # Fetch on-chain proposals from RPC
│   └── sync_preproposals.py      # Fetch pre-proposals from gonka.vote
└── .github/workflows/
    ├── deploy-docs.yml           # Deploy to GitHub Pages
    ├── sync-gonka-ai-docs.yml    # Sync documentation
    ├── sync-onchain-proposals.yml# Sync on-chain proposals
    ├── sync-discussions.yml      # Sync discussions
    ├── sync-issues.yml           # Sync issues
    └── sync-preproposals.yml     # Sync pre-proposals
```

---

## License

Documentation distributed under the Gonka protocol license. See `docs/gonka/docs/docs/protocol-license.pdf`.
