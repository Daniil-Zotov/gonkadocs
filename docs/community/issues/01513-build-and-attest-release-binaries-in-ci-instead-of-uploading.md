---
title: "#1513 — Build and attest release binaries in CI instead of uploading them manually"
source: https://github.com/gonka-ai/gonka/issues/1513
issue_number: 1513
synced_at: 2026-07-30T03:36:09Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Build and attest release binaries in CI instead of uploading them manually
    <span class="issues-number">#1513</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/KTibow">@KTibow</a> opened 2026-07-28 20:05 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-07-28 20:05 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
Release binaries are currently built on a maintainer's machine and uploaded by hand. On v0.2.14 the release was published 2026-07-20, and the four cross-platform `inferenced` binaries were attached 2026-07-27 — six days later.

```bash
gh api repos/gonka-ai/gonka/releases/tags/release/v0.2.15 \
  --jq '[.assets[].uploader.type] | unique'
# ["User"]    — not github-actions[bot]; same on v0.2.14
```

There are also no build attestations, so `gh attestation verify` has nothing to check:

```bash
gh api repos/gonka-ai/gonka/attestations/sha256:<digest>
# 404
```

So that someone downloading `inferenced` has no way to confirm the binary corresponds to any particular commit in this repo. That matters more for `inferenced` than for most artifacts here, because it's the key-custody tool — `inferenced keys add` generates the mnemonic, and `keys export --unarmored-hex` emits the raw private key. Following the OpenBroker flow, that key is then permanently bound to a broker account.

Building the artifacts in Actions and attesting them there would bind each one to a commit and workflow by a signature that can't be produced from a laptop:

```yaml
permissions:
  contents: write
  id-token: write
  attestations: write

steps:
  # ... build release artifacts ...
  - uses: actions/attest-build-provenance@v2
    with:
      subject-path: 'release/*'
```

For what it's worth, the project already does something stronger than most in this area — `devshard_escrow_params.approved_versions` pins a governance-voted `sha256` for `devshardd` on-chain. That's a genuine multi-party trust anchor. It just doesn't extend to the binaries end users download.

I asked Claude to look into this and it found this:

---

The repo does contain a release workflow, `.github/workflows/release.yml`, but it has never published an artifact. Across the 30 most recent runs (back to 2026-02-20), every **success** is a no-op — `should_release` is false, so `Issue Release Assets` and `Publish the Release` both report `→ skipped` — and every run that actually attempted a build **failed**, all with the same error:

```
could not locate your app's root dir: go.mod not found
```

It's unmodified ignite scaffolding that was never wired up for this repo's layout. The workflow sets `defaults.run.working-directory: ./inference-chain`, but that only applies to `run:` steps, and the build is a `uses:` step (`ignite/cli/actions/cli@main`, a Docker action with no inputs). So ignite executes at the workspace root, where there's no `go.mod` — the module is at `inference-chain/go.mod`.

Even repaired it wouldn't produce the releases in question. The trigger was narrowed from the scaffold's `on: push` to `on: push: branches: [main]`, which drops the tag path, so `ignite/cli/actions/release/vars` always resolves `tag_name=latest`. It could only ever publish a rolling `latest` prerelease, never `release/v0.2.x`.

It also has no arm64 Linux target — the release targets are `-t linux:amd64 -t darwin:amd64 -t darwin:arm64` — yet `inferenced-linux-arm64.zip` ships on both v0.2.14 and v0.2.15. Whatever produced that file, it wasn't CI.

Given it has never worked, can't produce tagged releases by design, and fails on every push to `main`, deleting it looks more sensible than repairing it. `Multi-Platform Build` already covers compile verification on PRs.
</div>

---

> 🔄 **Auto-synced** from [Issue #1513](https://github.com/gonka-ai/gonka/issues/1513) every hour.
