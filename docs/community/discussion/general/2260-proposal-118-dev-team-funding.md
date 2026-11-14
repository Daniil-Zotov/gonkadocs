---
title: "#2260 — Proposal #118: Dev Team Funding"
source: https://github.com/gonka-ai/gonka/discussions/2260
discussion_number: 2260
category: general
synced_at: 2026-11-14T16:58:53Z
---

> 🔄 **Auto-sync:** from [Discussion #2260](https://github.com/gonka-ai/gonka/discussions/2260) every hour. 

# Proposal #118: Dev Team Funding

**Автор:** [@gmorgachev](https://github.com/gmorgachev) · **Категория:** :speech_balloon: General · **Создано:** 2026-11-11 17:36 UTC · **Обновлено:** 2026-11-12 01:04 UTC

---

## 📝 Описание

Dear Gonka community,

I’m happy to announce that @mtvnastya and I have founded a new company, MillCreek R&D.
We’re building a strong team with deep expertise in the research, development, and marketing of verifiable AI, with a focus on inference and training in distributed, untrusted environments.

You might remember the[ idea](https://github.com/gonka-ai/gonka/discussions/1464) of funding a Dev Team that I brought to your attention several months ago. MillCreek is a spiritual successor to that idea. The details have changed, and the team’s scope of responsibilities has expanded. In our opinion, it now better fits Gonka’s Roadmap and current priorities.
We welcome the establishment of the Gonka Foundation and its commitment to supporting the protocol’s development. We hope MillCreek will be one of the teams the Foundation funds to work on the network in 2027. Right now, however, the Foundation still needs to finish its organizational processes and submit a proposal requesting funding from the community.

That takes time, and we want MillCreek to start working on the protocol as soon as possible. That’s why we’ve launched a proposal to fund the company directly from the Community Pool for two months. We are requesting 866,000 USDT to cover the team’s engineering, technical review, technical marketing, and network support services for Gonka, as well as related infrastructure costs.
You can find more details about the expected scope of work in the proposal description, and we hope you will support it.

Happy to answer your questions!


Proposal: https://gonkascan.com/?page=governance&proposal_id=118
Full descciption: https://github.com/millcreek-rd/gonka-public/blob/f91e281fd9cb16e2a362dd1a4870c8b1d8b0eefc/proposals/funding/README.md

---

## 💬 Комментарии (3)

### Комментарий 1 — [@Dolper](https://github.com/Dolper)

*2026-11-11 17:57 UTC*

Hey @gmorgachev I hope you're doin well. How do you see the role of community contributors who currently receive bounties from the Community Pool? Do you expect the bounty program to change or will it continue as it does today with contributors working alongside MillCreek?

**↳ Ответ от [@gmorgachev](https://github.com/gmorgachev)** · *2026-11-11 18:08 UTC*

> I think for the long-term success of the protocol, independent developers must continue to work together. I expect that independent contributors will continue their work on the protocol alongside MillCreek, and that the bounty program will continue
>
> I've also attached docs with the proposal details

### Комментарий 2 — [@baychak](https://github.com/baychak)

*2026-11-11 19:49 UTC*

Hi Gleb! Glad to hear the bounty program continues.

We (Kaitaku) work on some of the external tracks you list - MLNode/vLLM and hardware testing, observability - so two practical questions:

1. Several items are marked as depending on "additional engineering resources", e.g. bounty teams ([L17](https://github.com/millcreek-rd/gonka-public/blob/f91e281fd9cb16e2a362dd1a4870c8b1d8b0eefc/proposals/funding/README.md?plain=1#L17)). Which of them do you expect bounty teams to pick up in these two months? And how do we agree on scope, price and acceptance before the work starts?
2. Are you planning a short spending summary at the end of the period (team / servers / services / admin), like in [#1464](https://github.com/gonka-ai/gonka/discussions/1464)? That would help with the next funding rounds.

Thanks!

**↳ Ответ от [@gmorgachev](https://github.com/gmorgachev)** · *2026-11-11 21:57 UTC*

> Hi Mykola!
>
> > 1. Several items are marked as depending on "additional engineering resources", e.g. bounty teams ([L17](https://github.com/millcreek-rd/gonka-public/blob/f91e281fd9cb16e2a362dd1a4870c8b1d8b0eefc/proposals/funding/README.md?plain=1#L17)).
>
> About such directions themselves:
> - Image support: the inference engine part is essentially finished. The remaining work is mainly devshard integration, which is fairly simple to implement but may take time to test and audit because it could affect network security. Devshard contributors need enough time to give this proper attention but might lower its priority in favor of other features
> - Large-scale training experiments should start from a concrete experimental goal, with the exact setup depending on an R&D group
> - Work on KV-cache usage and devshard settlement is ongoing with several devshard contributors. I put these items in this category because their delivery depends on work of people inside and outside of such unit 
>
> We don't see this list as a roadmap for the network as a whole but rather as a list of our priorities. It covers directions we think are worth participating in through technical review and advice. Implementing these projects is not explicitly among our goals for the next couple of months. We will provide feedback on both bounty-funded projects in these directions and host-driven initiatives, such as support for specific hardware
>
> On bounties, I think the work should continue in the spirit of a decentralized system, where contributors propose projects to the community, hosts / the Foundation vote on them
>
> From my personal perspective, work in this direction should focus on solving specific problems. With the current volume of inference on the network, we have a working feedback loop to make sure improvements / new features reach production quality. This loop works quite well in devshard development already
>
> > 2. Are you planning a short spending summary at the end of the period?
>
> Yes, we will provide a high-level update on progress and spending at the end of the period

### Комментарий 3 — [@geeky02](https://github.com/geeky02)

*2026-11-12 01:04 UTC*

@gmorgachev 
One question in that direction. You mentioned that bounty projects are proposed by contributors and voted on by Hosts or the Foundation. For the tracks MillCreek lists as needing external engineering (devshard settlement, KV-cache work, observability around MLNode/vLLM), would MillCreek publish scoped items with acceptance criteria as `up-for-grabs` issues, or should contributors draft the scope themselves in a Discussion and have MillCreek review it before Hosts vote? 

For context on where I can help: I'm a backend/AI infra engineer (11 years), mostly Python services, vLLM and local-LLM deployment, Docker/Kubernetes, and distributed-systems debugging. I'm happy to take an MLNode or observability item first, since those overlap most with what I run day to day.
