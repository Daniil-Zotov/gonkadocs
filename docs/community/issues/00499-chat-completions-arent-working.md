---
title: "#499 — Chat Completions aren't working"
source: https://github.com/gonka-ai/gonka/issues/499
issue_number: 499
synced_at: 2026-07-06T09:52:53Z
template: issues-main.html
---

> 🔄 **Авто-синхронизация:** из [Issue #499](https://github.com/gonka-ai/gonka/issues/499) каждые 6 часов. 

# 🔴 Chat Completions aren't working

**Автор:** [@pentoxine](https://github.com/pentoxine) · **Состояние:** Closed · **Создано:** 2025-12-20 02:05 UTC · **Обновлено:** 2026-02-10 04:04 UTC

**Веха:** v0.2.10

---

## 📝 Описание

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

---

## 💬 Комментарии (1)

### Комментарий 1 — [@mtvnastya](https://github.com/mtvnastya)

*2026-02-10 04:04 UTC*

hi @pentoxine,I'd like to propose this for a bounty for reporting the issue.
can you please reach out to me in discord @mtvnastya or let me know how I can contact you directly?
