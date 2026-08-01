---
title: "#714 — Bug Report: New Nodes Fail to Sign Transactions (Keyring Backend Mismatch)"
source: https://github.com/gonka-ai/gonka/issues/714
issue_number: 714
synced_at: 2026-08-01T17:28:17Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    Bug Report: New Nodes Fail to Sign Transactions (Keyring Backend Mismatch)
    <span class="issues-number">#714</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/moro3one">@moro3one</a> opened 2026-02-07 08:47 UTC</span>
    <span class="issues-meta-item">4 comments</span>
    <span class="issues-meta-item">Updated 2026-02-10 00:33 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
*(empty)*
</div>

---

## 💬 Comments (4)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/moro3one">@moro3one</a></span>
    <span class="issues-meta-item">commented 2026-02-07 08:52 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Bug report: New nodes fail to sign transactions due to Keyring Backend mismatch in Docker config. Fix included in description.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/moro3one">@moro3one</a></span>
    <span class="issues-meta-item">commented 2026-02-07 08:58 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>FULL BUG REPORT:
Severity: High
Environment: Mainnet / Docker Compose</p>
<p>Summary:
The current Docker deployment setup for new join nodes fails to initialize the api service correctly due to a configuration mismatch in how KEYRING_BACKEND is handled. The init-docker.sh entrypoint fails to source config.env variables because of export prefixes, causing the api container to default to keyring-backend=file. However, the onboarding process generates keys using keyring-backend=test.</p>
<p>This results in the api service being unable to find the operator's private key, leading to a loop of 'account does not exist' errors. The node appears 'Active' in the explorer</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/gmorgachev">@gmorgachev</a></span>
    <span class="issues-meta-item">commented 2026-02-07 21:18 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Current onboarding pipeline uses manually creating warm key with <code>file</code> keyring backend:
https://gonka.ai/host/quickstart/#31-server-create-ml-operational-key</p>
<p>Explicitly suggest:</p>
<pre><code>printf '%s\n%s\n' &quot;$KEYRING_PASSWORD&quot; &quot;$KEYRING_PASSWORD&quot; | inferenced keys add &quot;$KEY_NAME&quot; --keyring-backend file
</code></pre>
<p><code>export</code> prefixes work with current onboarding pipeline as it uses explicit loading of environment variables via:</p>
<pre><code>source config.env
</code></pre>
<blockquote>
<p>However, the onboarding process generates keys using keyring-backend=test</p>
</blockquote>
<p>Are you refering to?</p>
<pre><code>if [ &quot;${CREATE_KEY:-false}&quot; = &quot;true&quot; ]; then
  echo &quot;Creating account key: $KEY_NAME&quot;

  if command -v inferenced &gt;/dev/null 2&gt;&amp;1; then
    APP_NAME=&quot;inferenced&quot;
  else
    APP_NAME=&quot;decentralized-api&quot;
  fi

  $APP_NAME keys add &quot;$KEY_NAME&quot; \
    --keyring-backend test \
    --keyring-dir /root/.inference

  ACCOUNT_PUBKEY=$($APP_NAME keys show &quot;$KEY_NAME&quot; --pubkey --keyring-backend test --keyring-dir /root/.inference | jq -r '.key')
  export ACCOUNT_PUBKEY
  echo &quot;Generated ACCOUNT_PUBKEY: $ACCOUNT_PUBKEY&quot;
fi
</code></pre>
<p>That part is used only during automatic testing in local testnet and is not used in onboarding pipeline</p>
<p>If i'm not missing smth, the <code>source config.env</code> step was skipped which caused unexpected behaviour.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/AlexeySamosadov">@AlexeySamosadov</a></span>
    <span class="issues-meta-item">commented 2026-02-08 14:13 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>PR created: https://github.com/gonka-ai/gonka/pull/715</p>
<p>Fixes keyring backend mismatch for new join nodes.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #714](https://github.com/gonka-ai/gonka/issues/714) every hour.
