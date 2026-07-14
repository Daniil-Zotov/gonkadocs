# Gonka Node Observability Platform

Proposal by INC4 (https://inc4.net) | 16 April 2026

Funding Request: \$96,000 USD (USDT) for 12 months

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Problem Statement](#2-problem-statement)
3. [Industry Context](#3-industry-context)
4. [Proposed Solution](#4-proposed-solution)
5. [Technical Approach](#5-technical-approach)
6. [Scope and Deliverables](#6-scope-and-deliverables)
7. [Budget and Payment Schedule](#7-budget-and-payment-schedule)
8. [Success Criteria](#8-success-criteria)
9. [Team](#9-team)

---

## 1. Executive Summary

Today's explorers and dashboards only show on-chain data, leaving the off-chain state of validators completely opaque. The few operators who do run their own monitoring use different tools, different metrics, and different baselines, leading to different interpretations and making it harder to coordinate when problems arise. The network lacks a single source of truth and a common framework for measuring validator health.

Even today, simply watching how validators operate reveals that many are not reacting to technical problems in time — growing Inference Miss Rates, dropping CPoC Ratios, network sync falling behind. These patterns persist because operators have no way to see the early warning signs or get emergency alerts inside their own infrastructure.

To address this, INC4 — an active Gonka validator operator with hands-on experience in blockchain infrastructure and observability — proposes the creation of the Gonka Node Observability Platform — an open-source, opt-in observability stack that aggregates off-chain metrics from Network nodes and ML nodes into a shared, publicly accessible dashboard. The platform is deployed on independent cloud infrastructure — without using resources of any individual validator or granting anyone privileged access — so that all operators have equal access and visibility into the data.

For the Core Team — a unified view of the entire network, visibility into problematic nodes and time periods, data for informed protocol decisions, SLA reports, and the ability to assess the scope of network-wide issues before and after upgrades. For Individual Validators — real-time alerts, performance comparison against network averages, opt-in log sharing to get help with troubleshooting and metrics interpretation, and no need to build your own monitoring stack.

Detecting and preventing even a single major network-wide incident, or a series of smaller incidents at individual validators, can save the ecosystem far more than the annual cost of this platform. The primary beneficiaries are the validator operators themselves, who bear the direct cost of every missed epoch and every hour of undiagnosed downtime — especially individual hosts without dedicated DevOps staff, for whom building and maintaining a comparable monitoring stack on their own is simply not feasible.

We request \$96,000 in USDT over 12 months, paid in quarterly tranches, to deploy and maintain a production-grade observability platform — custom Gonka exporters, fleet-wide and individual dashboards, opt-in log aggregation, external endpoint health checks, alerting and SLA reporting, hands-on validator onboarding, incident response support, and ongoing operational maintenance. All code, configurations, and dashboards will be open-source and published in public GitHub repositories.


---

## 2. Problem Statement

### Off-chain state of the network is not visible

Gonka is a growing network with over a hundred validators, an even larger number of ML nodes, and a combined GPU fleet exceeding 3,000 cards. Existing block explorers and dashboards show on-chain data — block heights, transactions, voting power. But there are zero tools for network-wide off-chain observability — GPU health, container status, miss rate root causes, model load times, LLM performance metrics, infrastructure trends, etc. Each operator monitors their infrastructure in isolation — or doesn't monitor at all. Those who do monitor set up their own tools, calculate metrics differently, and use different baselines — which leads to miscommunication and confusion when discussing network issues.

Specifically, existing tools do not show:

- Why a validator's miss rate is high
- Whether RAM or GPU memory is exhausted
- Whether ML or other containers are crash-looping
- How long model loading takes after a restart
- Whether a PUBLIC_URL is reachable from outside
- Comparative performance across validators

In practice, validators have experienced prolonged periods of high miss rate or inference downtime without being able to identify the root cause. At the same time, the Core Team had no way to see the scope of such issues across the network. These situations result in lost rewards for operators and delayed response from the team — problems that a shared observability platform would help detect and resolve much faster.

### What happens without a solution

- Silent failures go undetected for hours or days — costing validators missed epochs and lost rewards
- No common ground for debugging — each operator uses different tools, different baselines, different definitions of "normal"
- The Core Team lacks fleet-wide visibility — making it harder to diagnose network-level issues and plan upgrades
- New operators are on their own — high barrier to entry for smaller hosts without DevOps expertise

---

## 3. Industry Context

### Collecting validator metrics in one place is not new

Aggregating telemetry and metrics from validators into a shared backend is a well-established practice across the blockchain industry. Multiple major networks already do this:

- Solana — validators report metrics to a shared backend; the network publishes a public Grafana dashboard at `https://metrics.solana.com:3000`
- Polkadot — nodes send telemetry by default to a shared backend; a public real-time dashboard is available at `https://telemetry.polkadot.io`
- Kusama — uses the same Substrate Telemetry system as Polkadot, with its own view at `https://telemetry.polkadot.io/#list/Kusama`
- NEAR — every node ships with a default telemetry endpoint (`telemetry.nearone.org`) and pushes data every 10 seconds
- Aptos — all nodes push metrics to a centralized telemetry service (`telemetry.mainnet.aptoslabs.com`) by default; the architecture is documented in a public SPEC
- Celestia — maintains an OpenTelemetry collector endpoint (`otel.celestia.observer`) for DA nodes, plus a Prometheus-based observability stack for consensus nodes

This is not an exotic idea. It is how mature networks gain visibility into their health, diagnose issues faster, and make data-driven protocol decisions.

In many blockchain networks, node telemetry is collected without operators being fully aware of it — telemetry is often enabled by default in the node software, and in some cases operators have no way to disable it at all.

By contrast, the Gonka Node Observability Platform is designed as a fully opt-in system — validators choose to participate, and no data is collected without their explicit action.

The more validators that join, the more accurate and complete the picture of network health becomes. A platform with 30% of validators connected provides useful insights; one with 80% becomes a reliable source of truth for the entire ecosystem.

---

## 4. Proposed Solution

### Gonka Node Observability Platform

A managed, open-source observability stack where validator operators voluntarily push off-chain metrics to a shared platform maintained by INC4.

### Design principles

| Principle | Implementation |
|-----------|---------------|
| Open-source | All exporters, dashboards, alert rules, and configuration will be open-source and available for audit by any interested party |
| Opt-in | Participation is voluntary, no validator is required to share data — but every participant makes the platform more valuable for the entire network |
| Push-based | Nodes push metrics outbound via HTTPS, no new inbound ports required, existing firewall configs are preserved |
| Non-intrusive | The platform is a separate layer — it does not interact with consensus, block production, or inference execution, a platform outage has zero effect on the Gonka network |
| Privacy | The platform will only collect metrics necessary to understand validator health and performance — such as block height, sync status, miss rate, GPU utilization, container status, resource usage, etc. No sensitive information will be collected — no private keys, wallet balances, mnemonic phrases, or account credentials |

### Value delivered

For the Core Team:
- Aggregated fleet-wide metrics and logs in one place
- Instant visibility into problematic nodes, epochs, and time periods
- SLA reports and data-driven decision making for protocol upgrades
- Incident response support with root cause analysis

For validators:
- No need to build and maintain your own monitoring stack
- Compare your node's performance against network averages
- Receive alerts via Telegram or Discord when something goes wrong
- Share logs for collaborative troubleshooting when experiencing issues
- Access dashboards from any device, including mobile
- Hands-on help with metrics interpretation and incident diagnosis

For the community:
- A single source of truth for network health metrics
- Consistent data that all participants can reference in discussions
- Transparency into network operations

---

## 5. Technical Approach

The platform will be deployed on distributed cloud infrastructure, providing:

- High availability — no single point of failure; redundant infrastructure with 99.5%+ uptime SLA
- Automatic scaling — the platform grows seamlessly as more validators join, with no manual intervention required
- Push-based data collection — validators push metrics outbound via HTTPS; no new inbound ports are required, and existing firewall configurations are fully preserved

We will use well-established, industry-proven tools for observability: Prometheus for metrics collection, Grafana for dashboards and visualization, Alertmanager for notifications, Promtail/Loki for unified opt-in log aggregation, and PagerDuty for incident management and on-call escalation.

INC4 has hands-on experience building and operating observability infrastructure for blockchain networks. The choice of each component in the stack is driven by real-world operational requirements — reliability under load, ease of integration with existing validator setups, minimal resource overhead on the node side, and the ability to scale without rearchitecting as the network grows. This practical experience directly informs the architecture and tooling choices behind this platform.

The detailed architecture, including specific metric definitions, data flows, and exporter specifications, will be documented separately and will evolve as the platform matures.

---

## 6. Scope and Deliverables

| # | Deliverable | Description |
|---|-------------|-------------|
| 1 | Cloud infrastructure | Production-ready observability stack on distributed cloud infrastructure with high availability, redundancy, and data retention |
| 2 | gonka-exporter | Open-source exporter collecting Gonka node and AI compute metrics, kept up to date with every Gonka release |
| 3 | Unified opt-in log aggregation | Searchable log collection from Gonka nodes and ML containers — validators experiencing issues can share logs for collaborative troubleshooting with the community and the Core Team |
| 4 | External endpoint health checks | Automated reachability checks of validator reachability from independent external locations |
| 5 | Fleet Overview Dashboard | Single view of the entire network — node statuses, miss rates, GPU utilization, sync state, and trends over time |
| 6 | Individual Node Dashboard | Per-validator view with historical performance tracking and comparison against network averages |
| 7 | Custom dashboards | Additional dashboards developed on request from the Core Team and individual validators, iteratively improved based on community feedback |
| 8 | Alert rules and SLA reports | Alerting via Telegram, Discord, and PagerDuty. Automated SLA reports for validators and the Core Team |
| 9 | Onboarding documentation | Step-by-step guide for validators to connect to the platform |
| 10 | Validator onboarding | Hands-on onboarding support with a dedicated engineer during the initial rollout, followed by ongoing guidance for new validators |
| 11 | Incident response and advisory | Help for individual validators and the Core Team with metrics interpretation, incident diagnosis, root cause analysis, and post-incident reviews |
| 12 | Ongoing maintenance | Dedicated DevOps team ensuring platform reliability, compatibility with Gonka upgrades, and continuous operational improvements |

---

## 7. Budget and Payment Schedule

### Summary

| Category | Annual Cost | Basis |
|----------|------------|-------|
| Cloud infrastructure | \$18,000 | ~\$1,500/mo for managed Prometheus (metrics storage and querying), Grafana (dashboards and visualization), Alertmanager (notifications), Promtail/Loki (unified opt-in log aggregation), PagerDuty (incident management and on-call escalation), external endpoint health checks, and supporting infrastructure, includes metrics retention, log storage, and high-availability configuration with redundancy |
| Infrastructure operations and maintenance | \$36,000 | DevOps team with a combined allocation of 0.5 FTE (~\$3,000/mo) for platform operations, incident response, compatibility verification after Gonka network upgrades, capacity planning, on-call support, backup and disaster recovery, performance tuning and optimization, access management for connected validators, infrastructure-as-code maintenance, and platform self-monitoring |
| Exporter development and updates | \$12,000 | Development and maintenance of gonka-exporter (Gonka-specific node and AI compute metrics), Promtail log collection configurations, Blackbox exporter probes, integration with node_exporter and GPU metrics exporters, and ongoing compatibility updates for new Gonka releases. Some advanced metrics may require changes to the Gonka node software — INC4 will collaborate with the Core Team to propose and implement the necessary API extensions |
| Custom dashboards and custom alerts | \$12,000 | Fleet overview and individual node dashboards, alert rules with Telegram and Discord notifications, SLA reports, development of custom dashboards on request from the Core Team, personalized dashboards for individual validators on request, and iterative improvements based on ongoing collaboration with the validator community |
| Validator onboarding, incident response, and advisory | \$18,000 | First 3 months — dedicated DevOps engineer for hands-on onboarding of initial validators and end-to-end system setup. Ongoing — documentation maintenance, onboarding guidance for new validators, hands-on support for individual validators and the Core Team in interpreting metrics, diagnosing incidents, coordinating remediation, root cause analysis, actionable recommendations, and post-incident reviews for network-wide events |
| Total requested | \$96,000 | |

### Payment schedule

| Tranche | Period | Amount | Covers |
|---------|--------|--------|--------|
| 1 | Months 1–3 | \$51,000 | Cloud infrastructure setup and provisioning, core exporter and dashboard development, dedicated DevOps engineer for initial validator onboarding |
| 2 | Months 4–6 | \$15,000 | Platform operations, maintenance, incident response, validator support, and continued development of custom dashboards and alert rules |
| 3 | Months 7–9 | \$15,000 | Platform operations, maintenance, incident response, validator support, and iterative improvements to exporters and dashboards based on validator feedback |
| 4 | Months 10–12 | \$15,000 | Platform operations, maintenance, incident response, validator support, and year-end usage and adoption report |

Vesting contact: https://github.com/rwxr-xr-x/gonka-usdt-vesting-schedule

Each tranche is paid on the first day of the respective period.

The first tranche is larger because it covers the infrastructure setup and the most development-intensive phase of the project.

### Risks

- Low validator adoption — INC4 will actively support onboarding and demonstrate platform value through early adopters
- Infrastructure cost growth — the budget includes a reserve; if needed, migration to a more cost-effective solution is possible without service interruption
- Platform does not affect the Gonka network — it operates as a completely separate layer; any platform issue has zero impact on validators or consensus

The budget is calculated for one year. After the first year, the arrangement can be reviewed and renewed on the same or adjusted terms. INC4 will publish a transparent report on platform usage, adoption, and costs at the end of the grant period — giving the community a clear basis for the renewal decision. If the community decides not to renew, the fully configured and operational platform — including all infrastructure, code, and configurations — may be transferred to the Core Team.

---

## 8. Success Criteria

What INC4 delivers:
- Base version of the platform deployed and accepting metrics — within the first week, with continuous improvements and updates going forward
- Exporter, fleet dashboard, and alerting available in base version — within the first month, continuously improved throughout the grant period
- INC4 will actively assist validators who wish to connect — providing hands-on onboarding support alongside documentation in the GitHub repositories
- All code, configurations, and dashboards published in public GitHub repositories — open for anyone to review, audit, or contribute

What depends on the community:
- INC4 will actively support onboarding but cannot guarantee adoption levels, as participation is voluntary
- Target — wide adoption across the network within the first year
- Sunshine scenario: connecting to the platform becomes a standard part of every validator's setup

Key Performance Indicators:
- Platform availability: 99%+ uptime throughout the grant period
- Compatibility: platform verified and operational within 48 hours after each Gonka network upgrade
- Onboarding: any validator can connect to the platform in under 30 minutes using provided documentation
- Reporting: quarterly progress reports published to the community
- Adoption: wide adoption across the network within the first year

---

## 9. Team

- Website: https://inc4.net
- GitHub: https://github.com/inc4

INC4 is an active participant in the Gonka ecosystem. We operate validators on mainnet and testnet, and develop applications for the Gonka network. This proposal grows out of our direct experience — we face the lack of network-wide visibility firsthand as validator operators and want to solve this problem for the entire network.

INC4 is involved in multiple initiatives across the Gonka ecosystem — the observability platform is one of them. For example, we also develop NOP (Node Onboarding Package) — an open-source utility for fast validator deployment (https://github.com/inc4/gonka-nop). Our commitment to the network is long-term and not limited to this proposal.

As a company, INC4 was founded in 2013, with 70+ engineers and 230+ delivered projects in blockchain infrastructure and AI systems. Hands-on experience in building and maintaining mining infrastructure for Bitcoin, Ethereum, Filecoin.
