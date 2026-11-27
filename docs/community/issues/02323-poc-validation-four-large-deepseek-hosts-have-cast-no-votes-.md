---
title: "#2323 — PoC validation: four large DeepSeek hosts have cast no votes since moving to MLNode 4.0.0 pre-release images"
source: https://github.com/gonka-ai/gonka/issues/2323
issue_number: 2323
synced_at: 2026-11-27T11:00:01Z
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
    <span class="issues-meta-item">3 comments</span>
    <span class="issues-meta-item">Updated 2026-11-25 11:22 UTC</span>
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

Between DAPI handing a job to its ML node and the verdict callback. In the epoch 467 confirmation PoC (trigger 7201938), all 42 nodes of `…nnzdl2kv` were idle by block +89 of a 280-block window. In transition epochs, the few votes these hosts sent all came early in the window.

DAPI loses such votes silently (same in v0.2.16, `upgrade-v0.2.17` and `main`):
1. A job the ML node accepted but never answers stays `validateDispatched` and is never re-sent (`decentralized-api/poc/validator.go:990`). On the ML node, a job that throws sends no callback (gonka-vllm-plugins `generate_queue.py:401–404`), and `/stop` clears the queue (`routes.py:867–871`).
2. A job the ML node refuses is retried for about 14 minutes and then abstains.
3. Before dispatch, nodes are stopped one by one with `context.Background()` (`validator.go:1095–1099`). ~~On 4.0.0, `/stop` waits for `drain_poc()`~~ (not on today's prefill PoC, see below). #2188 removes the second pass but keeps the loop.

### Why it matters

A participant passes only with valid votes above 50% of the total network weight, so every silent validator raises the bar for the rest. Today the worst pass in epochs 467–468 is 67.6% (by the stage snapshot; corrected in the comment below). If the same failure spreads with the v0.2.17 move to MLNode 4.0.0, honest DeepSeek hosts can start failing PoC, and more outcomes fall to the guardian tiebreak. Nothing on chain records who validated, and not validating costs a host nothing.

### Questions

- Operators of these hosts: could you share the DAPI line `OffChainValidator: validation complete ...` (or `no nodes available for PoC validation`) and any ML node errors from one PoC? (`POC_WORKER_MINING` is not in these images, see below.)
- Maintainers: did you see validation callbacks go missing with worker mining or prefill-max on testnet?

A small DAPI change would make this visible and recoverable: re-dispatch a job that has no verdict after a timeout, and log dispatched versus answered counts per stage.

</div>

---

## 💬 Comments (3)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/gafrustam">@gafrustam</a></span>
    <span class="issues-meta-item">commented 2026-11-25 05:22 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Update: corrections and new data.</p>
<p><strong>1. My weights were wrong.</strong> I used the epoch subgroups' <code>voting_power</code>. The chain decides with the stage snapshot (<code>poc_validation_snapshot</code>, threshold against its <code>total_network_weight</code>). By the snapshot:</p>
<table>
<thead>
<tr>
<th>PoC</th>
<th>silent share of DeepSeek power</th>
<th>worst pass, any model</th>
</tr>
</thead>
<tbody>
<tr>
<td>465</td>
<td>18.5%</td>
<td>95.1%</td>
</tr>
<tr>
<td>466</td>
<td>25.3%</td>
<td>74.7%</td>
</tr>
<tr>
<td>467</td>
<td>23.8%</td>
<td>72.9%</td>
</tr>
<tr>
<td>468</td>
<td>16.6% (<code>…yfezmhjk</code>, <code>…j4vh7v62</code> have 0 power)</td>
<td>67.6% (MiniMax)</td>
</tr>
</tbody>
</table>
<p>The worst pass is 67.6%, not 59.5%. The margin is larger than I wrote.</p>
<p><strong>2. Two of my points do not apply.</strong> I pulled the plugin layers of the images from ghcr. <code>4.0.0-sigma1</code>, <code>-sigma1-cu12</code>, <code>-sigma2</code> and <code>-sigma3</code> pin gonka-poc to <code>e6988c06</code> / <code>c98fc00d</code>, which have no worker mining; only <code>-sigma1-minimaxxer</code> and <code>3.1.0-post3-pfrun0</code> have it. And <code>drain_poc()</code> tracks only decode requests, so <code>/stop</code> does not wait there on today's prefill PoC.</p>
<p><strong>3. It is not the image.</strong> Five hosts with DeepSeek on <code>4.0.0-sigma3</code> voted on every DeepSeek commit in the 14 stages since PoC 465 (one host missed one stage): <code>…s5ryv5le</code>, <code>…gdy552cp</code>, <code>…s7nm6wc5</code> (node1–3.gonka.ai), <code>…599rggst</code>, <code>…nj4gpvz8</code>. The validation code (<code>generate_queue.py</code>, <code>callbacks.py</code>, <code>validation.py</code>, <code>reservation.py</code>) is byte-identical in <code>3.1.0-post3-pfrun0</code>, on which <code>…8jz8s939</code> and <code>…yfezmhjk</code> voted in October, and in <code>4.0.0-sigma3</code>. DAPI commits are the same too. What differs is the fleets: 22–51 ML nodes each, and their setup.</p>
<p>Since Nov 11 no verdict has come back from their 4.0.0 ML nodes on any tag (<code>-sigma1-cu12</code>, <code>-sigma2</code>, <code>-sigma3</code>). Their DAPI still validates: in the Nov 17–18 confirmation PoCs <code>…nnzdl2kv</code> and <code>…8jz8s939</code> voted -1 on <code>…fglnkns2</code> like every other validator, and that vote comes from DAPI's own proof check, with no ML node involved. So jobs are dispatched and lost after that. DAPI sends each job to a random node, so a fleet goes silent only if almost every node drops its job. Only validation goes through the queued <code>/generate</code>, the KV lease, a forward next to live chat and the <code>/validated</code> callback. If any step throws, the node logs <code>Generate job … failed</code> and sends nothing.</p>
<p><strong>Operators:</strong> from one validation window, please grep the ML node logs for <code>Generate job</code>, <code>PoC reservation</code>, <code>borrow</code>, <code>Callback to</code>, <code>Traceback</code>, and share your vLLM args (TP/DP/EP, <code>--max-num-seqs</code>), <code>POC_BATCH_SIZE_DEFAULT</code> and driver version. Your <code>/v1/mlnodes/metrics</code> is off, so we cannot compare from outside.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/vbgd0">@vbgd0</a></span>
    <span class="issues-meta-item">commented 2026-11-25 10:53 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Thanks for the detailed report.</p>
<p>We checked epoch 469 (stage 7229734): 11 of 15 DeepSeek hosts voted, and the same four did not. node1–3.gonka.ai run <code>4.0.0-sigma3</code> and voted on all 15 commits, so we don't see this on that image.</p>
<p>We can confirm two gaps in the code: a validation job that throws on the ML node sends no callback, and DAPI does not re-dispatch a job that was accepted but never answered. A timeout with re-dispatch and dispatched/answered counts sounds reasonable.</p>
<p>To find the cause on these hosts we need ML node logs for one validation window. If their operators can share them, we are happy to take a look.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/gafrustam">@gafrustam</a></span>
    <span class="issues-meta-item">commented 2026-11-25 11:18 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Thanks for checking. 11 of 15 with the same four silent matches what I see in the stage snapshots.</p>
<p>Through the community I found the operator behind these hosts (it looks like one person) and reached him directly. He is looking into it and promised to send ML node logs from a validation window. I'll post them here when I get them.</p>
<p>I'm starting a PR for the DAPI side: after a timeout, re-dispatch a job that has no verdict to another node (once), and log dispatched / answered / re-dispatched counts per stage. It will target <code>upgrade-v0.2.17</code>; tell me if it should go to <code>main</code> instead.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #2323](https://github.com/gonka-ai/gonka/issues/2323) every hour.
