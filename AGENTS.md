# Gonka Docs — Repository Guide

This repository builds and deploys [gonkadocs.com](https://gonkadocs.com) — a unified documentation portal for the Gonka decentralized AI inference network.

## Project Structure

```
gonkadocs/
├── mkdocs.yml                   # MkDocs config (main site)
├── buildtools/
│   ├── build.sh                 # Master build script (7+ steps)
│   ├── serve.sh                 # Local preview server
│   ├── generate-llms.py         # Generate llms.txt
│   ├── generate-llms-full.py    # Generate llms-full.txt
│   ├── generate-page-md.py      # Generate .html.md copies
│   ├── mcp-server.py            # MCP server for AI agents
│   └── gonka-overrides/         # Shared templates for Gonka sub-build
├── docs/
│   ├── index.md                 # Homepage
│   ├── agents.md                # AI agent setup guide (served at /agents/)
│   ├── AGENTS.md                # This file (same file, case-insensitive FS)
│   ├── overrides/               # MkDocs Material overrides (Jinja2)
│   ├── stylesheets/             # CSS (github.css, proposals.css, issues.css)
│   ├── gonka/docs/              # Protocol docs (synced from gonka-ai/gonka-docs)
│   ├── community/               # Discussions, Issues, Roadmap, Committees
│   └── proposals/               # On-chain proposals + pre-proposals
├── hooks/                       # MkDocs hooks (Python)
├── .github/
│   ├── workflows/               # 6 GitHub Actions
│   └── scripts/                 # Sync scripts
├── mcp.json                     # MCP server config
└── .opencode/opencode.json      # opencode config
```

## Build Commands

| Command | Description |
|---------|-------------|
| `bash buildtools/build.sh` | Full build → `_site/` |
| `bash buildtools/serve.sh` | Build + serve on localhost:8000 |
| `python3 .github/scripts/sync_onchain_proposals.py` | Sync on-chain proposals |
| `python3 buildtools/generate-llms.py` | Regenerate llms.txt |
| `python3 buildtools/generate-llms-full.py` | Regenerate llms-full.txt |

## Key Architecture

- **Dual MkDocs build**: main site (`mkdocs.yml`) + Gonka protocol docs (`docs/gonka/docs/mkdocs.yml`) merged into `_site/`
- **AI-first**: llms.txt, llms-full.txt, .html.md page copies, MCP server
- **Auto-sync**: 5 hourly workflows sync Discussions, Issues, protocol docs, on-chain proposals, pre-proposals
- **SEO**: OpenGraph, JSON-LD, merged sitemap, zh sitemap, hreflang

## Conventions

- MkDocs hooks go in `hooks/` (Python files, auto-loaded by mkdocs.yml)
- CSS goes in `docs/stylesheets/`
- Templates go in `docs/overrides/` (main site) or `buildtools/gonka-overrides/` (gonka sub-build)
- Sync scripts go in `.github/scripts/`
- Do NOT modify `docs/gonka/docs/` directly — it's overwritten by hourly sync
