---
title: "#1178 — No available public Kimi-K2.6 inference gateways"
source: https://github.com/gonka-ai/gonka/issues/1178
issue_number: 1178
synced_at: 2026-08-10T06:46:24Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    No available public Kimi-K2.6 inference gateways
    <span class="issues-number">#1178</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/sspotanin">@sspotanin</a> opened 2026-05-17 06:11 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-05-18 10:50 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
## Summary

As of 2026-05-17T06:10:54Z, public monitoring shows zero available Kimi-K2.6 gateways, even though the chain still lists Kimi hosts.

## Observed

From `https://gonka.pw/providers`:

```text
monitored_providers=12
kimi_monitored=6
kimi_up=0
andrey-panasenko-gateway-kimi-k26: down, lastError=Probe request timed out before the provider returned a complete response.
gonkagate-kimi-k26: down, lastError=Performance probe was inconclusive because the provider was temporarily unavailable.
gate-joingonka-ai-kimi-k26: down, lastError=Performance probe was inconclusive because the provider was temporarily unavailable.
gonka-api-org-kimi-k26: down, lastError=fetch failed
mingles-gateway-kimi-k26: down
proxy-gonka-gg-kimi-k26: down
```

From `https://gonka.pw/incidents`:

```text
active_incidents=7
Kimi-related active incidents include temporarily unavailable, health probes failing, timeouts before complete response, and fetch failed.
```

From on-chain participants via `http://node2.gonka.ai:8000/v1/epochs/current/participants`:

```text
height=4105642
active_participants=48
kimi_hosts=8
models=[{"model":"Qwen/Qwen3-235B-A22B-Instruct-2507-FP8","hosts":42},{"model":"moonshotai/Kimi-K2.6","hosts":8}]
```

## Expected

At least one public Kimi-K2.6 inference route should be available, or there should be a clear public status/update explaining the outage.

## Reproduction commands

```bash
curl -sS https://gonka.pw/providers \
  | jq -r '"monitored_providers=\(length)", "kimi_monitored=\(map(select((.id|test("kimi|k26")) or ((.modelIds // []) | tostring | test("Kimi|k2.6|k26"))))|length)", "kimi_up=\(map(select(((.id|test("kimi|k26")) or ((.modelIds // []) | tostring | test("Kimi|k2.6|k26"))) and .status == "up"))|length)"'

curl -sS https://gonka.pw/incidents \
  | jq -r '.[] | select(.endedAt == null) | [.providerId, .status, .startedAt, .reason] | @tsv'

curl -sS http://node2.gonka.ai:8000/v1/epochs/current/participants \
  | jq -r '.active_participants.participants | map(.models[]?) | group_by(.) | map({model: .[0], hosts: length})'
```

## Notes

This looks related to public Kimi gateway availability rather than total network size: the chain reports active Kimi hosts, but public Kimi gateways are currently unavailable according to monitoring.
</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/sspotanin">@sspotanin</a></span>
    <span class="issues-meta-item">commented 2026-05-18 10:50 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>works fine today</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1178](https://github.com/gonka-ai/gonka/issues/1178) every hour.
