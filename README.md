# gonkadocs.com

**Gonka Docs** is a meta-repository for the [Gonka](https://gonka.ai) decentralized AI inference network (Proof of Compute consensus). It aggregates everything about the project in one place:

- **Official documentation** — auto-synced protocol docs (`/gonka/docs/`) with English and Chinese translations
- **Source code mirror** — the full `gonka-ai/gonka` source served verbatim (`/gonka-code/`), indexed by `/gonka-code-map.txt`
- **Community** — roadmap, calendar, activity feed, discussions, issues, and committees (GRC / GSC / GPC / GTM)
- **Governance** — off-chain pre-proposals (`gonka.vote`), on-chain proposal dashboard with quarterly summaries, tally results, funding sources, and published reports
- **Community funds** — live balances and full spend history of the Community Pool, Community Sale wallet, and Gov Module

The portal is designed **agent-first**: machine-readable `llms.txt` / `llms-full.txt`, `.html.md` page copies, a merged search index, sitemaps, RSS, an OpenAPI spec, and an MCP server so AI agents can answer questions about Gonka without manual context copying.

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
Auto-synced from [rpc.gonka.gg](https://rpc.gonka.gg) every 10 minutes. Proposals are organized by quarter:

- **Quarterly overviews** — per-quarter summaries with pass/reject/fail rates, category breakdowns, and approved funding totals by source
- **Individual proposal pages** — detailed view with status, tally results, funding amount and source (Community Pool / Gov Module), on-chain contract messages, and voter details
- **Funding source tracking** — each proposal shows where funding originates: `Community Pool` (community pool spend, execute contract) or `Gov Module` (batch vesting, multi-send)
- **Status filters** — filter by Passed / Rejected / Voting / With Funding
- **Tally results** — bold percentages followed by vote counts for Yes/No/Veto/Abstain with turnout/quorum
- **Report badges** — proposals with published reports (e.g. `report1.md`) show clickable green badges on overview cards
- **RSS feed** — `/proposals/proposals/proposals.xml`
- **Sitemap** — `/proposals/proposals/sitemap.xml`

### Pre-Proposals (`/proposals/preproposals/`)
Auto-synced from [gonka.vote](https://gonka.vote) every hour.

- Community proposals with vote tallies and comments
- Active and expired proposal tracking

### Community (`/community/`)
- **Roadmap** — three-horizon development strategy
- **Calendar** — collapsible month timeline; past months collapsed by default, auto-generated events for proposal milestones and report uploads
- **Activity Feed** — live changelog of all synced content (proposals, discussions, issues, docs, calendar) with AI-generated summaries and daily reminders
- **GRC** — restitution committee (bug compensation) at `/community/gonka restitution committee/`
- **GSC** — governance support committee at `/community/governance support committee/`
- **GPC** — gonka product committee
- **GTM** — go-to-market committee

### Source Code Mirror (`/gonka-code/`)
Auto-synced from [gonka-ai/gonka](https://github.com/gonka-ai/gonka) every hour.

- **Raw source mirror** — full protocol source served verbatim under `/gonka-code/` (blob-less sparse clone, `cosmovisor/` binaries and `*_test.go` excluded)
- **Code map** — `/gonka-code-map.txt` indexes every mirrored file for AI agents to locate code fast
- **Design docs** — `proposals/` docs included
- **On-chain bounties** — `inference-chain/app/upgrades/v0_2_*/upgrades.go` with `bountyRewards` arrays

---

## AI Integration

Portal designed as a single source of truth for AI agents.

### Standard Files

| URL | Description |
|-----|-------------|
| [`/llms.txt`](https://gonkadocs.com/llms.txt) | AI entry point: project overview, section links, key concepts |
| [`/llms-full.txt`](https://gonkadocs.com/llms-full.txt) | All docs in one file (~2.6 MB), optimized for context window |
| [`/robots.txt`](https://gonkadocs.com/robots.txt) | Permissions for AI crawlers (GPTBot, ClaudeBot, PerplexityBot, Google-Extended, etc.) |
| [`/openapi.yaml`](https://gonkadocs.com/openapi.yaml) | OpenAPI 3.0 specification for inference API |
| [`/sitemap.xml`](https://gonkadocs.com/sitemap.xml) | Full sitemap (main + gonka/docs merged) |
| [`/gonka/docs/zh/sitemap.xml`](https://gonkadocs.com/gonka/docs/zh/sitemap.xml) | Chinese-language sitemap for gonka docs |
| [`/search/search_index.json`](https://gonkadocs.com/search/search_index.json) | Lunr.js search index, queryable programmatically |
| [`/proposals/proposals/proposals.xml`](https://gonkadocs.com/proposals/proposals/proposals.xml) | RSS feed for on-chain governance proposals |
| [`/proposals/proposals/sitemap.xml`](https://gonkadocs.com/proposals/proposals/sitemap.xml) | Sitemap for governance proposals |
| [`/gonka-code-map.txt`](https://gonkadocs.com/gonka-code-map.txt) | Index of the source code mirror (fetch first to locate files) |
| [`/gonka-code/`](https://gonkadocs.com/gonka-code/) | Raw source code mirror of gonka-ai/gonka |
| [`/community/calendar/events/`](https://gonkadocs.com/community/calendar/events/) | Machine-readable list of all calendar events |
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
- `read_gonka_llms_full(max_chars)` — full context (optionally truncated)
- `read_gonka_proposal(id)` — read on-chain governance proposal detail page

### Machine-Readable Page Copies

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
    ├──► [0] generate_calendar_events.py + generate-llms.py + generate-llms-full.py
    │       Calendar events → events.md, then llms.txt + llms-full.txt
    │
    ├──► [0.5] generate-code-map.py
    │       Scans gonka-code/ → docs/gonka-code-map.txt
    │
    ├──► [1] mkdocs build (main site)
    │       Homepage + Community + Proposals
    │
    ├──► [2] mkdocs build (Gonka section)
    │       Original mkdocs.yml from gonka-ai/gonka-docs
    │       i18n: en + zh, shared header from main site overrides
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
    └──► [7] Copy service files + code mirror
            robots.txt, llms.txt, llms-full.txt, openapi.yaml → _site/
            gonka-code/ → _site/gonka-code/ + generated index.html

Additionally generated by sync scripts:
  - proposals/ proposals.xml + sitemap.xml (every 10 min)
  - community/activity/events.json (change detection + AI summaries)
  - community/calendar/manifest.json (event aggregation)
```

---

## Auto-Sync

8 GitHub Actions workflows automatically update content:

| Workflow | Source | Syncs | Triggers Deploy |
|----------|--------|-------|:---:|
| `sync-gonka-ai-docs.yml` | gonka-ai/gonka-docs | Protocol documentation | via push |
| `sync-onchain-proposals.yml` | rpc.gonka.gg (every 10 min) | On-chain governance proposals | via API |
| `sync-discussions.yml` | gonka-ai/gonka (GraphQL) | GitHub Discussions | via push |
| `sync-issues.yml` | gonka-ai/gonka (REST) | GitHub Issues | via push |
| `sync-preproposals.yml` | gonka.vote (REST) | Pre-Proposals | via push |
| `sync-gonka-code.yml` | gonka-ai/gonka | Source code mirror + code map (hourly) | via push |
| `activity-calendar.yml` | calendar JSON files | Activity feed events + daily reminders (hourly) | via push |
| `update-community-pool.yml` | rpc.gonka.gg (hourly) | Community pool balances + spend history | via API |

Every sync triggers the `deploy-docs.yml` workflow, which regenerates `llms.txt` and `llms-full.txt` and deploys the updated site to GitHub Pages.

---

## Local Development

```bash
# Install dependencies
pip install mkdocs mkdocs-material pymdown-extensions mcp

# Build full site
bash buildtools/build.sh

# Build + serve locally on :8000
bash buildtools/serve.sh

# Sync proposals (requires RPC access)
python3 .github/scripts/sync_onchain_proposals.py

# Sync source code mirror (requires network access)
python3 buildtools/sync-gonka-code.py
python3 buildtools/generate-code-map.py

# Regenerate calendar events page
python3 buildtools/generate_calendar_events.py

# Update community pool data
python3 buildtools/update-community-pool.py

# Activity feed
python3 buildtools/activity-feed.py detect --section calendar --dir docs/community/calendar --manifest .feed-manifests/calendar.json --events docs/community/activity/events.json

# Regenerate AI files
python3 buildtools/generate-llms.py
python3 buildtools/generate-llms-full.py
```

---

## Repository Structure

```
gonkadocs/
├── mkdocs.yml                    # MkDocs config (main site)
├── buildtools/
│   ├── build.sh                  # Master build script (9-step pipeline)
│   ├── serve.sh                  # Build + local preview server
│   ├── generate-llms.py          # Generate llms.txt
│   ├── generate-llms-full.py     # Generate llms-full.txt
│   ├── generate-page-md.py       # Generate .html.md page copies
│   ├── generate_calendar_events.py  # Generate community/calendar/events.md
│   ├── mcp-server.py             # MCP server for AI agents
│   ├── fetch-full-proposals.py   # Fetch full proposal text from GitHub
│   ├── activity-feed.py          # Change detection + AI-summarized events + daily reminders
│   ├── sync-gonka-code.py        # Filtered copy of gonka-ai/gonka → gonka-code/
│   ├── generate-code-map.py      # Generate gonka-code-map.txt from the mirror
│   ├── update-community-pool.py  # Update community pool balances + spend history
│   └── gonka-overrides/          # Tabs + language switcher for Gonka sub-build
├── docs/
│   ├── index.md                  # Homepage
│   ├── 404.md                    # Custom 404 page
│   ├── agents.md                 # AI agent setup guide (served at /agents/)
│   ├── llms.txt                  # AI entry point
│   ├── llms-full.txt             # Full documentation
│   ├── gonka-code-map.txt        # Source mirror index (generated)
│   ├── robots.txt                # AI crawler permissions
│   ├── openapi.yaml              # API specification
│   ├── CNAME                     # Custom domain
│   ├── humans.txt                # Credits
│   ├── manifest.json             # PWA manifest
│   ├── .well-known/
│   │   └── security.txt          # Security policy
│   ├── overrides/                # MkDocs Material overrides (Jinja2)
│   │   ├── main.html             # OG tags, JSON-LD, Yandex.Metrika, header scripts
│   │   ├── home.html             # Landing page hero
│   │   ├── 404.html              # Error page
│   │   ├── activity-feed.html    # Activity timeline
│   │   ├── calendar.html         # Event calendar grid (collapsible months)
│   │   ├── issues-main.html      # Issues with sidebar labels
│   │   ├── proposals-main.html   # Pre-proposal detail
│   │   ├── proposals-oview.html  # On-chain proposal overview with filters
│   │   ├── proposals-proposals-main.html  # On-chain proposal detail
│   │   └── partials/
│   │       ├── header.html       # Shared header (both builds use this)
│   │       ├── tabs.html         # Navigation tabs (Gonka.ai/docs, Community, Proposals, For Agents)
│   │       ├── comments.html     # Giscus comments
│   │       ├── issues-nav.html   # Issues left nav
│   │       ├── issues-sidebar.html  # Issues right sidebar
│   │       └── issues-labels-nav.html  # Label filters
│   ├── stylesheets/
│   │   ├── github.css            # GitHub Primer theme + layout
│   │   ├── proposals.css         # Proposal cards, tally bars, badges, filters
│   │   ├── issues.css            # GitHub-style issues list
│   │   ├── calendar.css          # Timeline calendar grid
│   │   └── activity.css          # Activity feed timeline
│   ├── scripts/
│   │   └── proposals-countdown.js  # Countdown timers for voting proposals
│   ├── gonka/
│   │   └── docs/                 # Protocol documentation (synced, DO NOT MODIFY)
│   ├── community/
│   │   ├── discussion/           # GitHub Discussions (synced)
│   │   ├── issues/               # GitHub Issues (synced)
│   │   ├── roadmap/              # Development roadmap
│   │   ├── activity/             # Activity feed (events.json)
│   │   ├── calendar/             # Event JSON files + manifest
│   │   ├── gonka restitution committee/  # GRC
│   │   ├── governance support committee/ # GSC
│   │   ├── gonka product committee/      # GPC
│   │   └── go-to-market committee/       # GTM
│   └── proposals/
│       ├── proposals/            # On-chain proposals by quarter
│       │   ├── index.md          # Overview with filters + summaries
│       │   ├── proposals.xml     # RSS feed (90+ items)
│       │   ├── sitemap.xml       # Proposals sitemap
│       │   ├── community pool.md # Community pool balances + spend history
│       │   ├── 2025-q3/         # Quarters with per-proposal subdirs
│       │   ├── 2025-q4/
│       │   ├── 2026-q1/
│       │   ├── 2026-q2/
│       │   └── 2026-q3/
│       │       └── {id}/
│       │           ├── index.md          # Proposal detail page
│       │           ├── messages.json     # Raw on-chain messages
│       │           ├── voting_power.json # Total voting power snapshot
│       │           ├── full-proposal.md  # Full text (when available)
│       │           └── report*.md        # Published reports (rendered as pages)
│       └── preproposals/         # Off-chain pre-proposals (synced)
│           ├── index.md          # Active/Expired tables
│           └── {uuid}/index.md   # Individual pre-proposal
├── hooks/                        # MkDocs build hooks (Python, auto-loaded)
│   ├── full_proposal.py          # Inject full-proposal.md into detail pages
│   ├── proposal_reports.py       # Inject published reports into proposal pages
│   ├── issues_nav.py             # Auto-expand Issues/Discussions nav
│   ├── proposals_nav.py          # Auto-expand Proposals nav
│   └── calendar_manifest.py      # Generate manifest.json from calendar events
├── mcp.json                      # MCP server config (for Cursor/Windsurf/Cline)
├── AGENTS.md                     # AI agent guide for this repo
├── README.md                     # This file
├── .opencode/
│   ├── opencode.json             # opencode config (commands, permissions, MCP)
│   ├── opencode.schema.json      # Local JSON Schema for opencode config
│   └── model-schema.json         # Model provider schema (local ref)
├── .github/
│   ├── workflows/
│   │   ├── deploy-docs.yml           # Build + deploy to GitHub Pages
│   │   ├── sync-gonka-ai-docs.yml    # Hourly: sync protocol docs
│   │   ├── sync-onchain-proposals.yml# Every 10 min: sync proposals
│   │   ├── sync-discussions.yml      # Hourly: sync discussions
│   │   ├── sync-issues.yml           # Hourly: sync issues
│   │   ├── sync-preproposals.yml     # Hourly: sync pre-proposals
│   │   ├── sync-gonka-code.yml       # Hourly: sync source code mirror
│   │   ├── activity-calendar.yml     # Hourly: activity feed + daily reminders
│   │   └── update-community-pool.yml # Hourly: community pool balances + spend history
│   └── scripts/
│       ├── sync_onchain_proposals.py # Fetch proposals from rpc.gonka.gg
│       ├── sync_preproposals.py      # Fetch pre-proposals from gonka.vote
│       ├── sync_all_discussions.py   # Fetch discussions via GraphQL
│       └── sync_gonka_issues.py      # Fetch issues via GitHub REST API
├── .feed-manifests/              # Change detection state for activity feed
└── gonka-code/                   # Source code mirror (synced, DO NOT MODIFY)
```

---

## License

Documentation distributed under the Gonka protocol license. See `docs/gonka/docs/docs/protocol-license.pdf`.
