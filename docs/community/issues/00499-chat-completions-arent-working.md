---
title: "#499 — Chat Completions aren't working"
source: https://github.com/gonka-ai/gonka/issues/499
issue_number: 499
synced_at: 2026-07-23T23:17:40Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    Chat Completions aren't working
    <span class="issues-number">#499</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/pentoxine">@pentoxine</a> opened 2025-12-20 02:05 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-02-10 04:04 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
```
base_url: http://192.241.240.19:8000/v1
Request signing is enabled through a custom HTTP client implementation.
Using Gonka address: gonka1twg5lhad6sc86yjqspanmp94md2dx0fhfppxus
INFO:httpx:HTTP Request: POST http://192.241.240.19:8000/v1/chat/completions "HTTP/1.1 500 Internal Server Error"
INFO:openai._base_client:Retrying request to /chat/completions in 0.400175 seconds
INFO:httpx:HTTP Request: POST http://192.241.240.19:8000/v1/chat/completions "HTTP/1.1 500 Internal Server Error"
INFO:openai._base_client:Retrying request to /chat/completions in 0.879420 seconds
INFO:httpx:HTTP Request: POST http://192.241.240.19:8000/v1/chat/completions "HTTP/1.1 500 Internal Server Error"
Traceback (most recent call last):
  File "/Users/bob/git/gonka/script.py", line 9, in <module>
    response = client.chat.completions.create(
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/bob/git/gonka/.venv/lib/python3.12/site-packages/openai/_utils/_utils.py", line 286, in wrapper
    return func(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/Users/bob/git/gonka/.venv/lib/python3.12/site-packages/openai/resources/chat/completions/completions.py", line 1192, in create
    return self._post(
           ^^^^^^^^^^^
  File "/Users/bob/git/gonka/.venv/lib/python3.12/site-packages/openai/_base_client.py", line 1259, in post
    return cast(ResponseT, self.request(cast_to, opts, stream=stream, stream_cls=stream_cls))
                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/bob/git/gonka/.venv/lib/python3.12/site-packages/openai/_base_client.py", line 1047, in request
    raise self._make_status_error_from_response(err.response) from None
openai.InternalServerError: Error code: 500 - {'error': 'rpc error: code = Unknown desc = runtime error: invalid memory address or nil pointer dereference: panic'}
```


script

```
import os
from gonka_openai import GonkaOpenAI

client = GonkaOpenAI(
    gonka_private_key=os.environ.get('GONKA_PRIVATE_KEY'),
    source_url="http://node3.gonka.ai:8000",
)

response = client.chat.completions.create(
    model="Qwen/Qwen3-235B-A22B-Instruct-2507-FP8",
    messages=[
        { "role": "user", "content": "Write a one-sentence bedtime story about a unicorn" }
    ]
)

print(response.choices[0].message.content)
```
</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/mtvnastya">@mtvnastya</a></span>
    <span class="issues-meta-item">commented 2026-02-10 04:04 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>hi @pentoxine,I'd like to propose this for a bounty for reporting the issue.
can you please reach out to me in discord @mtvnastya or let me know how I can contact you directly?</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #499](https://github.com/gonka-ai/gonka/issues/499) every hour.
