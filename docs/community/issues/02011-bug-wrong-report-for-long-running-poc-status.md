---
title: "#2011 — [BUG] Wrong report for long running POC status"
source: https://github.com/gonka-ai/gonka/issues/2011
issue_number: 2011
synced_at: 2026-10-22T22:27:17Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    [BUG] Wrong report for long running POC status
    <span class="issues-number">#2011</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/maria-mitina">@maria-mitina</a> opened 2026-10-15 09:38 UTC</span>
    <span class="issues-meta-item">2 comments</span>
    <span class="issues-meta-item">Updated 2026-10-21 09:38 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #d73a4a; color: #ffffff; border-color: #d73a4a;">bug</span></div>
</div>

<div class="issues-content" markdown="1">
# Wrong reporting on POC challenge status when host rejected it due to training
## Summary
Host which is under training, rejects POC challenge. So it is not generating commits. However, the on-chain status:



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
  **"generating": true,**
  "locked": "7062332259334",
  **"commits": 0**
}
decentai@702127:/srv/dai/gonka/deploy/join$ docker exec node $INF q inference all-poc-v2-store-commits 30166 -o j
{}


```
</div>

---

## 💬 Comments (2)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/x0152">@x0152</a></span>
    <span class="issues-meta-item">commented 2026-10-15 21:22 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>https://github.com/gonka-ai/gonka/commit/0853195ca2da7bb7553805ba26be9d0fb03ffaf1</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/maria-mitina">@maria-mitina</a></span>
    <span class="issues-meta-item">commented 2026-10-21 09:38 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>thank you, working</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #2011](https://github.com/gonka-ai/gonka/issues/2011) every hour.
