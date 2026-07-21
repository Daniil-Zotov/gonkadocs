---
title: "#857 — Test voting delegation"
source: https://github.com/gonka-ai/gonka/issues/857
issue_number: 857
synced_at: 2026-07-21T14:28:55Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    Test voting delegation
    <span class="issues-number">#857</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/maria-mitina">@maria-mitina</a> opened 2026-03-03 18:30 UTC</span>
    <span class="issues-meta-item">4 comments</span>
    <span class="issues-meta-item">Updated 2026-03-06 00:15 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
In order to make voting more convenient for the contributors, we are exploring delegation of voting rights. The flow of the delegation is the following:
Granter gives grantee permission to send specific message types on their behalf. The grantee uses MsgExec to run those messages; the chain checks the authz grant and treats the message as coming from the granter.


Permissions needs to:
1. be granted
2. allow action under permission to be executed
3. be revoked if necessary

Testnet will be used for the flow verification. 
</div>

---

## 💬 Comments (4)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/maria-mitina">@maria-mitina</a></span>
    <span class="issues-meta-item">commented 2026-03-04 12:15 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>all test cases on testnet PASSED with a caveat that the TX does not fail explicitly. (<strong>Expected:</strong> Tx fails (e.g. “authorization not found” / “unauthorized”). <strong>Reality:</strong> Nothing indicating that the voting did not go through)</p>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>

<meta http-equiv="Content-Style-Type" content="text/css">
<meta name="Generator" content="Cocoa HTML Writer">
<meta name="CocoaVersion" content="2685.3">
</head>
<body>
<p class="p1"><br></p>
<p class="p2"><b>1. [pass] Happy path</b></p>
<ul class="ul1">
<li class="li2">[pass] Grant → Grantee votes (Yes) with authz exec → Tx succeeds → Proposal votes show granter with Yes.</li>
<li class="li2">[pass] same for Abstain, No, and NoWithVeto.</li>
</ul>
<p class="p1"><br></p>
<p class="p2"><b>2. [pass] Revoke</b></p>
<ul class="ul1">
<li class="li2">Revoke MsgVote for that grantee.</li>
<li class="li2">Grantee runs authz exec again (same or new proposal).</li>
<li class="li3"><b>Expected: Tx fails (e.g. “authorization not found” / “unauthorized”). ——— fail here! Nothing indicating that the voting did not go through</b><b></b></li>
<li class="li2">[pass] Variant: Revoke, then re-grant → grantee votes again → expected success.</li>
</ul>
<p class="p1"><br></p>
<p class="p2"><b>3. [pass] Overwrite / double vote</b></p>
<ul class="ul1">
<li class="li2"><b>[pass]</b> 3a. Grantee votes, then granter votes (no revoke)</li>
</ul>
<p class="p2">Grantee votes Yes via authz exec → granter votes No (or Yes) with main key.</p>
<p class="p2">Expected: second vote replaces first (only one vote per address)</p>
<ul class="ul1">
<li class="li2"><b>[pass]</b> 3b. Grantee votes, then revoke, then granter votes</li>
</ul>
<p class="p2">Grantee votes → revoke → granter votes with main key.</p>
<p class="p2">Expected: Granter’s direct vote is valid; grantee can no longer vote (revoke test).</p>
<p class="p1"><br></p>
<p class="p2"><b>4. [pass] Wrong signer / wrong grantee</b></p>
<ul class="ul1">
<li class="li2"><b>[pass]</b> 4a. Wrong --from</li>
</ul>
<p class="p2">JSON has <span class="s1">grantee = A</span>, but you sign with key for B (or granter key).</p>
<p class="p4"><b>Expected: Tx fails (e.g. “authorization not found” / “unauthorized”). ——— fail here! Nothing indicating that the voting did not go through</b><b></b></p>
<ul class="ul1">
<li class="li2"><b>[pass] </b>4b. Wrong grantee in JSON</li>
</ul>
<p class="p2"><span class="s1">grantee</span> in JSON is not the address that was actually granted.</p>
<p class="p2">Expected: Tx fails when chain checks authz.</p>
<p class="p1"><br></p>
<ol class="ol1">
<li class="li2"><b>[pass] Authorization boundaries</b></li>
</ol>
<ul class="ul1">
<li class="li2"><b>[pass]</b> 5a. Wrong proposal</li>
</ul>
<p class="p2">Grant is for MsgVote; grantee sends vote for proposal_id that doesn’t exist or is not in voting.</p>
<p class="p4"><b>Nothing indicating that the voting did not go through</b><b></b></p>
<ul class="ul1">
<li class="li2"><b>[pass]</b> 5b. Wrong message type</li>
</ul>
<p class="p2">Grant is only for <span class="s1">/cosmos.gov.v1beta1.MsgVote</span>. Grantee sends authz exec with a different message (e.g. Send).</p>
<p class="p4"><b>Nothing indicating that the voting did not go through - however the money was not sent</b><b></b></p>
<ul class="ul1">
<li class="li2"><b>[pass]</b> 5c. Expired grant</li>
</ul>
<p class="p2">Create grant with short expiration, wait until after expiry, then grantee votes.</p>
<p class="p4"><b>Nothing indicating that the voting did not go through</b><b></b></p>
<p class="p1"><br></p>
<p class="p2"><b>8. [pass] Multiple grantees</b></p>
<ul class="ul1">
<li class="li2">Granter grants MsgVote to grantee A and grantee B (two grants).</li>
<li class="li2">A votes Yes, B votes No (or abstain) on behalf of the same granter.</li>
</ul>
<p class="p2">Expected: second exec overwrites.</p>
<p class="p1"><br></p>
<p class="p2"><b>9. [pass] Tally and visibility</b></p>
<ul class="ul1">
<li class="li2">After a successful authz exec, query proposal votes by proposal id.</li>
<li class="li2">Expected: Listed voter is granter address, option matches what you sent (Yes/No/Abstain/NoWithVeto).</li>
</ul>
<p class="p1"><br></p>
<p class="p2"><b>9. Summary table (for your setup)</b></p>

Test | Action | Expected
-- | -- | --
Happy path | Grant → grantee exec (Yes) | Success; granter has Yes on proposal
Revoke | Revoke → grantee exec | Fail (no permission)
Overwrite (no revoke) | Grantee votes → granter votes on main | Second vote replaces or fails (define)
Overwrite (with revoke) | Grantee votes → revoke → granter votes | Granter vote succeeds; grantee cannot vote
Change vote | Grantee Yes → grantee No (same proposal) | Replace or “not allowed” (define)
Wrong signer | exec with --from ≠ grantee | Fail
Wrong grantee in JSON | grantee ≠ actual grantee | Fail
Wrong proposal | Vote for invalid/wrong proposal_id | Fail
Wrong message type | Exec a non‑granted message type | Fail
Expired grant | Vote after grant expiration | Fail
Tally | Query votes after success | Granter appears with correct option


</body>
</html>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2026-03-05 23:46 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Hey @mayveskii, could you please clarify why you referenced this issue in [d4e74c4] and [e5995db]? Do you have any issues with delegating?</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/Mayveskii">@Mayveskii</a></span>
    <span class="issues-meta-item">commented 2026-03-06 00:05 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <blockquote>
<p>Hey <a href="https://github.com/Mayveskii">@Mayveskii</a>, could you please clarify why you referenced this issue in [<a href="https://github.com/gonka-ai/gonka/commit/d4e74c4da683bb4a1ee894a5004af2247ac65c3c">d4e74c4</a>] and [<a href="https://github.com/gonka-ai/gonka/commit/e5995db2391d9d1b9037ffd0b3c5d2344437bd2c">e5995db</a>]? Do you have any issues with delegating?</p>
</blockquote>
<p>Hi, Tanya!  I'm interested in participating as a grantee in the delegation test.</p>
<p>My address: gonka1l38meyucc0ajwdhn6ssevsj0xpvm3dysu59mh8
Account registered on-chain: account_number 1130693</p>
<p>Could you also send a small amount of tokens to this address so I can participate? 
Currently working on GIP #859 (semantic cache) and need tokens for both the delegation test and inference validation.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/Mayveskii">@Mayveskii</a></span>
    <span class="issues-meta-item">commented 2026-03-06 00:15 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <blockquote>
<p>Hey <a href="https://github.com/Mayveskii">@Mayveskii</a>, could you please clarify why you referenced this issue in [<a href="https://github.com/gonka-ai/gonka/commit/d4e74c4da683bb4a1ee894a5004af2247ac65c3c">d4e74c4</a>] and [<a href="https://github.com/gonka-ai/gonka/commit/e5995db2391d9d1b9037ffd0b3c5d2344437bd2c">e5995db</a>]? Do you have any issues with delegating?</p>
</blockquote>
<p>I referenced it intentionally — while working on GIP #859 
I found that MsgSubmitCacheQualitySummary was missing from 
InferenceOperationKeyPerms, which was blocking the Grant→Exec→Revoke 
flow you're testing in #857. Fixed it as part of the same permissions audit. 
No issues with delegating.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #857](https://github.com/gonka-ai/gonka/issues/857) every hour.
