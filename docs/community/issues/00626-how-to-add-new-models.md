---
title: "#626 — How to add new models"
source: https://github.com/gonka-ai/gonka/issues/626
issue_number: 626
synced_at: 2026-07-23T14:39:20Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    How to add new models
    <span class="issues-number">#626</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 2026-01-23 19:24 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-02-11 00:47 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
This issue outlines a direction for a larger project. Adding new models is not a standalone task and has system-level implications for the architecture. The impact on the overall architecture needs to be evaluated first, and a conceptual description should be provided upfront before any implementation begins.
</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/x0152">@x0152</a></span>
    <span class="issues-meta-item">commented 2026-01-29 18:51 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>If I understood current implementation correctly, then as minimum will be great to use adapter pattern on MLNode side, so poc flow can be defined per model without changing core vllm code. The idea is to keep adapters in mlnode and load them in vllm automatically by model_id, so adding new model is just adding a new adapter implementation and tests on MLNode side</p>
<p>As simple example:</p>
<h3><strong>Adapter core</strong></h3>
<pre><code class="language-python">class HookTap:
    def __init__(self, target, when, layer_idx=-1):
        # target layer router last
        # when pre post or none
        # layer_idx last if -1
        pass

class Adapter:
    def __init__(self, model_id, validation_config, tap):
        # model id for adapter
        # validation config placeholder
        # tap tells where to read hidden
        validation_config = {
            # dist_threshold
            # p_mismatch
            # p_value_threshold
        }
        pass

    def make_embeddings(self, block_hash, public_key, nonces, hidden_size, seq_len, device, dtype):
        # make poc inputs
        pass

    def select_hidden(self, last_hidden):
        # use tap value only
        # error if tap missing
        pass

    def extract_vectors(self, block_hash, public_key, nonces, k_dim, hidden):
        # normalize pick haar normalize
        pass

</code></pre>
<h3><strong>Dense and moe base adapters</strong></h3>
<pre><code class="language-python">class DenseAdapter(Adapter):
    def __init__(self, model_id):
        # take last post layer hidden
        tap = HookTap(&quot;layer&quot;, &quot;post&quot;, -1)
        validation_config = {
            # dist_threshold
            # p_mismatch
            # p_value_threshold
        }
        super().__init__(model_id, validation_config, tap)

    def make_embeddings(self, block_hash, public_key, nonces, hidden_size, seq_len, device, dtype):
        # standard poc inputs
        pass

    def select_hidden(self, last_hidden):
        # use post layer tap
        pass

    def extract_vectors(self, block_hash, public_key, nonces, k_dim, hidden):
        # standard extraction
        pass

class MoEAdapter(DenseAdapter):
    def __init__(self, model_id):
        # take last pre layer hidden
        tap = HookTap(&quot;layer&quot;, &quot;pre&quot;, -1)
        validation_config = {
            # dist_threshold
            # p_mismatch
            # p_value_threshold
        }
        super().__init__(model_id)
        self.tap = tap
        self.validation_config = validation_config

    def select_hidden(self, last_hidden):
        # use pre layer tap
        pass

    def extract_vectors(self, block_hash, public_key, nonces, k_dim, hidden):
        # standard or moe extraction
        pass
</code></pre>
<h3><strong>Model adapters</strong></h3>
<pre><code class="language-python">class Qwen3(DenseAdapter):
    def __init__(self):
        # qwen3 post last layer
        tap = HookTap(&quot;layer&quot;, &quot;post&quot;, -1)
        validation_config = {
            # dist_threshold
            # p_mismatch
            # p_value_threshold
        }
        super().__init__(&quot;Qwen/Qwen3-235B-A22B-Instruct-2507-FP8&quot;)
        self.tap = tap
        self.validation_config = validation_config

class Mixtral(MoEAdapter):
    def __init__(self):
        # mixtral pre last layer
        tap = HookTap(&quot;layer&quot;, &quot;pre&quot;, -1)
        validation_config = {
            # dist_threshold
            # p_mismatch
            # p_value_threshold
        }
        super().__init__(&quot;mistralai/Mixtral-8x7B-Instruct-v0.1&quot;)
        self.tap = tap
        self.validation_config = validation_config

def get_adapter(model_id):
    # select adapter by model id
    pass
</code></pre>
<h3><strong>Poc forward integration point</strong></h3>
<pre><code class="language-python">def execute_poc_forward(worker, block_hash, public_key, nonces, seq_len, hidden_size, k_dim, model_id):
    # pick adapter
    # tp pp sync
    # make embeddings
    # install tap hook
    # forward in poc context
    # get last hidden
    # select hidden
    # extract vectors
    # return result
    pass
</code></pre>
<h3><strong>Suggested layout in mlnode</strong></h3>
<pre><code class="language-bash">mlnode/
  adapters/
    core.py
    utils.py
    adapters/
      qwen3.py
      mixtral.py
      dense.py
      moe.py
</code></pre>
<p>This will simplify adding new models, but we'll still need to compute proper thresholds. Maybe it's worth thinking about automated pipeline to estimate these values?</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #626](https://github.com/gonka-ai/gonka/issues/626) every hour.
