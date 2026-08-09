---
title: "#780 — [1/4] `StartInference` and `FinishInference`"
source: https://github.com/gonka-ai/gonka/issues/780
issue_number: 780
synced_at: 2026-08-09T17:52:42Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    [1/4] `StartInference` and `FinishInference`
    <span class="issues-number">#780</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 2026-02-20 22:20 UTC</span>
    <span class="issues-meta-item">10 comments</span>
    <span class="issues-meta-item">Updated 2026-03-11 20:05 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #008672; color: #ffffff; border-color: #008672;">help wanted</span> <span class="issues-label" style="background-color: #4cbc0f; color: #24292f; border-color: #4cbc0f;">up-for-grabs</span> <span class="issues-label" style="background-color: #f86c7a; color: #24292f; border-color: #f86c7a;">Priority: High</span> <span class="issues-label" style="background-color: #9214a6; color: #ffffff; border-color: #9214a6;">requires own mainnet node</span></div>
</div>

<div class="issues-content" markdown="1">
# Background

`MsgStartInference` and `MsgFinishInference` are too slow in production. Blocks should be processed by nodes within 1-2 seconds, so that block time stays below 6 seconds. This means that to process 1000 inferences in a block, we need to record 1000 `MsgStartInference`, 1000 `MsgFinishInference`, and 100-200 `MsgValidation` transactions. This means that these transactions should be processed faster than 1ms. Even though they are quite fast in tests, in production with a large state they require 10-20ms, and on some nodes 50ms or more.

There are 2 main areas identified that contribute most of the time to transactions:
- Signatures validation (57% of `FinishInference` and 63% of `StartInference`)
- Stats query and recording (40% of `FinishInference` and 30% of `StartInference`)

Download profiling file:
https://drive.google.com/file/d/1yxY91lzMHxv_MeloAxW1zczcpbkBjZ0t/
And use command:
```
go tool pprof -http=:8080 /Users/davidliberman/Downloads/pprof.inferenced.samples.cpu.001.pb.gz
```

Screen recoding: https://drive.google.com/file/d/1yxDaJllxCQ-l3ZO6ZuBb5bTEUgZ5t7Yu/view?usp=sharing

And choose flame graph to explore

_**Signature validation**_ can be significantly optimized, reducing the number of signatures to be validated in most scenarios by 5x (from 5 signatures to just 1).

https://github.com/gonka-ai/gonka/issues/608 - which is now implemented by @DimaOrekhovPS

https://github.com/gonka-ai/gonka/pull/779 

**_Stats query and recording_** is designed to make it easier to query usage statistics for inference operations by storing this data on a chain. However, it is too heavy for on-chain operations and should be removed. In the end, we shouldn't read and write any large state record in `MsgStartInference`, `MsgFinishInference`, or `MsgValidation`.

`SetInference` (including the second time it is executed in `HandleInferenceComplete`): 
- 10% of `FinishInference`, 
- 12% of `StartInference`, 
- 14% of Validation
- 33% is Logging, 
- 38% `SetOrUpdateInferenceStatsByEpoch`, 
- 22% `SetOrUpdateInferenceStatusByTime` w/o logging

`HandleInferenceComplete`, excluding `SetInference`, accounts for 16% of `FinishInference` and 4% of `StartInference` (as it is rare for `StartInference` to come second).
- 20% is Logging
- 45% is 2xGetEpochGroupData
- 5% GetEpochIndex
- 10% SetEpochGroupData, 
- 20% SetParticipant/GetParticipants w/o logging

`ProcessInferencePayment`: 14% of `FinishInference` and 12% of `StartInference` 
- 63% is Logging
- 18% `SetParticipant`/2x`GetParticipant` w/o logging
- 9% Add/GetTokenomicsData

# Tasks:
- I.1. Measure this transaction on mainnet but with INFO level logging turned off. Check if it decreases duration by 15% for `FinishInference` and 13% for `StartInference`. When completed report results before moving forward. If we confirm the difference, do the (I.2).
- I.2. We need to test if that changes if we write logs to files rather than stdout. When results are measured, report them before moving forward. If that works. Do final clean implementation. If didn’t work do (I.3)  (see more details below)
- I.3. Or we need to move most of the logs of `StartInference` and `FinishInference` (except one per transaction) to DEBUG. Measure results and report them.

**More details for I.2**

1. Question: where is most of the output coming from, and from which part of the code (which file/module in code/python)?
2. For terminal, Docker, or k8s, we can build a wrapper using redirect_stdout from contextlib.

Important: when redirecting to a file via >, full buffering kicks in (buffer ~8KB). The writes still go through stdout, and flushing can be delayed for minutes. This can significantly slow down the entire process.

After using a wrapper (writing to a file with explicit buffering):
	•	You control the buffer size yourself (even 1MB).
	•	No Docker daemon involvement in I/O.
	•	Ability to do batched writes and use a dedicated writer thread.

Bottom line: it won’t magically become “16x faster,” but the main bottleneck, passing through stdout, will be removed completely. The wrapper will give you the maximum performance your filesystem can provide.

Something like:
import sys
from contextlib import redirect_stdout

def run_with_buffered_file(func, log_path, buffer_size=1024*64):
    """
    Temproraly redirects stdout to the file with buffer  
    """
    with open(log_path, 'w', buffering=buffer_size, encoding='utf-8') as f:
        with redirect_stdout(f):
            func()
or
def my_task():
    print("this goes to the file, not to the docker logs")
    # Subprocess output will NOT be captured unless you redirect it explicitly.

run_with_buffered_file(my_task, "/app/logs/task.log", buffer_size=128*1024)

```
high-load example / max speed prod gives more >10k rows/sec. 

import threading
import queue
import sys
import time
from contextlib import redirect_stdout

class AsyncFileWriter:
    def init(self, filepath, buffer_size=1024*1024, max_queue=10000):
        self.file = open(filepath, 'a', buffering=buffer_size, encoding='utf-8')
        self.queue = queue.Queue(maxsize=max_queue)
        self.running = True
        threading.Thread(target=self._writer, daemon=True).start()

    def write(self, s):
        try:
            self.queue.put_nowait(s)
        except queue.Full:
            # Memory overflow protection: flush to the main writer thread.
            self.file.write(s)

    def flush(self):
        self.file.flush()

    def _writer(self):
        while self.running:
            try:
                s = self.queue.get(timeout=0.1)
                self.file.write(s)
            except queue.Empty:
                continue

    def close(self):
        self.running = False
        time.sleep(0.2)  # Give the queue time to record.
        self.file.close()

def run_async_logging(func, log_path):
    writer = AsyncFileWriter(log_path, buffer_size=256*1024)
    with redirect_stdout(writer):
        func()
    writer.close()
```

Never do this:
```
CMD python app.py > /logs/app.log
```
It kills performance and adds two unnecessary pipes.

Do this instead:
```
FROM python:3.11-slim
WORKDIR /app
COPY app.py .

# The -u flag disables Python stdout buffering, but we don’t rely on it:
# we control file buffering ourselves. Keeping it as a safety measure.
ENV PYTHONUNBUFFERED=1

CMD ["python", "app.py"]
```
Then, in `app.py`, wrap the entry point:
```
if __name__ == "__main__":
    with open("/var/log/app/out.log", "a", buffering=64*1024, encoding="utf-8") as f:
        tee = Tee(sys.stdout, f)
        with redirect_stdout(tee):
            main()
```
Result:
	•	docker logs: you see logs immediately (via sys.stdout).
	•	The file /var/log/app/out.log is written with a 64KB buffer.
	•	No Docker daemon involvement in file I/O.

Pay attention:
- A high-load, max-speed production example outputs >10k lines/sec, showing an 8 to 16x difference.
- A simple wrapper will already solve the problem and should give a solid 5 to 6x speedup.
- stdout is the slowest path and it holds a lock until the operation completes.
- An unbuffered file will be slower than stdout, because every print becomes a write() to disk.
- A buffered file will be much faster, because it only writes when the 64KB buffer fills.

# Important
This issue is one of five issues in the [0/4] StartInference and FinishInference series (and correspondingly [1/4], [2/4], [3/4], [4/4]).
These tasks can be completed independently of each other by different contributors.
However, this specific task requires maintaining and operating a node on mainnet in order to test and validate the result.

All five issues [0/4], [1/4], [2/4], [3/4], [4/4] in this series must be completed as part of the v0.2.11 upgrade, which is scheduled for the week of February 23. After the v0.2.11 upgrade, these tasks will no longer be relevant, because a different solution can/will be proposed.
</div>

---

## 💬 Comments (10)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2026-02-20 22:41 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>If you’re ready to take this task on, please leave a comment here so other community members can see it’s already being worked on.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/hleb-albau">@hleb-albau</a></span>
    <span class="issues-meta-item">commented 2026-02-24 10:30 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>I ran CPU profiling (30 min each) on a synced mainnet node under two configurations: <code>log_level=info</code> and <code>log_level=error</code>.</p>
<p><strong>Results — logging overhead as % of total handler time (including all nested calls):</strong></p>
<table>
<thead>
<tr>
<th>Handler</th>
<th>Total time (info)</th>
<th>LogInfo overhead</th>
<th>% of handler</th>
<th>After log_level=error</th>
<th>Reduction</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>_Msg_StartInference_Handler</code></td>
<td>10.33s</td>
<td>1.14s</td>
<td><strong>11.0%</strong></td>
<td>0.05s (0.4%)</td>
<td><strong>-95.6%</strong></td>
</tr>
<tr>
<td><code>_Msg_FinishInference_Handler</code></td>
<td>15.40s</td>
<td>1.66s</td>
<td><strong>10.8%</strong></td>
<td>0.06s (0.4%)</td>
<td><strong>-96.4%</strong></td>
</tr>
</tbody>
</table>
<p>So ~11% of handler execution is spent in logging. Setting <code>log_level=error</code> reduces that to ~0.4% — essentially just the log level check in <code>Logger()</code>.</p>
<p>NOTE: CPU profiling is sample-based (100 samples/sec), not a precise timer — it tells us <em>where</em> the CPU spends time statistically, not exact wall-clock execution time per call. The 11% figure is a directional signal, not a precise measurement.</p>
<p>btw
1. what is a purpose to have that logs?
2. what is a purpose to have that logs with INFO level?</p>
<p>About the big task itself, 
i am not familiar with all stuff going on right now on chain, but in past a had experience, that you could use own storage, outside of IAVL tree, and commit to IAVL only small portion of that data.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/libermans">@libermans</a></span>
    <span class="issues-meta-item">commented 2026-02-26 04:11 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>An update on 780. As we can see in traces most of the time spend on logging is due "json" decoding-encoding. Which can be turn off by log_format = "json" (by default it is set to log_format = "plain"). @hleb-albau can you please run the same test but with log_format = "json" config? </p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2026-02-26 17:47 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@hleb-albau can I kindly ask you to contact me tania.charchian@productscience.ai</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2026-02-26 17:48 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <blockquote>
<p>An update on 780. As we can see in traces most of the time spend on logging is due "json" decoding-encoding. Which can be turn off by log_format = "json" (by default it is set to log_format = "plain"). <a href="https://github.com/hleb-albau">@hleb-albau</a> can you please run the same test but with log_format = "json" config?</p>
</blockquote>
<p>@hleb-albau are you ready to run the same test but with log_format = "json" config?</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/hleb-albau">@hleb-albau</a></span>
    <span class="issues-meta-item">commented 2026-02-26 20:01 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <blockquote>
<blockquote>
<p>An update on 780. As we can see in traces most of the time spend on logging is due "json" decoding-encoding. Which can be turn off by log_format = "json" (by default it is set to log_format = "plain"). <a href="https://github.com/hleb-albau">@hleb-albau</a> can you please run the same test but with log_format = "json" config?</p>
</blockquote>
<p><a href="https://github.com/hleb-albau">@hleb-albau</a> are you ready to run the same test but with log_format = "json" config?</p>
</blockquote>
<p>yes, will do it next 24h</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/hleb-albau">@hleb-albau</a></span>
    <span class="issues-meta-item">commented 2026-02-27 10:12 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>### Plain  (<code>prod-30min-logs-plain</code>)</p>
<table>
<thead>
<tr>
<th>method</th>
<th>cum total</th>
<th>LogInfo</th>
<th>logTransaction</th>
<th>sum log.</th>
<th>%</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>StartInference</code></td>
<td>5.25s</td>
<td>0.24s</td>
<td>0.06s</td>
<td>0.30s</td>
<td>5.7%</td>
</tr>
<tr>
<td><code>FinishInference</code></td>
<td>6.91s</td>
<td>0.45s</td>
<td>0.15s</td>
<td>0.60s</td>
<td>8.7%</td>
</tr>
<tr>
<td><code>processInferencePayments</code></td>
<td>0.72s</td>
<td>0.14s</td>
<td>0.21s</td>
<td>0.35s</td>
<td>48.6%</td>
</tr>
</tbody>
</table>
<h3>JSON (<code>prod-30min-logs-json</code>)</h3>
<table>
<thead>
<tr>
<th>method</th>
<th>cum total</th>
<th>LogInfo</th>
<th>logTransaction</th>
<th>sum log</th>
<th>%я</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>StartInference</code></td>
<td>34.78s</td>
<td>0.54s</td>
<td>—</td>
<td>0.54s</td>
<td>1.6%</td>
</tr>
<tr>
<td><code>FinishInference</code></td>
<td>35.90s</td>
<td>0.85s</td>
<td>—</td>
<td>0.85s</td>
<td>2.4%</td>
</tr>
<tr>
<td><code>processInferencePayments</code></td>
<td>2.54s</td>
<td>0.36s</td>
<td>0.33s</td>
<td>0.69s</td>
<td>27.2%</td>
</tr>
</tbody>
</table>
<p>NOTE: <code>StartInference</code> and  <code>FinishInference</code> in that table show total time spent in log, including subfunctions(like <code>processInferencePayments</code>). </p>
<hr />
<p>Zerolog internally stores all data as a JSON string (to minimize allocations) — every Append key=val call simply mutates that string. In our case we always log one message at a time, meaning the JSON is built once and immediately flushed to output.                                                         </p>
<p>In plain log mode, zerolog parses that JSON before writing, reformatting it into a human-readable string with colors. In JSON log mode, the JSON string is written as-is.                                                                                                                                        </p>
<hr />
<p>Looking at <code>processInferencePayments</code>, logging still accounts for roughly a quarter of its total time. About half of that quarter is spent building the JSON string — appending key-value pairs one by one. For primitive values (strings, numbers, etc.) this is fast. For struct values, zerolog invokes more complex serialization logic that depends on the struct's shape.</p>
<p>For example, in UpdateParticipantStatus, roughly half of the JSON-building time inside <code>k.LogInfo("Participant status updated", types.Validation, "address", participant.Address, "original", originalStatus, "new", newStatus, "reason", reason, "stats", participant.CurrentEpochStats)</code> is spent serializing <code>participant.CurrentEpochStats</code>. In other places, the bottleneck is converting types.AccAddress to a string — which internally goes through a cache protected by a mutex or calc bench32. Note: not only <code>UpdateParticipantStatus</code> suffer from this, other places in <code>StartInference</code> and <code>FinishInference</code> have similar  problems.</p>
<hr />
<p>It might make sense to rework the logger internals to store data as a map instead of a JSON string, so ConsoleWriter could print it directly without parsing JSON first. But it's worth thinking about whether that's actually needed right now.                                                                 </p>
<p>What's definitely worth doing is revisiting what data gets logged. I'll open a PR a bit later to remove the heavy structs from log calls. </p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/AlexeySamosadov">@AlexeySamosadov</a></span>
    <span class="issues-meta-item">commented 2026-03-03 11:25 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>PR: https://github.com/gonka-ai/gonka/pull/847</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/AlexeySamosadov">@AlexeySamosadov</a></span>
    <span class="issues-meta-item">commented 2026-03-03 12:00 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Summary of what was done in PR #847:</p>
<p>Based on the profiling analysis by @hleb-albau (logging overhead ~11% of handler time at INFO level, heavy struct serialization in <code>processInferencePayments</code> accounting for 25-48% of its time), the following changes were implemented:</p>
<p><strong>~20 LogInfo calls moved to LogDebug</strong> across 7 files in the StartInference/FinishInference hot path:
- <code>msg_server_start_inference.go</code> — 5 calls (entry log, DevPubKey, TransferAgentPubKey, validateTimestamp, addTimeout)
- <code>msg_server_finish_inference.go</code> — 1 call (entry log)
- <code>inference.go</code> — 1 call (developer stat update)
- <code>developer_stats_aggregation.go</code> — 1 call (verbose stat log)
- <code>developer_stats_store.go</code> — 3 calls (record-tracking logs)
- <code>payment_handler.go</code> — 7 calls (escrow, minting, paying, burning, refund)
- <code>dynamic_pricing.go</code> — 1 call + removed heavy <code>inference</code> struct from error log (replaced with lightweight fields)</p>
<p>All ERROR/WARN logs preserved. Per-block pricing logs stay at INFO (run once per block, not per inference). Expected result: with <code>log_level=info</code> + <code>log_format=json</code>, logging overhead should drop from ~11% to well under 1%.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/gmorgachev">@gmorgachev</a></span>
    <span class="issues-meta-item">commented 2026-03-11 20:05 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>The big part of inference flow optimization is merged in https://github.com/gonka-ai/gonka/pull/812
I'm closing all <code>[*/4] StartInference and FinishInference: optimiziation</code> tasks to finalize this work in milestone 0.2.11. I think it'd be better to re-open in case of additinal optimizations required</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #780](https://github.com/gonka-ai/gonka/issues/780) every hour.
