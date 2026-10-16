---
title: "#2012 — [BUG] Host in training rejects POC challenge but on-chain status of POC - generating"
source: https://github.com/gonka-ai/gonka/issues/2012
issue_number: 2012
synced_at: 2026-10-16T23:41:02Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    [BUG] Host in training rejects POC challenge but on-chain status of POC - generating
    <span class="issues-number">#2012</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/maria-mitina">@maria-mitina</a> opened 2026-10-15 09:40 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-10-15 21:51 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #d73a4a; color: #ffffff; border-color: #d73a4a;">bug</span></div>
</div>

<div class="issues-content" markdown="1">
## Summary
A host in training is not supposed to be reserved for a POC challenge. 

Training host:
```
decentai@702112:/srv/dai/gonka/deploy/join$ INFB=/srv/dai/gonka/inference-chain/build/linux/amd64/inferenced; NODE=http://127.0.0.1:8000/chain-rpc/
$INFB query inference training-node-reservations gonka197twxyr3j0a8uqdk9a25z7yfz6jk2e7tpqzrkz -o json --node $NODE
$INFB query inference active-trainshards -o json --node $NODE | jq '.. | objects | select(has("expires_at_height")) | {id, status, expires_at_height, creator}'
docker ps --format '{{.Names}} {{.Status}}' | grep trainshard-
{
  "node_ids": [
    "node1"
  ]
}
{
  "id": null,
  "status": "TRAINSHARD_STATUS_ACTIVE",
  "expires_at_height": "34961",
  "creator": "gonka197twxyr3j0a8uqdk9a25z7yfz6jk2e7tpqzrkz"
}
trainshard-11-node1 Up 22 minutes
trainshard-11-node1-net Up 22 minutes
decentai@702112:/srv/dai/gonka/deploy/join$
```


But POC challenge was marked as ongoing and status generating:
```
decentai@702127:/srv/dai/gonka/deploy/join$ cat /tmp/chal.json | tail -1 | jq '{code, txhash}'      # the successful tx
docker exec node $INF q inference open-poc-challenges -o json \
  | jq '.challenges[] | {target:.challenge.target, challenger:.challenge.challenger,
        start:.challenge.start_height, finish, generating, locked:.challenge.locked_payment, commits:(.commits|length)}'
parse error: Invalid numeric literal at line 1, column 4
{
  "target": "gonka197twxyr3j0a8uqdk9a25z7yfz6jk2e7tpqzrkz",
  "challenger": "gonka1l6dcl83kdv2ujn6uls8q92e4lt6ylqrj2pctcg",
  "start": "30167",
  "finish": "30390",
  "generating": true,
  "locked": "7062332259334",
  "commits": 0
}
decentai@702127:/srv/dai/gonka/deploy/join$ docker exec node $INF q inference all-poc-v2-store-commits 30166 -o j
{}
```
</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/x0152">@x0152</a></span>
    <span class="issues-meta-item">commented 2026-10-15 21:22 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>https://github.com/gonka-ai/gonka/commit/0853195ca2da7bb7553805ba26be9d0fb03ffaf1</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #2012](https://github.com/gonka-ai/gonka/issues/2012) every hour.
