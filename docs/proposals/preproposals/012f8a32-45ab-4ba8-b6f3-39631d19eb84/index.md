---
title: "Return Withheld Miner Rewards: Redistribute Gov-Wallet Balance for Ep 132–247"
template: proposals-main.html
---

# Return Withheld Miner Rewards: Redistribute Gov-Wallet Balance for Ep 132–247

<div class="preproposal-header">

<div class="preproposal-status">🔴 Expired</div>

| | |
|:---|:---|
| **Author** | Evgenii Maksimenkov |
| **Created** | 2026-05-01 05:34 UTC |
| **Closes** | 2026-05-08 05:34 UTC |
| **Language** | EN |
| **Votes** | 70 |
| **Avg. Bid** | 3.1M GNK |

</div>

Since v0.2.9 and v0.2.11, withheld miner rewards have accumulated in the gov account (~3 053 801 GNK). Proposal returns them via batch vesting to 1 623 miners, pro-rata by rewarded_coins per epoch.

---

## Full Proposal

Should we redistribute the gov-wallet balance back to miners? Looking for your feedback before drafting a proposal

Fellow miners and stakeholders — I want to gauge community sentiment on a
proposal idea before turning it into an on-chain vote. Concrete numbers,
working code, and a verifiable CSV of payouts are already prepared:

**Repo:** https://github.com/gonkavip/taxreturn

## The situation

Two governance upgrades quietly changed where unpaid miner rewards go:

- **v0.2.9** (proposal #26, executed 2026-02-01) — when a participant is
  penalized during cPoC validation, the unpaid portion of their epoch
  reward is no longer redistributed among the remaining participants in
  the epoch. It is sent to the **gov module account**.
- **v0.2.11** (proposal #31, executed 2026-03-20) — slashed collateral was
  changed from `BurnCoins` to `SendCoinsFromModuleToModule(gov)`, applying
  the same destination policy.

Result: the gov module account
(`gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33`) has been quietly
accumulating roughly **3 053 801 GNK** of withheld miner rewards since
epoch 132 (the first epoch where this mechanism was observed on chain).

## Why this is miner money, not community money

This is the part I think gets overlooked.

The **community pool** is a separate account
(`gonka1jv65s3grqf6v6jl3dp4t6c9t9rk99cd8h2rzwa`, `auth/distribution`
module). It is funded by an explicit fraction of inflation, spent through
`MsgCommunityPoolSpend`, and currently holds about **102 972 832 GNK +
10 000 IBC USDT**. That is more than enough capital for grants, marketing,
ecosystem initiatives, etc.

The **gov module account** is a different beast. Beyond holding live
proposal deposits, it now also holds withheld and slashed coins that were
**originally minted as miner reward** — not as community subsidy. They
sit there because v0.2.9 turned off the redistribution mechanic that used
to return them to the epoch's other participants, but no follow-up rule
was ever defined for what should happen to them next.

Two prior proposals (#32 for epoch 158, #33 for epochs 132–133) already
established that the gov balance is a legitimate source for miner
compensation. Both used ad-hoc per-incident loss models. They returned
about 55 000 GNK total — leaving the rest sitting in the wallet without a
plan.

## What I'm proposing

A single, deterministic distribution: **return every ngonka of in-range
inflow back to the miners who actually performed in the epochs where it
was withheld**, proportional to each miner's `rewarded_coins` for that
epoch.

The methodology in one sentence: for each epoch in `132..247`, find how
many ngonka the inference module sent to gov in that epoch, then split
that amount across the miners of the epoch in proportion to what they
actually earned.

Specifics:

- **Range**: epochs `132..247` (132 is the first epoch with observable
  inflow; 247 is the last epoch whose payouts were fully settled at
  computation time).
- **Source data**: 100% on-chain, fetched from a standard gonka full node
  via `block_search`, `block_results`, `epoch_group_data`, and
  `epoch_performance_summary`. No off-chain inputs.
- **Math**: Hamilton (largest-remainder) integer apportionment in pure
  ngonka. The CSV total equals the in-range inflow exactly — every
  ngonka accounted for.
- **#32 and #33**: not subtracted. The double-payment for the addresses
  involved in those two proposals works out to ~1.7% of the wallet
  balance — well below the typical per-epoch noise, and not worth the
  extra complexity in the algorithm.

The full algorithm, design rationale, reproduction script, and the actual
output CSV (1 623 recipients, sum exactly 3 053 800.853 GNK) are in the
repo: **https://github.com/gonkavip/taxreturn**

The script runs against any gonka node, takes a few minutes from cold,
and produces the same numbers byte-for-byte. Feel free to verify on your
own node.

## Questions for the community

1. Do you think the gov-wallet balance should be returned to the miners
   who would have received it under the pre-v0.2.9 rules?
2. Is the proportional-by-rewarded-coins approach fair, or do you prefer
   a different methodology (e.g. by raw weight, by number of validated
   inferences, etc)?
3. Would you vote **yes** on an on-chain proposal that uses
   `MsgBatchTransferWithVesting` (mirroring #32 and #33) to execute this
   exact distribution?
4. Anything missing — edge cases, addresses I've miscategorized, an
   epoch boundary I've drawn wrong?

Looking forward to your thoughts. Happy to adjust the methodology, the
range, or anything else based on feedback before writing this up as a
formal governance proposal.

---

## Votes (70)

| Voter | Amount | Date |
| :----- | :----- | :--- |
| `gonka1gm...gzg6ry` | 3.1M GNK | 2026-05-01 05:35 |
| `gonka1aw...f8af0w` | 3.1M GNK | 2026-05-01 05:36 |
| `gonka1u6...967mgk` | 3.1M GNK | 2026-05-01 06:38 |
| `gonka1a4...3ww4ac` | 3.1M GNK | 2026-05-01 06:38 |
| `gonka14y...5dwa34` | 3.1M GNK | 2026-05-01 06:39 |
| `gonka18p...6ssllv` | 3.1M GNK | 2026-05-01 06:38 |
| `gonka19s...mj5e06` | 3.1M GNK | 2026-05-01 06:38 |
| `gonka109...wdesy6` | 3.1M GNK | 2026-05-03 14:32 |
| `gonka1c8...wqml7f` | 3.1M GNK | 2026-05-01 06:38 |
| `gonka1y3...wmzvu9` | 3.1M GNK | 2026-05-01 06:39 |
| `gonka1ex...65kr6h` | 3.1M GNK | 2026-05-01 06:38 |
| `gonka1p2...6k652r` | 3.1M GNK | 2026-05-01 06:38 |
| `gonka14s...4aqm05` | 3.1M GNK | 2026-05-01 06:38 |
| `gonka1lh...2z4evj` | 3.1M GNK | 2026-05-01 06:38 |
| `gonka1nq...ax5vyc` | 3.1M GNK | 2026-05-01 06:38 |
| `gonka1sl...wkl054` | 3.1M GNK | 2026-05-01 06:38 |
| `gonka1ss...u07vzh` | 3.1M GNK | 2026-05-01 06:39 |
| `gonka1eh...ucxxhz` | 3.1M GNK | 2026-05-01 06:38 |
| `gonka19y...ynwuku` | 3.1M GNK | 2026-05-01 06:38 |
| `gonka1rw...dftj3l` | 3.1M GNK | 2026-05-01 05:36 |
| `gonka1yw...3h9jpe` | 3.1M GNK | 2026-05-01 05:36 |
| `gonka14f...rqkh93` | 3.1M GNK | 2026-05-01 06:38 |
| `gonka14l...7evgh4` | 3.1M GNK | 2026-05-01 06:39 |
| `gonka1la...rh0qyc` | 3.1M GNK | 2026-05-01 06:38 |
| `gonka1w2...hl7xtp` | 3.1M GNK | 2026-05-01 06:39 |
| `gonka173...dkdvje` | 3.1M GNK | 2026-05-01 06:39 |
| `gonka108...kvfazm` | 3.1M GNK | 2026-05-01 06:36 |
| `gonka136...wjqqw2` | 3.1M GNK | 2026-05-01 06:37 |
| `gonka1cr...gf27kd` | 3.1M GNK | 2026-05-01 06:37 |
| `gonka1dq...z4jfa4` | 3.1M GNK | 2026-05-01 06:37 |
| `gonka1e2...wj7y2t` | 3.1M GNK | 2026-05-01 06:37 |
| `gonka1au...05ccat` | 3.1M GNK | 2026-05-01 06:36 |
| `gonka1a4...c7q2a5` | 3.1M GNK | 2026-05-01 06:37 |
| `gonka1f8...9n0xtv` | 3.1M GNK | 2026-05-01 06:37 |
| `gonka182...hg8ed7` | 3.1M GNK | 2026-05-01 06:37 |
| `gonka1h4...m03mnn` | 3.1M GNK | 2026-05-01 06:36 |
| `gonka1h9...26p07n` | 3.1M GNK | 2026-05-01 06:36 |
| `gonka1zs...7ln5c0` | 3.1M GNK | 2026-05-01 06:37 |
| `gonka1j3...sdekrc` | 3.1M GNK | 2026-05-01 06:36 |
| `gonka1jw...gmv0za` | 3.1M GNK | 2026-05-01 06:37 |
| `gonka1jy...vvf2gd` | 3.1M GNK | 2026-05-01 06:37 |
| `gonka1jz...hzaaq5` | 3.1M GNK | 2026-05-01 06:36 |
| `gonka1k7...jws70h` | 3.1M GNK | 2026-05-01 06:36 |
| `gonka1l9...8yhee5` | 3.1M GNK | 2026-05-01 06:36 |
| `gonka17g...lze0dx` | 3.1M GNK | 2026-05-01 06:36 |
| `gonka1lf...7q8ahj` | 3.1M GNK | 2026-05-01 06:37 |
| `gonka170...zrkh8p` | 3.1M GNK | 2026-05-01 06:36 |
| `gonka16x...kd5quj` | 3.1M GNK | 2026-05-01 06:37 |
| `gonka159...jleju2` | 3.1M GNK | 2026-05-01 06:37 |
| `gonka1p5...rc0q0g` | 3.1M GNK | 2026-05-01 06:37 |
| `gonka1pj...m3mddj` | 3.1M GNK | 2026-05-01 06:37 |
| `gonka1pp...kj60de` | 3.1M GNK | 2026-05-01 06:38 |
| `gonka1q3...vz3kgn` | 3.1M GNK | 2026-05-01 06:36 |
| `gonka150...zrwhta` | 3.1M GNK | 2026-05-01 06:37 |
| `gonka1s0...4d0lxs` | 3.1M GNK | 2026-05-01 06:37 |
| `gonka1sg...asss9u` | 3.1M GNK | 2026-05-01 06:36 |
| `gonka13n...wsx33n` | 3.1M GNK | 2026-05-01 06:36 |
| `gonka1sq...0wuqt8` | 3.1M GNK | 2026-05-01 06:37 |
| `gonka13e...g8pcpn` | 3.1M GNK | 2026-05-01 06:37 |
| `gonka1ta...gffgvy` | 3.1M GNK | 2026-05-01 06:36 |
| `gonka1av...0c8pmf` | 3.1M GNK | 2026-05-01 06:36 |
| `gonka1uk...ygy2mg` | 3.1M GNK | 2026-05-01 06:36 |
| `gonka1up...mjlvv9` | 3.1M GNK | 2026-05-01 06:36 |
| `gonka12u...fne9un` | 3.1M GNK | 2026-05-01 06:36 |
| `gonka1w9...e8q4tg` | 3.1M GNK | 2026-05-01 06:38 |
| `gonka1xy...r65ky8` | 3.1M GNK | 2026-05-01 06:37 |
| `gonka12l...dafxdh` | 3.1M GNK | 2026-05-01 06:36 |
| `gonka1yt...da3yv2` | 3.1M GNK | 2026-05-01 06:38 |
| `gonka10x...metmqz` | 3.1M GNK | 2026-05-01 06:36 |
| `gonka1hj...7dnj05` | 3.1M GNK | 2026-05-01 06:37 |

---

## Comments (15)

### 💬 Evgenii Maksimenkov
*2026-05-01 14:49* · 👍 2 · 👎 0

В предложении я специально подчеркнул, что у комьюнити уже есть свой пул который уже пополняется на 2% и там уже скопилось 102 972 832 GNK этого хватит на более чем 10 лет, если тратить по миллиону. А ранние майнеры помимо этого уже были “наказаны” дополнительным 10-30% налогом каждую эпоху, из-за того что сеть не могла эффективно бороться с ддос атаками. (Сейчас это уже изменилось, я описал ниже) 
Оригинальное предложение было составлено на английском языке и слово “legitimate source” там имело другую окраску. Имелось ввиду, что это правильный источник, который для этого и предназначается. 
Если будут какие-то конкретные идеи по алгоритму распределения (и чем они лучше предложенного), я буду рад обсудить.

---

### 💬 Evgenii Maksimenkov
*2026-05-01 06:02* · 👍 1 · 👎 0

Просто вернуть. Отключение может возобновить ддос.

---

### 💬 Evgenii Maksimenkov
*2026-05-01 06:03* · 👍 1 · 👎 0

Нужно различать govrnance и комьюнити кошелек. то разные вещи и для разных целей. Я  написал об этом в самом предложении.

---

### 💬 Nik
*2026-05-01 07:54* · 👍 1 · 👎 0

Отличная идея, распределить пропорционально выполненной работе - то есть обработанным инференсам!

---

### 💬 Alex Sharoiko Александр Шаройко
*2026-05-01 10:29* · 👍 1 · 👎 0

Ты предлагаешь вернуть награды всем майнерам? И читерам тоже?

Там чел в течение 35 дней обманывал сеть.
https://prnt.sc/x0M-Pq9kv4gG

А теперь мы ему выплатим раз в 5 больше того, что он наобманывал )

Уж лучше пусть средства будут в Комьюнити Пуле.

---

### 💬 Evgenii Maksimenkov
*2026-05-01 14:34* · 👍 1 · 👎 0

С момента 130 эпохи было многое реализовано для предотвращения ддоса: 
Закрыты порты 26657 - теперь все запросы идут через прокси
Инфиренс запросы распределяют TA.
И это правильно - нужно бороться в целом с возможностью ддоса, т.к. мотивация может быть и не GNK-материальная (например, участники другой сети решат положить конкурента).
Не факт, что комьюнити снова договориться о выплате. И мало кто будет тратить свои ресурсы, ради призрачной надежды получить дополнительно 10% через 3 месяца. К тому же выплата происходит постфактум и рычаг всегда остаётся у комьюнити - если видим что попытки ддоса возобновились, голосуем против очередного распределения.

---

### 💬 Evgenii Maksimenkov
*2026-05-01 14:38* · 👍 1 · 👎 0

Если мы вступаем на путь чери пикинга, то нужно четко оглашать правила кто достоин, а кто нет. И если уже есть такие критерии, то они априори уже должны быть внедрены в саму сеть.
Любой участник получит не в 5 раз больше, а примерно +10% от того что он недополучил.
P.S. Конкретно у твоего примера - там больше половина нод отключалась и по итогу они и так не получат награду.

---

### 💬 Дмитрий В
*2026-05-01 18:46* · 👍 1 · 👎 0

Это точно хороший алгоритм и хорошо продуман. Как разовая акция тут все прекрасно и поделана хорошая работа. 

Вижу, что не я один подсветил, что тут риск ненужного прецедента может быть. Но если попробовать изначально сразу позиционировать идею как разовую, типа закрыть прошлые «косяки», тогда риск минимизируется. 

Источники копилки думаю могут быть разные, это везде так, я бы лично не создавал ощущения, что штрафы могут быть амнистированы в будущем, но это мой подход, я не налоговик.) просто мнение.)

---

### 💬 Mikhail Chudinov
*2026-05-02 04:07* · 👍 1 · 👎 0

Ок, убедил.
Я проголосовал YES

---

### 💬 Alex Sharoiko Александр Шаройко
*2026-05-01 05:51* · 👍 0 · 👎 0

А ты хочешь вернуть, или вообще отключить эту фичу?

---

### 💬 Alex Sharoiko Александр Шаройко
*2026-05-01 05:57* · 👍 0 · 👎 0

Сейчас это получается около 10%. Но, я думаю, после обновления % будет ниже. Токеномика Gonka предполагает налог 2%. А тут получилось чуть больше) Интересно, какой % будет дальше тратиться?

С одной стороны, хорошо, когда в Комьюнити пул есть средства, а с другой, хорошо бы, чтобы майнеры были довольны.

Не знаю. У меня нет чёткого мнения. Но то, что налог должен быть, я считаю правильным. Но его пока нет. Зато есть эта фича)

---

### 💬 Дмитрий В
*2026-05-01 07:30* · 👍 0 · 👎 0

- Считаю нужно тратить деньги из пула, а не смотреть на них.) 
- Думаю этот кошель ровно такой же пул, хорошо что есть механизм возобновления баланса пула.
- Большой остаток в пуле говорит о том, что деньги срочно нужно тратить, но не о том, что откуда пришли, то туда же и отправить. Странный механизм сбора штрафов и налогов.)
- Нужно тем не менее как-то вознаградить ранних майневро.
- Хотя участие сейчас в сети отчасти и есть вознаграждение, хоть есть и риск, что проект не стрельнет. Мы сами на это идем.
- Логическая ошибка на мой взгляд в предложении и небольшая манипуляция): названы «законными» возвраты майнерам лишь по тому что прошло голосование. Звучит как отсылка к прецеденту. По такой логике текущий возврат можно тоже будет назвать законным. Тогда следующий возврат тоже можно назвать законным. Что на дистанции опосредованно узаконит ошибки и нарушения за которые берется штраф, ибо регулярная амнистия это поощрение нарушений.
- Если как-то возможно сделать отсев и вознаградить ранних майнеров по другой математике или за другие заслуги, то было бы хорошо. На мой взгляд это не обязательно должно быть справедливо распределено, можно вознаградить кого-то за самое долгое участие в сети или тех у кого самые оптимизированные мощности. Как сказал Павел Дуров, конкуренцию нужно вознаграждать, а если ставить всем пятерки только за то, что они пришли на урок, убивает результат.
- Считаю искать правду в том как поступить с монетами, в зависимости от туда откуда они пришли, чуть противоречит мировой налоговой практике. Пользовался бы принципом в том числе «От каждого по возможности, каждому по потребности», можно выдать наоборот тем, у кого самые не оптимизированные мощности, за участие в сети и поддержку даже в сложных для самого себя условиях.
- Но фонды это нужная идея, считать откуда пришло, чтобы поддерживать конкретный сектор всей экономики. Но тут получается это единственный источник, фонды должны быть значительно меньше тогда. Обычно каждый 5-10-20%, не больше.
- Можно исходить из этого и вернуть по 20% например, получится налоговый вычет, такой механизм есть в мировой практике. Но на сколько это будет опять же поощрять ошибки или ДДОС или другие действия, надо считать.

---

### 💬 Nik
*2026-05-01 07:52* · 👍 0 · 👎 0

"можно выдать наоборот тем, у кого самые не оптимизированные мощности" - это же полностью противоречит принципу Дурова вознаграждать конкуренцию.

---

### 💬 Дмитрий В
*2026-05-01 08:11* · 👍 0 · 👎 0

Да, верно подмечено. Просто накидываю идеи, эта не удачная, я бы ее не брал.)

---

### 💬 Mikhail Chudinov
*2026-05-01 12:33* · 👍 0 · 👎 0

Если сейчас вернуть - то логично, что и через месяц когда будет выдвинуто аналогичное предложение, давайте опять поделим, то так же поделим.
Мотивация ддосить, чтоб другие майнеры остались без выплат, чтобы получить самому повышенную выплату - появится.
Пусть выплата не гарантирована, и через время.. Но мотивация ддосить появляется, это плохо.

---


---

<div class="preproposal-link">

[View on gonka.vote](https://gonka.vote/proposal/012f8a32-45ab-4ba8-b6f3-39631d19eb84)

</div>
