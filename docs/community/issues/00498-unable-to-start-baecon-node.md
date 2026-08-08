---
title: "#498 — Unable to start baecon node"
source: https://github.com/gonka-ai/gonka/issues/498
issue_number: 498
synced_at: 2026-08-08T19:50:01Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    Unable to start baecon node
    <span class="issues-number">#498</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/Knoxpix">@Knoxpix</a> opened 2025-12-19 08:41 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-01-22 00:12 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
From this raw log. I need assist how to fix this issue. Or can i change checkpoint origin state and block to other?

`bridge  | Stopping Prysm log formatter (PID: 82343)
bridge  | 
bridge  | GETH: INFO [12-19|08:28:53.728] New local node record                    seq=1,765,953,858,893 id=a29a8022f2c83caa ip=203.156.3.38 udp=38205 tcp=30303
bridge  | Restarting processes due to crash...
bridge  | Restarting both processes...
bridge  | Stopping Geth (PID: 82111)
bridge  | tail: /var/log/geth/geth.log: file truncated
bridge  | Starting Geth...
bridge  | GETH: WARN [12-19|08:28:55.180] Unknown config environment variable      envvar=GETH_DATA_DIR
bridge  | GETH: INFO [12-19|08:28:55.193] Starting Geth on Ethereum mainnet...
bridge  | GETH: INFO [12-19|08:28:55.194] Bumping default cache on mainnet         provided=1024 updated=4096
bridge  | GETH: INFO [12-19|08:28:55.197] Maximum peer count                       ETH=50 total=50
bridge  | GETH: INFO [12-19|08:28:55.198] Smartcard socket not found, disabling    err="stat /run/pcscd/pcscd.comm: no such file or directory"
bridge  | GETH: Fatal: Failed to create the protocol stack: datadir already used by another process
bridge  | Geth failed to stay alive after start (PID: 82797)
bridge  | Geth restart failed; will retry in monitor loop
bridge  | Geth process (PID: 82797) died
bridge  | Prysm process (PID: 82341) exited with status 127
bridge  | --- Last 100 lines of Prysm raw log ---
bridge  | PRSM: time="2025-12-19 08:28:46.18" level=info msg="Finished reading JWT secret from /data/jwt/jwt.hex" prefix=execution
bridge  | PRSM: time="2025-12-19 08:28:46.18" level=info msg="Using checkpoint sync url https://beaconstate.ethstaker.cc/ for value in --genesis-beacon-api-url flag"
bridge  | PRSM: time="2025-12-19 08:28:46.19" level=info msg="Running on Ethereum Mainnet" prefix=flags
bridge  | PRSM: time="2025-12-19 08:28:46.19" level=warning msg="In order to receive transaction fees from proposing blocks, you must provide flag --suggested-fee-recipient with a valid ethereum address when starting your beacon node. Please see our documentation for more information on this requirement (https://docs.prylabs.network/docs/execution-node/fee-recipient)." prefix=node
bridge  | PRSM: time="2025-12-19 08:28:46.19" level=info msg="Checking DB" databasePath="/data/prysm/beaconchaindata" prefix=node
bridge  | PRSM: time="2025-12-19 08:28:46.19" level=info msg="Opening Bolt DB" path="/data/prysm/beaconchaindata/beaconchain.db" prefix=db
bridge  | PRSM: time="2025-12-19 08:28:46.20" level=warning msg="Removing database" prefix=node
bridge  | PRSM: time="2025-12-19 08:28:46.20" level=info msg="Opening Bolt DB" path="/data/prysm/beaconchaindata/beaconchain.db" prefix=db
bridge  | PRSM: time="2025-12-19 08:28:46.21" level=info msg="Setting genesis validators root" genesis_validators_root=0x4b363db94e286120d76eb905340fdd4e54bfe9f06bf33ff6cf5ad27f511bfe95
bridge  | PRSM: time="2025-12-19 08:28:46.21" level=warning msg="Removing blob storage" prefix=node
bridge  | PRSM: time="2025-12-19 08:28:46.21" level=warning msg="Removing data columns storage" prefix=node
bridge  | PRSM: time="2025-12-19 08:28:46.32" level=info msg="Checkpoint sync - Downloading origin state and block" prefix=node
bridge  | PRSM: time="2025-12-19 08:28:47.15" level=fatal msg="unable to start beacon node: could not start modules: could not start DB: Error retrieving checkpoint origin state and block: error requesting state by id = finalized: code=502, url=https://beaconstate.ethstaker.cc/eth/v2/debug/beacon/states/finalized, body=response body:
bridge  | PRSM: <html>
bridge  | PRSM: <head><title>502 Bad Gateway</title></head>
bridge  | PRSM: <body>
bridge  | PRSM: <center><h1>502 Bad Gateway</h1></center>
bridge  | PRSM: <hr><center>nginx/1.28.0</center>
bridge  | PRSM: </body>
bridge  | PRSM: </html>
bridge  | PRSM: : did not receive 2xx response from API" prefix=main
bridge  | --- End Prysm raw log excerpt ---
bridge  | Restarting processes due to crash...
bridge  | Restarting both processes...
bridge  | Starting Geth...
bridge  | tail: /var/log/geth/geth.log: file truncated`
</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2026-01-22 00:12 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Hi @Knoxpix! Thank you for reaching out.
Please note that technical support is not provided here.
For assistance, we kindly recommend asking for help in Gonka <a href="https://discord.com/invite/RADwCT2U6R">Discord community</a>, where community members may be able to support you.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #498](https://github.com/gonka-ai/gonka/issues/498) every hour.
