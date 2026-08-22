---
title: "#1513 — Build and attest release binaries in CI instead of uploading them manually"
source: https://github.com/gonka-ai/gonka/issues/1513
issue_number: 1513
synced_at: 2026-08-22T01:53:49Z
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
    <span class="issues-meta-item">2 comments</span>
    <span class="issues-meta-item">Updated 2026-08-19 03:02 UTC</span>
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

## 💬 Comments (2)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/redstartechno">@redstartechno</a></span>
    <span class="issues-meta-item">commented 2026-08-19 00:05 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>A data point that may be useful here: the repo already contains a workflow meant to build the release binaries in Actions — <code>.github/workflows/release.yml</code> — and no run of it on <code>main</code> has ever got past the build step.</p>
<p>Job <code>might_release</code>, step <code>Issue Release Assets</code>:</p>
<pre><code>Run ignite/cli/actions/cli@main
  args: chain build --release --release.prefix latest -t linux:amd64 -t darwin:amd64 -t darwin:arm64 -y
could not locate your app's root dir: go.mod not found
✘ Could not locate your app's root dir: go.mod not found
</code></pre>
<p>Most recent occurrence: run 31996838266 on <code>379bebced</code>. Across the 200 recorded runs of that workflow the tally is 184 success / 16 failure, and all 16 failures are <code>push</code> / <code>main</code> — an unbroken streak from <code>e13d4c658</code> (2026-02-22) through <code>379bebced</code> (2026-08-17). The successes all predate 2026-02-20 and are feature-branch runs from when the trigger was a bare <code>on: push</code>; it was narrowed to <code>main</code> in <code>a0cdbf64f</code>.</p>
<p>The cause is that the job declares</p>
<pre><code class="language-yaml">defaults:
  run:
    working-directory: ./inference-chain
</code></pre>
<p>which applies only to <code>run:</code> steps. <code>Issue Release Assets</code> is a <code>uses:</code> step, and specifically a Docker action invoked with <code>--workdir /github/workspace</code>, so it executes at the repository root regardless. There has been no root <code>go.mod</code> since <code>0c42e64c9</code> ("Move back to sub-folder", 2024-07-17) — the modules are <code>inference-chain/</code>, <code>decentralized-api/</code>, <code>devshard/</code>, <code>common/</code>, <code>edge-api/</code>, <code>proxy-ssl/</code>, <code>versioned/</code>, and the ignite config lives at <code>inference-chain/config.yml</code>. <code>Prepare Release Variables</code> itself succeeds and emits <code>should_release: true</code> / <code>tag_name: latest</code>, so the workflow does reach the build and then stops there.</p>
<p>Two things follow. First, the permanent red ✗ on every <code>main</code> commit is this workflow and nothing else — the other checks on <code>379bebced</code> are green. Second, the "build it in CI" half of this issue is less far off than it looks, since the scaffolding is present and misconfigured rather than absent.</p>
<p>Which way to take it is a maintainer call, though, because the options are not equivalent: repairing the workflow would start publishing a rolling <code>latest</code> prerelease off <code>main</code>, which may well not be wanted, whereas deleting it would just retire dead scaffolding and clear the red X. Attestations would be a separate addition on top of either. I am happy to open a PR for whichever direction you prefer.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/KTibow">@KTibow</a></span>
    <span class="issues-meta-item">commented 2026-08-19 03:02 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@redstartechno repeating what was already in the issue comment with ai is antisocial</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1513](https://github.com/gonka-ai/gonka/issues/1513) every hour.
