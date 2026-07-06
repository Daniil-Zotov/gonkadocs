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

### Pre-Proposals (`/proposals/preproposals/`)
Auto-synced from [gonka.vote](https://gonka.vote) every hour.

- Community proposals with vote tallies and comments
- Active and expired proposal tracking

### Community (`/community/`)
- **Roadmap** — three-horizon development strategy
- **GRC** — restitution committee (bug compensation)
- **GSC** — self-regulation committee

### On-Chain Proposals (`/proposals/`)
Dashboard of all governance proposals with statuses and descriptions.

---

## AI Integration

Portal designed as a single source of truth for AI agents.

### Standard Files

| URL | Description |
|-----|-------------|
| [`/llms.txt`](https://gonkadocs.com/llms.txt) | AI entry point: project overview, section links, key concepts |
| [`/llms-full.txt`](https://gonkadocs.com/llms-full.txt) | All docs in one file (~800 KB), optimized for context window |
| [`/robots.txt`](https://gonkadocs.com/robots.txt) | Permissions for GPTBot, ClaudeBot, Google-Extended |
| [`/openapi.yaml`](https://gonkadocs.com/openapi.yaml) | OpenAPI 3.0 specification for inference API |
| [`/sitemap.xml`](https://gonkadocs.com/sitemap.xml) | Full sitemap |

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
    ├──► [1] generate-llms-full.py
    │       Dynamic scanning of docs/ → llms-full.txt
    │
    ├──► [2] mkdocs build (main site)
    │       Homepage + Community + Proposals
    │
    ├──► [3] mkdocs build (Gonka section)
    │       Original mkdocs.yml from gonka-ai/gonka-docs
    │       i18n: en + zh, custom overrides
    │
    ├──► [4] Post-processing
    │       Fix image paths
    │       Language switcher (LINK_EN/LINK_ZH → real paths)
    │
    └──► [5] generate-llms.py + generate-page-md.py
            Generate llms.txt and .html.md page copies
```

---

## Auto-Sync

7 GitHub Actions workflows automatically update content every hour:

| Workflow | Source | Syncs |
|----------|--------|-------|
| `sync-gonka-ai-docs.yml` | gonka-ai/gonka-docs | Protocol documentation |
| `sync-discussions.yml` | gonka-ai/gonka (GraphQL) | GitHub Discussions |
| `sync-issues.yml` | gonka-ai/gonka (REST) | GitHub Issues |
| `sync-preproposals.yml` | gonka.vote (REST) | Pre-Proposals |
| `sync-gdocs.yml` | Google Docs | GSC regulation |
| `sync-roadmap.yml` | gonka-ai/gonka | Roadmap |

All sync workflows regenerate `llms.txt` and `llms-full.txt` after each update.

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
│   ├── overrides/                # MkDocs Material overrides
│   ├── stylesheets/
│   │   └── github.css            # GitHub Primer theme
│   ├── gonka/
│   │   ├── docs/                 # Protocol documentation (synced)
│   │   └── discussion/           # GitHub Discussions (synced)
│   ├── community/
│   │   ├── discussion/           # Discussions (synced)
│   │   ├── issues/               # GitHub Issues (synced)
│   │   ├── roadmap/              # Roadmap (synced)
│   │   ├── grc/                  # Restitution committee
│   │   └── gsc/                  # Self-regulation committee (synced)
│   └── proposals/                # On-chain proposals + Pre-Proposals (synced)
├── hooks/
│   └── issues_nav.py             # MkDocs hook for issue page navigation
├── mcp.json                      # MCP server config
└── .github/workflows/
    ├── deploy-docs.yml           # Deploy to GitHub Pages
    ├── sync-gonka-ai-docs.yml    # Sync documentation
    ├── sync-discussions.yml      # Sync discussions
    ├── sync-issues.yml           # Sync issues
    ├── sync-preproposals.yml     # Sync pre-proposals
    ├── sync-gdocs.yml            # Sync Google Docs
    └── sync-roadmap.yml          # Sync roadmap
```

---

## License

Documentation distributed under the Gonka protocol license. See `docs/gonka/docs/docs/protocol-license.pdf`.
