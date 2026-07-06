---
title: "#518 — \"Request timestamp is in the future\" leads to missed inferences for hosts"
source: https://github.com/gonka-ai/gonka/issues/518
issue_number: 518
synced_at: 2026-07-06T09:53:13Z
template: issues-main.html
---

> 🔄 **Auto-synced:** from [Issue #518](https://github.com/gonka-ai/gonka/issues/518) every 6 hours. 

# 🔴 "Request timestamp is in the future" leads to missed inferences for hosts

**Author:** [@akup](https://github.com/akup) · **State:** Closed · **Created:** 2026-01-02 06:22 UTC · **Updated:** 2026-01-20 17:55 UTC

**Веха:** v0.2.8

---

## 📝 Описание

# Problem

On load healthy nodes are missing inferences that could be served, that leads to striking the hosts.

# What cause the problem

Sometime network is overloaded and up to 1/3 of network-nodes could be behind latest block that already reached the consensus.
As blocks can be build on load in more then 30 seconds, it leads, that even being behind to one block for host means it is behind more then 30 seconds from the latest consensus block.
It leads, that inference requests could be in the future relative to host network node, that is behind, but it still is functional and can serve inferences. At `decentalized-api` at `post-chat-handler.go` there is a check before node starts processing inference:
```go
if requestOffset < -timestampAdvanceNs {
    logging.Warn("Request timestamp is in the future", types.Inferences,
    	"inferenceId", request.InferenceId,
    	"offset", time.Duration(requestOffset).String())
    return echo.NewHTTPError(http.StatusBadRequest, "Request timestamp is in the future")
}
```
It leads that node is missing inferences, when it is behind consensus block, and **on load even just one block behind** can lead to missed inferences for healthy node that can serve inference requests. And from the side of network that reached the consensus it is ok if inference will be served by api node that is synced to inference-chain node that is behind consensus.

Meanwhile at `inference-chain` it is ok to accept inference finish requests during 1 hour. From the `inference-chain`, `msg_server_finish_inference.go` at `verifyFinishKeys` function:

```go
// Extra seconds for long-running inferences; deduping via inferenceId is primary replay defense
if err := k.validateTimestamp(ctx, devComponents, msg.InferenceId, 60*60); err != nil {
	return err
}
```

it gives 1 hour to send inference finish message, so it can be served in this 1 hour, while `timestamp_advance` is set to 30 seconds.

If api node removes check for 'timestamp is in the future' it will be serving inference and they are accepted by protocol.

# Why we need the request in the future check?

From the side of the chain that tries to reach consensus checking if timestamp is in the future is a kind of protection.

But from the api component it just means that it is syncing with node that is behind consensus. Checking against expired requests can help node to do not serve inferences that will not be accepted by network. But it is not in sync with code at node that adds 1 hour for request expiration.

Checking against request in the future gives nothing to api component, and should be checked against real local machine time.

# Solution

We can check against local machine time at api node, or just add extra seconds, like it is done at chain. We can add less extra-seconds then 1 hour as the check is done before inference, and we need to keep some time for serving inference.

**And this change is not affecting protocol, but only decentralized-api**

# Remarks

1 hour for inference serve seams to be very much and is unreliable from the user side.

# Extra proposal for discussion

p.s.: It seams it could be good for decentralized-api to sync to other seed nodes, when node block time is behind local machine time more then 1 minute. This will lead that if it send PoCs to other node it will loose the voting power per the epoch, but it will generally increase network stability.
The problem of being behind the consensus block is unknown, and it was seen, that restarting the node docker container, makes the node to catch new blocks faster and reach the latest block, so it's not the hardware issue.

---

## 💬 Comments (3)

### Комментарий 1 — [@akup](https://github.com/akup)

*2026-01-02 06:35 UTC*

Also use of hardcoded value 60*60 at node level is VERY BAD.
And it could be fixed by parameters. Moreover it even doesn't need extra parameters, and can use `timestampExpirationNs` and `timestampAdvanceNs` that are regulated by the voting.

### Комментарий 2 — [@trokl1](https://github.com/trokl1)

*2026-01-07 18:31 UTC*

+1, same issue. Node falls behind during PoC, missing inferences. This fix would help.



### Комментарий 3 — [@akup](https://github.com/akup)

*2026-01-14 12:27 UTC*

It is fixed by this PR:
https://github.com/gonka-ai/gonka/pull/549
