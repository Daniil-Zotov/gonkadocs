---
title: "#2233 — Participant registration timeout issue (improve UX)"
source: https://github.com/gonka-ai/gonka/issues/2233
issue_number: 2233
synced_at: 2026-11-12T03:08:16Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    Participant registration timeout issue (improve UX)
    <span class="issues-number">#2233</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 2026-11-06 06:06 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-11-06 09:39 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #c2e0c6; color: #24292f; border-color: #c2e0c6;">Priority: Low</span></div>
</div>

<div class="issues-content" markdown="1">
```
~ # inferenced register-new-participant \
"$DAPI_API__PUBLIC_URL" 
  "$ACCOUNT_PUBKEY" 
  --node-address "$DAPI_CHAIN_NODE__SEED_API_URL"
No consensus key provided, attempting to auto-fetch from chain node...
Successfully auto-fetched and validated consensus key from chain node
Registering new participant:
Node URL: xxx
Account Address: gonka14uqdfkp0qkxxx
Account Public Key: AvhKJCyo34zmxxx
Validator Consensus Key: JA5lJ7WWXgOBAxxx(auto-fetched)
Seed Node Address: xxx
Sending registration request to http://xxx/v1/participants
Response status code: 200
Participant registration successful.
Waiting for participant to be available (timeout: 30 seconds)...
...............Warning: timeout after 30s waiting for participant to be available
You can manually check your participant at http://xxx/v2/participants/gonka14uqdfkp0qkxp74sdhv9y293mvujn262npx9ncc
Account balance: 0
```
and then i had to exit the container and follow the fix from host quickstart:
```
./inferenced tx inference submit-new-participant \
$PUBLIC_URL \
--validator-key JA5lJ7WWxxx\
--keyring-backend file --home=/xxx \
--from gonka-account-key \
--timeout-duration 1m \
--unordered \
--node $SEED_NODE_RPC_URL \
--chain-id gonka-testnet
```
authors @maria-mitina @d-bogdan-engenious 
</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/maria-mitina">@maria-mitina</a></span>
    <span class="issues-meta-item">commented 2026-11-06 09:39 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@tcharchian we should close it 
since those tests, we have rewritten the code to allow only submit-new-participant to register a participant, and added the fee. This is 2.17 change. 
this bug is gone and the workaround from the bug is now an official way.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #2233](https://github.com/gonka-ai/gonka/issues/2233) every hour.
