---
title: "#2233 — Participant registration timeout issue (improve UX)"
source: https://github.com/gonka-ai/gonka/issues/2233
issue_number: 2233
synced_at: 2026-11-06T07:03:07Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Participant registration timeout issue (improve UX)
    <span class="issues-number">#2233</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 2026-11-06 06:06 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-11-06 06:20 UTC</span>
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

> 🔄 **Auto-synced** from [Issue #2233](https://github.com/gonka-ai/gonka/issues/2233) every hour.
