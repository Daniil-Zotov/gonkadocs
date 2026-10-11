---
title: "#1201 — [P0] Training on Gonka"
source: https://github.com/gonka-ai/gonka/issues/1201
issue_number: 1201
synced_at: 2026-10-11T01:59:11Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    [P0] Training on Gonka
    <span class="issues-number">#1201</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 2026-05-19 23:46 UTC</span>
    <span class="issues-meta-item">2 comments</span>
    <span class="issues-meta-item">Updated 2026-09-29 00:18 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #4cbc0f; color: #24292f; border-color: #4cbc0f;">up-for-grabs</span> <span class="issues-label" style="background-color: #f86c7a; color: #24292f; border-color: #f86c7a;">Priority: High</span></div>
</div>

<div class="issues-content" markdown="1">
## WHAT DOES TRAINING ON GONKA MEAN?
Being able to train frontier-level models is an important long-term goal to make AI fully independent of centralized datacenters.

## What decentralized training implies:
- Geo-distributed
- Trustless
- With no single point of control

## BASIC PRINCIPLES

- Pluralism: Do not to lock the network in on a single team or a single approach
- Anyone can propose their approach
- Community reviews it approves/rejects
- Many approaches and training runs can run at the same time
- Isolation: Training happens in separate self-contained shards based on simple primitives
- Heavy data transfers and all the training coordinations doesn’t mess with the main chain
- Gradualism: Training infrastructure develops gradually as more runs are made and different methods are being established as successful ones.
- Different validation, optimization, communication mechanisms can be tested inside the shards
- The effective ones can be reused and established in the infrastructure

## INFRASTRUCTURE LEVELS

- Shards primitives: open shard, settle shard — prioritized 
- Training primitives: save/exchange artifacts, allreduce, evaluate checkpoint — prioritized 
- Post-training tools: generate synth data/rollout traces, GRPO loss
- RL environments: separate agent containers
- Scaling: research on how to scale everything up

<img width="960" height="540" alt="Image" src="https://github.com/user-attachments/assets/c3664aeb-3073-4fee-9816-8900b8fbb20d" />

<img width="960" height="540" alt="Image" src="https://github.com/user-attachments/assets/89dd43c6-380b-4662-b898-f065d1e53d31" />

Source: https://docs.google.com/presentation/d/1dX26zZLWAlLqdRylKQ5FYIZTlsgEt3ZJKKmw5_5PSxw/edit?slide=id.g380f8445137_1_0#slide=id.g380f8445137_1_0

Discussed on GIP: https://discord.com/channels/1336477374442770503/1415622117629624362/1500920059936116807
</div>

---

## 💬 Comments (2)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/loopghost">@loopghost</a></span>
    <span class="issues-meta-item">commented 2026-09-26 21:24 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>I would like to take a bounded, non-overlapping slice of #1201: a TrainShard Checkpoint Artifact MVP covering the prioritized <code>save/exchange artifacts</code> primitive.</p>
<p>Scope would be a versioned content-addressed checkpoint manifest, resumable quota-bounded transfer and verification inside the existing trainshard run volume, plus a two-host Docker E2E and adversarial tests.</p>
<p>I would not touch #1350 reserve/release, #1618 mesh or run control, #1820 ML experiment/evaluation, allreduce, economics, or mainnet launch.</p>
<p>Mapping this scope to the two milestone diagrams in #1201: it covers the checkpointing and recovery part of M1, First Run. It does not claim all of M1. PR #1790 already owns shard reservation, node allocation, mesh, train-container setup, run control, sync, monitoring surfaces, and an NCCL/DDP allreduce example. Issue #1820 is assigned for the ML part, local verification, and experiment launch, which is the closest owner of the 100M to 500M first-run validation. This claim also excludes M2 dataset generation and distillation, M3 GRPO and verifier integration, M4 full training, and M5 scale and model parallelism.</p>
<p>Proposed acceptance is publish/list/fetch/verify/resume with atomic completion, SHA-256 integrity, existing signed shard authorization, traversal, symlink, special-file, quota, replay and wrong-audience protections, restart recovery, and a byte-identical two-host E2E. The E2E would also prove interrupted resume, corrupt-chunk rollback, unauthorized request rejection, quota failure, and durable state across daemon restart.</p>
<p>ETA: 15 business days after interface confirmation, followed by review fixes.</p>
<p>Suggested reward: 9,000 USDT after acceptance, subject to maintainer review, Host approval, and governance. The calibration basis is the delivered-work payout table in #1584: 6,500 USDT for the testing contribution set, 12,000 USDT for the larger HA delivery set, 11,500 USDT for devshard protocol review and formalization, 23,000 USDT for the broader validation and gateway delivery set, and 36,000 USDT for the multi-release devshard and height-sync work. That figure is for the bounded MVP exactly as scoped above, so scope added during review would be repriced rather than absorbed. It also assumes the current trainshard base stays available: <code>main</code> carries no <code>trainshard/</code> tree today, so this work would branch from the trainshards integration line, and a materially different base would be a schedule change rather than something I would absorb silently.</p>
<p>Before implementation, could maintainers confirm that commit <code>504cb1cb8</code> removed the earlier artifacts command only to narrow v0 scope, and that this checkpoint contract is the desired next primitive? @DimaOrekhovPS, as an assignee here and the author of #1790, you are probably the right person for two of these: which branch a checkpoint PR should target, given <code>main</code> carries no <code>trainshard/</code> tree and #1790 is still open, and whether this primitive is the one you want next or whether it should wait behind run control. I am starting the design, threat model, overlap audit, and test matrix now and will post them before the implementation PR.</p>
<p>If maintainers want a larger M1 integration milestone after interfaces and ownership are confirmed, I can propose it separately with independent acceptance and pricing rather than changing this bounded milestone retroactively.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2026-09-29 00:18 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Hey @loopghost! Thanks for the write-up. Training is an important feature, and contributions there are welcome. The way into this work is the same as in any open-source project: join the design discussions and the reviews of the training PRs already in flight, and pick up tasks once they are marked up for grabs. That public back-and-forth is what makes a contributor's approach visible before anyone takes ownership of a slice. Relevant open-source history belongs in this thread too. Distributed systems, training infrastructure, or similar — please share links. That record is what gets read when someone new shows up with a proposal.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1201](https://github.com/gonka-ai/gonka/issues/1201) every hour.
