---
title: "#398 — API -> Node Connection Issues"
source: https://github.com/gonka-ai/gonka/issues/398
issue_number: 398
synced_at: 2026-07-07T20:19:49Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    API -> Node Connection Issues
    <span class="issues-number">#398</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item">[@gmorgachev](https://github.com/gmorgachev) opened 2025-10-19 05:17 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-01-29 06:17 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #d73a4a; color: #ffffff; border-color: #d73a4a;">bug</span></div>
</div>

<div class="issues-content" markdown="1">
# 1. Too large HTTP body:

```
2025/10/17 11:11:18 INFO Submitting MsgFinishInference subsystem=Inferences inferenceId="KXLiAV7ygVDb+fKlU3LOUZtagN+j/hi3FO77w4mnOb4FxmWyRWh712bwBLJIYzYO/PR79xxMI5EDGEqu+NcP5w=="
2025/10/17 11:11:18 ERROR tx failed to broadcast, failed to put in queue subsystem=Messages tx_id=d17c9c5e-e535-4506-b567-fcbf5e77a9d4 broadcast_err="error while requesting node 'http://node:26657': error in json rpc client, with http response metadata: (Status: 400 Bad Request, Protocol HTTP/1.1). RPC error -32600 - Invalid Request: error reading request body: http: request body too large\n(1) attached stack trace\n  -- stack trace:\n  | github.com/ignite/cli/v28/ignite/pkg/errors.Wrapf\n  | \t/go/pkg/mod/github.com/ignite/cli/v28@v28.11.0/ignite/pkg/errors/xerrors.go:53\n  | github.com/ignite/cli/v28/ignite/pkg/cosmosclient.rpcError\n  | \t/go/pkg/mod/github.com/ignite/cli/v28@v28.11.0/ignite/pkg/cosmosclient/rpc.go:24\n  | github.com/ignite/cli/v28/ignite/pkg/cosmosclient.rpcWrapper.BroadcastTxSync\n  | \t/go/pkg/mod/github.com/ignite/cli/v28@v28.11.0/ignite/pkg/cosmosclient/rpc.go:54\n  | github.com/cosmos/cosmos-sdk/client.Context.BroadcastTxSync\n  | \t/go/pkg/mod/github.com/gonka-ai/cosmos-sdk@v0.53.3-ps8/client/broadcast.go:94\n  | decentralized-api/cosmosclient/tx_manager.(*manager).broadcastMessage\n  | \t/app/decentralized-api/cosmosclient/tx_manager/tx_manager.go:438\n  | decentralized-api/cosmosclient/tx_manager.(*manager).SendTransactionAsyncWithRetry\n  | \t/app/decentralized-api/cosmosclient/tx_manager/tx_manager.go:147\n  | decentralized-api/cosmosclient.(*InferenceCosmosClient).FinishInference\n  | \t/app/decentralized-api/cosmosclient/cosmosclient.go:292\n  | decentralized-api/internal/server/public.(*Server).sendInferenceTransaction\n  | \t/app/decentralized-api/internal/server/public/post_chat_handler.go:701\n  | decentralized-api/internal/server/public.(*Server).handleExecutorRequest\n  | \t/app/decentralized-api/internal/server/public/post_chat_handler.go:468\n  | decentralized-api/internal/server/public.(*Server).postChat\n  | \t/app/decentralized-api/internal/server/public/post_chat_handler.go:163\n  | github.com/labstack/echo/v4.(*Echo).add.func1\n  | \t/go/pkg/mod/github.com/labstack/echo/v4@v4.10.0/echo.go:546\n  | decentralized-api/internal/server/middleware.LoggingMiddleware.func1\n  | \t/app/decentralized-api/internal/server/middleware/middleware.go:14\n  | github.com/labstack/echo/v4.(*Echo).ServeHTTP\n  | \t/go/pkg/mod/github.com/labstack/echo/v4@v4.10.0/echo.go:633\n  | net/http.serverHandler.ServeHTTP\n  | \t/usr/local/go/src/net/http/server.go:3210\n  | net/http.(*conn).serve\n  | \t/usr/local/go/src/net/http/server.go:2092\n  | runtime.goexit\n  | \t/usr/local/go/src/runtime/asm_amd64.s:1700\nWraps: (2) error while requesting node 'http://node:26657'\nWraps: (3) error in json rpc client, with http response metadata: (Status: 400 Bad Request, Protocol HTTP/1.1). RPC error -32600 - Invalid Request: error reading request body: http: request body too large\nWraps: (4) RPC error -32600 - Invalid Request: error reading request body: http: request body too large\nError types: (1) *withstack.withStack (2) *errutil.withPrefix (3) *fmt.wrapError (4) *types.RPCError" resend_err="nats: maximum payload exceeded" error-type=*withstack.withStack error-type=*errors.errorString
2025/10/17 11:11:18 ERROR Failed to submit MsgFinishInference subsystem=Inferences inferenceId="KXLiAV7ygVDb+fKlU3LOUZtagN+j/hi3FO77w4mnOb4FxmWyRWh712bwBLJIYzYO/PR79xxMI5EDGEqu+NcP5w==" error="failed to broadcast and put on retry" error-type=*errors.errorString
```

## Quickfix: 

Increase `rpc-max-body-bytes` to 

## Long Term Fix: off-chain storage of payload 


# 2. Failed to get inference requester

```
2025/10/18 17:06:00 ERROR Failed to get inference requester subsystem=Inferences address=gonka1hwcu7h7kmt5t8g506zwjp04d972t2gucjleq63 error="error while requesting node 'http://node:26657': post failed: Post \"http://node:26657\": dial tcp 172.31.1.3:26657: connect: connection refused\n(1) attached stack trace\n  -- stack trace:\n  | github.com/ignite/cli/v28/ignite/pkg/errors.Wrapf\n  | \t/go/pkg/mod/github.com/ignite/cli/v28@v28.11.0/ignite/pkg/errors/xerrors.go:53\n  | github.com/ignite/cli/v28/ignite/pkg/cosmosclient.rpcError\n  | \t/go/pkg/mod/github.com/ignite/cli/v28@v28.11.0/ignite/pkg/cosmosclient/rpc.go:24\n  | github.com/ignite/cli/v28/ignite/pkg/cosmosclient.rpcWrapper.ABCIQueryWithOptions\n  | \t/go/pkg/mod/github.com/ignite/cli/v28@v28.11.0/ignite/pkg/cosmosclient/rpc.go:39\n  | github.com/cosmos/cosmos-sdk/client.Context.queryABCI\n  | \t/go/pkg/mod/github.com/gonka-ai/cosmos-sdk@v0.53.3-ps8/client/query.go:98\n  | github.com/cosmos/cosmos-sdk/client.Context.QueryABCI\n  | \t/go/pkg/mod/github.com/gonka-ai/cosmos-sdk@v0.53.3-ps8/client/query.go:56\n  | github.com/cosmos/cosmos-sdk/client.Context.Invoke\n  | \t/go/pkg/mod/github.com/gonka-ai/cosmos-sdk@v0.53.3-ps8/client/grpc_query.go:92\n  | github.com/productscience/inference/x/inference/types.(*queryClient).InferenceParticipant\n  | \t/app/inference-chain/x/inference/types/query.pb.go:6987\n  | decentralized-api/internal/server/public.(*Server).validateFullRequest\n  | \t/app/decentralized-api/internal/server/public/post_chat_handler.go:504\n  | decentralized-api/internal/server/public.(*Server).handleExecutorRequest\n  | \t/app/decentralized-api/internal/server/public/post_chat_handler.go:408\n  | decentralized-api/internal/server/public.(*Server).postChat\n  | \t/app/decentralized-api/internal/server/public/post_chat_handler.go:163\n  | github.com/labstack/echo/v4.(*Echo).add.func1\n  | \t/go/pkg/mod/github.com/labstack/echo/v4@v4.10.0/echo.go:546\n  | decentralized-api/internal/server/middleware.LoggingMiddleware.func1\n  | \t/app/decentralized-api/internal/server/middleware/middleware.go:14\n  | github.com/labstack/echo/v4.(*Echo).ServeHTTP\n  | \t/go/pkg/mod/github.com/labstack/echo/v4@v4.10.0/echo.go:633\n  | net/http.serverHandler.ServeHTTP\n  | \t/usr/local/go/src/net/http/server.go:3210\n  | net/http.(*conn).serve\n  | \t/usr/local/go/src/net/http/server.go:2092\n  | runtime.goexit\n  | \t/usr/local/go/src/runtime/asm_amd64.s:1700\nWraps: (2) error while requesting node 'http://node:26657'\nWraps: (3) post failed\nWraps: (4) Post \"http://node:26657\"\nWraps: (5) dial tcp 172.31.1.3:26657\nWraps: (6) connect\nWraps: (7) connection refused\nError types: (1) *withstack.withStack (2) *errutil.withPrefix (3) *fmt.wrapError (4) *url.Error (5) *net.OpError (6) *os.SyscallError (7) syscall.Errno" error-type=*withstack.withStack
2025/10/18 17:06:00 INFO Received request subsystem=Server method=POST path=/v1/chat/completions
```

Is that happen only when `node` is really off? Or smth else? 
Probably we need to add retry in client?



# 2. Executor side Future Timestamp 

Caused by https://github.com/gonka-ai/gonka/issues/387, do we need to handle explicitly ?


</div>

---

> 🔄 **Auto-synced** from [Issue #398](https://github.com/gonka-ai/gonka/issues/398) every hour.
