---
title: "#421 — Validators are marked for removal but haven't removed"
source: https://github.com/gonka-ai/gonka/issues/421
issue_number: 421
synced_at: 2026-07-06T09:52:50Z
template: issues-main.html
---

> 🔄 **Авто-синхронизация:** из [Issue #421](https://github.com/gonka-ai/gonka/issues/421) каждые 6 часов. 

# 🟢 Validators are marked for removal but haven't removed

**Автор:** [@gmorgachev](https://github.com/gmorgachev) · **Состояние:** Open · **Создано:** 2025-11-07 22:56 UTC · **Обновлено:** 2026-02-12 15:25 UTC

**Метки:** `bug` `up-for-grabs`

---

## 📝 Описание

Validators are marked for removal but haven't removed. Happens in cosmos-sdk 
```
7:48AM INF marking validator for removal (not in compute results) jailed=false module=x/staking operator=gonkavaloper1p5zz3d87hy5gn5jphhnljkv7pg06xj6gaa7g6p status=BOND_STATUS_UNBONDED
7:48AM INF marking validator for removal (not in compute results) jailed=false module=x/staking operator=gonkavaloper1rqpallfz6y9nukjhyvcv27zwtjptxph0qtvsjf status=BOND_STATUS_UNBONDING
7:48AM INF marking validator for removal (not in compute results) jailed=false module=x/staking operator=gonkavaloper1rk4ftnqp2pehy0scq3nl3d7nwe0ssq32jpyn9f status=BOND_STATUS_UNBONDING
7:48AM INF marking validator for removal (not in compute results) jailed=false module=x/staking operator=gonkavaloper1pu7kmkx300rj02z7tjffhkdtnas7cdcymcgzqm status=BOND_STATUS_UNBONDING
7:48AM INF marking validator for removal (not in compute results) jailed=false module=x/staking operator=gonkavaloper1yqamx9y94xnytgp9dzped2av7th6r8a57r56ls status=BOND_STATUS_UNBONDING
7:48AM INF marking validator for removal (not in compute results) jailed=false module=x/staking operator=gonkavaloper1d22n3vhrslellmxecscr49m0wtv6fva4gavcya status=BOND_STATUS_UNBONDING
7:48AM INF marking validator for removal (not in compute results) jailed=false module=x/staking operator=gonkavaloper1lzwf6hx5qlct2dx5szj4yrqappxjfzh0eft38s status=BOND_STATUS_UNBONDING
7:48AM INF marking validator for removal (not in compute results) jailed=false module=x/staking operator=gonkavaloper1x7zh2277spp7jfqjhv0g5mnezg290xdrfkswym status=BOND_STATUS_UNBONDING
7:48AM INF marking validator for removal (not in compute results) jailed=false module=x/staking operator=gonkavaloper1ap0lnyema9tt9mld8zgf6kl0ptqj8z5g5mh3ec status=BOND_STATUS_UNBONDING
7:48AM INF marking validator for removal (not in compute results) jailed=false module=x/staking operator=gonkavaloper18lluv53n4h9z34qu20vxcvypgdkhsg6n02fcaq status=BOND_STATUS_UNBONDING
7:48AM INF marking validator for removal (not in compute results) jailed=false module=x/staking operator=gonkavaloper1jjm60sezst40nmtmj6l0cj0evax7lyg8lhv023 status=BOND_STATUS_UNBONDING
7:48AM INF marking validator for removal (not in compute results) jailed=false module=x/staking operator=gonkavaloper1sqwpuxkspyp483l64knd5rp6qp56ymj4s6f6sh status=BOND_STATUS_UNBONDING
7:48AM INF marking validator for removal (not in compute results) jailed=false module=x/staking operator=gonkavaloper1ygv9tv8fthcd43xeehfwagvrud66w9lvt9u3cg status=BOND_STATUS_UNBONDING
7:48AM INF marking validator for removal (not in compute results) jailed=false module=x/staking operator=gonkavaloper1lf8zrnapty4nny6l9dr66nd7xc4j4ktrxrd4qs status=BOND_STATUS_UNBONDING
7:48AM INF marking validator for removal (not in compute results) jailed=false module=x/staking operator=gonkavaloper1pzuq9ygxfrcp5e6qdzu2py5qgcw5gqvd978vcx status=BOND_STATUS_BONDED
7:48AM INF marking validator for removal (not in compute results) jailed=false module=x/staking operator=gonkavaloper16rt63h7ens8dvnf5nhl7yxtkkw7pc7q0ux6ckt status=BOND_STATUS_UNBONDING
7:48AM INF marking validator for removal (not in compute results) jailed=true module=x/staking operator=gonkavaloper1ux4gjvk07z6utgjqs3ttwk9lzr4cn7y0k295rn status=BOND_STATUS_UNBONDING
```



Happens here:
https://github.com/gonka-ai/cosmos-sdk/blob/1ace5dd25d1a78f6b189cbdfec9b76839fe45a20/x/staking/keeper/compute.go#L166

---

## 💬 Комментарии (3)

### Комментарий 1 — [@tcharchian](https://github.com/tcharchian)

*2026-01-28 22:19 UTC*

Needs to be rechecked

### Комментарий 2 — [@AlexeySamosadov](https://github.com/AlexeySamosadov)

*2026-02-08 15:16 UTC*

PR: https://github.com/gonka-ai/gonka/pull/720

### Комментарий 3 — [@AlexeySamosadov](https://github.com/AlexeySamosadov)

*2026-02-12 15:25 UTC*

I already have a PR for this: #720 — it implements validator removal cleanup hooks. Would appreciate a review when you get a chance.
