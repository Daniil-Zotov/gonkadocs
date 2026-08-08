---
title: "#1464 — Dev Team Funding"
source: https://github.com/gonka-ai/gonka/discussions/1464
discussion_number: 1464
category: protocol-improvements
synced_at: 2026-08-08T20:42:48Z
---

> 🔄 **Auto-sync:** from [Discussion #1464](https://github.com/gonka-ai/gonka/discussions/1464) every hour. 

# Dev Team Funding

**Автор:** [@gmorgachev](https://github.com/gmorgachev) · **Категория:** :gear: Protocol Improvements · **Создано:** 2026-07-17 01:38 UTC · **Обновлено:** 2026-08-03 20:22 UTC

---

## 📝 Описание

Hello everyone! I am Gleb Morgachev, one of Gonka's co-creators.

In the next couple of weeks, I plan to submit a proposal requesting 1.5 million USDT from the community pool. The funding would support an independent engineering team working on core protocol development aligned with the community roadmap. It would cover the team and expenses directly related to its work, not servers or GPU infrastructure for mining.

## Scope

This independent team would be a small group of top-tier engineers working on Gonka's core protocol for approximately one year. I would prioritize engineers with strong first-principles thinking who can work across a wide range of technical problems, rather than selecting primarily for previous blockchain experience. Based on my experience, this is the most productive format for Gonka's core development. The goals below define the team's direction, not a fixed scope to be completed within one year.

- A reliable, high-performance DevShard protocol. Using the same model, hardware, request parameters, and load, the target is at least 90% of direct vLLM output-token throughput and TTFT no more than 10% higher. This also includes accurately identifying and recording missed and invalid inferences, then safely enabling settlement of complete per-host statistics to Gonka mainnet for reward and penalty calculations.
- Strong alignment between PoC and actual inference quality and performance across different model architectures, domains and hardware classes.
- Security improvements for the protocol and bridges.

Exact priorities would be adjusted as the protocol's technical needs evolve. All work would be open source and contributed to the main Gonka repository.

The funding would be dedicated to core protocol engineering. It would not cover host or user support, dashboards, centralized monitoring, other infrastructure around Gonka, or marketing.

From my personal perspective, developing core training primitives that enable research teams to work on distributed training workloads on Gonka remains a high priority. It is not part of this team's primary scope, but the team may work on it after making substantial progress toward the goals above.

## Structure

### Organization and reward

As part of this initiative, I plan to establish a new LLC to manage the team and its work. My role would be to organize the team's work and processes, provide technical guidance, and lead the initiative.

My main personal incentive comes from the GNK I already hold and the protocol's long-term success. From the requested 1.5 million USDT, I propose a one-time reward of 50,000 USDT for organizing and leading this initiative. Besides this reward, I would not receive any personal compensation from these funds. All other funds would be used only for the engineering team and expenses related to its work.

Every six months, I will publish a high-level spending summary grouped into team, servers, services, and administrative costs.

### Collaboration

If established, this team would contribute to Gonka alongside individual contributors and other community-funded teams, such as the approved [External Test Lab and Community DevNet](https://github.com/gonka-ai/gonka/discussions/1388). It would collaborate with contributors across the community on protocol development and testing. I hope to see more teams working on different parts of Gonka.

### Funding transfer

The proposal will request a single transfer of 1.5 million USDT from the community pool to a smart contract controlled by Gonka governance. The first tranche of 750,000 USDT would be transferred to the recipient account defined in the contract immediately after the contract receives the funds. The second tranche of 750,000 USDT would be transferred six months later. Any funds not spent during the first year would remain reserved for further engineering work on Gonka's core protocol. The contract code will be published a few days before the governance proposal is submitted.


----

I plan to hold an AMA session next week to answer questions about this proposal.

Contact me:

- Telegram: [@gmorgachev](https://t.me/gmorgachev)
- Email: [morgachev.g@gmail.com](mailto:morgachev.g@gmail.com)


---

## 💬 Комментарии (5)

### Комментарий 1 — [@paranjko](https://github.com/paranjko)

*2026-07-20 23:22 UTC*

Count me in! I’d love to get involved and contribute to the initiative.

### Комментарий 2 — [@Daniil-Zotov](https://github.com/Daniil-Zotov)

*2026-07-31 19:00 UTC*

обсуждение на gonka.vote https://gonka.vote/proposal/nlabjc
обсуждение в тг https://telegram.me/gonka_proposals


### Комментарий 3 — [@Daniil-Zotov](https://github.com/Daniil-Zotov)

*2026-08-01 09:37 UTC*

вопросы:
1. какова роль Product Science сейчас и в ближайшей перспективе работы над протоколом? Новая команда заменит ее или работа будет вестись параллельно? 
2. сейчас в комьюнити пуле 720к usdt - согласован ли ваш пропозал с BF и планируется ли новый транш от BF до создания пропозала ончейн?
3. будет ли открытость в разработке - будет ли доступен роадмап и дашборд этой команды? прозрачности работы core team и внешних участников очень не хватает.
4. кто будет оплачивать инфраструктуру, необходимую для тестирования и разработки?
5. будут ли дублирующие баунти реварды этой команде при апдейтах?


### Комментарий 4 — [@konstantingostev77](https://github.com/konstantingostev77)

*2026-08-02 11:51 UTC*

Hi Gleb,
Thanks for putting this proposal together — the direction on DevShard performance and PoC/inference-quality alignment sounds like exactly the kind of first-principles engineering work Gonka needs.

I'd like to explore joining the engineering team.  I  recently started building decentralized VPS/VPN infrastructure on top of Gonka.

I'd be glad to share details if useful.
Since you mentioned prioritizing strong first-principles thinkers over prior blockchain experience specifically, I wanted to ask about the selection process:

Will there be a public/open call for applications, or is the team being assembled through direct outreach?

What's the best way to submit background/code samples for consideration?

Is there a timeline for when the team will start forming, relative to the governance proposal and funding transfer?

Looking forward to the AMA

Good Luck with the project,
Konstantin

### Комментарий 5 — [@Daniil-Zotov](https://github.com/Daniil-Zotov)

*2026-08-03 20:22 UTC*

AMA with Gleb Morgachev, Gonka co-creator: Dev Team Funding proposal

🕣 Tuesday, Aug. 4
8:30am PDT · 3:30pm UTC · 11:30pm CST

Gleb Morgachev 
[@gmorgachev](https://x.com/gmorgachev)
 will hold an AMA session where he'll cover the upcoming proposal dedicated to funding of an independent dev team.

Key topics:
- What tasks the funding is being requested for
- How the independent development team will be structured
- Funding mechanics
- Expense transparency, reporting, and Gleb’s role in the initiative
- Other questions

💻 Zoom: the link will be published before the session starts
🗣️ Language: English
📄 Proposal: [https://github.com/gonka-ai/gonka/discussions/1464](https://t.co/yETdroL6Kx)

See you next week!
