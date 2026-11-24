---
title: "#2323 — PoC validation: four large DeepSeek hosts have cast no votes since moving to MLNode 4.0.0 pre-release images"
source: https://github.com/gonka-ai/gonka/issues/2323
issue_number: 2323
synced_at: 2026-11-24T21:21:58Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    PoC validation: four large DeepSeek hosts have cast no votes since moving to MLNode 4.0.0 pre-release images
    <span class="issues-number">#2323</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/gafrustam">@gafrustam</a> opened 2026-11-24 20:16 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-11-24 20:16 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
### Summary

Four DeepSeek-V4-Flash hosts commit PoC on every stage but have cast **no PoC validation votes** since late October or mid-November. Each of them went silent right after moving its ML nodes to the MLNode `4.0.0-sigma1` images. Together they hold about 25% of the DeepSeek voting power. Nobody fails PoC because of this yet, but v0.2.17 moves every host to MLNode 4.0.0. I am still investigating and would like to compare notes.

### What we see

| Host | Last full votes | Then |
|---|---|---|
| `gonka1ajmhqgvkf76hss5xe35kcnntqqhs7r8jz8s939` | epoch 432 (14 votes) | Oct 19–22: nodes moved to `4.0.0-sigma1-minimaxxer` / `4.0.0-sigma1-cu12`. From epoch 433: 1–7 votes per stage, from 452: none. All 19 nodes on `4.0.0-sigma3` since Nov 22, still none. |
| `gonka19wskgkz4xwwxa9s80nfx4q97w2ucmcyfezmhjk` | epoch 421 | Rejoined on Nov 3–4 with nodes on `4.0.0-sigma1-cu12`: 4, then 1, then none from 452. |
| `gonka1g9gs3k6e3kstnu487wsycpyrd23typnnzdl2kv` | epochs 452–453 on `4.0.0-sigma2` (10–11 per stage) | Nov 11–13: moved to `4.0.0-sigma1-cu12`. Epoch 454: 4 votes, from 456: none. |
| `gonka1ewlw9wtf0fzpct7hzdmgxc7qkvvv2tj4vh7v62` | never | Joined Nov 13 with all nodes on `4.0.0-sigma1-cu12`. |

Data: stored votes (`poc_v2_validations_for_stage`) for epochs 467–468 and tx bodies of the validation windows for epochs 386–466. A fifth host, `gonka1g0guvdkl08x58lv0xemjeejfakc89ttwex0gz9`, is silent for an unrelated reason: 24 of its 25 nodes are FAILED.

### What it is not

- Not the DAPI build: voting hosts run the same commits.
- Not authz: `MsgSubmitPocValidationsV2` is granted until 2027.
- Not fees: validation messages are in no fee group.
- Not failed transactions: none in all of epoch 467. The votes are never sent.
- Not the image alone: about ten hosts vote fine on `4.0.0-sigma3`.

### Where the votes get lost

Between DAPI handing a job to its ML node and the verdict callback. In the epoch 467 confirmation PoC (trigger 7201938), all 42 nodes of `g9gs3k6e` were idle by block +89 of a 280-block window. In transition epochs, the few votes these hosts sent all came early in the window.

DAPI loses such votes silently (same in v0.2.16, `upgrade-v0.2.17` and `main`):
1. A job the ML node accepted but never answers stays `validateDispatched` and is never re-sent (`decentralized-api/poc/validator.go:990`). On the ML node, a job that throws sends no callback (gonka-vllm-plugins `generate_queue.py:401–404`), and `/stop` clears the queue (`routes.py:867–871`).
2. A job the ML node refuses is retried for about 14 minutes and then abstains.
3. Before dispatch, nodes are stopped one by one with `context.Background()` (`validator.go:1095–1099`). On 4.0.0, `/stop` waits for `drain_poc()`, so a large fleet can use up much of the window. #2188 removes the second pass but keeps the loop.

### Why it matters

A participant passes only with valid votes above 50% of the total network weight, so every silent validator raises the bar for the rest. Today the worst pass in epochs 467–468 is 59.5%, and DeepSeek participants get about 73%. If the same failure spreads with the v0.2.17 move to MLNode 4.0.0, honest DeepSeek hosts can start failing PoC, and more outcomes fall to the guardian tiebreak. Nothing on chain records who validated, and not validating costs a host nothing.

### Questions

- Operators of these hosts: could you share the DAPI line `OffChainValidator: validation complete ...` (or `no nodes available for PoC validation`) and any ML node errors from one PoC? Are you using `POC_WORKER_MINING` or the prefill-max configs?
- Maintainers: did you see validation callbacks go missing with worker mining or prefill-max on testnet?

A small DAPI change would make this visible and recoverable: re-dispatch a job that has no verdict after a timeout, and log dispatched versus answered counts per stage.

</div>

---

> 🔄 **Auto-synced** from [Issue #2323](https://github.com/gonka-ai/gonka/issues/2323) every hour.
