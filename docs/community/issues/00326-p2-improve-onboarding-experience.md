---
title: "#326 — [P2] Improve onboarding experience"
source: https://github.com/gonka-ai/gonka/issues/326
issue_number: 326
synced_at: 2026-07-06T09:51:46Z
---

> 🔄 **Авто-синхронизация:** из [Issue #326](https://github.com/gonka-ai/gonka/issues/326) каждые 6 часов. 

# 🟢 [P2] Improve onboarding experience

**Автор:** [@tcharchian](https://github.com/tcharchian) · **Состояние:** Open · **Создано:** 2025-09-03 23:10 UTC · **Обновлено:** 2026-06-24 01:10 UTC

**Веха:** v0.2.15

---

## 📝 Описание

Improve onboarding experience: 

- [ ] Clearer logging when node is launched and waiting for PoC
- [ ] remove errors which doesn’t mean errors
- [ ] automatic testing that everything will work when PoC starts (models can be deployed, all endpoints are accessible); 
- [ ] Clean up logs to avoid confusing ERROR messages;

Description of the proposal: 
[https://github.com/gonka-ai/gonka/blob/a2a15267ea4aa55288fc873f4e5e68bc69366447/proposals/onboarding-clarity-v1/README.md](https://www.google.com/url?q=https://github.com/gonka-ai/gonka/blob/a2a15267ea4aa55288fc873f4e5e68bc69366447/proposals/onboarding-clarity-v1/README.md&sa=D&source=docs&ust=1756918029145609&usg=AOvVaw3j8xsw5yvYWpDeCcVHBhZY)

---

## 💬 Комментарии (4)

### Комментарий 1 — [@Pegasus-starry](https://github.com/Pegasus-starry)

*2025-12-08 18:47 UTC*

1. How to judge if participant is actually in active set?  Is it the state from client: "current_status": "INFERENCE"?
2. About "Pre-PoC Validation Flow...Manual testing request through admin interface...Send test inference request and validate response".  How to do this scenario? Is it to invoke mlnode interface "/v1/pow/init/generate" of mlnode in directory decentralized-api/internal/server/admin/?
3. About "Provide countdown timers for user interfaces & Alert users when they should be online."，is it need to provide one new interface and where the countdown info should be shown?  what's more,  how to alert users proactively?  
Or just shown in log ?

### Комментарий 2 — [@DimaOrekhovPS](https://github.com/DimaOrekhovPS)

*2025-12-09 01:15 UTC*

1. You can use query defined in `query_current_epoch_group_data.go` and then iterate over participants. If you need to access this data in `decentralized-api` please make a client with `NewInferenceQueryClient`

2. I think we should create a new admin endpoint, something like `admin/v1/test-poc`, then it should automatically locate all nodes that aren't busy and start PoC by sending `/v1/pow/init/generate` to them. Ideally it should also confirm that it receives the batches back. Maybe it should an external script? @gmorgachev what do you think?

3. I think the proposal just asks to show this info in logs clearly

### Комментарий 3 — [@tcharchian](https://github.com/tcharchian)

*2026-03-21 01:03 UTC*

Hey @zyz-007 @jacky6block @icydark @wushuo-6 @mumu714 @Ryanchen911 @x0152 @akup! It would be great if some of you could sync on the next steps for this pull request and make the needed decisions together. If you are able to move it forward on your own, it could potentially be included in v0.2.12. But overall, this is a nice-to-have rather than something critical.

### Комментарий 4 — [@tcharchian](https://github.com/tcharchian)

*2026-05-22 01:04 UTC*

Hey @zyz-007 @jacky6block @icydark @Ryanchen911 @x0152! It would be great if some of you could sync on the next steps for this issue and make the needed decisions together. If you are able to move it forward on your own, it could potentially be included in v0.2.14. But overall, this is a nice-to-have rather than something critical.

See: https://github.com/gonka-ai/gonka/pull/866#issuecomment-4172544143


