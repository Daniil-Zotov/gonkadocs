---
title: "#431 — inferenced:0.2.4 contains outdated hard-coded genesis → AppHash mismatch prevents all nodes from syncing"
source: https://github.com/gonka-ai/gonka/issues/431
issue_number: 431
synced_at: 2026-08-07T16:15:24Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    inferenced:0.2.4 contains outdated hard-coded genesis → AppHash mismatch prevents all nodes from syncing
    <span class="issues-number">#431</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/Asplana92">@Asplana92</a> opened 2025-11-13 20:39 UTC</span>
    <span class="issues-meta-item">6 comments</span>
    <span class="issues-meta-item">Updated 2025-11-15 22:57 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
🚨 TL;DR / Summary

The Docker image ghcr.io/product-science/inferenced:0.2.4 contains a hard-coded outdated genesis, causing a permanent AppHash mismatch with the live chain.
Nodes discover peers, establish MConnection links, but instantly drop all peers due to AppHash validation errors.
StateSync and BlockSync do not work → MLNode pipeline never starts.

This prevents any new operator from joining the network.



🐞 Bug: Outdated hard-coded genesis inside inferenced:0.2.4 → AppHash mismatch prevents sync

Affected Containers (from my test environment)

Node (Chain Node / inferenced): d1720fd3ae413
API: 15d1c336e0fc
Proxy: 2543bb1b2940a



🔍 Problem Description

Even when providing a fresh genesis.json from the repository or a working seed node,
the Chain Node ignores it and uses a baked-in internal genesis.

This results in:

❌ AppHash mismatch
❌ All peers dropped instantly
❌ StateSync never starts
❌ BlockSync never progresses
❌ MLNode stage never begins

Expected AppHash (from baked-in Docker genesis)
       91B9DFB33D5CA4E2A9E18755129512000BDBB6B8B3A458BF02EACB32819EC3FDF

Actual network AppHash (current chain)
       9A3FAFD33F4694FD906B41860C6DA3EA1D5DABF6F6ACB5B8E56CFABBDD8384E13




📜 Logs (AppHash mismatch loop)

ERR error in validation err="wrong Block.Header.AppHash.
Expected 91B9DFB33D5CA4E2A9E18755129512000BDBB6B8B3A458BF02EACB32819EC3FDF,
got 9A3FAFD33F4694FD906B41860C6DA3EA1D5DABF6F6ACB5B8E56CFABBDD8384E13"
module=blocksync



🌱 Additional Issues Identified

1. Trusting Period Problems

A. Light Client expiration
Logs show:
     old header has expired at 2025-08-29

Meaning:

StateSync cannot work at all

trusting period is far in the past

even custom trust_period / trust_height do not help

Light Client rejects all snapshots


B. PEX fails silently
PEX keeps printing:
       We need more addresses. Sending pexRequest...

But:
node drops all peers immediately due to AppHash mismatch
PEX never receives valid peer lists
node loops forever



2. MLNode Integration Blocked (architectural note)

Although MLNode was not deployed in this test, the Chain Node crashes before MLNode can participate.

Consequences:

      Chain Node never reaches a stable height
      API → InferenceD → MLNode pipeline cannot form
      MLNode is unreachable because the base chain never becomes operational

 This is important for debugging distributed execution.




🔁 Reproduction Steps

1. Clone the repo
2. Use the official deploy/join Docker Compose setup
3. Download fresh genesis:
    curl -L https://raw.githubusercontent.com/gonka-ai/gonka/main/genesis/genesis.json -o genesis.json
4. Place it into .inference/config/genesis.json
5. Configure peers from a working seed node
6. Start:
      docker compose up -d
7. Observe AppHash mismatch:
      docker logs node | grep AppHash



🧠 Diagnosis

Root cause:

→ The Docker image inferenced:0.2.4 contains an internal outdated genesis.

Therefore:

The node always expects the old AppHash
Ignores external genesis.json
Rejects all real network blocks
Drops all peers
Fails StateSync
Fails BlockSync
Never reaches MLNode stage



✅ Suggested Fix

1. Regenerate Docker image with updated genesis
or
2. Move genesis outside of the binary (recommended)
Load dynamically (standard in Cosmos/CometBFT chains).
3. Publish a verified genesis hash in documentation
So node operators can validate before launch.



🛠 Suggested PR Enhancement

Automatic fallback when trusting period has expired.

Logic:

If:
       server_time > trusting_period_end

Then:

 disable StateSync

  print warning:
          State Sync disabled — trusting period expired. Network likely requires new genesis or upgrade.

fall back to BlockSync

This improves UX and avoids silent failure loops.




🧪 Environment (for reproducibility)

Hetzner VPS, Ubuntu 24.04, 8GB RAM
Docker 27.x
Compose v2.29
All ports validated
Peers reachable & responsive




🙌 Thank you!
Happy to test patched builds, provide logs, configs, or help verify new images.

   





</div>

---

## 💬 Comments (6)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/gmorgachev">@gmorgachev</a></span>
    <span class="issues-meta-item">commented 2025-11-14 01:08 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Hello! To reproduce from block 1 (assuming that from the message in discord that your node stucked at height=1) you need to start with initial release and apply all upgrades and patches starting v0.2.0:</p>
<pre><code>https://github.com/gonka-ai/gonka/releases/tag/release%2Fv0.2.0
</code></pre>
<p>Version v0.2.4 can be used to load from snapshot's after v0.2.4. Successfully reproduced from <code>genesis.json</code> in repo:</p>
<p><a href="https://github.com/user-attachments/files/23537305/genesis-reproduce.log">genesis-reproduce.log</a>
<a href="https://github.com/user-attachments/files/23537306/genesis-reproduce.md">genesis-reproduce.md</a></p>
<pre><code>&gt; sha256sum genesis.json
47ab596779fce181882bfcc62c7588947a76ac9d0f49d87cb3a6336ae59ff210  genesis.json
</code></pre>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/Asplana92">@Asplana92</a></span>
    <span class="issues-meta-item">commented 2025-11-14 02:20 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Hi Gleb, thanks for the detailed explanation!</p>
<p>I understand — to reproduce the block-1 issue, I need to start from the initial version and apply all updates incrementally starting from v0.2.0.</p>
<p>Here is some additional info from my side:</p>
<p>✅ My setup</p>
<p>Fresh server (Hetzner, Ubuntu 22.04)</p>
<p>Docker 27.3.1</p>
<p>I followed the current official instructions in deploy/join</p>
<p>The genesis I used was taken directly from the repository:
https://raw.githubusercontent.com/gonka-ai/gonka/refs/heads/main/genesis/genesis.json</p>
<p>❗️Observed mismatch</p>
<p>Even with the official genesis.json, I consistently get:</p>
<p>Image expects AppHash:
91B9DFB33D5CA24E9187551295120008BDBB6B8B3A458BF02EACB32B19EC3FDF</p>
<p>Network reports AppHash:
9A3FAFD33F4694FD906B41860C6D3AE1DA5DA8F6F6A8C58BE56CFABBD8384E13</p>
<p>The node discovers peers, RPC works, but it gets stuck at height 1 with a permanent AppHash mismatch.</p>
<p>📎 My genesis file (from repo)</p>
<p>Gist link:
https://gist.github.com/Asplana92/f35e0b7cf7cf0c4c50ef0644fea3e4e6</p>
<p>Let me know if you need:</p>
<p>my full docker logs</p>
<p>the exact steps I followed</p>
<p>or if you want me to test with version v0.2.0</p>
<p>Happy to help reproduce and debug this! 🙌</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/Asplana92">@Asplana92</a></span>
    <span class="issues-meta-item">commented 2025-11-14 02:32 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>I understand that v0.2.4 requires either:
- A) Starting from v0.2.0 and upgrading through all versions
- B) Using a snapshot created after v0.2.4</p>
<p><strong>My situation:</strong>
✅ Genesis hash is correct: 47ab596779fce181882bfcc62c7588947a76ac9d0f49d87cb3a6336ae59ff210
✅ 10 peers connected
❌ Node stuck at height 0 with State Sync enabled (continuously discovering snapshots)</p>
<p><strong>Questions:</strong>
1. Is there an official snapshot URL I can download for v0.2.4?
2. If I disable State Sync, will v0.2.4 work for syncing from block 1, or do I MUST upgrade from v0.2.0?</p>
<p>Your reproduction succeeded with genesis.json - did you disable State Sync or use a snapshot?</p>
<p><strong>My preference:</strong> Use snapshot (Option B) if available, as it's faster for new deployments.</p>
<p>Thank you for your help! 🚀</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/Asplana92">@Asplana92</a></span>
    <span class="issues-meta-item">commented 2025-11-14 03:19 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@glebmorgachev,
Thank you for confirming the upgrade path from v0.2.0!</p>
<p>Before I start the full sync process from v0.2.0, I have one important question:</p>
<p>Do you have an official snapshot for v0.2.4?</p>
<p>You mentioned that “v0.2.4 can be used to load from snapshots created after v0.2.4.”
If such a snapshot exists, could you please share:</p>
<p>📥 Download URL</p>
<p>📊 Snapshot height</p>
<p>📝 Any restoration instructions</p>
<p>This will significantly help new node operators get started without needing multi-week sync from block 1.</p>
<p>If no snapshot is available yet, I’ll proceed with the full upgrade path.</p>
<p>Thank you very much!</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/gmorgachev">@gmorgachev</a></span>
    <span class="issues-meta-item">commented 2025-11-14 11:00 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>docker compose files in main branch reference pre-build docker containers https://github.com/gonka-ai/gonka/blob/main/deploy/join/docker-compose.yml</p>
<p>The same ones can be built from main branch</p>
<p>The <a href="https://gonka.ai/host/quickstart/">quickstart</a> instruction deploys from snapshot automatically until not disabled explicitly </p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/Asplana92">@Asplana92</a></span>
    <span class="issues-meta-item">commented 2025-11-15 22:57 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Great news — the issue is fully resolved! 🎉<br />
Everything works perfectly now. Thank you so much for the quick help and support!</p>
<p>I’ll wait for the new epoch to start so I can connect again.<br />
Closing the issue — thanks once again! 🚀</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #431](https://github.com/gonka-ai/gonka/issues/431) every hour.
