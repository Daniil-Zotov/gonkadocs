---
title: "GitHub Issues"
template: issues-main.html
---

# GitHub Issues — `gonka-ai/gonka`

All issues from [gonka-ai/gonka](https://github.com/gonka-ai/gonka/issues).
Total: **68** (🟢 open: **60**, 🔴 closed: **8**).
Updated: `2026-09-09 14:40 UTC`.

<ul class="issues-list">
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="01733-extend-e2e-for-ha-devshard-config-with-multiple-routers-and-/">Extend e2e for HA devshard config with multiple routers and multiple versiond</a>
      <span class="issues-number">#1733</span>
    </div>
    <p class="issues-desc"># Proposal: Unjoined-network citest for multiple versiond-routers  **Status:** Draft   **Related:** [PR #1610](https://github.com/gonka-ai/gonka/pull/1610) (`VERSIOND_POOL_ENDPOINTS_FILE`), existing `...</p>
    <div class="issues-labels"><span class="issues-label" style="background-color: #a2eeef; color: #24292f; border-color: #a2eeef;">enhancement</span></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/a-kuprin">@a-kuprin</a> opened 22 hours ago</span>
      
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="01470-security-residual-ssrf-on-inferenceurl-dnsrebind-validator-r/">Security: Residual SSRF on InferenceUrl — DNS/rebind + validator redirect (incomplete fix after #505/#534)</a>
      <span class="issues-number">#1470</span>
    </div>
    <p class="issues-desc">## Summary  **Residual SSRF** after prior paid mitigations (v0.2.7 / v0.2.8):  | Prior fix | What it covered | What remains broken | |-----------|-----------------|---------------------| | [PR #534](h...</p>
    <div class="issues-labels"></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/Aphelios01-sdk">@Aphelios01-sdk</a> opened 1 day ago</span>
      <span class="issues-meta-item"><svg viewBox="0 0 16 16"><path d="M1 2.75C1 1.784 1.784 1 2.75 1h10.5c.966 0 1.75.784 1.75 1.75v7.5A1.75 1.75 0 0 1 13.25 12H9.06l-2.573 2.573A1.458 1.458 0 0 1 4 13.543V12H2.75A1.75 1.75 0 0 1 1 10.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h4.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"/></svg> 2</span>
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="01719-harden-ecies-primitive-restore-curve-validation-and-reject-s/">Harden ECIES primitive: restore curve validation and reject short ciphertexts</a>
      <span class="issues-number">#1719</span>
    </div>
    <p class="issues-desc">The application-level gate here looks right, but the root cause is still live in `github.com/gonka-ai/cosmos-sdk`: `crypto/ecies` diverges from the go-ethereum code it was copied from in two places —...</p>
    <div class="issues-labels"><span class="issues-label" style="background-color: #4cbc0f; color: #24292f; border-color: #4cbc0f;">up-for-grabs</span></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 1 day ago</span>
      <span class="issues-meta-item"><svg viewBox="0 0 16 16"><path d="M1 2.75C1 1.784 1.784 1 2.75 1h10.5c.966 0 1.75.784 1.75 1.75v7.5A1.75 1.75 0 0 1 13.25 12H9.06l-2.573 2.573A1.458 1.458 0 0 1 4 13.543V12H2.75A1.75 1.75 0 0 1 1 10.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h4.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"/></svg> 1</span>
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="01692-monitoring-public-repository/">Monitoring: public repository</a>
      <span class="issues-number">#1692</span>
    </div>
    <p class="issues-desc">Public Grafana repo (Pitstop): https://github.com/kaitakuai/gonka-grafana Pasha @clanster has it ready for review.   When it is out: - [ ] the stack actually works - [ ] Grafana shows what is really h...</p>
    <div class="issues-labels"></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 1 day ago</span>
      <span class="issues-meta-item"><svg viewBox="0 0 16 16"><path d="M1 2.75C1 1.784 1.784 1 2.75 1h10.5c.966 0 1.75.784 1.75 1.75v7.5A1.75 1.75 0 0 1 13.25 12H9.06l-2.573 2.573A1.458 1.458 0 0 1 4 13.543V12H2.75A1.75 1.75 0 0 1 1 10.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h4.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"/></svg> 6</span>
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="01688-decode-poc-integration-support/">Decode PoC: integration support</a>
      <span class="issues-number">#1688</span>
    </div>
    <p class="issues-desc">Integration of Decode PoC with the current chain and MLNode path. Design and seeding questions stay on this issue. Verification of the current MiniMax implementation on a full image is #1689. DeepSeek...</p>
    <div class="issues-labels"></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 1 day ago</span>
      <span class="issues-meta-item"><svg viewBox="0 0 16 16"><path d="M1 2.75C1 1.784 1.784 1 2.75 1h10.5c.966 0 1.75.784 1.75 1.75v7.5A1.75 1.75 0 0 1 13.25 12H9.06l-2.573 2.573A1.458 1.458 0 0 1 4 13.543V12H2.75A1.75 1.75 0 0 1 1 10.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h4.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"/></svg> 4</span>
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="01691-glm-53-flash-vllm-028-image-poc-fix/">GLM 5.3 Flash: vLLM 0.28 image + PoC fix</a>
      <span class="issues-number">#1691</span>
    </div>
    <p class="issues-desc">Pitstop’s main track is MLNode images, experiments, and evaluations for bringing new models onto the network.  The current piece of work is GLM 5.3 Flash: a vLLM 0.28 image plus a PoC fix. PoC current...</p>
    <div class="issues-labels"></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 1 day ago</span>
      <span class="issues-meta-item"><svg viewBox="0 0 16 16"><path d="M1 2.75C1 1.784 1.784 1 2.75 1h10.5c.966 0 1.75.784 1.75 1.75v7.5A1.75 1.75 0 0 1 13.25 12H9.06l-2.573 2.573A1.458 1.458 0 0 1 4 13.543V12H2.75A1.75 1.75 0 0 1 1 10.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h4.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"/></svg> 4</span>
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
    <div class="issues-labels"></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/kAIPraxisBot">@kAIPraxisBot</a> opened 1 day ago</span>
      <span class="issues-meta-item"><svg viewBox="0 0 16 16"><path d="M1 2.75C1 1.784 1.784 1 2.75 1h10.5c.966 0 1.75.784 1.75 1.75v7.5A1.75 1.75 0 0 1 13.25 12H9.06l-2.573 2.573A1.458 1.458 0 0 1 4 13.543V12H2.75A1.75 1.75 0 0 1 1 10.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h4.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"/></svg> 1</span>
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="01725-xinference-getallmodelcapacities-keys-the-epoch-group-map-wi/">x/inference: GetAllModelCapacities keys the epoch-group map with a block height, so the query always returns empty</a>
      <span class="issues-number">#1725</span>
    </div>
    <p class="issues-desc">`GetAllModelCapacities` reads `EpochGroupDataMap` with a block height where the map is keyed by epoch index, so the lookup never hits and the query returns an empty list on every call.  ## The mismatc...</p>
    <div class="issues-labels"></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/kAIPraxisBot">@kAIPraxisBot</a> opened 1 day ago</span>
      <span class="issues-meta-item"><svg viewBox="0 0 16 16"><path d="M1 2.75C1 1.784 1.784 1 2.75 1h10.5c.966 0 1.75.784 1.75 1.75v7.5A1.75 1.75 0 0 1 13.25 12H9.06l-2.573 2.573A1.458 1.458 0 0 1 4 13.543V12H2.75A1.75 1.75 0 0 1 1 10.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h4.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"/></svg> 1</span>
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="01722-incomplete-http-200-streams-are-cached-and-replayed-as-succe/">Incomplete HTTP 200 streams are cached and replayed as successful responses</a>
      <span class="issues-number">#1722</span>
    </div>
    <p class="issues-desc">## Problem  The devshard gateway can store an incomplete streamed chat response in the one-hour response cache. Identical requests then receive the same partial body immediately instead of starting a...</p>
    <div class="issues-labels"></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/aleksandr-cstl">@aleksandr-cstl</a> opened 2 days ago</span>
      
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="01628-bug-public-routers-hangtimeout-on-prompts-75k-tokens-prefill/">[BUG] Public routers hang/timeout on prompts ≥ ~7.5K tokens (prefill); 502 `all_providers_failed`; DeepSeek missing from /v1/models</a>
      <span class="issues-number">#1628</span>
    </div>
    <p class="issues-desc">## Summary  Public Gonka routers hang or fail on any request whose total prefill is ≥ ~7.5K tokens: tested 2026-08-23 across `api.opengonka.com`, `node.gonka.lat`, `gate.joingonka.ai`, `openbroker.gon...</p>
    <div class="issues-labels"></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/inecro1">@inecro1</a> opened 3 days ago</span>
      <span class="issues-meta-item"><svg viewBox="0 0 16 16"><path d="M1 2.75C1 1.784 1.784 1 2.75 1h10.5c.966 0 1.75.784 1.75 1.75v7.5A1.75 1.75 0 0 1 13.25 12H9.06l-2.573 2.573A1.458 1.458 0 0 1 4 13.543V12H2.75A1.75 1.75 0 0 1 1 10.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h4.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"/></svg> 5</span>
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="01689-first-full-mnode-image-for-decode-poc-minimax-testing/">First full MNode image for Decode PoC (MiniMax): testing</a>
      <span class="issues-number">#1689</span>
    </div>
    <p class="issues-desc">A full MLNode image for Decode PoC on MiniMax, with the current implementation verified. Collecting coefficients or thresholds is not acceptance. Self-validation and cross-device validation must pass...</p>
    <div class="issues-labels"></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 4 days ago</span>
      <span class="issues-meta-item"><svg viewBox="0 0 16 16"><path d="M1 2.75C1 1.784 1.784 1 2.75 1h10.5c.966 0 1.75.784 1.75 1.75v7.5A1.75 1.75 0 0 1 13.25 12H9.06l-2.573 2.573A1.458 1.458 0 0 1 4 13.543V12H2.75A1.75 1.75 0 0 1 1 10.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h4.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"/></svg> 3</span>
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="01690-first-full-mnode-image-for-decode-poc-deepseek-testing-coeff/">First full MNode image for Decode PoC (DeepSeek): testing + coefficients</a>
      <span class="issues-number">#1690</span>
    </div>
    <p class="issues-desc">Decode PoC thresholds and expert seeding for DeepSeek. DeepSeek seeding is more complex than MiniMax; the scheme needs a fix before coefficients alone are useful. Kimi Decode PoC thresholds stay on ho...</p>
    <div class="issues-labels"></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 4 days ago</span>
      <span class="issues-meta-item"><svg viewBox="0 0 16 16"><path d="M1 2.75C1 1.784 1.784 1 2.75 1h10.5c.966 0 1.75.784 1.75 1.75v7.5A1.75 1.75 0 0 1 13.25 12H9.06l-2.573 2.573A1.458 1.458 0 0 1 4 13.543V12H2.75A1.75 1.75 0 0 1 1 10.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h4.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"/></svg> 3</span>
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="01696-devshard-bridgeclassifyqueryerror-has-no-production-callers-/">devshard: bridge.ClassifyQueryError has no production callers, so transient chain-query failures return 500 instead of the intended retryable 503</a>
      <span class="issues-number">#1696</span>
    </div>
    <p class="issues-desc">## Summary  `bridge.ClassifyQueryError` — the function whose job is to mark transient chain query failures as `ErrChainUnavailable` so they can be retried — has **zero non-test callers**. As a result...</p>
    <div class="issues-labels"></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/Ryanchen911">@Ryanchen911</a> opened 5 days ago</span>
      <span class="issues-meta-item"><svg viewBox="0 0 16 16"><path d="M1 2.75C1 1.784 1.784 1 2.75 1h10.5c.966 0 1.75.784 1.75 1.75v7.5A1.75 1.75 0 0 1 13.25 12H9.06l-2.573 2.573A1.458 1.458 0 0 1 4 13.543V12H2.75A1.75 1.75 0 0 1 1 10.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h4.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"/></svg> 2</span>
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="01714-devshard-bind-the-gateway-stream-to-msgfinishinference-with-/">`devshard` bind the gateway stream to `MsgFinishInference` with a second hash</a>
      <span class="issues-number">#1714</span>
    </div>
    <p class="issues-desc"># Proposal: bind the gateway stream to `MsgFinishInference` with a second hash  **Status:** Design, not implemented **Related:** [PR #1650](https://github.com/gonka-ai/gonka/pull/1650) (compress infer...</p>
    <div class="issues-labels"><span class="issues-label" style="background-color: #a2eeef; color: #24292f; border-color: #a2eeef;">enhancement</span></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/a-kuprin">@a-kuprin</a> opened 5 days ago</span>
      
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="01695-proxy-rate-limiting-no-exemption-path-for-trusted-high-volum/">Proxy rate limiting: no exemption path for trusted high-volume clients, and the tuning variables are not passed through in compose</a>
      <span class="issues-number">#1695</span>
    </div>
    <p class="issues-desc">## Summary  A devshard gateway run by our team was rate-limited by a network node's nginx for weeks without either side realising it: **8,000+ rejected requests in 24 hours** across three zones. The l...</p>
    <div class="issues-labels"></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/Ryanchen911">@Ryanchen911</a> opened 5 days ago</span>
      <span class="issues-meta-item"><svg viewBox="0 0 16 16"><path d="M1 2.75C1 1.784 1.784 1 2.75 1h10.5c.966 0 1.75.784 1.75 1.75v7.5A1.75 1.75 0 0 1 13.25 12H9.06l-2.573 2.573A1.458 1.458 0 0 1 4 13.543V12H2.75A1.75 1.75 0 0 1 1 10.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h4.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"/></svg> 1</span>
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="01708-chain-halt-validatorbyconsaddr-propagates-errnovalidatorfoun/">chain-halt: ValidatorByConsAddr propagates ErrNoValidatorFound, so the evidence/slashing BeginBlock nil-guards never run</a>
      <span class="issues-number">#1708</span>
    </div>
    <p class="issues-desc">## Summary  `ValidatorByConsAddr` (`x/staking/keeper/alias_functions.go` in the [`gonka-ai/cosmos-sdk`](https://github.com/gonka-ai/cosmos-sdk) fork) returns `ErrNoValidatorFound` when the consensus a...</p>
    <div class="issues-labels"></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/vitaly-andr">@vitaly-andr</a> opened 6 days ago</span>
      <span class="issues-meta-item"><svg viewBox="0 0 16 16"><path d="M1 2.75C1 1.784 1.784 1 2.75 1h10.5c.966 0 1.75.784 1.75 1.75v7.5A1.75 1.75 0 0 1 13.25 12H9.06l-2.573 2.573A1.458 1.458 0 0 1 4 13.543V12H2.75A1.75 1.75 0 0 1 1 10.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h4.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"/></svg> 1</span>
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="01680-kimi-k26-non-stream-on-gateway-v4-502-nonce-finishedfalse-st/">Kimi-K2.6 non-stream on gateway v4: 502 nonce_finished=false (stream OK)</a>
      <span class="issues-number">#1680</span>
    </div>
    <p class="issues-desc">We ran into a Kimi-K2.6 issue on **gateway v4** (`mainnet-v0.2.15-v4`) and wanted to flag it.  **What we see.** `stream=true` is fine. `stream=false` with a tiny `max_tokens` (64) often returns JSON....</p>
    <div class="issues-labels"><span class="issues-label" style="background-color: #d73a4a; color: #ffffff; border-color: #d73a4a;">bug</span></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/paranjko">@paranjko</a> opened 7 days ago</span>
      <span class="issues-meta-item"><svg viewBox="0 0 16 16"><path d="M1 2.75C1 1.784 1.784 1 2.75 1h10.5c.966 0 1.75.784 1.75 1.75v7.5A1.75 1.75 0 0 1 13.25 12H9.06l-2.573 2.573A1.458 1.458 0 0 1 4 13.543V12H2.75A1.75 1.75 0 0 1 1 10.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h4.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"/></svg> 3</span>
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="01698-gateway-allowlist-request-axis-ordo/">Gateway allowlist request: Axis Ordo</a>
      <span class="issues-number">#1698</span>
    </div>
    <p class="issues-desc">**Operator:** Axis Ordo — multi-tenant SaaS platform for AI agents, operated by Soft Dev Oy (Finland). https://platform.axis-ordo.com  **Contact:** @leonidkachuliak-eng · support@softdev.fi  **Creator...</p>
    <div class="issues-labels"></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/leonidkachuliak-eng">@leonidkachuliak-eng</a> opened 7 days ago</span>
      <span class="issues-meta-item"><svg viewBox="0 0 16 16"><path d="M1 2.75C1 1.784 1.784 1 2.75 1h10.5c.966 0 1.75.784 1.75 1.75v7.5A1.75 1.75 0 0 1 13.25 12H9.06l-2.573 2.573A1.458 1.458 0 0 1 4 13.543V12H2.75A1.75 1.75 0 0 1 1 10.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h4.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"/></svg> 1</span>
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="01542-devshardctl-parseprotocolversion-rejects-route-v4-noisy-rota/">devshardctl: ParseProtocolVersion rejects route v4 (noisy rotation fallback log)</a>
      <span class="issues-number">#1542</span>
    </div>
    <p class="issues-desc">## Summary  When the gateway serves `DEVSHARD_ROUTE_PREFIX=/devshard/v4`, escrow autorotation logs a fallback on every create:  ``` escrow_rotation_protocol_version_fallback route_prefix="/devshard/v4...</p>
    <div class="issues-labels"><span class="issues-label" style="background-color: #a2eeef; color: #24292f; border-color: #a2eeef;">enhancement</span> <span class="issues-label" style="background-color: #7057ff; color: #ffffff; border-color: #7057ff;">good first issue</span> <span class="issues-label" style="background-color: #95b500; color: #24292f; border-color: #95b500;">Priority: Low</span> <span class="issues-label" style="background-color: #aaaaaa; color: #24292f; border-color: #aaaaaa;">devshards</span></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/maria-mitina">@maria-mitina</a> opened 9 days ago</span>
      <span class="issues-meta-item"><svg viewBox="0 0 16 16"><path d="M1 2.75C1 1.784 1.784 1 2.75 1h10.5c.966 0 1.75.784 1.75 1.75v7.5A1.75 1.75 0 0 1 13.25 12H9.06l-2.573 2.573A1.458 1.458 0 0 1 4 13.543V12H2.75A1.75 1.75 0 0 1 1 10.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h4.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"/></svg> 5</span>
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="01654-bug-openai-api-compatibility-deepseek-reasoning-output-conca/">⁠[Bug] OpenAI API compatibility: DeepSeek reasoning output concatenated into content & invalid reasoning_effort validation⁠</a>
      <span class="issues-number">#1654</span>
    </div>
    <p class="issues-desc">### Summary When using `deepseek-ai/DeepSeek-V4-Flash-0731` via Open Broker (`api.openbroker.gonka.gg`), the gateway fails to parse reasoning tokens into `message.reasoning_content`.  Instead, the mod...</p>
    <div class="issues-labels"><span class="issues-label" style="background-color: #d73a4a; color: #ffffff; border-color: #d73a4a;">bug</span></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/dmrtest">@dmrtest</a> opened 9 days ago</span>
      <span class="issues-meta-item"><svg viewBox="0 0 16 16"><path d="M1 2.75C1 1.784 1.784 1 2.75 1h10.5c.966 0 1.75.784 1.75 1.75v7.5A1.75 1.75 0 0 1 13.25 12H9.06l-2.573 2.573A1.458 1.458 0 0 1 4 13.543V12H2.75A1.75 1.75 0 0 1 1 10.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h4.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"/></svg> 5</span>
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="01677-bug-gatewaymlnode-agent-sized-prefill-hangs-or-fails-with-no/">[BUG] Gateway/mlnode: agent-sized prefill hangs or fails with no usable error</a>
      <span class="issues-number">#1677</span>
    </div>
    <p class="issues-desc">## Summary  Chat completions whose **total prefill is on the order of ≥ ~8K tokens** (typical agent/RAG system prompts; not a single-message format bug) often **never produce a first token**: client s...</p>
    <div class="issues-labels"></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/paranjko">@paranjko</a> opened 10 days ago</span>
      <span class="issues-meta-item"><svg viewBox="0 0 16 16"><path d="M1 2.75C1 1.784 1.784 1 2.75 1h10.5c.966 0 1.75.784 1.75 1.75v7.5A1.75 1.75 0 0 1 13.25 12H9.06l-2.573 2.573A1.458 1.458 0 0 1 4 13.543V12H2.75A1.75 1.75 0 0 1 1 10.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h4.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"/></svg> 1</span>
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="01205-chain-halt-markvalidatorfordeletion-jailed-branch-races-come/">chain-halt: `markValidatorForDeletion` jailed branch races CometBFT validator-update lag → slashing fails with ErrNoValidatorFound</a>
      <span class="issues-number">#1205</span>
    </div>
    <p class="issues-desc">## Summary  In the [`gonka-ai/cosmos-sdk`](https://github.com/gonka-ai/cosmos-sdk) fork, the jailed branch of `markValidatorForDeletion` (`x/staking/keeper/compute.go:559-563`) immediately deletes the...</p>
    <div class="issues-labels"></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/vitaly-andr">@vitaly-andr</a> opened 10 days ago</span>
      <span class="issues-meta-item"><svg viewBox="0 0 16 16"><path d="M1 2.75C1 1.784 1.784 1 2.75 1h10.5c.966 0 1.75.784 1.75 1.75v7.5A1.75 1.75 0 0 1 13.25 12H9.06l-2.573 2.573A1.458 1.458 0 0 1 4 13.543V12H2.75A1.75 1.75 0 0 1 1 10.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h4.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"/></svg> 4</span>
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="00955-p0-make-handling-of-warm-keys-deterministic-implementation/">[P0] Make handling of warm keys deterministic (implementation)</a>
      <span class="issues-number">#955</span>
    </div>
    <p class="issues-desc">See #913   Once research is finished and we agree on a decision, we'll update this issue with the implementation steps.</p>
    <div class="issues-labels"><span class="issues-label" style="background-color: #aaaaaa; color: #24292f; border-color: #aaaaaa;">devshards</span></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/dcastro">@dcastro</a> opened 11 days ago</span>
      <span class="issues-meta-item"><svg viewBox="0 0 16 16"><path d="M1 2.75C1 1.784 1.784 1 2.75 1h10.5c.966 0 1.75.784 1.75 1.75v7.5A1.75 1.75 0 0 1 13.25 12H9.06l-2.573 2.573A1.458 1.458 0 0 1 4 13.543V12H2.75A1.75 1.75 0 0 1 1 10.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h4.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"/></svg> 1</span>
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="01671-choredeps-rebase-forked-cosmos-sdk-onto-v0538-base-is-v0533-/">chore(deps): rebase forked cosmos-sdk onto v0.53.8 (base is v0.53.3, ~5 patch releases behind)</a>
      <span class="issues-number">#1671</span>
    </div>
    <p class="issues-desc">## Summary  Our forked cosmos-sdk (`github.com/gonka-ai/cosmos-sdk`, currently `v0.53.3-ps19-observability`, referenced by both `inference-chain` and `decentralized-api` via `go.mod` replace) is based...</p>
    <div class="issues-labels"></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/kAIPraxisBot">@kAIPraxisBot</a> opened 11 days ago</span>
      
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="01665-height-sync-one-roundtrip-per-host-not-per-slot/">Height-sync: one roundtrip per host, not per slot</a>
      <span class="issues-number">#1665</span>
    </div>
    <p class="issues-desc"># Height-sync: one roundtrip per host, not per slot  **Labels:** `enhancement`, `devshard`, `height-sync`  ## Summary  Idle height-sync still fans out **one signed `/chat/completions` roundtrip per es...</p>
    <div class="issues-labels"><span class="issues-label" style="background-color: #a2eeef; color: #24292f; border-color: #a2eeef;">enhancement</span></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/a-kuprin">@a-kuprin</a> opened 12 days ago</span>
      
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="01080-bridge-stale-epoch-keys-can-authorize-withdrawals-up-to-365-/">Bridge: Stale epoch keys can authorize withdrawals up to 365 epochs after rotation</a>
      <span class="issues-number">#1080</span>
    </div>
    <p class="issues-desc">## Summary  `withdraw()` and `mintWithSignature()` in `BridgeContract.sol` accept signatures from **any historical epoch** as long as the epoch's group key has not been cleaned up by `_cleanupOldEpoch...</p>
    <div class="issues-labels"></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/Doog-bot534">@Doog-bot534</a> opened 12 days ago</span>
      <span class="issues-meta-item"><svg viewBox="0 0 16 16"><path d="M1 2.75C1 1.784 1.784 1 2.75 1h10.5c.966 0 1.75.784 1.75 1.75v7.5A1.75 1.75 0 0 1 13.25 12H9.06l-2.573 2.573A1.458 1.458 0 0 1 4 13.543V12H2.75A1.75 1.75 0 0 1 1 10.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h4.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"/></svg> 3</span>
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="01086-p2-devshard-escrow-stats-collection-and-off-chain-stats-supp/">[P2] Devshard escrow stats collection and off chain stats support</a>
      <span class="issues-number">#1086</span>
    </div>
    
    <div class="issues-labels"></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 12 days ago</span>
      <span class="issues-meta-item"><svg viewBox="0 0 16 16"><path d="M1 2.75C1 1.784 1.784 1 2.75 1h10.5c.966 0 1.75.784 1.75 1.75v7.5A1.75 1.75 0 0 1 13.25 12H9.06l-2.573 2.573A1.458 1.458 0 0 1 4 13.543V12H2.75A1.75 1.75 0 0 1 1 10.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h4.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"/></svg> 2</span>
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="01352-bridge-auto-refund-does-not-run-when-bls-signing-expires-exp/">Bridge: auto-refund does not run when BLS signing expires (EXPIRED)</a>
      <span class="issues-number">#1352</span>
    </div>
    <p class="issues-desc">## Summary  When an outbound `RequestBridgeMint` BLS request reaches terminal **`EXPIRED`** (threshold not met), the chain emits `inference.bls.EventThresholdSigningFailed` but **does not** auto-refun...</p>
    <div class="issues-labels"></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/maria-mitina">@maria-mitina</a> opened 12 days ago</span>
      <span class="issues-meta-item"><svg viewBox="0 0 16 16"><path d="M1 2.75C1 1.784 1.784 1 2.75 1h10.5c.966 0 1.75.784 1.75 1.75v7.5A1.75 1.75 0 0 1 13.25 12H9.06l-2.573 2.573A1.458 1.458 0 0 1 4 13.543V12H2.75A1.75 1.75 0 0 1 1 10.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h4.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"/></svg> 2</span>
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="01285-bridge-merge-eth-readme-messagehash-quickfix-into-v0214/">Bridge: merge ETH README messageHash quickfix into v0.2.14</a>
      <span class="issues-number">#1285</span>
    </div>
    <p class="issues-desc">## Summary  The Ethereum bridge README currently documents the mint/withdraw `messageHash` format without the `address(this)` bridge contract field, while the actual contract source includes it.  A fi...</p>
    <div class="issues-labels"></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/Ryanchen911">@Ryanchen911</a> opened 12 days ago</span>
      <span class="issues-meta-item"><svg viewBox="0 0 16 16"><path d="M1 2.75C1 1.784 1.784 1 2.75 1h10.5c.966 0 1.75.784 1.75 1.75v7.5A1.75 1.75 0 0 1 13.25 12H9.06l-2.573 2.573A1.458 1.458 0 0 1 4 13.543V12H2.75A1.75 1.75 0 0 1 1 10.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h4.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"/></svg> 4</span>
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="01286-bridge-add-retry-cap-or-monitoring-for-stale-refund-cleanup-/">Bridge: add retry cap or monitoring for stale refund cleanup retries</a>
      <span class="issues-number">#1286</span>
    </div>
    <p class="issues-desc">## Summary  When a threshold signing request reaches COMPLETED, the inference BLS hook calls `CleanupBridgePendingRefundByBlsRequestID` to remove pending bridge refund state.  If this cleanup persiste...</p>
    <div class="issues-labels"></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/Ryanchen911">@Ryanchen911</a> opened 12 days ago</span>
      <span class="issues-meta-item"><svg viewBox="0 0 16 16"><path d="M1 2.75C1 1.784 1.784 1 2.75 1h10.5c.966 0 1.75.784 1.75 1.75v7.5A1.75 1.75 0 0 1 13.25 12H9.06l-2.573 2.573A1.458 1.458 0 0 1 4 13.543V12H2.75A1.75 1.75 0 0 1 1 10.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h4.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"/></svg> 4</span>
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="00326-p2-improve-onboarding-experience/">[P2] Improve onboarding experience</a>
      <span class="issues-number">#326</span>
    </div>
    <p class="issues-desc">Improve onboarding experience:   - [ ] Clearer logging when node is launched and waiting for PoC - [ ] remove errors which doesn’t mean errors - [ ] automatic testing that everything will work when Po...</p>
    <div class="issues-labels"></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 12 days ago</span>
      <span class="issues-meta-item"><svg viewBox="0 0 16 16"><path d="M1 2.75C1 1.784 1.784 1 2.75 1h10.5c.966 0 1.75.784 1.75 1.75v7.5A1.75 1.75 0 0 1 13.25 12H9.06l-2.573 2.573A1.458 1.458 0 0 1 4 13.543V12H2.75A1.75 1.75 0 0 1 1 10.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h4.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"/></svg> 4</span>
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="00412-p2-mlnode-token-based-authentication-and-fqdn-support/">[P2] MLNode Token-Based Authentication and FQDN Support</a>
      <span class="issues-number">#412</span>
    </div>
    <p class="issues-desc">## Goal / Problem  Current MLNode registration in the API service requires three static parameters: - Static IP address - PoC port (management API, default 8080) - Inference port (vLLM inference API,...</p>
    <div class="issues-labels"><span class="issues-label" style="background-color: #95b500; color: #24292f; border-color: #95b500;">Priority: Low</span></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/gmorgachev">@gmorgachev</a> opened 12 days ago</span>
      <span class="issues-meta-item"><svg viewBox="0 0 16 16"><path d="M1 2.75C1 1.784 1.784 1 2.75 1h10.5c.966 0 1.75.784 1.75 1.75v7.5A1.75 1.75 0 0 1 13.25 12H9.06l-2.573 2.573A1.458 1.458 0 0 1 4 13.543V12H2.75A1.75 1.75 0 0 1 1 10.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h4.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"/></svg> 6</span>
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="00560-p2-finalizing-the-websocket-merge-with-call-back-new-vllm-wi/">[P2] Finalizing the WebSocket (merge with `call_Back`, new vLLM will require python side implementation)</a>
      <span class="issues-number">#560</span>
    </div>
    
    <div class="issues-labels"><span class="issues-label" style="background-color: #95b500; color: #24292f; border-color: #95b500;">Priority: Low</span></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 12 days ago</span>
      <span class="issues-meta-item"><svg viewBox="0 0 16 16"><path d="M1 2.75C1 1.784 1.784 1 2.75 1h10.5c.966 0 1.75.784 1.75 1.75v7.5A1.75 1.75 0 0 1 13.25 12H9.06l-2.573 2.573A1.458 1.458 0 0 1 4 13.543V12H2.75A1.75 1.75 0 0 1 1 10.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h4.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"/></svg> 5</span>
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="00330-p2-security-merkletree-proofs-merge-participant-validation-t/">[P2] Security MerkleTree Proofs; Merge participant validation till block0; Need to add signature check at recording</a>
      <span class="issues-number">#330</span>
    </div>
    <p class="issues-desc">This is a future task. A detailed description will be provided in the near future.  Please do not start working on this task without the detailed specification, as it may turn out to be a different di...</p>
    <div class="issues-labels"></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 12 days ago</span>
      <span class="issues-meta-item"><svg viewBox="0 0 16 16"><path d="M1 2.75C1 1.784 1.784 1 2.75 1h10.5c.966 0 1.75.784 1.75 1.75v7.5A1.75 1.75 0 0 1 13.25 12H9.06l-2.573 2.573A1.458 1.458 0 0 1 4 13.543V12H2.75A1.75 1.75 0 0 1 1 10.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h4.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"/></svg> 1</span>
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="01223-p1-clean-up-the-state/">[P1] Clean up the state</a>
      <span class="issues-number">#1223</span>
    </div>
    <p class="issues-desc">Review what’s currently stored, identify any leftovers, and remove them.</p>
    <div class="issues-labels"><span class="issues-label" style="background-color: #12a6e8; color: #24292f; border-color: #12a6e8;">Priority: Medium</span></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 12 days ago</span>
      <span class="issues-meta-item"><svg viewBox="0 0 16 16"><path d="M1 2.75C1 1.784 1.784 1 2.75 1h10.5c.966 0 1.75.784 1.75 1.75v7.5A1.75 1.75 0 0 1 13.25 12H9.06l-2.573 2.573A1.458 1.458 0 0 1 4 13.543V12H2.75A1.75 1.75 0 0 1 1 10.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h4.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"/></svg> 1</span>
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="01220-p0-off-chain-devshard-implementation-track/">[P0] Off-chain / devshard implementation track</a>
      <span class="issues-number">#1220</span>
    </div>
    <p class="issues-desc">Open for community contributors. Multiple parallel efforts in this direction are welcome to explore different approaches and accelerate progress.</p>
    <div class="issues-labels"><span class="issues-label" style="background-color: #4cbc0f; color: #24292f; border-color: #4cbc0f;">up-for-grabs</span> <span class="issues-label" style="background-color: #f86c7a; color: #24292f; border-color: #f86c7a;">Priority: High</span></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 12 days ago</span>
      <span class="issues-meta-item"><svg viewBox="0 0 16 16"><path d="M1 2.75C1 1.784 1.784 1 2.75 1h10.5c.966 0 1.75.784 1.75 1.75v7.5A1.75 1.75 0 0 1 13.25 12H9.06l-2.573 2.573A1.458 1.458 0 0 1 4 13.543V12H2.75A1.75 1.75 0 0 1 1 10.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h4.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"/></svg> 2</span>
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="01219-p0-basic-primitives-for-training/">[P0] Basic primitives for training</a>
      <span class="issues-number">#1219</span>
    </div>
    <p class="issues-desc">The framing is simple: you can prepare any container, it will run across different GPUs in the network, a protocol layer will coordinate interaction between nodes, they will perform training, and then...</p>
    <div class="issues-labels"><span class="issues-label" style="background-color: #f86c7a; color: #24292f; border-color: #f86c7a;">Priority: High</span></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 12 days ago</span>
      <span class="issues-meta-item"><svg viewBox="0 0 16 16"><path d="M1 2.75C1 1.784 1.784 1 2.75 1h10.5c.966 0 1.75.784 1.75 1.75v7.5A1.75 1.75 0 0 1 13.25 12H9.06l-2.573 2.573A1.458 1.458 0 0 1 4 13.543V12H2.75A1.75 1.75 0 0 1 1 10.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h4.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"/></svg> 6</span>
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="01660-large-per-host-catch-up-diff-backlog-can-cause-413-on-host-t/">Large per-host catch-up diff backlog can cause 413 on host transport</a>
      <span class="issues-number">#1660</span>
    </div>
    <p class="issues-desc">## Summary  A host can fall far behind the current session state and later receive an oversized catch-up request, causing `413 Payload Too Large` on host transport.  This is related to large payload h...</p>
    <div class="issues-labels"></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/aikuznetsov">@aikuznetsov</a> opened 13 days ago</span>
      
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="01659-proposal-repair-loop-for-escrow-state-root-diverged/">Proposal: Repair loop for `escrow_state_root_diverged`</a>
      <span class="issues-number">#1659</span>
    </div>
    <p class="issues-desc"># Proposal: Repair loop for `escrow_state_root_diverged`  **Status:** Draft / proposal   **Related:** [PR #1581 accounting review](../pr-1581-accounting-review.md) §1 (ghosts) and §3 (capability / sta...</p>
    <div class="issues-labels"><span class="issues-label" style="background-color: #a2eeef; color: #24292f; border-color: #a2eeef;">enhancement</span></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/a-kuprin">@a-kuprin</a> opened 13 days ago</span>
      
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="01658-413-on-large-chat-payload-due-to-gatewayhost-request-size-mi/">413 on large chat payload due to gateway/host request size mismatch</a>
      <span class="issues-number">#1658</span>
    </div>
    <p class="issues-desc">### Summary  Large `/v1/chat/completions` requests can pass the gateway-side body limit but fail later with `413 Payload Too Large` on host transport.  The issue appears to be a mismatch between:  - w...</p>
    <div class="issues-labels"></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/aikuznetsov">@aikuznetsov</a> opened 13 days ago</span>
      
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="01525-poc-auto-validatedweight-1-on-missing-model-executors-guardi/">PoC auto ValidatedWeight:-1 on missing model executors + guardian tiebreaker can wipe model weight (v0.2.14)</a>
      <span class="issues-number">#1525</span>
    </div>
    <p class="issues-desc">## Summary  On Gonka **testnet**, PoC stage **98080** (epoch **273→274**), we reproduced the **v0.2.14** PoC path where a host assigned to validate a model it cannot execute eventually submits `Valida...</p>
    <div class="issues-labels"></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/maria-mitina">@maria-mitina</a> opened 14 days ago</span>
      <span class="issues-meta-item"><svg viewBox="0 0 16 16"><path d="M1 2.75C1 1.784 1.784 1 2.75 1h10.5c.966 0 1.75.784 1.75 1.75v7.5A1.75 1.75 0 0 1 13.25 12H9.06l-2.573 2.573A1.458 1.458 0 0 1 4 13.543V12H2.75A1.75 1.75 0 0 1 1 10.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h4.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"/></svg> 1</span>
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="01624-personal-solo-use-inference-gateway-allowlist-request/">Personal / Solo-use Inference Gateway — Allowlist Request</a>
      <span class="issues-number">#1624</span>
    </div>
    <p class="issues-desc">Hello Gonka team,  I would like to request allowlisting for a **personal, self-hosted inference gateway**.  This gateway will be used exclusively for my own AI coding and development tasks. It will **...</p>
    <div class="issues-labels"></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/AndreyVoenkov">@AndreyVoenkov</a> opened 15 days ago</span>
      <span class="issues-meta-item"><svg viewBox="0 0 16 16"><path d="M1 2.75C1 1.784 1.784 1 2.75 1h10.5c.966 0 1.75.784 1.75 1.75v7.5A1.75 1.75 0 0 1 13.25 12H9.06l-2.573 2.573A1.458 1.458 0 0 1 4 13.543V12H2.75A1.75 1.75 0 0 1 1 10.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h4.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"/></svg> 1</span>
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="01637-gateway-allowlist-request-fusion-ai-gateway-production-whole/">Gateway allowlist request: Fusion AI Gateway — production wholesale broker (DeepSeek Flash / MiniMax / Kimi)</a>
      <span class="issues-number">#1637</span>
    </div>
    <p class="issues-desc">## Operator  - **Name:** Aung Myat Moe - **GitHub:** [@theaungmyatmoe](https://github.com/theaungmyatmoe) - **Project:** Fusion AI Gateway (`https://api.fusioncode.app`) — production OpenAI-compatible...</p>
    <div class="issues-labels"></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/theaungmyatmoe">@theaungmyatmoe</a> opened 15 days ago</span>
      
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="01632-openbroker-strips-provider-prompt-cache-metadata-prompt-toke/">OpenBroker strips provider prompt-cache metadata (prompt_tokens_details is always null)</a>
      <span class="issues-number">#1632</span>
    </div>
    <p class="issues-desc"># OpenBroker strips provider prompt-cache metadata (`prompt_tokens_details` is always `null`)  ## Summary  OpenBroker performs prompt/prefix caching — latency collapses from 12–31 s on a cold 52k-toke...</p>
    <div class="issues-labels"><span class="issues-label" style="background-color: #d73a4a; color: #ffffff; border-color: #d73a4a;">bug</span></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/theaungmyatmoe">@theaungmyatmoe</a> opened 16 days ago</span>
      
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="00617-ledger-wallet-integration/">Ledger wallet integration</a>
      <span class="issues-number">#617</span>
    </div>
    
    <div class="issues-labels"></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 20 days ago</span>
      <span class="issues-meta-item"><svg viewBox="0 0 16 16"><path d="M1 2.75C1 1.784 1.784 1 2.75 1h10.5c.966 0 1.75.784 1.75 1.75v7.5A1.75 1.75 0 0 1 13.25 12H9.06l-2.573 2.573A1.458 1.458 0 0 1 4 13.543V12H2.75A1.75 1.75 0 0 1 1 10.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h4.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"/></svg> 1</span>
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="01398-gateway-allowlist-request-niro/">Gateway allowlist request: niro</a>
      <span class="issues-number">#1398</span>
    </div>
    <p class="issues-desc">## Operator  Nichita R. — independent developer Contact: GitHub @niro58  ## Address  gonka142rw2k5qwh3rxm774z56uzcgfyqfnnclqewr36  ## Models  - MiniMaxAI/MiniMax-M2.7 - moonshotai/Kimi-K2.6  ## Use ca...</p>
    <div class="issues-labels"></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/niro58">@niro58</a> opened 20 days ago</span>
      <span class="issues-meta-item"><svg viewBox="0 0 16 16"><path d="M1 2.75C1 1.784 1.784 1 2.75 1h10.5c.966 0 1.75.784 1.75 1.75v7.5A1.75 1.75 0 0 1 13.25 12H9.06l-2.573 2.573A1.458 1.458 0 0 1 4 13.543V12H2.75A1.75 1.75 0 0 1 1 10.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h4.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"/></svg> 1</span>
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="01510-gateway-allowlist-request-bagtyyar-kovusov/">Gateway allowlist request - Bagtyyar Kovusov</a>
      <span class="issues-number">#1510</span>
    </div>
    <p class="issues-desc">## Operator information  - Operator name: Bagtyyar Kovusov - Contact: Discord: key_b.official - Devshard creator address: gonka1zsy3dqrc0h889u32jk40kl7hd2tugt0ymtfy7y - Deployment region: China  ## In...</p>
    <div class="issues-labels"></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/bagtyyarkovusov">@bagtyyarkovusov</a> opened 20 days ago</span>
      <span class="issues-meta-item"><svg viewBox="0 0 16 16"><path d="M1 2.75C1 1.784 1.784 1 2.75 1h10.5c.966 0 1.75.784 1.75 1.75v7.5A1.75 1.75 0 0 1 13.25 12H9.06l-2.573 2.573A1.458 1.458 0 0 1 4 13.543V12H2.75A1.75 1.75 0 0 1 1 10.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h4.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"/></svg> 1</span>
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="01513-build-and-attest-release-binaries-in-ci-instead-of-uploading/">Build and attest release binaries in CI instead of uploading them manually</a>
      <span class="issues-number">#1513</span>
    </div>
    <p class="issues-desc">Release binaries are currently built on a maintainer's machine and uploaded by hand. On v0.2.14 the release was published 2026-07-20, and the four cross-platform `inferenced` binaries were attached 20...</p>
    <div class="issues-labels"></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/KTibow">@KTibow</a> opened 21 days ago</span>
      <span class="issues-meta-item"><svg viewBox="0 0 16 16"><path d="M1 2.75C1 1.784 1.784 1 2.75 1h10.5c.966 0 1.75.784 1.75 1.75v7.5A1.75 1.75 0 0 1 13.25 12H9.06l-2.573 2.573A1.458 1.458 0 0 1 4 13.543V12H2.75A1.75 1.75 0 0 1 1 10.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h4.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"/></svg> 2</span>
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="01593-verification-note-timeoutretry-terminalization-depends-on-pr/">Verification note: timeout/retry terminalization depends on protocol-time, not wall-clock time</a>
      <span class="issues-number">#1593</span>
    </div>
    <p class="issues-desc">Hi Gonka team — we’ve been independently pressure-testing the timeout/retry + accounting path against a pinned local devshard revision (`f040d0a5b5ef207a0c431894c9f9e2608f9d3073`) and found a verifica...</p>
    <div class="issues-labels"></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/safal207">@safal207</a> opened 26 days ago</span>
      
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="01591-gateway-timeout-can-orphan-client-correlation-from-completed/">Gateway timeout can orphan client correlation from completed request accounting</a>
      <span class="issues-number">#1591</span>
    </div>
    <p class="issues-desc">## Summary  I’ve been independently testing Gonka’s gateway/request-accounting flow in the local devshard test environment and found a reproducible causal-addressability edge case around client timeou...</p>
    <div class="issues-labels"></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/safal207">@safal207</a> opened 27 days ago</span>
      
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="00850-bug-managedstorage-silently-skips-failed-epoch-pruning-minpr/">Bug: ManagedStorage silently skips failed epoch pruning — minPruned advanced before goroutines complete</a>
      <span class="issues-number">#850</span>
    </div>
    <p class="issues-desc">## Location  `decentralized-api/payloadstorage/managed_storage.go` — lines 129–138  ## Description  In `ManagedStorage.cleanup()`, `m.minPruned` is advanced to `threshold` **before** the pruning gorou...</p>
    <div class="issues-labels"></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/Mayveskii">@Mayveskii</a> opened 28 days ago</span>
      <span class="issues-meta-item"><svg viewBox="0 0 16 16"><path d="M1 2.75C1 1.784 1.784 1 2.75 1h10.5c.966 0 1.75.784 1.75 1.75v7.5A1.75 1.75 0 0 1 13.25 12H9.06l-2.573 2.573A1.458 1.458 0 0 1 4 13.543V12H2.75A1.75 1.75 0 0 1 1 10.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h4.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"/></svg> 1</span>
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="01570-devshard-timeout-vote-threshold-unreachable-under-skewed-slo/">Devshard: timeout-vote threshold unreachable under skewed slot distribution — stranded nonce cannot be resolved (liveness)</a>
      <span class="issues-number">#1570</span>
    </div>
    <p class="issues-desc">## Summary  When a Devshard escrow's slots are distributed unevenly across participants, the **timeout-vote path can become structurally unable to reach its weight threshold**, leaving a stranded nonc...</p>
    <div class="issues-labels"></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/kAIPraxisBot">@kAIPraxisBot</a> opened 29 days ago</span>
      <span class="issues-meta-item"><svg viewBox="0 0 16 16"><path d="M1 2.75C1 1.784 1.784 1 2.75 1h10.5c.966 0 1.75.784 1.75 1.75v7.5A1.75 1.75 0 0 1 13.25 12H9.06l-2.573 2.573A1.458 1.458 0 0 1 4 13.543V12H2.75A1.75 1.75 0 0 1 1 10.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h4.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"/></svg> 1</span>
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="01539-hardening-network-duty-fee-bypass-admits-zero-fee-txs-from-n/">Hardening: network-duty fee-bypass admits zero-fee txs from non-participants (no signer authorization at the ante layer)</a>
      <span class="issues-number">#1539</span>
    </div>
    <p class="issues-desc">## Summary  `NetworkDutyFeeBypassDecorator` waives fees + clears min-gas-price for ~12 "network duty" message types, and the exemption is decided **purely by Go message type** (`isExemptMessageType` i...</p>
    <div class="issues-labels"></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/kAIPraxisBot">@kAIPraxisBot</a> opened 29 days ago</span>
      <span class="issues-meta-item"><svg viewBox="0 0 16 16"><path d="M1 2.75C1 1.784 1.784 1 2.75 1h10.5c.966 0 1.75.784 1.75 1.75v7.5A1.75 1.75 0 0 1 13.25 12H9.06l-2.573 2.573A1.458 1.458 0 0 1 4 13.543V12H2.75A1.75 1.75 0 0 1 1 10.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h4.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"/></svg> 1</span>
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="01572-bug-unauthenticated-mlnode-trainstart-accepts-a-raw-dict-let/">[BUG] Unauthenticated mlnode /train/start accepts a raw dict, letting a remote attacker control training and inject arbitrary process environment variables on GPU workers</a>
      <span class="issues-number">#1572</span>
    </div>
    <p class="issues-desc">**Summary** The mlnode control API exposes POST /api/v1/train/start with no authentication and no schema — the handler takes a raw dict. From that dict, the service sets arbitrary process environment...</p>
    <div class="issues-labels"><span class="issues-label" style="background-color: #d73a4a; color: #ffffff; border-color: #d73a4a;">bug</span></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/iceiceic3">@iceiceic3</a> opened 29 days ago</span>
      <span class="issues-meta-item"><svg viewBox="0 0 16 16"><path d="M1 2.75C1 1.784 1.784 1 2.75 1h10.5c.966 0 1.75.784 1.75 1.75v7.5A1.75 1.75 0 0 1 13.25 12H9.06l-2.573 2.573A1.458 1.458 0 0 1 4 13.543V12H2.75A1.75 1.75 0 0 1 1 10.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h4.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"/></svg> 1</span>
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="01573-bug-devshard-executor-can-validate-its-own-challenged-result/">[BUG] devshard executor can validate its own challenged result, letting a fraudulent executor push a bad settlement and steal escrowed funds</a>
      <span class="issues-number">#1573</span>
    </div>
    <p class="issues-desc">**Summary** In devshard’s challenge/validation flow, applyValidationVote does not reject a validation vote cast by the same party that produced the challenged result. Combined with the fact that the S...</p>
    <div class="issues-labels"><span class="issues-label" style="background-color: #d73a4a; color: #ffffff; border-color: #d73a4a;">bug</span></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/iceiceic3">@iceiceic3</a> opened 29 days ago</span>
      <span class="issues-meta-item"><svg viewBox="0 0 16 16"><path d="M1 2.75C1 1.784 1.784 1 2.75 1h10.5c.966 0 1.75.784 1.75 1.75v7.5A1.75 1.75 0 0 1 13.25 12H9.06l-2.573 2.573A1.458 1.458 0 0 1 4 13.543V12H2.75A1.75 1.75 0 0 1 1 10.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h4.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"/></svg> 1</span>
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="01466-better-devshardd-inference-handling/">Better devshardd inference handling</a>
      <span class="issues-number">#1466</span>
    </div>
    <p class="issues-desc">While reviewing this PR: https://github.com/gonka-ai/gonka/pull/1460 I have found couple of problems/tasks, and listed them at PR comment https://github.com/gonka-ai/gonka/pull/1460#issuecomment-50017...</p>
    <div class="issues-labels"></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/a-kuprin">@a-kuprin</a> opened 29 days ago</span>
      <span class="issues-meta-item"><svg viewBox="0 0 16 16"><path d="M1 2.75C1 1.784 1.784 1 2.75 1h10.5c.966 0 1.75.784 1.75 1.75v7.5A1.75 1.75 0 0 1 13.25 12H9.06l-2.573 2.573A1.458 1.458 0 0 1 4 13.543V12H2.75A1.75 1.75 0 0 1 1 10.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h4.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"/></svg> 2</span>
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="00983-bug-get-apiv1epochsnparticipants-returns-500-for-past-epochs/">Bug: GET /api/v1/epochs/{N}/participants returns 500 for past epochs (CreatedAtBlockHeight=0)</a>
      <span class="issues-number">#983</span>
    </div>
    <p class="issues-desc">## Bug  `GET /api/v1/epochs/{N}/participants` returns **500 Internal Server Error** for past epochs. Current epoch works fine.  ## Repro  ``` GET http://node1.gonka.ai:8000/api/v1/epochs/215/participa...</p>
    <div class="issues-labels"></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/mingles-agent">@mingles-agent</a> opened 2026-08-06</span>
      <span class="issues-meta-item"><svg viewBox="0 0 16 16"><path d="M1 2.75C1 1.784 1.784 1 2.75 1h10.5c.966 0 1.75.784 1.75 1.75v7.5A1.75 1.75 0 0 1 13.25 12H9.06l-2.573 2.573A1.458 1.458 0 0 1 4 13.543V12H2.75A1.75 1.75 0 0 1 1 10.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h4.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"/></svg> 3</span>
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="01225-p2-clean-pow-from-mlnode-and-keep-poc-networking-patch-local/">[P2] Clean PoW from MLNode and keep PoC networking patch local</a>
      <span class="issues-number">#1225</span>
    </div>
    <p class="issues-desc">The task was completed by Aleksandr @a-kuprin here: https://github.com/gonka-ai/gonka/pull/994  However, it was submitted from his previous account, which is currently blocked, so the PR is not access...</p>
    <div class="issues-labels"><span class="issues-label" style="background-color: #95b500; color: #24292f; border-color: #95b500;">Priority: Low</span></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 2026-08-06</span>
      <span class="issues-meta-item"><svg viewBox="0 0 16 16"><path d="M1 2.75C1 1.784 1.784 1 2.75 1h10.5c.966 0 1.75.784 1.75 1.75v7.5A1.75 1.75 0 0 1 13.25 12H9.06l-2.573 2.573A1.458 1.458 0 0 1 4 13.543V12H2.75A1.75 1.75 0 0 1 1 10.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h4.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"/></svg> 1</span>
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="01545-bug-post-v1participants-returns-unclear-error-for-malformed-/">[BUG] POST /v1/participants returns unclear error for malformed JSON</a>
      <span class="issues-number">#1545</span>
    </div>
    <p class="issues-desc">## Description  `POST /v1/participants` returns a nested parser error when the request body contains malformed JSON.  ## Current behavior  ```json {"error":{"message":"unexpected EOF"}} ```  ## Expect...</p>
    <div class="issues-labels"><span class="issues-label" style="background-color: #d73a4a; color: #ffffff; border-color: #d73a4a;">bug</span></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/Parikalp-Bhardwaj">@Parikalp-Bhardwaj</a> opened 2026-08-04</span>
      
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="01537-bug-api-test-does-not-apply-portable-blst-flags-on-apple-sil/">[BUG] api-test does not apply portable BLST flags on Apple Silicon</a>
      <span class="issues-number">#1537</span>
    </div>
    <p class="issues-desc">## Description  On Apple Silicon, `scripts/blst-portable.mk` sets:  ```text BLST_PORTABLE=1 ```  but the `api-test` target does not apply `BLST_PORTABLE_CGO_CFLAGS`.  As a result, BLST-dependent packa...</p>
    <div class="issues-labels"><span class="issues-label" style="background-color: #d73a4a; color: #ffffff; border-color: #d73a4a;">bug</span></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/Parikalp-Bhardwaj">@Parikalp-Bhardwaj</a> opened 2026-08-03</span>
      
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="01529-devshard-v4-epoch-prune-leaves-zombie-in-memory-hosts-append/">devshard v4: epoch prune leaves zombie in-memory Hosts → AppendDiff session not found</a>
      <span class="issues-number">#1529</span>
    </div>
    <p class="issues-desc">## Summary  On testnet (`gonka-testnet`, participant `versiond` / `devshardd` `0.2.14-v4-r4`), gateway chat fails with:  ```text persist diff nonce N: diff persist retries exhausted: session not found...</p>
    <div class="issues-labels"></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/maria-mitina">@maria-mitina</a> opened 2026-08-01</span>
      <span class="issues-meta-item"><svg viewBox="0 0 16 16"><path d="M1 2.75C1 1.784 1.784 1 2.75 1h10.5c.966 0 1.75.784 1.75 1.75v7.5A1.75 1.75 0 0 1 13.25 12H9.06l-2.573 2.573A1.458 1.458 0 0 1 4 13.543V12H2.75A1.75 1.75 0 0 1 1 10.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h4.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"/></svg> 1</span>
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="01506-gateway-host-health-deadlock-mass-quarantine-all-hosts-stuck/">Gateway host-health deadlock: mass quarantine → all hosts stuck as no-winner/suspicious</a>
      <span class="issues-number">#1506</span>
    </div>
    <p class="issues-desc">## Summary  I managed to get all hosts into a kind of deadlock on testnet.  ### How everyone entered quarantine  I created an escrow with the wrong owner (CLI key ≠ `DEVSHARD_PRIVATE_KEY` the gateway...</p>
    <div class="issues-labels"></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/maria-mitina">@maria-mitina</a> opened 2026-07-30</span>
      <span class="issues-meta-item"><svg viewBox="0 0 16 16"><path d="M1 2.75C1 1.784 1.784 1 2.75 1h10.5c.966 0 1.75.784 1.75 1.75v7.5A1.75 1.75 0 0 1 13.25 12H9.06l-2.573 2.573A1.458 1.458 0 0 1 4 13.543V12H2.75A1.75 1.75 0 0 1 1 10.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h4.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"/></svg> 3</span>
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="00435-bug-report-api-container-sends-abci-query-with-height-0-desp/">Bug Report: api container sends abci_query with height: 0 despite being synced</a>
      <span class="issues-number">#435</span>
    </div>
    <p class="issues-desc">Bug Report: api container sends abci_query with height: 0 despite being synced Title: api container sends abci_query for EpochInfo with "height":"0", causing requests to /v1/epochs/current/participant...</p>
    <div class="issues-labels"></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/VaniaHilkovets">@VaniaHilkovets</a> opened 2026-07-29</span>
      <span class="issues-meta-item"><svg viewBox="0 0 16 16"><path d="M1 2.75C1 1.784 1.784 1 2.75 1h10.5c.966 0 1.75.784 1.75 1.75v7.5A1.75 1.75 0 0 1 13.25 12H9.06l-2.573 2.573A1.458 1.458 0 0 1 4 13.543V12H2.75A1.75 1.75 0 0 1 1 10.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h4.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"/></svg> 2</span>
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="01408-model-lineup-improvement-add-an-accessible-glm-52-candidate-/">Model lineup improvement: add an accessible GLM-5.2 candidate and reconsider MiniMax-M2.7 as default</a>
      <span class="issues-number">#1408</span>
    </div>
    <p class="issues-desc">## Model lineup improvement: add an accessible GLM-5.2 candidate and reconsider the default model  ### Problem  At the moment, the network appears to have very limited active capacity for `GLM-5.2`....</p>
    <div class="issues-labels"><span class="issues-label" style="background-color: #a2eeef; color: #24292f; border-color: #a2eeef;">enhancement</span></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/enonog">@enonog</a> opened 2026-07-25</span>
      <span class="issues-meta-item"><svg viewBox="0 0 16 16"><path d="M1 2.75C1 1.784 1.784 1 2.75 1h10.5c.966 0 1.75.784 1.75 1.75v7.5A1.75 1.75 0 0 1 13.25 12H9.06l-2.573 2.573A1.458 1.458 0 0 1 4 13.543V12H2.75A1.75 1.75 0 0 1 1 10.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h4.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"/></svg> 3</span>
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="01450-dynamic-pricing-price-pinned-at-min-by-integer-truncation-ca/">Dynamic pricing: price pinned at min by integer truncation; capacity proxy miscalibrated per model</a>
      <span class="issues-number">#1450</span>
    </div>
    <p class="issues-desc">Reporting two verified defects in the dynamic-pricing keeper. Everything below was checked against tag `release/v0.2.13` (the mainnet chain version) and against live mainnet state via `node3.gonka.ai`...</p>
    <div class="issues-labels"></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/len5ky">@len5ky</a> opened 2026-07-24</span>
      
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="01480-gateway-allowlist-request-ancapex/">Gateway allowlist request: Ancapex</a>
      <span class="issues-number">#1480</span>
    </div>
    <p class="issues-desc">**Operator**  Ancapex — mining platform for Gonka (https://ancapex.ai/) Contact: <GitHub @alancapex / al@ancapex.ai> About Ancapex  Ancapex is a platform for mining on the Gonka Network. Launched as a...</p>
    <div class="issues-labels"></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/alancapex">@alancapex</a> opened 2026-07-23</span>
      <span class="issues-meta-item"><svg viewBox="0 0 16 16"><path d="M1 2.75C1 1.784 1.784 1 2.75 1h10.5c.966 0 1.75.784 1.75 1.75v7.5A1.75 1.75 0 0 1 13.25 12H9.06l-2.573 2.573A1.458 1.458 0 0 1 4 13.543V12H2.75A1.75 1.75 0 0 1 1 10.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h4.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"/></svg> 2</span>
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="01493-request-to-be-added-as-a-gonka-broker-devshard-escrow-creato/">Request to be added as a Gonka broker (devshard escrow creator allowlist)</a>
      <span class="issues-number">#1493</span>
    </div>
    <p class="issues-desc">```markdown Hi Gonka core team & community,  Requesting inclusion of our escrow creator address in `devshard_escrow_params.allowed_creator_addresses` to operate a self-hosted devshard gateway.  ## Esc...</p>
    <div class="issues-labels"></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/nikshh">@nikshh</a> opened 2026-07-22</span>
      
    </div>
  </div>
</li>
<li class="issues-list-item">
  <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
  <div class="issues-body">
    <div class="issues-title">
      <a href="01222-p1-int-overflow/">[P1] Int overflow</a>
      <span class="issues-number">#1222</span>
    </div>
    <p class="issues-desc">The goal of this is to have in place after this a standard way of handling possible overflows, have it implemented consistently across the entire codebase and to have a check (preferably a static chec...</p>
    <div class="issues-labels"><span class="issues-label" style="background-color: #12a6e8; color: #24292f; border-color: #12a6e8;">Priority: Medium</span> <span class="issues-label" style="background-color: #aaaaaa; color: #24292f; border-color: #aaaaaa;">nice-to-have</span></div>
    <div class="issues-meta">
      <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 2026-07-22</span>
      <span class="issues-meta-item"><svg viewBox="0 0 16 16"><path d="M1 2.75C1 1.784 1.784 1 2.75 1h10.5c.966 0 1.75.784 1.75 1.75v7.5A1.75 1.75 0 0 1 13.25 12H9.06l-2.573 2.573A1.458 1.458 0 0 1 4 13.543V12H2.75A1.75 1.75 0 0 1 1 10.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h4.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"/></svg> 6</span>
    </div>
  </div>
</li>
</ul>
