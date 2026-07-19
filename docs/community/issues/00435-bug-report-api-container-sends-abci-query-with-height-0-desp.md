---
title: "#435 — Bug Report: api container sends abci_query with height: 0 despite being synced"
source: https://github.com/gonka-ai/gonka/issues/435
issue_number: 435
synced_at: 2026-07-19T15:28:29Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Bug Report: api container sends abci_query with height: 0 despite being synced
    <span class="issues-number">#435</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/VaniaHilkovets">@VaniaHilkovets</a> opened 2025-11-14 12:45 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-02-08 14:14 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
Bug Report: api container sends abci_query with height: 0 despite being synced
Title: api container sends abci_query for EpochInfo with "height":"0", causing requests to /v1/epochs/current/participants to fail.

Description:
Hello, I am running a node following the official deployment guide. My node container is fully synced with the mainnet. However, the api container is unable to correctly fetch epoch information, because it sends RPC requests to the node with height: 0, even though it knows the correct current height.

Environment:

Deployment: Docker Compose (docker-compose.yml and docker-compose.mlnode.yml)

Server: Ubuntu 22.04

Images: Using default/latest tags as per the official guide.

Steps to Reproduce:

Set up the node according to the join deployment guide.

Wait for the node container to fully sync (catching_up: false).

Observe the api container logs. It correctly logs the current block height on new blocks.

Make a GET request to the api endpoint: http://81.27.97.154

[log.txt](https://github.com/user-attachments/files/23547425/log.txt)

:8000/v1/epochs/current/participants.

Expected Result:
The API should return a JSON object with the current epoch participants, as described in the documentation.

Actual Result:
The API returns a JSON error:
json
{"error":"error in json rpc client, with http response metadata: (Status: 200 OK, Protocol HTTP/1.1). RPC error -32603 - Internal error: height must be greater than 0, but got 0"}


**Root Cause Analysis & Proof:**

I have performed a `tcpdump` on the internal Docker network to trace the communication between the `api` container (`172.18.0.7`) and the `node` container (`172.18.0.6`).

**1. The `api` container CORRECTLY gets the sync status:**
The `api` container sends a `status` request and receives a correct response with the current height.

*   **Request from `api`:**
    ```
    {"jsonrpc":"2.0", "id":0, "method":"status", "params":{}}
    ```
*   **Response from `node`:**
    ``````json
    {"jsonrpc":"2.0", "id":0, "result":{ ... "sync_info":{"latest_block_height":"1287647", ... "catching_up":false}, ... }}
    ```

**2. The `api` container INCORRECTLY queries for epoch info:**
Immediately after, when processing the external request, the `api` container sends an `abci_query` but **erroneously uses `"height":"0"`** in the parameters.

*   **Faulty Request from `api`:**
    ```json    ```
    {"jsonrpc":"2.0", "id":333, "method":"abci_query", "params":{"data":"", "height":"0", "path":"/inference.inference.Query/EpochInfo", "prove":false}}
    ```

This proves that the `api` container is aware of the correct block height but fails to use it in subsequent critical queries, causing the failure. This appears to be a bug within the `api` client itself.

Could you please advise on which version/tag of the `gonka/api` image is stable and does not have this bug? Or is there a known workaround?

Thank you.

---

*
</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/AlexeySamosadov">@AlexeySamosadov</a></span>
    <span class="issues-meta-item">commented 2026-02-08 14:14 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>PR created: https://github.com/gonka-ai/gonka/pull/681</p>
<p>Uses current block height for ABCI queries.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #435](https://github.com/gonka-ai/gonka/issues/435) every hour.
