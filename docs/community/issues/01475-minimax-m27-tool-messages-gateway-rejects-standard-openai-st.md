---
title: "#1475 — MiniMax-M2.7 tool messages: gateway rejects standard OpenAI string content instead of normalizing it"
source: https://github.com/gonka-ai/gonka/issues/1475
issue_number: 1475
synced_at: 2026-08-09T23:51:34Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    MiniMax-M2.7 tool messages: gateway rejects standard OpenAI string content instead of normalizing it
    <span class="issues-number">#1475</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/Ryanchen911">@Ryanchen911</a> opened 2026-07-18 15:51 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-07-20 01:46 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
## Summary

The devshard gateway (`devshardctl`) rejects standard OpenAI-format `role:"tool"`
messages for MiniMax-M2.7 with an HTTP 400, when their `content` is a plain string
(the most common and spec-compliant OpenAI shape). Multi-turn tool-calling
requests from standard OpenAI clients (coding agents, etc.) fail as a result.

## Where this comes from

Introduced in **#1427 (Aggregated gateway fixes, @gmorgachev)**, which added the
`messagevalidators` package. The MiniMax tool-message content shape is enforced by:

- `devshard/cmd/devshardctl/messagevalidators/minimax_tool_message.go`
  ```go
  ErrMinimaxToolContentShape = errors.New("content: must be a non-empty array of {name,type,text} objects")
  ```
- Wired in `devshard/cmd/devshardctl/request_filters_messages.go` as the
  `ContentValidator` on `modelRoles[miniMaxM27ModelID][tool]`.

Present in `release/v0.2.13-devshard-v3.0.0` / `release/devshard/v3.0.0` /
`release/v0.2.14-testnet-7`. Observed on running image
`ghcr.io/gonka-ai/devshard-gateway:mainnet-v0.2.13-v3-post1`.

## The design gap

For MiniMax-M2.7, the normalizer chain deliberately **skips** the `tool` role:

```go
messagevalidators.EmptyContentNormalizer{ SkipRoles: []string{"tool"} },
messagevalidators.TextPartsFlattener{     SkipRoles: []string{"tool"} },
```

...and then attaches a **validate-only** `MinimaxToolMessage` validator. So the
gateway *knows* MiniMax needs `content` as a `[{name,type,text}]` array, but instead
of normalizing string content up to that shape, it hard-rejects with 400. This
pushes a MiniMax-specific quirk onto every OpenAI-compatible caller, which
contradicts the OpenAI-compat contract.

## Log evidence (production, mainnet-v0.2.13-v3-post1)

`devshardctl` emits its own parse-failure stage — this is not an upstream
passthrough error:

```
stage=gateway_parse_failed error="messages[2].content: must be a non-empty array of {name,type,text} objects: not an array"
stage=gateway_parse_failed error="messages[3].content: must be a non-empty array of {name,type,text} objects: not an array"
stage=gateway_parse_failed error="messages[9].content: must be a non-empty array of {name,type,text} objects: not an array"
stage=gateway_parse_failed error="messages[15].content: must be a non-empty array of {name,type,text} objects: not an array"
```

Surfaced to callers (via new-api) as:
```
channel error (channel #3, status code: 400): messages[N].content: must be a non-empty array of {name,type,text} objects: not an array   type=upstream_error
```

Notes:
- The failing index is never `messages[0]` — always a mid-conversation
  `tool` message in multi-turn tool-calling flows. The first user turn (string
  content) passes; the tool-result turns fail.
- In the same window MiniMax-M2.7 served 183k+ `status=200` responses, so this is
  purely the tool-message content shape, not a backend/model issue.

## Proposed fix

Add a `tool`-role content normalizer for MiniMax-M2.7 (mirroring the existing
`TextPartsFlattener` / `EmptyContentNormalizer` pattern) that upgrades a plain
string `content` into the required array shape before validation, e.g.:

```json
{"role":"tool","tool_call_id":"call_x","content":"result text"}
```
->
```json
{"role":"tool","content":[{"name":"<tool name>","type":"text","text":"result text"}]}
```

The existing caps in `request_filters_config.go` still apply after normalization
(MaxEntries=16, NameMaxLen=64, TextMaxSize=64KiB, closed {name,type,text} key
allow-list). This keeps the SGLang #16057 defensive intent while restoring
OpenAI-compat for standard clients.

Doc reference: `docs/chat-api/minimax-m2.7.md`.

cc @gmorgachev

</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/Ryanchen911">@Ryanchen911</a></span>
    <span class="issues-meta-item">commented 2026-07-20 01:46 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Thanks — this looks already fixed by #1467 (<code>fix(gateway): minimax tools regression</code>, merged into <code>upgrade-v0.2.14</code>), which removes the <code>MinimaxToolMessage</code> array-shape validator so <code>role:"tool"</code> messages accept standard OpenAI string content again (unified <code>ValidateRequiredContentField</code> path for all models). Closing as duplicate. Now just waiting for a mainnet gateway image containing #1467 — the currently deployed <code>mainnet-v0.2.13-v3-post1</code> still carries the pre-fix validator.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1475](https://github.com/gonka-ai/gonka/issues/1475) every hour.
