---
title: "#1178 — No available public Kimi-K2.6 inference gateways"
source: https://github.com/gonka-ai/gonka/issues/1178
issue_number: 1178
synced_at: 2026-07-06T09:52:04Z
---

> 🔄 **Авто-синхронизация:** из [Issue #1178](https://github.com/gonka-ai/gonka/issues/1178) каждые 6 часов. 

# 🔴 No available public Kimi-K2.6 inference gateways

**Автор:** [@sspotanin](https://github.com/sspotanin) · **Состояние:** Closed · **Создано:** 2026-05-17 06:11 UTC · **Обновлено:** 2026-05-18 10:50 UTC

---

## 📝 Описание

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

---

## 💬 Комментарии (1)

### Комментарий 1 — [@sspotanin](https://github.com/sspotanin)

*2026-05-18 10:50 UTC*

works fine today
