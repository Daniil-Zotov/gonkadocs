---
title: "#626 — How to add new models"
source: https://github.com/gonka-ai/gonka/issues/626
issue_number: 626
synced_at: 2026-07-06T09:52:50Z
template: issues-main.html
---

> 🔄 **Auto-synced:** from [Issue #626](https://github.com/gonka-ai/gonka/issues/626) every 6 hours. 

# 🔴 How to add new models

**Author:** [@tcharchian](https://github.com/tcharchian) · **State:** Closed · **Created:** 2026-01-23 19:24 UTC · **Updated:** 2026-02-11 00:47 UTC

**Веха:** v0.2.11

---

## 📝 Описание

This issue outlines a direction for a larger project. Adding new models is not a standalone task and has system-level implications for the architecture. The impact on the overall architecture needs to be evaluated first, and a conceptual description should be provided upfront before any implementation begins.

---

## 💬 Comments (1)

### Комментарий 1 — [@x0152](https://github.com/x0152)

*2026-01-29 18:51 UTC*

If I understood current implementation correctly, then as minimum will be great to use adapter pattern on MLNode side, so poc flow can be defined per model without changing core vllm code. The idea is to keep adapters in mlnode and load them in vllm automatically by model_id, so adding new model is just adding a new adapter implementation and tests on MLNode side

As simple example:

### **Adapter core**
```python
class HookTap:
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

```


### **Dense and moe base adapters**
```python
class DenseAdapter(Adapter):
    def __init__(self, model_id):
        # take last post layer hidden
        tap = HookTap("layer", "post", -1)
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
        tap = HookTap("layer", "pre", -1)
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
```


### **Model adapters**
```python
class Qwen3(DenseAdapter):
    def __init__(self):
        # qwen3 post last layer
        tap = HookTap("layer", "post", -1)
        validation_config = {
            # dist_threshold
            # p_mismatch
            # p_value_threshold
        }
        super().__init__("Qwen/Qwen3-235B-A22B-Instruct-2507-FP8")
        self.tap = tap
        self.validation_config = validation_config

class Mixtral(MoEAdapter):
    def __init__(self):
        # mixtral pre last layer
        tap = HookTap("layer", "pre", -1)
        validation_config = {
            # dist_threshold
            # p_mismatch
            # p_value_threshold
        }
        super().__init__("mistralai/Mixtral-8x7B-Instruct-v0.1")
        self.tap = tap
        self.validation_config = validation_config

def get_adapter(model_id):
    # select adapter by model id
    pass
```

### **Poc forward integration point**
```python
def execute_poc_forward(worker, block_hash, public_key, nonces, seq_len, hidden_size, k_dim, model_id):
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
```

### **Suggested layout in mlnode**
```bash
mlnode/
  adapters/
    core.py
    utils.py
    adapters/
      qwen3.py
      mixtral.py
      dense.py
      moe.py
```


This will simplify adding new models, but we'll still need to compute proper thresholds. Maybe it's worth thinking about automated pipeline to estimate these values?
