---
title: "#895 — [P0] Allow hosts to vote on timeouts if they haven't yet seen `MsgStartInference`"
source: https://github.com/gonka-ai/gonka/issues/895
issue_number: 895
synced_at: 2026-08-02T09:25:59Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    [P0] Allow hosts to vote on timeouts if they haven't yet seen `MsgStartInference`
    <span class="issues-number">#895</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/dcastro">@dcastro</a> opened 2026-03-16 14:00 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-04-01 23:52 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #aaaaaa; color: #24292f; border-color: #aaaaaa;">devshards</span></div>
</div>

<div class="issues-content" markdown="1">
In the current implementation of the "refused timeout" workflow, we seem to rely on all hosts having seen the inference's `MsgStartInference` before the user calls for a vote.
If a user calls for a vote, and a Host does not yet have the inference in its `EscrowState`, then it votes "no" (function `VerifyRefusedTimeout`)

This seems like a problem, the mechanism will only work if the user is continuously doing full rounds every 60s (in a `devshard` of 128 hosts, that's 128 inferences per minute). If the rate is slower than that, or if the user is close to being done with the `devshard`, the mechanism stops working, and the user is unable to assert that an inference was refused.

----

One possible solution could be: Instead of checking if the inference exists in `EscrowState`, we could make the request `VerifyTimeoutRequest` carry the inference itself.
And then `VerifyRefusedTimeout` would vote against that inference instead.

We would have to skip the "inference status" check in `VerifyRefusedTimeout`, but that's ok. That means a host would potentially be able to vote "yes" on an inference that is e.g. already finished, but later hosts would reject `MsgTimeoutInference` if the user attempts to include it in a diff. So such "yes" votes would be useless. 

----

A simpler alternative could be to have the user propagate all created Diffs with signatures when requesting timeout votes. 
The host would first apply the diffs, and then vote on the timeout.

NOTE: we should generalize this, so that _all_ requests sent by the user include the catchup diffs.

---

Some tests currently do a full round through hosts to sync up their states, e.g. in `TestHTTP_TimeoutRefused`:

```go
	// Catch up all non-executor hosts so they have the inference state.
	allDiffs := env.session.Diffs()
	for i, h := range env.hosts {
		if i == 1 {
			continue
		}
		_, err := h.HandleRequest(ctx, host.HostRequest{Diffs: allDiffs, Nonce: allDiffs[len(allDiffs)-1].Nonce})
		require.NoError(t, err)
	}
```

We should remove such checks and ensure the tests still pass.
We should also have a look at the e2e testermint tests.
</div>

---

> 🔄 **Auto-synced** from [Issue #895](https://github.com/gonka-ai/gonka/issues/895) every hour.
