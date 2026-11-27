---
title: "#2306 — [Draft for discussion] WGNK bridge hack: three compensation options, per-address register, open data"
source: https://github.com/gonka-ai/gonka/discussions/2306
discussion_number: 2306
category: ecosystem
synced_at: 2026-11-27T08:10:16Z
---

> 🔄 **Auto-sync:** from [Discussion #2306](https://github.com/gonka-ai/gonka/discussions/2306) every hour. 

# [Draft for discussion] WGNK bridge hack: three compensation options, per-address register, open data

**Автор:** [@Konyakoff](https://github.com/Konyakoff) · **Категория:** :jigsaw: Ecosystem · **Создано:** 2026-11-23 08:16 UTC · **Обновлено:** 2026-11-23 08:16 UTC

---

## 📝 Описание

> [!IMPORTANT]
> **Draft for community discussion — not an official position of Gonka or its Core Team.** I am Sergey Konyakov, a community member acting in a personal capacity. The research was done with Claude Code (Fable 5.2); I have not yet independently verified every address and amount. **I ask community members and the Core Team to re-check the logic of the calculation and the listed addresses and amounts.** A shared position on compensation should be reached here, in discussion.

Everything is open: **https://github.com/Konyakoff/gonka-wgnk-bridge-compensation/tree/6339c5b446f3b5ca51411b4149759bd294d95b75** (method, raw on-chain data, calculation code, per-address register, a critique of the method, three independent reviews; English with a full Russian version).

## Motivation

On 18 Nov 2026 an attacker drained the Gonka ↔ Ethereum bridge reserve (884,150.87 USDT and 647.74 USDC) and minted 22,000,000 unbacked WGNK, which were dumped into the Uniswap pools. The attacker later returned 593.435 ETH and 12,900,401 GNK. People still hold losses: holders of WGNK whose backing was taken, those who bought or sold during the incident, liquidity providers, holders of bridged USDT/USDC on Gonka.

There is no public, checkable calculation yet of who lost what and what making everyone whole would cost the community pool. This draft offers one, so that the discussion can be about numbers and principles rather than impressions.

## High-level solution

Three rules, the same for everyone:

1. **What was yours before the hack is yours** — WGNK at the last block before the unbacked mint is honoured one for one in native GNK (or new WGNK).
2. **Lost money is returned in the same currency** — USDT for USDT, USDC for USDC, ETH for ETH, net of what was received.
3. **Payouts let nobody profit** — gains are deducted, WGNK bought after the hack is voided, the attacker gets nothing.

One dividing line: the project's official warning “Do not trade WGNK”, **19 Nov 2026 00:24:07 UTC**. Losses on trades before it are treated as a commitment; for trades after it there are three options:

| Option | Recipients | GNK | USDT | USDC | ETH | Protocol top-up | Share of community pool |
|---|---:|---:|---:|---:|---:|---:|---:|
| **1** — before the warning only | 948 | 13,032,441 | 213,395.34 | 21,880.08 | 34.1599 | $158,074 | 0.96% |
| **2** — plus a declining share after (½ → ¼ → ⅛ → 0 within a day) | 989 | 13,035,064 | 215,650.17 | 22,345.27 | 34.3856 | $161,563 | 0.98% |
| **3** — plus everything after (until the data freeze, 23 Nov 04:30 UTC) | 997 | 13,037,901 | 225,171.55 | 24,192.27 | 35.5408 | $175,340 | 1.06% |

In every option the bridge reserve is restored and 27 senders of GNK → WGNK bridge requests that were never minted get 1,509.70 GNK back. “Protocol top-up” is what is missing beyond the attacker's return and the 98,277 GNK still in the bridge escrow, at ETH = $1,729.15. The options differ by $17,266 — it is a choice of principle more than of money.

- Proposal in words: [PROPOSAL.md](https://github.com/Konyakoff/gonka-wgnk-bridge-compensation/blob/6339c5b446f3b5ca51411b4149759bd294d95b75/PROPOSAL.md) · slides (visual summary only): [EN](https://github.com/Konyakoff/gonka-wgnk-bridge-compensation/blob/6339c5b446f3b5ca51411b4149759bd294d95b75/presentations/Gonka_Compensation_3_Options_EN.pdf), [RU](https://github.com/Konyakoff/gonka-wgnk-bridge-compensation/blob/6339c5b446f3b5ca51411b4149759bd294d95b75/presentations/Gonka_Compensation_3_Options_RU.pdf)
- Method: [METHODOLOGY.md](https://github.com/Konyakoff/gonka-wgnk-bridge-compensation/blob/6339c5b446f3b5ca51411b4149759bd294d95b75/METHODOLOGY.md)
- **Find your address:** [registers/register.csv](https://github.com/Konyakoff/gonka-wgnk-bridge-compensation/blob/6339c5b446f3b5ca51411b4149759bd294d95b75/registers/register.csv) (searchable table)
- Recompute the register from raw data with one command: [verify/](https://github.com/Konyakoff/gonka-wgnk-bridge-compensation/tree/6339c5b446f3b5ca51411b4149759bd294d95b75/verify)

## Implementation roadmap

1. Discussion here: the dividing line and the option.
2. Everyone checks their line in the register; an objection window; address-specific corrections as issues in the repository.
3. Preconditions, each needing an on-chain decision: cancel the pending bridge claims for unbacked WGNK (1,280,942 WGNK were burned after the hack and are still `BRIDGE_PENDING`), stop the old WGNK contract, convert the returned ETH (the top-up moves by about ±$97K per 10% of the ETH price).
4. An on-chain governance proposal with the final register. Nothing in this draft decides or pays anything.

## Open questions

The method has weak points, and I would rather name them myself — [CRITIQUE.md](https://github.com/Konyakoff/gonka-wgnk-bridge-compensation/blob/6339c5b446f3b5ca51411b4149759bd294d95b75/CRITIQUE.md):

1. **Someone did profit.** About $96,606 of trading profit stays with 131 addresses; the protocol cannot claw it back. Is that acceptable?
2. **Is the line too generous?** 88% of the refunds to traders are for purchases made after the first public alert (18:28 UTC on 18 Nov) but before the official warning. Should the line be earlier, or stepped?
3. **Concentration.** One liquidity provider receives 30% of all GNK and 43% of all money. The arithmetic was re-checked against contract state, but should the largest recipients confirm their addresses and disclose any link to the team?
4. **An address is not a person.** Off-chain deals are invisible; two unlinked wallets of one person are treated as two people. How long should the objection window be?
5. **Which option** — 1, 2 or 3 — and are the fractions of option 2 right?

## Please re-check

- the logic (`METHODOLOGY.md`, section 5 is the formula);
- the addresses and amounts (`registers/`);
- anything in the data or the code — `AGENTS.md` in the repository is a guide for AI assistants, with ready-made review tasks.

## Who I am

Sergey Konyakov ([@Konyakoff](https://github.com/Konyakoff)), a member of the Gonka community; not a member of the Core Team and not speaking for it. I have followed the WGNK market on Uniswap since launch. This work was done with an AI coding assistant, checked by three separate AI reviewers and by a recomputation script — and not yet by people. That is why it is published as a draft and why I ask for your review.

## Integrity of the published files

So that nobody has to trust my repository: this post refers to one fixed version.

- commit: `6339c5b446f3b5ca51411b4149759bd294d95b75` (tag `v0.1-draft`)
- release archive: `gonka-wgnk-bridge-compensation-v0.1-draft.zip`, SHA-256 `3176c3ce9533edbdfbffe64e61c229df290d865941b3f0310b244dfd009649cc`
- independent archive (Software Heritage): `swh:1:rev:6339c5b446f3b5ca51411b4149759bd294d95b75` — https://archive.softwareheritage.org/swh:1:rev:6339c5b446f3b5ca51411b4149759bd294d95b75;origin=https://github.com/Konyakoff/gonka-wgnk-bridge-compensation

Published content will not be rewritten; any correction will be a new tagged version announced in this thread with its own hash. If you can, please quote the commit hash in a reply — a comment by someone else cannot be edited by me.

<details>
<summary><b>Русская версия</b></summary>

> **Проект для обсуждения — не официальная позиция Gonka и её Core Team.** Я, Сергей Коньяков, член сообщества, действую как частное лицо. Исследование сделано с помощью Claude Code (Fable 5.2); я ещё не проверил самостоятельно каждый адрес и каждую сумму. **Прошу членов сообщества и Core Team перепроверить логику расчёта и перечисленные адреса с суммами.** К общему мнению о компенсациях нужно прийти здесь, в ходе обсуждения.

Всё открыто: **https://github.com/Konyakoff/gonka-wgnk-bridge-compensation/tree/6339c5b446f3b5ca51411b4149759bd294d95b75** (методика, сырые данные блокчейнов, код расчёта, реестр по адресам, критика метода, три независимые проверки; английский и полная русская версия — файлы `*.ru.md`).

**Зачем.** 18.11.2026 атакующий вывел резерв моста Gonka ↔ Ethereum (884,150.87 USDT и 647.74 USDC) и выпустил 22,000,000 необеспеченных WGNK, которые были слиты в пулы Uniswap. Позже он вернул 593.435 ETH и 12,900,401 GNK. У людей остались потери: у держателей WGNK, у покупавших и продававших во время инцидента, у поставщиков ликвидности, у держателей перенесённых USDT/USDC в сети Gonka. Публичного проверяемого расчёта — кто сколько потерял и во что это обойдётся комьюнити-пулу — пока нет. Этот черновик предлагает такой расчёт, чтобы спорить о числах и принципах, а не о впечатлениях.

**Что предлагается.** Три правила, одинаковые для всех: что было твоим до взлома — твоё (WGNK на последнем блоке до выпуска — один к одному нативными GNK или новыми WGNK); потерянные деньги возвращаются той же валютой за вычетом полученного; на выплатах никто не зарабатывает (прибыль вычитается, купленные после взлома WGNK аннулируются, атакующий не получает ничего). Одна граница — официальное предупреждение проекта «Do not trade WGNK», **19.11.2026 00:24:07 UTC**: потери по сделкам до него — обязательство, по сделкам после него — три варианта (таблица выше): 1 — только до предупреждения; 2 — плюс убывающая доля после (½ → ¼ → ⅛ → 0 за сутки); 3 — плюс всё после, до заморозки данных. Доплата протокола — $158,074, $161,563 и $175,340 (0.96%, 0.98% и 1.06% комьюнити-пула). Во всех вариантах восстанавливается резерв моста.

**Найдите свой адрес:** [registers/register.csv](https://github.com/Konyakoff/gonka-wgnk-bridge-compensation/blob/6339c5b446f3b5ca51411b4149759bd294d95b75/registers/register.csv) — таблица с поиском. Предложение текстом: [PROPOSAL.ru.md](https://github.com/Konyakoff/gonka-wgnk-bridge-compensation/blob/6339c5b446f3b5ca51411b4149759bd294d95b75/PROPOSAL.ru.md); методика: [METHODOLOGY.ru.md](https://github.com/Konyakoff/gonka-wgnk-bridge-compensation/blob/6339c5b446f3b5ca51411b4149759bd294d95b75/METHODOLOGY.ru.md); презентация (только наглядное изложение): [RU](https://github.com/Konyakoff/gonka-wgnk-bridge-compensation/blob/6339c5b446f3b5ca51411b4149759bd294d95b75/presentations/Gonka_Compensation_3_Options_RU.pdf).

**Шаги.** Обсуждение границы и варианта → каждый проверяет свою строку реестра, окно возражений → условия, требующие решения в сети: отменить висящие заявки моста за необеспеченные WGNK (1,280,942 WGNK), остановить старый контракт WGNK, обменять возвращённые ETH → предложение на голосование в сети с итоговым реестром. Этот черновик ничего не решает и не выплачивает.

**Открытые вопросы** — слабые места метода я называю сам, [CRITIQUE.ru.md](https://github.com/Konyakoff/gonka-wgnk-bridge-compensation/blob/6339c5b446f3b5ca51411b4149759bd294d95b75/CRITIQUE.ru.md): около $96,606 прибыли остаётся у 131 адресов; 88% возврата трейдерам — за покупки после первого публичного сигнала (18:28 UTC 18.11), но до официального предупреждения; один поставщик ликвидности получает 30% всех GNK и 43% всех денег; адрес — не человек, сделки вне сети не видны; какой вариант выбрать и верны ли доли варианта 2.

**Неизменность файлов.** Этот пост ссылается на одну зафиксированную версию: коммит `6339c5b446f3b5ca51411b4149759bd294d95b75` (метка `v0.1-draft`), архив выпуска `gonka-wgnk-bridge-compensation-v0.1-draft.zip` с SHA-256 `3176c3ce9533edbdfbffe64e61c229df290d865941b3f0310b244dfd009649cc`, независимый архив Software Heritage — `swh:1:rev:6339c5b446f3b5ca51411b4149759bd294d95b75` — https://archive.softwareheritage.org/swh:1:rev:6339c5b446f3b5ca51411b4149759bd294d95b75;origin=https://github.com/Konyakoff/gonka-wgnk-bridge-compensation. Опубликованное не переписывается; любая правка — новая версия с новой меткой и новым хэшем, объявленная в этой ветке. Если можете, процитируйте хэш коммита в ответе — чужой комментарий я отредактировать не могу.

</details>

