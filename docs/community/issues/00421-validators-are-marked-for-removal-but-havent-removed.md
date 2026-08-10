---
title: "#421 — Validators are marked for removal but haven't removed"
source: https://github.com/gonka-ai/gonka/issues/421
issue_number: 421
synced_at: 2026-08-10T02:40:27Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Validators are marked for removal but haven't removed
    <span class="issues-number">#421</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/gmorgachev">@gmorgachev</a> opened 2025-11-07 22:56 UTC</span>
    <span class="issues-meta-item">3 comments</span>
    <span class="issues-meta-item">Updated 2026-02-12 15:25 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #d73a4a; color: #ffffff; border-color: #d73a4a;">bug</span> <span class="issues-label" style="background-color: #4cbc0f; color: #24292f; border-color: #4cbc0f;">up-for-grabs</span></div>
</div>

<div class="issues-content" markdown="1">
Validators are marked for removal but haven't removed. Happens in cosmos-sdk 
```
7:48AM INF marking validator for removal (not in compute results) jailed=false module=x/staking operator=gonkavaloper1p5zz3d87hy5gn5jphhnljkv7pg06xj6gaa7g6p status=BOND_STATUS_UNBONDED
7:48AM INF marking validator for removal (not in compute results) jailed=false module=x/staking operator=gonkavaloper1rqpallfz6y9nukjhyvcv27zwtjptxph0qtvsjf status=BOND_STATUS_UNBONDING
7:48AM INF marking validator for removal (not in compute results) jailed=false module=x/staking operator=gonkavaloper1rk4ftnqp2pehy0scq3nl3d7nwe0ssq32jpyn9f status=BOND_STATUS_UNBONDING
7:48AM INF marking validator for removal (not in compute results) jailed=false module=x/staking operator=gonkavaloper1pu7kmkx300rj02z7tjffhkdtnas7cdcymcgzqm status=BOND_STATUS_UNBONDING
7:48AM INF marking validator for removal (not in compute results) jailed=false module=x/staking operator=gonkavaloper1yqamx9y94xnytgp9dzped2av7th6r8a57r56ls status=BOND_STATUS_UNBONDING
7:48AM INF marking validator for removal (not in compute results) jailed=false module=x/staking operator=gonkavaloper1d22n3vhrslellmxecscr49m0wtv6fva4gavcya status=BOND_STATUS_UNBONDING
7:48AM INF marking validator for removal (not in compute results) jailed=false module=x/staking operator=gonkavaloper1lzwf6hx5qlct2dx5szj4yrqappxjfzh0eft38s status=BOND_STATUS_UNBONDING
7:48AM INF marking validator for removal (not in compute results) jailed=false module=x/staking operator=gonkavaloper1x7zh2277spp7jfqjhv0g5mnezg290xdrfkswym status=BOND_STATUS_UNBONDING
7:48AM INF marking validator for removal (not in compute results) jailed=false module=x/staking operator=gonkavaloper1ap0lnyema9tt9mld8zgf6kl0ptqj8z5g5mh3ec status=BOND_STATUS_UNBONDING
7:48AM INF marking validator for removal (not in compute results) jailed=false module=x/staking operator=gonkavaloper18lluv53n4h9z34qu20vxcvypgdkhsg6n02fcaq status=BOND_STATUS_UNBONDING
7:48AM INF marking validator for removal (not in compute results) jailed=false module=x/staking operator=gonkavaloper1jjm60sezst40nmtmj6l0cj0evax7lyg8lhv023 status=BOND_STATUS_UNBONDING
7:48AM INF marking validator for removal (not in compute results) jailed=false module=x/staking operator=gonkavaloper1sqwpuxkspyp483l64knd5rp6qp56ymj4s6f6sh status=BOND_STATUS_UNBONDING
7:48AM INF marking validator for removal (not in compute results) jailed=false module=x/staking operator=gonkavaloper1ygv9tv8fthcd43xeehfwagvrud66w9lvt9u3cg status=BOND_STATUS_UNBONDING
7:48AM INF marking validator for removal (not in compute results) jailed=false module=x/staking operator=gonkavaloper1lf8zrnapty4nny6l9dr66nd7xc4j4ktrxrd4qs status=BOND_STATUS_UNBONDING
7:48AM INF marking validator for removal (not in compute results) jailed=false module=x/staking operator=gonkavaloper1pzuq9ygxfrcp5e6qdzu2py5qgcw5gqvd978vcx status=BOND_STATUS_BONDED
7:48AM INF marking validator for removal (not in compute results) jailed=false module=x/staking operator=gonkavaloper16rt63h7ens8dvnf5nhl7yxtkkw7pc7q0ux6ckt status=BOND_STATUS_UNBONDING
7:48AM INF marking validator for removal (not in compute results) jailed=true module=x/staking operator=gonkavaloper1ux4gjvk07z6utgjqs3ttwk9lzr4cn7y0k295rn status=BOND_STATUS_UNBONDING
```



Happens here:
https://github.com/gonka-ai/cosmos-sdk/blob/1ace5dd25d1a78f6b189cbdfec9b76839fe45a20/x/staking/keeper/compute.go#L166
</div>

---

## 💬 Comments (3)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2026-01-28 22:19 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Needs to be rechecked</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/AlexeySamosadov">@AlexeySamosadov</a></span>
    <span class="issues-meta-item">commented 2026-02-08 15:16 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>PR: https://github.com/gonka-ai/gonka/pull/720</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/AlexeySamosadov">@AlexeySamosadov</a></span>
    <span class="issues-meta-item">commented 2026-02-12 15:25 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>I already have a PR for this: #720 — it implements validator removal cleanup hooks. Would appreciate a review when you get a chance.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #421](https://github.com/gonka-ai/gonka/issues/421) every hour.
