---
title: "#2032 — Residual: whitespace `InferenceUrl` overwrites a live one"
source: https://github.com/gonka-ai/gonka/issues/2032
issue_number: 2032
synced_at: 2026-10-25T22:39:13Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Residual: whitespace `InferenceUrl` overwrites a live one
    <span class="issues-number">#2032</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/a-kuprin">@a-kuprin</a> opened 2026-10-15 18:01 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-10-15 20:40 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #a2eeef; color: #24292f; border-color: #a2eeef;">enhancement</span></div>
</div>

<div class="issues-content" markdown="1">
# Residual: whitespace `InferenceUrl` overwrites a live one

Raised with https://github.com/gonka-ai/gonka/pull/1792#discussion_r4277929808. The host and gateway now open a session when one participant's URL is blank or the lookup fails, so this no longer refuses Chat. It still deletes the address the rest of the network dials.

A followup to the PR https://github.com/gonka-ai/gonka/pull/2031

## What is wrong

An update with an empty URL is supposed to leave the stored address alone. `TestMsgServer_SubmitNewParticipant_EmptyValuesNoEffect` locks that in: `Url: ""` keeps `http://url`.

`ValidateBasic` treats a whitespace-only URL the same way it treats "not provided". The SSRF check runs only when `strings.TrimSpace(msg.Url) != ""`:

```27:31:inference-chain/x/inference/types/message_submit_new_participant.go
	if strings.TrimSpace(msg.Url) != "" {
		if err := utils.ValidateURLWithSSRFProtection("url", msg.Url); err != nil {
			return err
		}
	}
```

The handler then stores `msg.Url` whenever it is not exactly `""`:

```20:22:inference-chain/x/inference/keeper/msg_server_submit_new_participant.go
		if msg.Url != "" {
			existing.InferenceUrl = msg.Url
		}
```

`"   "` passes validation and replaces a live `InferenceUrl`. The validator-key field already rejects that shape of value (`msg.ValidatorKey != "" && strings.TrimSpace(msg.ValidatorKey) == ""`). The URL field lets it through and writes it.

`InferenceUrl` is the address peers dial for Chat, payload fetch, and peer RPC. After the overwrite that participant has no usable endpoint until they submit a real URL again. They can do that before PoC, so the blank window is temporary and they still look like a normal participant at the boundary. During the window nobody can dial them, and a timeout check against them has no client, so the timeout is accepted without a challenge.

The same message is a footgun. A key rotation that sends a padded URL, meaning "leave the address", silently deletes the registered one.

## Change

Trim before the update, and store the URL only when the trimmed value is non-empty. Whitespace then follows the empty-string rule the handler and `EmptyValuesNoEffect` already describe.

```go
if url := strings.TrimSpace(msg.Url); url != "" {
    existing.InferenceUrl = url
}
```

Store the trimmed value, so a padded real URL (`"  http://host  "`) is not written with the padding. `ValidateBasic` already accepts it and runs SSRF on the untrimmed string; `ValidateURLWithSSRFProtection` should keep seeing the original, and only the stored field is trimmed.

Do the same on create, in `createNewParticipant`: set `InferenceUrl` from the trimmed URL. A first registration of `"   "` currently stores the spaces.

No migration. Participants already stored with a whitespace URL stay that way until they submit a real one. The devshard side already treats a blank trimmed URL as missing.

## Test

Extend `TestMsgServer_SubmitNewParticipant_EmptyValuesNoEffect` (or add a sibling) with a second update whose `Url` is `"   "` and whose keys are `""`. Expect `InferenceUrl`, `ValidatorKey`, and `WorkerPublicKey` unchanged.

Add a create case: `Url: "   "` stores `InferenceUrl == ""`.

</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/redstartechno">@redstartechno</a></span>
    <span class="issues-meta-item">commented 2026-10-15 20:40 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Taking this one: trim <code>msg.Url</code> in the <code>SubmitNewParticipant</code> handler and store it only when the trimmed value is non-empty (update and create paths), with cases added to the existing <code>EmptyValuesNoEffect</code> test. Branch based on <code>upgrade-v0.2.17</code>; PR follows shortly.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #2032](https://github.com/gonka-ai/gonka/issues/2032) every hour.
