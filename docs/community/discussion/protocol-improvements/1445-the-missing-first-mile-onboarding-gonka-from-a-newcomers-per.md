---
title: "#1445 — The missing first mile: onboarding Gonka from a newcomer’s perspective"
source: https://github.com/gonka-ai/gonka/discussions/1445
discussion_number: 1445
category: protocol-improvements
synced_at: 2026-08-06T15:24:01Z
---

> 🔄 **Auto-sync:** from [Discussion #1445](https://github.com/gonka-ai/gonka/discussions/1445) every hour. 

# The missing first mile: onboarding Gonka from a newcomer’s perspective

**Автор:** [@julb1992](https://github.com/julb1992) · **Категория:** :gear: Protocol Improvements · **Создано:** 2026-07-12 20:31 UTC · **Обновлено:** 2026-07-25 11:59 UTC

---

## 📝 Описание

**Motivation**

Over the past two weeks, I have spent a significant amount of time trying to understand Gonka as a non-technical newcomer.

I initially discovered Gonka through GNK. From there, I tried to understand the full economic and technical model: Hosts, GPU economics, PoC, collateral, vesting, GNK vs WGNK, bridging, HeX, NOP, gateways, brokers, devshards, and finally the fundamental role of Developers in the network economy.

The information exists. The documentation is extensive.

The problem I experienced was different: as a newcomer, I did not know which questions to ask, in which order, or which concepts I needed to understand first.

It took me almost two weeks of active research to build a clear mental model of Gonka.

I believe there may be a missing layer before the technical documentation: the “first mile.”

Gonka is naturally explained by people who already understand Gonka. Newcomers may need Gonka explained from the perspective of someone discovering it.

**High-Level Solution**

Build a very simple onboarding layer around three initial journeys:

_I want to use AI_

Gateway → API key → models → first inference.

_I want to provide compute_

Hardware requirements → Host economics → NOP → first PoC.

_I want to understand GNK_

GNK vs WGNK → wallet → bridge → collateral → vesting → liquidity.

The objective would not be to replace or rewrite Gonka’s technical documentation.

The objective would be to help a newcomer understand where to start and what to learn next, then route them to the existing documentation at the right moment.

**Implementation Roadmap**

At this stage, I am not submitting a funding request.

I would first propose to:

1. Document the exact newcomer journey and questions I experienced over the last two weeks.
2. Map the main friction points and moments of confusion.
3. Build a simple prototype of the three onboarding journeys.
4. Test it with people who have never used Gonka.
5. Measure time to first successful action: first inference, first native GNK transaction, or a clear understanding of the Host/NOP path.

If the community recognises the problem, this could then become a small, measurable onboarding pilot.

**Open Questions**

* Do existing contributors recognise this onboarding problem?
* Are similar onboarding initiatives already being built?
* Which newcomer journey currently creates the most friction: Developer, Host, or GNK user?
* Would the community see value in testing a newcomer-first onboarding layer before the official documentation?

**Who I am**

My name is Julien. I am based in France and work in investment and business management.

I am not a protocol engineer or an AI infrastructure specialist.

That is precisely the perspective behind this proposal.

I discovered Gonka as a potential participant, became deeply interested in its economic model, and spent the last two weeks actively trying to understand the network from first principles.

I am not proposing to explain Gonka better than its builders. I am proposing to document the questions newcomers ask before they understand what Gonka’s builders are explaining.

I would genuinely appreciate critical feedback before taking this idea any further.

---

## 💬 Комментарии (2)

### Комментарий 1 — [@sultee](https://github.com/sultee)

*2026-07-13 15:39 UTC*

Hey Julien! Thank you so much for sharing your experience and ideas! I'd propose also bringing attention to this issue on Gonka community's Discord (not dropping links here, but you'll find it in the README)

### Комментарий 2 — [@tcharchian](https://github.com/tcharchian)

*2026-07-24 23:49 UTC*

Hi @julb1992! Have a look at the recently updated https://gonka.ai/ website. Do you think it’s better now?
By the way, the website documentation is hosted in a public repository https://github.com/gonka-ai/gonka-docs, so anyone can suggest changes by submitting a pull request. 

**↳ Ответ от [@julb1992](https://github.com/julb1992)** · *2026-07-25 11:59 UTC*

> Thanks! I definitely think it’s a improvement.
>
> It actually reinforces the point I was trying to make in my “missing first mile” post.
>
> The documentation for developers keeps getting better, which is great.
>
> But I still think there’s something missing for people who **aren’t developers or GPU providers**.
>
> I’m coming at Gonka as an **investor who’s trying to really understand the project**, and honestly it has taken me weeks of reading GitHub, Discord, Medium posts and talking with people from the community before everything started to make sense. And even now, I still don’t feel like I’ve got the full picture.
>
> I’m actually writing my own document just to understand the ecosystem properly, and I think it’s going to end up being a few dozen pages. That probably says a lot.
>
> How everything fits together, how the network works, where the token fits in, the key metrics, and a few real-world use cases.
>
> Developers need documentation.
> People discovering Gonka need the bigger picture.
