---
title: "#402 — [BUG]: API container doesn't start due to "nats: insufficient resources""
source: https://github.com/gonka-ai/gonka/issues/402
issue_number: 402
synced_at: 2026-07-25T09:15:56Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    [BUG]: API container doesn't start due to "nats: insufficient resources"
    <span class="issues-number">#402</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 2025-10-22 18:36 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-01-15 22:24 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #d73a4a; color: #ffffff; border-color: #d73a4a;">bug</span></div>
</div>

<div class="issues-content" markdown="1">
API container doesn't start with:
```
...
Signature:cebe1551ed35b140dce921e98cb291b77cdf99bb246be8600445e072bb5f453a2b21479f2551074e21da5ce8ee1d835213227f703cf09f5fe2ac3995be75a987 Claimed:false} CurrentHeight:935127 LastProcessedHeight:935127 UpgradePlan:{Name: Height:0 Binaries:map[] NodeVersion:} MLNodeKeyConfig:{WorkerPublicKey: WorkerPrivateKey:} Nats:{Host: Port:0} CurrentNodeVersion:v3.0.8 LastUsedVersion:v3.0.8 ValidationParams:{TimestampExpiration:60 TimestampAdvance:30 ExpirationBlocks:20} BandwidthParams:{EstimatedLimitsPerBlockKb:10752 KbPerInputToken:0.0023 KbPerOutputToken:0.64}}
2025/10/22 08:59:31 INFO starting nats server subsystem=Messages port=4222 host=0.0.0.0
current upgrade name v0.2.3, new upgrade name v0.2.3
current upgrade height 645399, new upgrade height 645399
panic: NATS server not ready after 3 attempts
goroutine 1 [running]:
main.main()
 /app/decentralized-api/main.go:67 +0x16a7
```

There is some interactive action:
```
Error: exit status 2
Config file /root/.dapi/api-config.yaml already exists
```

```
9:02AM INF the current symlink points to: "/root/.dapi/cosmovisor/upgrades/v0.2.3/bin/decentralized-api" module=cosmovisor
file /root/.dapi/cosmovisor/config.toml already exists, do you want to overwrite it? [y/n]: 9:02AM INF file already exists, not overriding module=cosmovisor
```
Did a full down and up.. and it's the same
```
init for nats
9:06AM INF checking on the genesis/bin directory module=cosmovisor
9:06AM INF the "/root/.dapi/cosmovisor/genesis/bin" directory already exists module=cosmovisor
9:06AM INF checking on the genesis/bin executable module=cosmovisor
9:06AM INF the "/root/.dapi/cosmovisor/genesis/bin/decentralized-api" file already exists module=cosmovisor
9:06AM INF making sure "/root/.dapi/cosmovisor/genesis/bin/decentralized-api" is executable module=cosmovisor
9:06AM INF checking on the current symlink and creating it if needed module=cosmovisor
9:06AM INF the current symlink points to: "/root/.dapi/cosmovisor/upgrades/v0.2.3/bin/decentralized-api" module=cosmovisor
file /root/.dapi/cosmovisor/config.toml already exists, do you want to overwrite it? [y/n]: 9:06AM INF file already exists, not overriding module=cosmovisor
9:06AM INF cosmovisor config.toml created at: /root/.dapi/cosmovisor/config.toml module=cosmovisor
Running decentralized-api with cosmovisor
...

2025/10/22 09:06:37 INFO starting nats server subsystem=Messages port=4222 host=0.0.0.0
current upgrade name v0.2.3, new upgrade name v0.2.3
current upgrade height 645399, new upgrade height 645399
panic: NATS server not ready after 3 attempts
```

tried
```
sudo rm .dapi/data/upgrade-info.json
```

```
source config.env && docker compose up --no-deps api --force-recreate -d
```

It seems to be progressing, however i see this in logs:
```
2025/10/22 09:10:45 ERROR tx broadcast, but failed to put in queue subsystem=Messages tx_id=c3ebe871-eb98-4bbe-9628-77147ecc0401 err="nats: insufficient resources" error-type=*nats.APIError
```

They know about 1 issue on connectivity between the two nodes we have.. will fix that

Nats is in the same container...
Then checked disk space / ram

nats storage is in `.dapi/.nats.` trying to find how to check it's size

There is no resource exhaustion on that server
```
root@CL-Gonka-NetNode:~/inference-ignite/deploy/join/.dapi/.nats# du -d1 -h .
17G ./jetstream
17G .
```

Nothing bad should happen if, when api container stopped, we just delete this dir `.dapi/.nats` and then restart

this queue is needed to maintain retry for sending transaction. by some reason it's huge

all important TXS (validation, claim reward) will still be retried

Cleared the queue, started the api container, seems to be working from what they see
```
2025/10/22 09:20:02 INFO Upgrade already ready subsystem=Upgrades name=v0.2.4
```

we should double check that in next upgrade. @gmorgachev assumption is that missed validation transactions were added many times in queue. not sure why another nodes are successfully sending them all 

it might be related to the fact that the node was offline some time ago. Those could have been old queue entries as well

This node just claimed reward for epoch 59 btw. That means no problem with sending transactions now

that part is actually also modified in new PR
</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2025-12-02 20:28 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>This is related to the <a href="https://github.com/gonka-ai/gonka/issues/429">Cleaning nats issue</a> 
NATS didn't delete any items from the queue, so the queues were constantly growing. Setting a limit to NATS messages by age must resolve this problem, too. @0xBECEDA @patimen @gmorgachev </p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #402](https://github.com/gonka-ai/gonka/issues/402) every hour.
