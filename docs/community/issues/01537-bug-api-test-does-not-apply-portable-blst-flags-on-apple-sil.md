---
title: "#1537 — [BUG] api-test does not apply portable BLST flags on Apple Silicon"
source: https://github.com/gonka-ai/gonka/issues/1537
issue_number: 1537
synced_at: 2026-08-10T17:13:16Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    [BUG] api-test does not apply portable BLST flags on Apple Silicon
    <span class="issues-number">#1537</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/Parikalp-Bhardwaj">@Parikalp-Bhardwaj</a> opened 2026-08-03 14:53 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-08-03 14:53 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #d73a4a; color: #ffffff; border-color: #d73a4a;">bug</span></div>
</div>

<div class="issues-content" markdown="1">
## Description

On Apple Silicon, `scripts/blst-portable.mk` sets:

```text
BLST_PORTABLE=1
```

but the `api-test` target does not apply `BLST_PORTABLE_CGO_CFLAGS`.

As a result, BLST-dependent packages fail with:

```text
Caught SIGILL in blst_cgo_init
```

## Environment

```text
Host: arm64
Go: darwin/amd64
CGO_ENABLED: 1
```

## Reproduction

```bash
make api-test
```

## Proposed fix

Apply the existing portable BLST flags when `BLST_PORTABLE=1`:

```makefile
CGO_CFLAGS="$(go env CGO_CFLAGS) -O2 $(BLST_PORTABLE_CGO_CFLAGS)"
```

## Verification

After the change:

```text
Passed: 1097 tests
Failed: 0 tests
```

I have a minimal Makefile patch ready.

</div>

---

> 🔄 **Auto-synced** from [Issue #1537](https://github.com/gonka-ai/gonka/issues/1537) every hour.
