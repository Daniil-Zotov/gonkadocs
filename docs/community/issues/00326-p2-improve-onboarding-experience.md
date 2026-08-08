---
title: "#326 — [P2] Improve onboarding experience"
source: https://github.com/gonka-ai/gonka/issues/326
issue_number: 326
synced_at: 2026-08-08T02:25:19Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    [P2] Improve onboarding experience
    <span class="issues-number">#326</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 2025-09-03 23:10 UTC</span>
    <span class="issues-meta-item">4 comments</span>
    <span class="issues-meta-item">Updated 2026-06-24 01:10 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
Improve onboarding experience: 

- [ ] Clearer logging when node is launched and waiting for PoC
- [ ] remove errors which doesn’t mean errors
- [ ] automatic testing that everything will work when PoC starts (models can be deployed, all endpoints are accessible); 
- [ ] Clean up logs to avoid confusing ERROR messages;

Description of the proposal: 
[https://github.com/gonka-ai/gonka/blob/a2a15267ea4aa55288fc873f4e5e68bc69366447/proposals/onboarding-clarity-v1/README.md](https://www.google.com/url?q=https://github.com/gonka-ai/gonka/blob/a2a15267ea4aa55288fc873f4e5e68bc69366447/proposals/onboarding-clarity-v1/README.md&sa=D&source=docs&ust=1756918029145609&usg=AOvVaw3j8xsw5yvYWpDeCcVHBhZY)
</div>

---

## 💬 Comments (4)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/Pegasus-starry">@Pegasus-starry</a></span>
    <span class="issues-meta-item">commented 2025-12-08 18:47 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <ol>
<li>How to judge if participant is actually in active set?  Is it the state from client: "current_status": "INFERENCE"?</li>
<li>About "Pre-PoC Validation Flow...Manual testing request through admin interface...Send test inference request and validate response".  How to do this scenario? Is it to invoke mlnode interface "/v1/pow/init/generate" of mlnode in directory decentralized-api/internal/server/admin/?</li>
<li>About "Provide countdown timers for user interfaces &amp; Alert users when they should be online."，is it need to provide one new interface and where the countdown info should be shown?  what's more,  how to alert users proactively?<br />
Or just shown in log ?</li>
</ol>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/DimaOrekhovPS">@DimaOrekhovPS</a></span>
    <span class="issues-meta-item">commented 2025-12-09 01:15 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <ol>
<li>
<p>You can use query defined in <code>query_current_epoch_group_data.go</code> and then iterate over participants. If you need to access this data in <code>decentralized-api</code> please make a client with <code>NewInferenceQueryClient</code></p>
</li>
<li>
<p>I think we should create a new admin endpoint, something like <code>admin/v1/test-poc</code>, then it should automatically locate all nodes that aren't busy and start PoC by sending <code>/v1/pow/init/generate</code> to them. Ideally it should also confirm that it receives the batches back. Maybe it should an external script? @gmorgachev what do you think?</p>
</li>
<li>
<p>I think the proposal just asks to show this info in logs clearly</p>
</li>
</ol>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2026-03-21 01:03 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Hey @zyz-007 @jacky6block @icydark @wushuo-6 @mumu714 @Ryanchen911 @x0152 @akup! It would be great if some of you could sync on the next steps for this pull request and make the needed decisions together. If you are able to move it forward on your own, it could potentially be included in v0.2.12. But overall, this is a nice-to-have rather than something critical.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2026-05-22 01:04 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Hey @zyz-007 @jacky6block @icydark @Ryanchen911 @x0152! It would be great if some of you could sync on the next steps for this issue and make the needed decisions together. If you are able to move it forward on your own, it could potentially be included in v0.2.14. But overall, this is a nice-to-have rather than something critical.</p>
<p>See: https://github.com/gonka-ai/gonka/pull/866#issuecomment-4172544143</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #326](https://github.com/gonka-ai/gonka/issues/326) every hour.
