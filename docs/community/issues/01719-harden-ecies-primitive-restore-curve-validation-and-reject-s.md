---
title: "#1719 — Harden ECIES primitive: restore curve validation and reject short ciphertexts"
source: https://github.com/gonka-ai/gonka/issues/1719
issue_number: 1719
synced_at: 2026-09-08T21:55:05Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Harden ECIES primitive: restore curve validation and reject short ciphertexts
    <span class="issues-number">#1719</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 2026-09-04 23:26 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-09-07 19:21 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #4cbc0f; color: #24292f; border-color: #4cbc0f;">up-for-grabs</span></div>
</div>

<div class="issues-content" markdown="1">
The application-level gate here looks right, but the root cause is still live in `github.com/gonka-ai/cosmos-sdk`: `crypto/ecies` diverges from the go-ethereum code it was copied from in two places — `GenerateShared` dropped the `IsOnCurve` check, and `Decrypt`'s length gate is `rLen+hLen+1` (98) instead of `rLen+hLen+params.BlockSize` (113). Anything in the 98–112 band reaches `symDecrypt`, where `make([]byte, len(ct)-params.BlockSize)` is a negative length and panics.

That means this PR fixes one caller, not the primitive. `kr.Decrypt` / `ecies.Decrypt` stays panic-on-attacker-input for every other consumer, now and future, and the new `decryptKeyring` recover is what stands between us and a process kill. Better to fix it upstream in the fork — restore the `IsOnCurve` check in `GenerateShared` and raise the `Decrypt` floor to `rLen+hLen+params.BlockSize`, matching geth — and keep this PR as defense-in-depth. Worth adding the 98-byte regression test on the fork side too, since `ecies_short_ciphertext_test.go` currently reimplements the fork's KDF/MAC internals from outside the module just to reach the panic.

I think it is good to fix primitive, while PR sounds and closes what it should

_Originally posted by @a-kuprin in https://github.com/gonka-ai/gonka/issues/1687#issuecomment-5509311830_
            
</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/redstartechno">@redstartechno</a></span>
    <span class="issues-meta-item">commented 2026-09-07 19:21 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Picked this up: gonka-ai/cosmos-sdk#20 restores both guards verbatim from go-ethereum (<code>IsOnCurve</code> in <code>GenerateShared</code>, <code>rLen + hLen + params.BlockSize</code> floor in <code>Decrypt</code>) and adds the fork-side regression tests, including the 98-byte case, which panics on <code>release/v0.53.x</code> today.</p>
<p>One thing to plan for when the fork tag is bumped here: <code>TestDecryptKeyringShortMACValidReturnsError</code> in <code>decentralized-api/cosmosclient</code> asserts on the <code>"ecies decrypt panic"</code> message. With the primitive fixed, <code>Decrypt</code> returns <code>ecies: invalid message</code> instead, so that assertion needs to become <code>require.Error</code>. Happy to open that follow-up alongside the <code>go.mod</code> bump.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1719](https://github.com/gonka-ai/gonka/issues/1719) every hour.
