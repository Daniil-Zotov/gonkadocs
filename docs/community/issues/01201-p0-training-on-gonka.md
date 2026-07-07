---
title: "#1201 — [P0] Training on Gonka"
source: https://github.com/gonka-ai/gonka/issues/1201
issue_number: 1201
synced_at: 2026-07-07T21:46:05Z
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
    <span class="issues-meta-item">[@tcharchian](https://github.com/tcharchian) opened 2026-05-19 23:46 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-05-21 22:33 UTC</span>
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

> 🔄 **Auto-synced** from [Issue #1201](https://github.com/gonka-ai/gonka/issues/1201) every hour.
