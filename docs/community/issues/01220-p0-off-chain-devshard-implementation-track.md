---
title: "#1220 — [P0] Off-chain / devshard implementation track"
source: https://github.com/gonka-ai/gonka/issues/1220
issue_number: 1220
synced_at: 2026-07-06T09:51:48Z
template: issues-main.html
---

> 🔄 **Auto-synced:** from [Issue #1220](https://github.com/gonka-ai/gonka/issues/1220) every 6 hours. 

# 🟢 [P0] Off-chain / devshard implementation track

**Author:** [@tcharchian](https://github.com/tcharchian) · **State:** Open · **Created:** 2026-05-21 22:00 UTC · **Updated:** 2026-06-24 00:31 UTC

**Labels:** `up-for-grabs` `Priority: High`

**Веха:** v0.2.15

---

## 📝 Описание

Open for community contributors. Multiple parallel efforts in this direction are welcome to explore different approaches and accelerate progress.

---

## 💬 Comments (2)

### Комментарий 1 — [@orvionx](https://github.com/orvionx)

*2026-06-22 23:37 UTC*

Hi, @tcharchian 
I’d like to work on this issue.

I reviewed the current `devshard` structure and would like to start with a scoped implementation pass rather than trying to cover the whole off-chain/devshard track at once.

My initial plan is:

1. Review the existing `devshard` packages and current off-chain flow
2. Identify the smallest useful vertical slice that can be implemented and tested
3. Add or improve the missing devshard/off-chain logic
4. Include tests and documentation updates where needed
5. Open a focused PR linked to this issue

Before I start the implementation, could you confirm whether there is a preferred first milestone or acceptance criteria for this track? If there is no strict preference, I can start by proposing a small PR around the current devshard flow and iterate from maintainer feedback.


### Комментарий 2 — [@mtvnastya](https://github.com/mtvnastya)

*2026-06-23 21:31 UTC*

hi @orvionx, thanks for you interest!

I'd say that these milestones are very broad to assess at this stage.
there are some important differences between inference off-chain logic (devshards) and requirements for training.

specifically, because inference is a very well-defined flow and all devshards are doing exactly the same work all the time. 
decentralized training, on the other hand, is a research direction with a lot of open questions regarding particular low-communication training methods, validation mechanisms etc. and it should allow researchers to run experiments, test these approaches and iterate quickly.

the first iteration of how communication with main net will work is proposed [here](https://github.com/gonka-ai/gonka/issues/1219)

I'd suggest to start with reviewing that issue and the corresponding PR with trainshard v0 plan and join the discussion from there.
