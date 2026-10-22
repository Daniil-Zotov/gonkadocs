---
title: "GitHub Issues"
template: issues-main.html
---

# GitHub Issues — `gonka-ai/gonka`

All issues from [gonka-ai/gonka](https://github.com/gonka-ai/gonka/issues).
Total: **21** (🟢 open: **14**, 🔴 closed: **7**).
Updated: `2026-10-22 15:21 UTC`.

<ul class="issues-list">
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="02085-bug-minor-devshard-gateway-healthcheck-uses-curl-which-the-i/">[BUG: minor] devshard-gateway healthcheck uses curl, which the image does not contain → container permanently unhealthy</a>
      <span class="issues-number">#2085</span>
    </div>
    <p class="issues-desc">**Summary**  `deploy/join/docker-compose.devshard-gateway.yml` defines the gateway healthcheck as  ```yaml healthcheck:   test: ["CMD", "curl", "-f", "http://localhost:8080/v1/status"] ```  but the im...</p>
    <div class="issues-labels"></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/maria-mitina">@maria-mitina</a> opened 4 hours ago</span>
      
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="02082-devshard-gateway-polls-v1versions-and-v1epochs-at-12min-but-/">devshard gateway polls /v1/versions and /v1/epochs/* at 12/min, but default proxy api_zone allows 10/min → permanent 503s after ~5 h</a>
      <span class="issues-number">#2082</span>
    </div>
    <p class="issues-desc">**Summary**  `devshardctl gateway` polls public API endpoints on a hardcoded 5 s ticker. The default nginx proxy puts those endpoints in `api_zone` (10 r/min per client IP, burst 600, `nodelay`). 12 r...</p>
    <div class="issues-labels"></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/maria-mitina">@maria-mitina</a> opened 7 hours ago</span>
      
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="01726-xinference-collateralparamsdowntimemissedpercentagethreshold/">x/inference: CollateralParams.DowntimeMissedPercentageThreshold is governance-settable but read by nothing, and SlashForDowntime's comment describes a check it does not perform</a>
      <span class="issues-number">#1726</span>
    </div>
    <p class="issues-desc">`CollateralParams.DowntimeMissedPercentageThreshold` is declared, defaulted, validated, registered as a governance-settable param and live on chain at `0.05` — and no code reads it. A governance vote...</p>
    <div class="issues-labels"><span class="issues-label" style="background-color: #d73a4a; color: #ffffff; border-color: #d73a4a;">bug</span></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/kaileido">@kaileido</a> opened 16 hours ago</span>
      <span class="issues-meta-item"><svg viewBox="0 0 16 16"><path d="M1 2.75C1 1.784 1.784 1 2.75 1h10.5c.966 0 1.75.784 1.75 1.75v7.5A1.75 1.75 0 0 1 13.25 12H9.06l-2.573 2.573A1.458 1.458 0 0 1 4 13.543V12H2.75A1.75 1.75 0 0 1 1 10.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h4.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"/></svg> 4</span>
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="02079-issue-hosts-behind-at-finalize-must-pull-the-missing-diffs/">Issue: hosts behind at finalize must pull the missing diffs</a>
      <span class="issues-number">#2079</span>
    </div>
    <p class="issues-desc"># Issue: hosts behind at finalize must pull the missing diffs  **Milestone:** Devshard v7  **Follows:** [#1785](https://github.com/gonka-ai/gonka/pull/1785) (`fix/devshard-finalize-resume-v6`)  ## Sum...</p>
    <div class="issues-labels"><span class="issues-label" style="background-color: #a2eeef; color: #24292f; border-color: #a2eeef;">enhancement</span></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/a-kuprin">@a-kuprin</a> opened 18 hours ago</span>
      
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="01810-devshard-tool-calling-protocol-errors-invalid/">`devshard`: Tool-calling / protocol errors → INVALID</a>
      <span class="issues-number">#1810</span>
    </div>
    
    <div class="issues-labels"></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 18 hours ago</span>
      <span class="issues-meta-item"><svg viewBox="0 0 16 16"><path d="M1 2.75C1 1.784 1.784 1 2.75 1h10.5c.966 0 1.75.784 1.75 1.75v7.5A1.75 1.75 0 0 1 13.25 12H9.06l-2.573 2.573A1.458 1.458 0 0 1 4 13.543V12H2.75A1.75 1.75 0 0 1 1 10.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h4.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"/></svg> 7</span>
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="02078-devshard-v7-a-context-length-refusal-at-the-governance-max-m/">devshard v7: a context-length refusal at the governance --max-model-len should never cost the host a miss or an invalidation</a>
      <span class="issues-number">#2078</span>
    </div>
    <p class="issues-desc">This is for v7, alongside #1903 (client-caused engine rejections, by @zpoken, moved to v7) and the v7 max-context-length item #1807. The code paths below are `devshard/v7` (67230e4dc) and #1903 at b20...</p>
    <div class="issues-labels"></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/cyberdelamain">@cyberdelamain</a> opened 23 hours ago</span>
      
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="02011-bug-wrong-report-for-long-running-poc-status/">[BUG] Wrong report for long running POC status</a>
      <span class="issues-number">#2011</span>
    </div>
    <p class="issues-desc"># Wrong reporting on POC challenge status when host rejected it due to training ## Summary Host which is under training, rejects POC challenge. So it is not generating commits. However, the on-chain s...</p>
    <div class="issues-labels"><span class="issues-label" style="background-color: #d73a4a; color: #ffffff; border-color: #d73a4a;">bug</span></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/maria-mitina">@maria-mitina</a> opened 1 day ago</span>
      <span class="issues-meta-item"><svg viewBox="0 0 16 16"><path d="M1 2.75C1 1.784 1.784 1 2.75 1h10.5c.966 0 1.75.784 1.75 1.75v7.5A1.75 1.75 0 0 1 13.25 12H9.06l-2.573 2.573A1.458 1.458 0 0 1 4 13.543V12H2.75A1.75 1.75 0 0 1 1 10.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h4.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"/></svg> 2</span>
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="02012-bug-host-in-training-rejects-poc-challenge-but-on-chain-stat/">[BUG] Host in training rejects POC challenge but on-chain status of POC - generating</a>
      <span class="issues-number">#2012</span>
    </div>
    <p class="issues-desc">## Summary A host in training is not supposed to be reserved for a POC challenge.   Training host: ``` decentai@702112:/srv/dai/gonka/deploy/join$ INFB=/srv/dai/gonka/inference-chain/build/linux/amd64...</p>
    <div class="issues-labels"><span class="issues-label" style="background-color: #d73a4a; color: #ffffff; border-color: #d73a4a;">bug</span></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/maria-mitina">@maria-mitina</a> opened 1 day ago</span>
      <span class="issues-meta-item"><svg viewBox="0 0 16 16"><path d="M1 2.75C1 1.784 1.784 1 2.75 1h10.5c.966 0 1.75.784 1.75 1.75v7.5A1.75 1.75 0 0 1 13.25 12H9.06l-2.573 2.573A1.458 1.458 0 0 1 4 13.543V12H2.75A1.75 1.75 0 0 1 1 10.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h4.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"/></svg> 2</span>
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="02013-bug-short-segment-is-treated-as-passed-challenger-pays-a-tar/">[BUG] Short segment is treated as PASSED (challenger pays a target that did nothing)</a>
      <span class="issues-number">#2013</span>
    </div>
    <p class="issues-desc">## Summary decideCurrentChallengeSegment skips evaluation whenever the segment is shorter than min_punishable_segment_blocks and returns nil; the caller treats nil as "passed":  if finish <= ch.StartH...</p>
    <div class="issues-labels"><span class="issues-label" style="background-color: #d73a4a; color: #ffffff; border-color: #d73a4a;">bug</span></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/maria-mitina">@maria-mitina</a> opened 1 day ago</span>
      <span class="issues-meta-item"><svg viewBox="0 0 16 16"><path d="M1 2.75C1 1.784 1.784 1 2.75 1h10.5c.966 0 1.75.784 1.75 1.75v7.5A1.75 1.75 0 0 1 13.25 12H9.06l-2.573 2.573A1.458 1.458 0 0 1 4 13.543V12H2.75A1.75 1.75 0 0 1 1 10.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h4.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"/></svg> 2</span>
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="02014-bug-fully-reserved-by-training-abort-is-unreachable-on-a-sho/">[BUG] fully_reserved_by_training abort is unreachable on a short segment</a>
      <span class="issues-number">#2014</span>
    </div>
    <p class="issues-desc"># Title fully_reserved_by_training abort is unreachable on a short segment  ## Summary The intended guard for a target whose nodes are all training-reserved lives inside the punishable-segment evaluat...</p>
    <div class="issues-labels"><span class="issues-label" style="background-color: #d73a4a; color: #ffffff; border-color: #d73a4a;">bug</span></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/maria-mitina">@maria-mitina</a> opened 1 day ago</span>
      <span class="issues-meta-item"><svg viewBox="0 0 16 16"><path d="M1 2.75C1 1.784 1.784 1 2.75 1h10.5c.966 0 1.75.784 1.75 1.75v7.5A1.75 1.75 0 0 1 13.25 12H9.06l-2.573 2.573A1.458 1.458 0 0 1 4 13.543V12H2.75A1.75 1.75 0 0 1 1 10.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h4.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"/></svg> 2</span>
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="02015-bug-cpoc-rotation-can-shrink-the-final-challenge-segment-bel/">[BUG] cPoC rotation can shrink the final challenge segment below the punishable minimum</a>
      <span class="issues-number">#2015</span>
    </div>
    <p class="issues-desc">## Summary  **How it is supposed to work**  When a challenge is created, the chain checks that enough blocks remain until the safety window:  `safetyHeight − startHeight ≥ min_punishable_segment_block...</p>
    <div class="issues-labels"><span class="issues-label" style="background-color: #d73a4a; color: #ffffff; border-color: #d73a4a;">bug</span></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/maria-mitina">@maria-mitina</a> opened 1 day ago</span>
      <span class="issues-meta-item"><svg viewBox="0 0 16 16"><path d="M1 2.75C1 1.784 1.784 1 2.75 1h10.5c.966 0 1.75.784 1.75 1.75v7.5A1.75 1.75 0 0 1 13.25 12H9.06l-2.573 2.573A1.458 1.458 0 0 1 4 13.543V12H2.75A1.75 1.75 0 0 1 1 10.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h4.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"/></svg> 3</span>
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="02066-training-carry-host-poc-weight-ratchets-down-while-a-node-is/">Training carry: host PoC weight ratchets down while a node is leased (training_carry.go)</a>
      <span class="issues-number">#2066</span>
    </div>
    <p class="issues-desc">## Summary  While a node is leased to a trainshard, the host's total PoC weight can only go down, never back up. Normal PoC noise on the host's free node and sub-100% cPoC readings get turned into a p...</p>
    <div class="issues-labels"></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/maria-mitina">@maria-mitina</a> opened 1 day ago</span>
      <span class="issues-meta-item"><svg viewBox="0 0 16 16"><path d="M1 2.75C1 1.784 1.784 1 2.75 1h10.5c.966 0 1.75.784 1.75 1.75v7.5A1.75 1.75 0 0 1 13.25 12H9.06l-2.573 2.573A1.458 1.458 0 0 1 4 13.543V12H2.75A1.75 1.75 0 0 1 1 10.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h4.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"/></svg> 1</span>
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="02000-devshard-executor-reported-output-tokens-set-the-payment-and/">devshard: executor-reported output tokens set the payment and are checked only on sampled replays</a>
      <span class="issues-number">#2000</span>
    </div>
    <p class="issues-desc">**TL;DR**  1. The executor signs `input_tokens` and `output_tokens` in `MsgFinishInference` (the Finish below), and the group's state machine pays from them, capped only on their combined cost. Nothi...</p>
    <div class="issues-labels"></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/vitaly-andr">@vitaly-andr</a> opened 1 day ago</span>
      <span class="issues-meta-item"><svg viewBox="0 0 16 16"><path d="M1 2.75C1 1.784 1.784 1 2.75 1h10.5c.966 0 1.75.784 1.75 1.75v7.5A1.75 1.75 0 0 1 13.25 12H9.06l-2.573 2.573A1.458 1.458 0 0 1 4 13.543V12H2.75A1.75 1.75 0 0 1 1 10.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h4.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"/></svg> 3</span>
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="01965-bug-incomplete-json-clock-timestamps-produce-a-false-diverge/">[BUG] Incomplete JSON clock timestamps produce a false divergence sample</a>
      <span class="issues-number">#1965</span>
    </div>
    <p class="issues-desc">## Summary  `common/probe` treats a JSON clock response with `send_unix_ns` but no usable `recv_unix_ns` as a valid four-timestamp sample. In a deterministic local reproduction, it reports a clock off...</p>
    <div class="issues-labels"></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/EazyHood">@EazyHood</a> opened 3 days ago</span>
      <span class="issues-meta-item"><svg viewBox="0 0 16 16"><path d="M1 2.75C1 1.784 1.784 1 2.75 1h10.5c.966 0 1.75.784 1.75 1.75v7.5A1.75 1.75 0 0 1 13.25 12H9.06l-2.573 2.573A1.458 1.458 0 0 1 4 13.543V12H2.75A1.75 1.75 0 0 1 1 10.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h4.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"/></svg> 1</span>
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="00820-investigate-missed-inference-on-some-nodes-root-causes-mitig/">Investigate missed inference on some nodes (root causes + mitigation)</a>
      <span class="issues-number">#820</span>
    </div>
    <p class="issues-desc">### Discussed in https://github.com/gonka-ai/gonka/discussions/817  <div type='discussions-op-text'>  <sup>Originally posted by **tcharchian** February 27, 2026</sup>  Task: Some nodes experience mis...</p>
    <div class="issues-labels"><span class="issues-label" style="background-color: #d73a4a; color: #ffffff; border-color: #d73a4a;">bug</span> <span class="issues-label" style="background-color: #008672; color: #ffffff; border-color: #008672;">help wanted</span> <span class="issues-label" style="background-color: #4cbc0f; color: #24292f; border-color: #4cbc0f;">up-for-grabs</span> <span class="issues-label" style="background-color: #f86c7a; color: #24292f; border-color: #f86c7a;">Priority: High</span></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 4 days ago</span>
      <span class="issues-meta-item"><svg viewBox="0 0 16 16"><path d="M1 2.75C1 1.784 1.784 1 2.75 1h10.5c.966 0 1.75.784 1.75 1.75v7.5A1.75 1.75 0 0 1 13.25 12H9.06l-2.573 2.573A1.458 1.458 0 0 1 4 13.543V12H2.75A1.75 1.75 0 0 1 1 10.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h4.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"/></svg> 3</span>
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="01935-bug-devshardctl-attempt-duration-is-measured-when-the-reques/">[BUG] devshardctl: attempt duration is measured when the request settles, not when the attempt ends</a>
      <span class="issues-number">#1935</span>
    </div>
    <p class="issues-desc"># Title devshardctl: attempt duration is measured when the request settles, not when the attempt ends  ## Summary  `buildInvolvement` in `devshard/cmd/devshardctl/redundancy.go` sets `TotalTimeMs = ti...</p>
    <div class="issues-labels"></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/vitaly-andr">@vitaly-andr</a> opened 5 days ago</span>
      <span class="issues-meta-item"><svg viewBox="0 0 16 16"><path d="M1 2.75C1 1.784 1.784 1 2.75 1h10.5c.966 0 1.75.784 1.75 1.75v7.5A1.75 1.75 0 0 1 13.25 12H9.06l-2.573 2.573A1.458 1.458 0 0 1 4 13.543V12H2.75A1.75 1.75 0 0 1 1 10.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h4.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"/></svg> 1</span>
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="02049-important-challengereceipt-memory-overflows/">Important! ChallengeReceipt memory overflows</a>
      <span class="issues-number">#2049</span>
    </div>
    <p class="issues-desc"># ChallengeReceipt memory: problem statement  A refused-timeout check sends the executor the diffs it may have missed, in one `ChallengeReceipt`. Today the verifier loads that range into one decoded s...</p>
    <div class="issues-labels"><span class="issues-label" style="background-color: #a2eeef; color: #24292f; border-color: #a2eeef;">enhancement</span></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/a-kuprin">@a-kuprin</a> opened 5 days ago</span>
      <span class="issues-meta-item"><svg viewBox="0 0 16 16"><path d="M1 2.75C1 1.784 1.784 1 2.75 1h10.5c.966 0 1.75.784 1.75 1.75v7.5A1.75 1.75 0 0 1 13.25 12H9.06l-2.573 2.573A1.458 1.458 0 0 1 4 13.543V12H2.75A1.75 1.75 0 0 1 1 10.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h4.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"/></svg> 1</span>
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="01955-bug-min-tokens-floor-mintokensfloor64-breaks-tool-calling-ru/">[BUG] `min_tokens` floor (MinTokensFloor=64) breaks tool calling: runaway garbage, fabricated tool results, up to max_tokens billed per turn</a>
      <span class="issues-number">#1955</span>
    </div>
    <p class="issues-desc">## Summary Every inference request runs with `min_tokens >= 64` (`EnforceTokenBudgetFloor`, #1391), and `stop_token_ids` are stripped. This masks every stop token, including end-of-turn and tool-call...</p>
    <div class="issues-labels"><span class="issues-label" style="background-color: #d73a4a; color: #ffffff; border-color: #d73a4a;">bug</span></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/KTibow">@KTibow</a> opened 5 days ago</span>
      
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="01940-security-chore-gateway-signing-key-protection/">[Security Chore]: Gateway signing-key protection</a>
      <span class="issues-number">#1940</span>
    </div>
    <p class="issues-desc"># Chore: Gateway signing-key protection  **Status:** Deferred. Not part of PR #1568.   **Related:** [PR #1568 review](https://github.com/gonka-ai/gonka/pull/1568#discussion_r4189385988) on `gateway_de...</p>
    <div class="issues-labels"><span class="issues-label" style="background-color: #a2eeef; color: #24292f; border-color: #a2eeef;">enhancement</span></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/a-kuprin">@a-kuprin</a> opened 6 days ago</span>
      
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="02039-bug-devshardctl-an-escrow-the-gateway-cannot-serve-is-never-/">[BUG] devshardctl: an escrow the gateway cannot serve is never settled, and the chain splits its deposit after two epochs</a>
      <span class="issues-number">#2039</span>
    </div>
    <p class="issues-desc">## Summary An escrow that the gateway cannot serve is excluded from routing but is not settled. The gateway deactivates an escrow when its runtime build ends with a final reason (`ErrLocalStateUnrecov...</p>
    <div class="issues-labels"></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/snevolin">@snevolin</a> opened 6 days ago</span>
      
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="02037-bug-low-a-failed-inline-catch-up-read-leaves-a-committed-sta/">[BUG, LOW] A failed inline catch-up read leaves a committed Start with funds reserved</a>
      <span class="issues-number">#2037</span>
    </div>
    <p class="issues-desc">## What fails  `PrepareInferenceFn` composes the next diff, then reads the host's catch-up, still holding `Session.mu`:  ```go diff, composedIdx, err := s.composeDiffLocked(persistCtx, txsForDiff) //...</p>
    <div class="issues-labels"><span class="issues-label" style="background-color: #d73a4a; color: #ffffff; border-color: #d73a4a;">bug</span> <span class="issues-label" style="background-color: #a2eeef; color: #24292f; border-color: #a2eeef;">enhancement</span></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/a-kuprin">@a-kuprin</a> opened 6 days ago</span>
      
    </div>
  </div>
</li>
</ul>
