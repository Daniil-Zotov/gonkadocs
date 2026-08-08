---
title: "#983 — Bug: GET /api/v1/epochs/{N}/participants returns 500 for past epochs (CreatedAtBlockHeight=0)"
source: https://github.com/gonka-ai/gonka/issues/983
issue_number: 983
synced_at: 2026-08-08T09:04:34Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Bug: GET /api/v1/epochs/{N}/participants returns 500 for past epochs (CreatedAtBlockHeight=0)
    <span class="issues-number">#983</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/mingles-agent">@mingles-agent</a> opened 2026-03-31 08:51 UTC</span>
    <span class="issues-meta-item">3 comments</span>
    <span class="issues-meta-item">Updated 2026-08-06 22:28 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
## Bug

`GET /api/v1/epochs/{N}/participants` returns **500 Internal Server Error** for past epochs. Current epoch works fine.

## Repro

```
GET http://node1.gonka.ai:8000/api/v1/epochs/215/participants
→ 500 Internal Server Error: height must be greater than 0, but got 0
```

Epoch 215 consistently reproduces this. Any past epoch where `CreatedAtBlockHeight` was not yet populated will fail.

## Root Cause

In `queryActiveParticipants` (`get_participants_handler.go`):

1. First query (no height) fetches `activeParticipants`
2. `blockHeight := activeParticipants.CreatedAtBlockHeight` — for old epochs this is **0** (field was not populated at storage time)
3. Second call `QueryByKeyWithOptions(..., height=0, prove=true)` — CometBFT rejects `height=0` with the above error

## Fix

Check if `blockHeight == 0` before the second query. If so, skip the proof query and return the first result directly, with a `Warn` log for observability.

Fix is implemented in PR #973.
</div>

---

## 💬 Comments (3)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/bonujel">@bonujel</a></span>
    <span class="issues-meta-item">commented 2026-08-03 09:07 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>This is still reproducible on current <code>main</code> (<code>4fa6be0</code>, Upgrade v0.2.15 #1497) — but the root cause in the description is not the one that fires, and #973 patches a call site that no longer exists.</p>
<p><strong>TL;DR</strong>
- The 500 is real and live.
- It does <strong>not</strong> come from the proof-bearing ABCI query. <code>height=0 + prove=true</code> is accepted.
- It comes from <code>GetValidatorSetByHeight(Height: CreatedAtBlockHeight)</code>, which is fatal.
- The handler moved from <code>decentralized-api/internal/server/public/get_participants_handler.go</code> to <code>common/queryapi/epoch.go</code>, so #973 no longer applies to anything.</p>
<h3>Reproduction</h3>
<p>Drop into <code>common/queryapi/tests/</code>. The stub mirrors the real backend's height contract; each behaviour is sourced in the comment.</p>
<pre><code class="language-go">package queryapitest

// Repro for #983 against current main (common/queryapi/epoch.go).
//
// Stub behaviour, traced through the pinned deps:
//
//   ABCIQuery(Height=0, Prove=true) -&gt; OK.
//     gonka-ai/cosmos-sdk@v0.53.3-ps17-observability baseapp/abci.go:1256
//     CreateQueryContextWithCheckHeader: `isLatest := height == 0`, and the
//     proof guard is only `height == 1 &amp;&amp; prove`. height 0 means &quot;latest&quot;.
//
//   GetValidatorSetByHeight(Height=0) -&gt; error.
//     cmtservice/service.go:128 has no `Height &lt; 1` guard (only `&gt; blockHeight`),
//     and forwards to ValidatorsOutput -&gt; getValidators (validator.go:16) -&gt;
//     CometBFT node.Validators(ctx, &amp;0) -&gt; rpc/core/env.go:177 getHeight, which
//     rejects height &lt;= 0 with &quot;height must be greater than 0, but got 0&quot;.
//
//   GetBlockByHeight(1) -&gt; OK. The handler asks for CreatedAtBlockHeight+1,
//     which is 1 when the field is 0, and 1 is a valid height.

import (
    &quot;context&quot;
    &quot;fmt&quot;
    &quot;net/http&quot;
    &quot;testing&quot;

    &quot;github.com/cosmos/cosmos-sdk/client/grpc/cmtservice&quot;
    &quot;github.com/golang/protobuf/proto&quot;
    inferencetypes &quot;github.com/productscience/inference/x/inference/types&quot;
    &quot;github.com/stretchr/testify/require&quot;
)

type zeroHeightComet struct {
    cmtservice.UnimplementedServiceServer
    value            []byte
    validatorHeights []int64
}

func (s *zeroHeightComet) ABCIQuery(_ context.Context, req *cmtservice.ABCIQueryRequest) (*cmtservice.ABCIQueryResponse, error) {
    if s.value == nil {
        // Old epoch: the field was never populated at storage time.
        ap := inferencetypes.ActiveParticipants{CreatedAtBlockHeight: 0, EpochGroupId: 1}
        var err error
        if s.value, err = proto.Marshal(&amp;ap); err != nil {
            return nil, err
        }
    }
    if req.Prove {
        return &amp;cmtservice.ABCIQueryResponse{
            Code:  0,
            Value: s.value,
            ProofOps: &amp;cmtservice.ProofOps{
                Ops: []cmtservice.ProofOp{{Type: &quot;iavl:v&quot;, Key: []byte(&quot;key&quot;), Data: []byte(&quot;value&quot;)}},
            },
        }, nil
    }
    return &amp;cmtservice.ABCIQueryResponse{Code: 0, Value: s.value}, nil
}

func (s *zeroHeightComet) GetBlockByHeight(_ context.Context, req *cmtservice.GetBlockByHeightRequest) (*cmtservice.GetBlockByHeightResponse, error) {
    if req.Height &lt; 1 {
        return nil, fmt.Errorf(&quot;height must be greater than 0, but got %d&quot;, req.Height)
    }
    return &amp;cmtservice.GetBlockByHeightResponse{
        SdkBlock: &amp;cmtservice.Block{
            Header: cmtservice.Header{Height: req.Height, ChainID: &quot;gonka-test&quot;, AppHash: []byte(&quot;apphash&quot;)},
        },
    }, nil
}

func (s *zeroHeightComet) GetValidatorSetByHeight(_ context.Context, req *cmtservice.GetValidatorSetByHeightRequest) (*cmtservice.GetValidatorSetByHeightResponse, error) {
    s.validatorHeights = append(s.validatorHeights, req.Height)
    if req.Height &lt; 1 {
        return nil, fmt.Errorf(&quot;height must be greater than 0, but got %d&quot;, req.Height)
    }
    return &amp;cmtservice.GetValidatorSetByHeightResponse{Validators: nil}, nil
}

// A past epoch whose ActiveParticipants predates CreatedAtBlockHeight being
// populated must not blow up the endpoint.
func TestIssue983_PastEpochWithZeroCreatedAtBlockHeight(t *testing.T) {
    srv := &amp;zeroHeightComet{}
    h := handlersWithInferenceAndComet(t, &amp;stubEpochParticipantsInference{}, srv)

    ctx, rec := echoContext(t, http.MethodGet, &quot;/v1/epochs/215/participants&quot;)
    err := h.GetEpochParticipants(ctx, &quot;215&quot;)

    t.Logf(&quot;GetValidatorSetByHeight called with heights: %v&quot;, srv.validatorHeights)
    t.Logf(&quot;handler err: %v&quot;, err)
    t.Logf(&quot;recorded status: %d&quot;, rec.Code)

    require.NoError(t, err, &quot;endpoint fails for a past epoch with CreatedAtBlockHeight=0&quot;)
}
</code></pre>
<p>Result (<code>go test ./queryapi/tests/ -run TestIssue983 -v</code>, Go 1.25.9):</p>
<pre><code>ERROR Failed to get validators subsystem=Participants
      error=&quot;rpc error: code = Unknown desc = height must be greater than 0, but got 0&quot;

GetValidatorSetByHeight called with heights: [0]
handler err: code=500, message=height must be greater than 0, but got 0
--- FAIL: TestIssue983_PastEpochWithZeroCreatedAtBlockHeight
</code></pre>
<p>Same error string as the report, reached from a different call than the description claims. Note the proof query in the same run returned normally — <code>height=0 + prove=true</code> is not what breaks.</p>
<h3>Where it actually breaks</h3>
<p><code>common/queryapi/epoch.go</code>:</p>
<ul>
<li><strong>L142–152</strong> — proof query at <code>Height: CreatedAtBlockHeight</code>. With 0 the SDK resolves it to latest, so no error. (Worth noting separately: the proof is then anchored to the latest app hash while verification at L174–186 compares against block <code>CreatedAtBlockHeight+1</code> = 1. Verification fails, but it is log-only, so the endpoint would still answer 200 with a proof that verifies against nothing.)</li>
<li><strong>L163–170</strong> — <code>GetBlockByHeight(CreatedAtBlockHeight + 1)</code> = height 1, valid, and non-fatal anyway. Fine.</li>
<li><strong>L192–198</strong> — <code>GetValidatorSetByHeight(Height: CreatedAtBlockHeight)</code> = 0 → error → <code>return nil, err</code> → <strong>500</strong>. This is the one.</li>
</ul>
<p>The old handler had two fatal zero-height calls (<code>Block</code> and <code>Validators</code>). The move to <code>common/queryapi</code> fixed the first and kept the second.</p>
<h3>Why no test catches it</h3>
<p><code>common/queryapi/tests/epoch_participants_golden_test.go</code> hardcodes <code>CreatedAtBlockHeight: 100</code> (L113), and its <code>GetValidatorSetByHeight</code> stub discards the request entirely (L148, <code>_ *cmtservice.GetValidatorSetByHeightRequest</code>), so the height never reaches an assertion.</p>
<h3>On #973</h3>
<p>It guards the ABCI proof query, which is not the failing call, so it would not have removed the 500 even when it was written. Separately, the function it patches no longer exists on <code>main</code> — <code>get_participants_handler.go</code> is down to 84 lines and holds only <code>getParticipantByAddress</code> / <code>getAccountByAddress</code>. It needs redoing against <code>common/queryapi/epoch.go</code> rather than rebasing.</p>
<h3>Suggested fix</h3>
<p>Guard <code>CreatedAtBlockHeight == 0</code> before the validator-set call in <code>common/queryapi/epoch.go</code>. The design question worth settling first: this endpoint returns <code>ActiveParticipantWithProof</code>, so degrading to a 200 without <code>proof_ops</code> is fail-open on a verification endpoint — a client that does not nil-check would treat unverified data as verified. A 400/404 for epochs that predate the field may be the safer contract. Happy to open a PR either way once the direction is agreed.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/bonujel">@bonujel</a></span>
    <span class="issues-meta-item">commented 2026-08-04 00:55 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Correction to my comment above: I wrote that the 500 is "live". That was not supported — the repro forces <code>CreatedAtBlockHeight = 0</code> through a stub, which shows the code path fails <em>if reached</em>, not that it is reachable.</p>
<p>Checking the public nodes: current epoch is 348 (height 5,377,294), and every past epoch I probed — 1, 5, 50, 100, 200, 215, 300, 330, 340, 344, 346, 347 — returns 404 <code>active participants not found for epoch</code> on both node1 and node2. Only the current epoch returns 200, and its record has <code>created_at_block_height</code> populated (5367703). So on those nodes the zero-height path cannot be exercised at all.</p>
<p>I could not determine why past epochs are unretrievable. Nothing in the module deletes the <code>ActiveParticipants</code> blob (only the <code>ActiveParticipantsSet</code> collection is cleared, and only per-epoch on write), no upgrade handler removes it, and the key format matches what the live proof shows — <code>ActiveParticipants/value/</code> + big-endian epoch + <code>/</code>, which decodes correctly out of epoch 348's <code>proof_ops</code>. By code reading the blob for epoch 347 should be in state and readable. It isn't. So I can't rule out that an archive node serving historical records would still hit this path.</p>
<p>Net:</p>
<ul>
<li>The root-cause correction stands — the error comes from <code>GetValidatorSetByHeight</code>, not the proof-bearing ABCI query.</li>
<li>The note about #973 stands — it patches a call that isn't the failing one, and the function it targets no longer exists on <code>main</code>.</li>
<li><strong>Nobody should spend time on a fix until reachability is settled.</strong> Withdrawing my offer to open a PR for now.</li>
</ul>
<p>The larger question this turned up is probably worth more attention than the original report: <code>/v1/epochs/{N}/participants</code> appears to serve only the current epoch, which would make historical participant data — and the proofs over it — unretrievable through this endpoint. If that is intended, this issue can just be closed. If it is not, that is the thing to look at.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/redstartechno">@redstartechno</a></span>
    <span class="issues-meta-item">commented 2026-08-06 22:28 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Following up on the investigation above: I've opened #1556 fixing the code-level fatal path that was confirmed here — <code>getEpochParticipants</code> no longer sends <code>CreatedAtBlockHeight == 0</code> to <code>GetValidatorSetByHeight</code> (which CometBFT rejects), and instead degrades to an empty <code>validators</code> array, mirroring the function's existing non-fatal <code>GetBlockByHeight</code> handling.</p>
<p>Deliberately <strong>not</strong> marked as fixing this issue: the question raised above — why live public nodes return 404 for all past epochs while no delete path for the <code>ActiveParticipants</code> blob exists in the code — remains open and looks operational (pruning/statesync config) rather than code-level. That still deserves its own investigation.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #983](https://github.com/gonka-ai/gonka/issues/983) every hour.
