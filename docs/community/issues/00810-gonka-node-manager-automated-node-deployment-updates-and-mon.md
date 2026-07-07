---
title: "#810 — Gonka Node Manager — Automated Node Deployment, Updates, and Monitoring"
source: https://github.com/gonka-ai/gonka/issues/810
issue_number: 810
synced_at: 2026-07-07T04:29:40Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    Gonka Node Manager — Automated Node Deployment, Updates, and Monitoring
    <span class="issues-number">#810</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item">[@ochenUmnayaKatyshka](https://github.com/ochenUmnayaKatyshka) opened 2026-02-26 11:49 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-02-27 20:15 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #a2eeef; color: #24292f; border-color: #a2eeef;">enhancement</span> <span class="issues-label" style="background-color: #008672; color: #ffffff; border-color: #008672;">help wanted</span></div>
</div>

<div class="issues-content" markdown="1">
## Executive Summary

Running Gonka nodes currently requires manual CLI-based installation, configuration, and ongoing maintenance. For experienced operators, initial setup typically takes several hours per node. For less experienced participants, the process often stretches to one or two days — or results in abandonment before a node is ever launched.

This friction actively filters out potential operators, concentrating power among technically advanced users and slowing organic decentralization.

Gonka Node Manager requests **$80,000 USD equivalent** from the Community Pool to build a production-ready MVP that automates node deployment, updates, and monitoring.

> Note: On-chain governance vote (Community Pool spend) will be submitted as a separate transaction once the contract is deployed. This issue tracks the technical proposal and implementation plan.

---

## Problem Statement

Current node operation requires:
- Manual CLI setup taking hours to days per node
- SSH access and server-level configuration for every update
- No automated monitoring or health visibility
- No streamlined process for attaching ML nodes to network nodes

This effectively limits participation to a narrow group of technically advanced users, concentrating operational power and slowing organic decentralization.

---

## Proposed Solution

Gonka Node Manager — a unified tool that allows node operators to:

- Deploy network and ML nodes in a consistent, automated way
- Keep nodes up to date without manual intervention
- Attach and operate ML nodes alongside network nodes
- Observe basic node status and health without logging into servers

The system operates on top of user-provided infrastructure (physical or virtual) and fits naturally into a decentralized network model.

---

## Architecture Overview

### Components

| Component | Role |
|---|---|
| **Control Plane (Web UI + API)** | User auth, node management, issues tasks to agents, displays status |
| **Node Agent (host daemon)** | Installed once per host, manages local Docker Compose stacks, communicates outbound only |
| **Stack Bundles** | Deployment definitions: services, ports, health checks, references to official Gonka images |

### Core User Flows

1. **Node bootstrap** — user adds node in UI → agent installed once on server → node available
2. **Deployment & updates** — automated via preconfigured stable release path, no user intervention
3. **Network/ML attachment** — ML node attached to network node, firewall rules applied automatically, connectivity validated
4. **Warm key workflow** — warm key generated locally on node, only public key exposed, cold-key signing stays with operator

---

## Security Model

- SSH access stays entirely under operator control — Control Plane never stores credentials or uses SSH
- No inbound management ports required on nodes
- Agent executes only approved, predefined operations — no arbitrary remote commands
- Stack bundles verified before application
- Cold keys never leave the operator's device

This preserves node sovereignty and aligns with Gonka's decentralization principles.

---

## MVP Scope

### Included

- Host-level node agent
- Deployment of network and ML nodes
- Automatic updates via preconfigured stable release path
- Network/ML attachment with firewall automation
- Warm key generation and binding workflow
- Basic status and health reporting

### Explicitly Out of Scope

- Advanced metrics and observability stacks
- Arbitrary remote command execution
- Manual version selection or multiple update channels
- Role-based access control
- Automated rollback mechanisms (except those recommended by Gonka developers)
- On-chain enforcement of updates
- Remote administrative access

---

## Implementation Plan

### Phase 1 — MVP Installation (45–50% of budget)
**Outcome:** Network and ML nodes can be deployed and operate end-to-end
- Node agent: deploy, attach, health — 160–200h
- Control Plane core APIs — 80–100h
- Architecture & core design — 40–60h
- Minimal UI — 40–60h
- Integration testing — 40–60h

### Phase 2 — MVP Auto-Updates (20–25% of budget)
**Outcome:** Running nodes update themselves automatically
- Bundle versioning & signatures — 40–60h
- Agent update logic — 40–60h
- Control Plane update coordination — 20–30h
- Update testing — 20–30h

### Phase 3 — MVP Monitoring (15–20% of budget)
**Outcome:** Operators can observe node status and health
- Agent health reporting — 30–40h
- Backend status aggregation — 20–30h
- UI status views — 40–50h

### Phase 4 — Stabilization & Technical Debt (10–15% of budget)
**Outcome:** Stable, documented, production-ready MVP
- Bug fixes and edge cases
- Security hardening
- Documentation
- Final testing

**Total estimated effort: 650–880 engineering hours**

---

## Budget

**Requested: $80,000 USD equivalent** (one-time, from Community Pool)

Funding released in stages tied to phase completion. Cost overruns covered by the team at its own expense — no retroactive compensation requests will be made.

---

## Accountability

- All progress tracked in a single public GitHub repository
- `progress.md` updated after each phase with written summary, deliverables, and artifact links
- Code, docs, release notes, and demo materials committed per phase
- Repository URL announced immediately after proposal approval

---

## Expected Outcome

- Easier onboarding for new node operators
- Increased number of independent nodes
- Reduced downtime caused by manual configuration
- Stronger and more sustainable decentralization of the Gonka network
</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@tcharchian](https://github.com/tcharchian)</span>
    <span class="issues-meta-item">commented 2026-02-27 00:11 UTC</span>
  </div>
  <div class="issues-comment-body issues-content" markdown="1">
    Hi @ochenUmnayaKatyshka! I'd suggetst publishing proposals in Discussion section: https://github.com/gonka-ai/gonka/discussions/categories/proposals
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #810](https://github.com/gonka-ai/gonka/issues/810) every hour.
