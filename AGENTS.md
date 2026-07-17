# Gonka Docs — Repository Guide

This repository builds and deploys [gonkadocs.com](https://gonkadocs.com) — a unified documentation portal for the Gonka decentralized AI inference network.

## Project Structure

```
gonkadocs/
├── mkdocs.yml                   # MkDocs config (main site)
├── buildtools/
│   ├── build.sh                 # Master build script (9-step pipeline)
│   ├── serve.sh                 # Local preview server
│   ├── generate-llms.py         # Generate llms.txt
│   ├── generate-llms-full.py    # Generate llms-full.txt
│   ├── generate-page-md.py      # Generate .html.md copies
│   ├── mcp-server.py            # MCP server for AI agents
│   ├── fetch-full-proposals.py  # Fetch full proposal text from GitHub
│   ├── activity-feed.py         # Change detection + AI-summarized events
│   └── gonka-overrides/         # Tabs + language switcher for Gonka sub-build
├── docs/
│   ├── index.md                 # Homepage
│   ├── 404.md                   # Custom 404 page
│   ├── agents.md                # AI agent setup guide (served at /agents/)
│   ├── AGENTS.md                # This file (same file, case-insensitive FS)
│   ├── overrides/               # MkDocs Material overrides (Jinja2)
│   │   ├── main.html            # OG tags, JSON-LD, analytics, header scripts
│   │   ├── home.html            # Landing page hero
│   │   ├── 404.html             # Error page
│   │   ├── activity-feed.html   # Activity timeline
│   │   ├── calendar.html        # Event calendar grid
│   │   ├── proposals-*.html     # 4 proposal templates
│   │   ├── issues-*.html        # 3 issue templates
│   │   └── partials/            # header, tabs, comments, issue nav
│   ├── stylesheets/             # CSS (github, proposals, issues, calendar, activity)
│   ├── scripts/                 # JS (proposals-countdown.js)
│   ├── gonka/docs/              # Protocol docs (synced from gonka-ai/gonka-docs)
│   ├── community/               # Discussions, Issues, Roadmap, Calendar, Activity, Committees
│   └── proposals/               # On-chain proposals (by quarter, with RSS + sitemap) + pre-proposals
├── hooks/                       # MkDocs hooks (Python, auto-loaded by mkdocs.yml)
├── mcp.json                     # MCP server config (Cursor/Windsurf/Cline)
├── .opencode/
│   ├── opencode.json            # opencode config (commands, permissions, MCP)
│   ├── opencode.schema.json     # Local JSON Schema for opencode config
│   └── model-schema.json        # Model provider schema (local ref)
├── .github/
│   ├── workflows/               # 6 GitHub Actions (5 sync + 1 deploy)
│   └── scripts/                 # 4 sync scripts
└── .feed-manifests/             # Change detection state for activity feed
```

## Build Commands

| Command | Description |
|---------|-------------|
| `bash buildtools/build.sh` | Full build → `_site/` |
| `bash buildtools/serve.sh` | Build + serve on localhost:8000 |
| `python3 .github/scripts/sync_onchain_proposals.py` | Sync on-chain proposals |
| `python3 buildtools/generate-llms.py` | Regenerate llms.txt |
| `python3 buildtools/generate-llms-full.py` | Regenerate llms-full.txt |
| `python3 buildtools/generate-page-md.py` | Regenerate .html.md page copies |
| `python3 buildtools/activity-feed.py` | Regenerate activity feed events |

## Key Architecture

- **Dual MkDocs build**: main site (`mkdocs.yml`) + Gonka protocol docs (`docs/gonka/docs/mkdocs.yml`) merged into `_site/`
- **AI-first**: llms.txt, llms-full.txt, .html.md page copies, MCP server
- **Auto-sync**: 5 hourly workflows sync Discussions, Issues, protocol docs, pre-proposals + on-chain proposals every 10 min
- **SEO**: OpenGraph, JSON-LD, merged sitemap, zh sitemap, hreflang, proposals sitemap

## Conventions

- MkDocs hooks go in `hooks/` (Python files, auto-loaded by mkdocs.yml)
- CSS goes in `docs/stylesheets/`
- Templates go in `docs/overrides/` (main site) or `buildtools/gonka-overrides/` (gonka sub-build)
- Sync scripts go in `.github/scripts/`
- Do NOT modify `docs/gonka/docs/` directly — it's overwritten by hourly sync
