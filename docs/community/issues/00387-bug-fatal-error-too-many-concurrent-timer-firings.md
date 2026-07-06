---
title: "#387 — Bug: fatal error: too many concurrent timer firings"
source: https://github.com/gonka-ai/gonka/issues/387
issue_number: 387
synced_at: 2026-07-06T09:53:26Z
template: issues-main.html
---

> 🔄 **Авто-синхронизация:** из [Issue #387](https://github.com/gonka-ai/gonka/issues/387) каждые 6 часов. 

# 🔴 Bug: fatal error: too many concurrent timer firings

**Автор:** [@gmorgachev](https://github.com/gmorgachev) · **Состояние:** Closed · **Создано:** 2025-10-09 05:51 UTC · **Обновлено:** 2026-01-15 22:12 UTC

**Метки:** `bug`

**Веха:** v0.2.6

---

## 📝 Описание

node container restarted due to:
```
fatal error: too many concurrent timer firings

runtime stack:
runtime.throw({0x5422134?, 0x7f3d16444260?})
	/usr/local/go/src/runtime/panic.go:1067 +0x48 fp=0x7f3d164441f8 sp=0x7f3d164441c8 pc=0x4c80e8
runtime.(*timer).unlockAndRun(0xc0027fe250, 0x473246?)
	/usr/local/go/src/runtime/time.go:1076 +0x28e fp=0x7f3d16444260 sp=0x7f3d164441f8 pc=0x4b030e
runtime.(*timers).run(0xc000288290, 0x7e04cdbdb5274)
	/usr/local/go/src/runtime/time.go:1008 +0xf0 fp=0x7f3d16444288 sp=0x7f3d16444260 pc=0x4b0030
runtime.(*timers).check(0xc000288290, 0x0?)
	/usr/local/go/src/runtime/time.go:942 +0x13d fp=0x7f3d164442d0 sp=0x7f3d16444288 pc=0x4afe5d
runtime.stealWork(0x941cbc0?)
	/usr/local/go/src/runtime/proc.go:3687 +0x1f3 fp=0x7f3d16444340 sp=0x7f3d164442d0 pc=0x498433
runtime.findRunnable()
	/usr/local/go/src/runtime/proc.go:3364 +0x405 fp=0x7f3d164444b8 sp=0x7f3d16444340 pc=0x497485
runtime.schedule()
	/usr/local/go/src/runtime/proc.go:3995 +0xb1 fp=0x7f3d164444f0 sp=0x7f3d164444b8 pc=0x498eb1
runtime.park_m(0xc00042ec40)
	/usr/local/go/src/runtime/proc.go:4102 +0x1eb fp=0x7f3d16444548 sp=0x7f3d164444f0 pc=0x4992cb
runtime.mcall()
	/usr/local/go/src/runtime/asm_amd64.s:459 +0x4e fp=0x7f3d164445
```


[node-failure-oct8.log](https://github.com/user-attachments/files/22790665/node-failure-oct8.log)

---

## 💬 Комментарии (2)

### Комментарий 1 — [@gmorgachev](https://github.com/gmorgachev)

*2025-10-19 04:36 UTC*

One more case:
[issue-4.log](https://github.com/user-attachments/files/22988429/issue-4.log)

### Комментарий 2 — [@gmorgachev](https://github.com/gmorgachev)

*2025-11-22 00:53 UTC*

Seems like we need to bump go version: https://github.com/golang/go/issues/69880
TODO: propoperly test compartibility
