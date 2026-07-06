---
title: "Bounty for open-source PoC throughput contributions"
template: proposals-main.html
---

# Bounty for open-source PoC throughput contributions

<div class="preproposal-header">

<div class="preproposal-status">🔴 Expired</div>

| | |
|:---|:---|
| **Author** | Serhii Hovorov |
| **Created** | 2026-05-01 21:04 UTC |
| **Closes** | 2026-05-08 21:04 UTC |
| **Language** | EN |
| **Votes** | 5 |
| **Avg. Bid** | 20.0K GNK |

</div>

Pay a fixed GNK/USDT bounty to anyone who upstreams a reproducible ≥5% PoC throughput optimization. Lifts the network floor; rewards contribution over hoarding.

---

## Full Proposal

Problem                                                                                                                           
                                           
  PoC throughput optimizations are network-wide value, but today they stay private.
  A pool operator who finds a +5% kernel rewrite has every incentive to keep it
  secret — they get 5% more weight relative to the rest of the network for as
  long as nobody else has it. The result:                                                                                              
                                          
  - Big pools capture the gains; smaller miners stay slow                                                                              
  - Optimizations don't flow back into the public `gonka-ai/vllm` and `mlnode` repos                                                   
  - New miners join a network whose floor is lower than it could be
  - The chain's actual realized GNK/GPU-hour is below what's technically achievable                                                    
                                              
  This is a coordination failure, not a malice problem. There's no mechanism today                                                     
  that pays contributors for raising the network floor.
                                                                                                                                       
  ## Proposal                                                                                                                          
                                                                                                                                       
  Establish a standing bounty in GNK for any PoC-related throughput optimization                                                       
  that meets **all** of these criteria:    

  1. **Merged upstream** into a public Gonka repo — `gonka-ai/vllm`,                                                                   
     `gonka-ai/mlnode`, `gonka-ai/inference-chain`, or a designated successor.
  2. **Reproducible benchmark** — a public A/B harness against a reference build                                                       
     (currently Qwen3-235B-A22B-Instruct-2507-FP8) on at least one supported GPU                                                       
     class (B200 / H100 / A100). Includes "before" and "after" commit SHAs.
  3. **Net positive impact** — at least 5% sustained nonces/min uplift on the                                                          
     reference setup.                                                                                                                  
  4. **Independently verified** — reproduced by ≥ 2 unrelated miners on their                                                          
     own hardware, attested on-chain.                                                                                                  
                                                                                                                                       
  ### Reward structure (for community discussion)
                                                                                                                                       
  - Flat bounty per qualifying contribution: **2,000 GNK**                                                                             
  - Bonus tier for ≥ 10% uplift: **+3,000 GNK**
  - Funded from a dedicated optimization-bounty pool topped up via routine                                                             
    community-pool spend proposals tied to confirmed merges — no extra emissions
  - Contributor names the recipient address at PR submission
  - One person can receive multiple bounties for distinct optimizations                                                                
                                                                                                                                       
  ### Why this is fair to the rest of the network                                                                                      
                                                                                                                                       
  The bounty is one-time per contribution and capped. The throughput gain is
  permanent and accrues to **every** miner forever. The community-pool trades a                                                        
  small fixed cost now for a permanent uplift in the network's earning capacity.
  Positive-sum by construction.                                                                                                        
                                          
  ## Why now                                                                                                                           
                                                                                                                                       
  A reward mechanism works best when there's already a verifiable example of                                                           
  someone choosing to upstream rather than hoard. There is one in flight today:                                                        
                                              
  - [`gonka-ai/vllm#36`](https://github.com/gonka-ai/vllm/pull/36) —                                                                   
    `@torch.compile` decorator on `apply_householder`. Measured **+10.2% on
    8×B200** and **+12.5% on 8×H100** for Qwen3-235B-FP8. One-line change.                                                             
    Reproducible A/B harness in the PR.                                                                                                
                                                                                                                                       
  If this tender passes, that PR becomes the first concrete test of the bounty                                                         
  workflow: independent reproduction on community hardware, on-chain attestation,                                                      
  payout via a follow-up community-pool spend. Every future optimization — from
  anyone — would follow the same path.                                                                                                 
                                              
  Every week this stays unaddressed is a week where private wins outpace public                                                        
  ones. There are pool operators sitting on similar optimizations right now. A
  clear, public reward path flips the math from "hoard" to "ship."                                                                     
                                                                                                                                       
  ## What this is *not*                                                                                                                
                                                                                                                                       
  - **Not** a proposal to pay any specific person — it's a standing policy                                                             
    anyone can claim.                                                                                                                  
  - **Not** a vote on `vllm#36` itself — that PR lands or not on its technical                                                         
    merits regardless of this tender.         
  - **Not** a binding tx — tenders are indicative polls. If this passes, a
    separate formal community-pool spend funds the first round.
                                                                                                                                       
  ## Open questions for the community
                                                                                                                                       
  - Right uplift threshold? (5% suggested; could be 3% or 10%)
  - Right bounty size? (2k + 3k GNK suggested; could scale with measured                                                               
    network-wide impact)                      
  - Verification process? (2 independent miners suggested)
  - Scope: PoC-only, or also general inference throughput? (broader = more
    impact, harder to verify)                                                                                                          
  - Eligibility for retroactive contributions? (e.g. anything merged in the
    last 30 days)

---

## Votes (5)

| Voter | Amount | Date |
| :----- | :----- | :--- |
| `gonka1gm...gzg6ry` | 20.0K GNK | 2026-05-01 21:06 |
| `gonka1aw...f8af0w` | 20.0K GNK | 2026-05-01 21:06 |
| `gonka1wv...zsa8f6` | 20.0K GNK | 2026-05-01 21:11 |
| `gonka178...08g7pn` | 20.0K GNK | 2026-05-04 07:03 |
| `gonka1yw...3h9jpe` | 20.0K GNK | 2026-05-01 21:07 |

---

## Comments (1)

### 💬 Mikhail Chudinov
*2026-05-04 14:34* · 👍 1 · 👎 0

Идея правильная, считаю что давать нужно минимум эквивалент 1000$ за каждый % прироста веса.
Дала оптимизация +10% = выдать 10к$
Курс GNK может сильно плавать, поэтому такой бонус я бы привязывал к USD.
Это будет хорошее, более понятное предложение для программистов, которые впервые услышали про гонку.
Что тут можно пооптимизировать, понятным образом протестировать результат в нонсах в минуту скриптом и получить разовую приличную выплату в случае успеха.

Создавать отдельный пулл под финансирование не вижу смысла. 
Считаю что достаточно каждое такое улучшение проводить как пропозал отдельный, из комьюнити пула.
В качестве верификации что эта оптимизация полезна выступают майнеры, своим голосованием.

---


---

<div class="preproposal-link">

[View on gonka.vote](https://gonka.vote/proposal/6392c2ea-7fb8-45c7-b1ec-80fb16d81d93)

</div>
