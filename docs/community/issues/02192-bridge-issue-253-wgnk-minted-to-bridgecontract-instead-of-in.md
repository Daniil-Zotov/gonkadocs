---
title: "#2192 — Bridge issue: 253 WGNK minted to BridgeContract instead of intended wallet"
source: https://github.com/gonka-ai/gonka/issues/2192
issue_number: 2192
synced_at: 2026-11-10T17:57:40Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    Bridge issue: 253 WGNK minted to BridgeContract instead of intended wallet
    <span class="issues-number">#2192</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/AkSwiss573">@AkSwiss573</a> opened 2026-10-31 05:07 UTC</span>
    <span class="issues-meta-item">8 comments</span>
    <span class="issues-meta-item">Updated 2026-11-03 19:05 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">

Problem

I accidentally received 253 WGNK at the BridgeContract address instead of my intended Ethereum wallet address during a GNK-to-WGNK bridge operation.

Transaction details

- Transaction hash: "0xffcf0eec7058b01597ccf0ffb0d513ec1915fca04216d092e2a6779c437458ee"
- Amount: 253 WGNK
- Incorrect recipient (BridgeContract): "0x972a7A92D92796a98801A8818bcF91f1648f2F68"
- Intended recipient (my wallet): "0xd0A76F94f432Ec4Fba3B701127bB0D47EEf00254"

Actual result

The transaction logs show that 253 WGNK were minted directly to the BridgeContract address.

Expected result

The 253 WGNK should have been minted to my intended Ethereum wallet address.

Request

Could the Gonka bridge developers please investigate whether the original transaction can be corrected or the 253 WGNK recovered through an authorized contract-level intervention?

Please escalate this issue to the developers responsible for the bridge smart contract.

I am not requesting a duplicate mint. I am requesting assistance with the original transaction.

Thank you.
</div>

---

## 💬 Comments (8)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/AkSwiss573">@AkSwiss573</a></span>
    <span class="issues-meta-item">commented 2026-11-03 03:17 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Additional important information:</p>
<p>All the affected GNK transactions mentioned in PR #2179 belong to me.</p>
<p>The amounts listed are 2, 2, 1.5 and 253 GNK. There is also an additional 1 GNK that belongs to me.</p>
<p>The total amount I need help recovering is 259.5 GNK / WGNK.</p>
<p>Please investigate all affected transactions and the full 259.5 WGNK balance held by the BridgeContract.</p>
<p>I am requesting recovery of my original funds, not a duplicate mint.</p>
<p>Thank you for your help.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/AkSwiss573">@AkSwiss573</a></span>
    <span class="issues-meta-item">commented 2026-11-03 03:18 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@cyberdelamain @GLiberman Could you please review this issue? All affected transactions belong to me. Thank you.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/cyberdelamain">@cyberdelamain</a></span>
    <span class="issues-meta-item">commented 2026-11-03 03:30 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Hi @AkSwiss573, I looked at all five transactions. Good news: your GNK are not lost.</p>
<p><strong>Where the GNK are.</strong> When WGNK is minted to the bridge contract itself, the chain treats it as a burn and releases the same amount of GNK from escrow to the Gonka address derived from the key of the wallet that submitted the Ethereum tx. For your four mints that wallet is <code>0x64920118b0bb74af42600741710d462c22343d27</code>, and the 258.5 GNK (2 + 2 + 1.5 + 253) are sitting untouched on <code>gonka1au59g7ny8v7csp8gaue07mz7vy0heau6wl6fp6</code> (balance 258.5 GNK, no outgoing txs). To access them, import the private key of <code>0x6492…3d27</code> into a Gonka wallet (same secp256k1 key, Cosmos address derivation) and send the GNK wherever you like.</p>
<p><strong>The extra 1 GNK</strong> (09.06, ETH block 25282474) was already released back to the requesting account <code>gonka15av07hfqre9s3jmr7pt4d944e25fzt7ylj3u75</code>.</p>
<p><strong>The 259.5 WGNK on the bridge contract</strong> stay frozen there, but nothing is owed on them: the matching GNK was already released on the Gonka side, as above.</p>
<p><strong>Fix.</strong> #2179 makes the chain reject a bridge contract as the mint/withdrawal destination, so this can no longer happen. It is open and waiting for review.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/AkSwiss573">@AkSwiss573</a></span>
    <span class="issues-meta-item">commented 2026-11-03 07:35 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Thank you for confirming that my 258.5 GNK are safe.</p>
<p>I understand that I need to import the private key of my Ethereum address
into a Gonka wallet.</p>
<p>However, the official Gonka CLI import keeps failing on Android/Termux
because of the keyring password prompt.</p>
<p>Could you please provide one of the following:</p>
<ol>
<li>An Android-compatible method to import my existing Ethereum private key
into a Gonka wallet, or</li>
<li>A supported alternative wallet or recovery tool that can import this
exact secp256k1 private key using Gonka's Cosmos address derivation.</li>
</ol>
<p>I do not want to create a new wallet or repeat the same failed CLI
procedure.</p>
<p>I can then transfer the 258.5 GNK to my existing Keplr Gonka address.</p>
<p>Thank you for helping me complete the recovery.</p>
<p>Delamain <strong><em>@</em></strong>.***&gt; schrieb am Di., 3. Nov. 2026, 11:30:</p>
<blockquote>
<p><em>cyberdelamain</em> left a comment (gonka-ai/gonka#2192)
<a href="https://github.com/gonka-ai/gonka/issues/2192#issuecomment-6594711720">https://github.com/gonka-ai/gonka/issues/2192#issuecomment-6594711720</a></p>
<p>Hi @AkSwiss573 <a href="https://github.com/AkSwiss573">https://github.com/AkSwiss573</a>, I looked at all five
transactions. Good news: your GNK are not lost.</p>
<p><em>Where the GNK are.</em> When WGNK is minted to the bridge contract itself,
the chain treats it as a burn and releases the same amount of GNK from
escrow to the Gonka address derived from the key of the wallet that
submitted the Ethereum tx. For your four mints that wallet is
0x64920118b0bb74af42600741710d462c22343d27, and the 258.5 GNK (2 + 2 +
1.5 + 253) are sitting untouched on
gonka1au59g7ny8v7csp8gaue07mz7vy0heau6wl6fp6 (balance 258.5 GNK, no
outgoing txs). To access them, import the private key of 0x6492…3d27 into
a Gonka wallet (same secp256k1 key, Cosmos address derivation) and send the
GNK wherever you like.</p>
<p><em>The extra 1 GNK</em> (09.06, ETH block 25282474) was already released back
to the requesting account gonka15av07hfqre9s3jmr7pt4d944e25fzt7ylj3u75.</p>
<p><em>The 259.5 WGNK on the bridge contract</em> stay frozen there, but nothing is
owed on them: the matching GNK was already released on the Gonka side, as
above.</p>
<p><em>Fix.</em> #2179 <a href="https://github.com/gonka-ai/gonka/pull/2179">https://github.com/gonka-ai/gonka/pull/2179</a> makes the
chain reject a bridge contract as the mint/withdrawal destination, so this
can no longer happen. It is open and waiting for review.</p>
<p>—
Reply to this email directly, view it on GitHub
<a href="https://github.com/gonka-ai/gonka/issues/2192?email_source=notifications&amp;email_token=CTS6GTU4F5W35AOUM3CXNOD5XFGNPA5CNFSNUABFM5UWIORPF5TWS5BNNB2WEL2JONZXKZKDN5WW2ZLOOQXTMNJZGQ3TCMJXGIYKM4TFMFZW63VHNVSW45DJN5XKKZLWMVXHJLDGN5XXIZLSL5RWY2LDNM#issuecomment-6594711720">https://github.com/gonka-ai/gonka/issues/2192?email_source=notifications&amp;email_token=CTS6GTU4F5W35AOUM3CXNOD5XFGNPA5CNFSNUABFM5UWIORPF5TWS5BNNB2WEL2JONZXKZKDN5WW2ZLOOQXTMNJZGQ3TCMJXGIYKM4TFMFZW63VHNVSW45DJN5XKKZLWMVXHJLDGN5XXIZLSL5RWY2LDNM#issuecomment-6594711720</a>,
or unsubscribe
<a href="https://github.com/notifications/unsubscribe-auth/CTS6GTWS2QA5OGTJXISXO235XFGNPAVCNFSNUABFKJSXA33TNF2G64TZHM4DENZQGYYTAOJSHNEXG43VMU5TMMJTGE2DCNRQGM3KC5QC">https://github.com/notifications/unsubscribe-auth/CTS6GTWS2QA5OGTJXISXO235XFGNPAVCNFSNUABFKJSXA33TNF2G64TZHM4DENZQGYYTAOJSHNEXG43VMU5TMMJTGE2DCNRQGM3KC5QC</a>
.
Triage notifications, keep track of coding agent tasks and review pull
requests on the go with GitHub Mobile for iOS
<a href="https://github.com/notifications/mobile/ios/CTS6GTSQWFFU2OPM2U6KKYT5XFGNPA5CNFSNUABFM5UWIORPF5TWS5BNNB2WEL2JONZXKZKDN5WW2ZLOOQXTMNJZGQ3TCMJXGIYKM4TFMFZW63VHNVSW45DJN5XKKZLWMVXHJKTGN5XXIZLSL5UW64Y">https://github.com/notifications/mobile/ios/CTS6GTSQWFFU2OPM2U6KKYT5XFGNPA5CNFSNUABFM5UWIORPF5TWS5BNNB2WEL2JONZXKZKDN5WW2ZLOOQXTMNJZGQ3TCMJXGIYKM4TFMFZW63VHNVSW45DJN5XKKZLWMVXHJKTGN5XXIZLSL5UW64Y</a>
and Android
<a href="https://github.com/notifications/mobile/android/CTS6GTUABYEB4T3VJ6M6ES35XFGNPA5CNFSNUABFM5UWIORPF5TWS5BNNB2WEL2JONZXKZKDN5WW2ZLOOQXTMNJZGQ3TCMJXGIYKM4TFMFZW63VHNVSW45DJN5XKKZLWMVXHJLTGN5XXIZLSL5QW4ZDSN5UWI">https://github.com/notifications/mobile/android/CTS6GTUABYEB4T3VJ6M6ES35XFGNPA5CNFSNUABFM5UWIORPF5TWS5BNNB2WEL2JONZXKZKDN5WW2ZLOOQXTMNJZGQ3TCMJXGIYKM4TFMFZW63VHNVSW45DJN5XKKZLWMVXHJLTGN5XXIZLSL5QW4ZDSN5UWI</a>.
Download it today!
You are receiving this because you were mentioned.Message ID:
<strong><em>@</em></strong>.***&gt;
</p>
</blockquote>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/AkSwiss573">@AkSwiss573</a></span>
    <span class="issues-meta-item">commented 2026-11-03 07:36 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@cyberdelamain </p>
<p>Thank you for confirming that my 258.5 GNK are safe.</p>
<p>I understand that I need to import the private key of my Ethereum address into a Gonka wallet.</p>
<p>However, the official Gonka CLI import keeps failing on Android/Termux because of the keyring password prompt.</p>
<p>Could you please provide one of the following:</p>
<ol>
<li>An Android-compatible method to import my existing Ethereum private key into a Gonka wallet, or</li>
<li>A supported alternative wallet or recovery tool that can import this exact secp256k1 private key using Gonka's Cosmos address derivation.</li>
</ol>
<p>I do not want to create a new wallet or repeat the same failed CLI procedure.</p>
<p>I can then transfer the 258.5 GNK to my existing Keplr Gonka address.</p>
<p>Thank you for helping me complete the recovery.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/cyberdelamain">@cyberdelamain</a></span>
    <span class="issues-meta-item">commented 2026-11-03 07:41 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@AkSwiss573 You don't need the CLI for this. Keplr (mobile app included) can import a private key directly: add a new wallet in the same Keplr where your main Gonka account is, choose the private key import option, and paste the private key of <code>0x6492…3d27</code>. It should show <code>gonka1au59g7ny8v7csp8gaue07mz7vy0heau6wl6fp6</code> with 258.5 GNK, and you can then send them to your main address.</p>
<p>If you're unsure about the exact steps, any guide on "import private key into Keplr" covers it, or you can ask an AI assistant to walk you through it. Please never share the key itself with anyone, including here.</p>
<p>If you still prefer the CLI on Termux, <code>--keyring-backend test</code> avoids the keyring password prompt.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/AkSwiss573">@AkSwiss573</a></span>
    <span class="issues-meta-item">commented 2026-11-03 09:02 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Thank you very much for your help!!!! I have recovered my GNK and
successfully transferred it to MetaMask by bridging it into wGNK.</p>
<p>Delamain <strong><em>@</em></strong>.***&gt; schrieb am Di., 3. Nov. 2026, 15:42:</p>
<blockquote>
<p><em>cyberdelamain</em> left a comment (gonka-ai/gonka#2192)
<a href="https://github.com/gonka-ai/gonka/issues/2192#issuecomment-6598141592">https://github.com/gonka-ai/gonka/issues/2192#issuecomment-6598141592</a></p>
<p>@AkSwiss573 <a href="https://github.com/AkSwiss573">https://github.com/AkSwiss573</a> You don't need the CLI for
this. Keplr (mobile app included) can import a private key directly: add a
new wallet in the same Keplr where your main Gonka account is, choose the
private key import option, and paste the private key of 0x6492…3d27. It
should show gonka1au59g7ny8v7csp8gaue07mz7vy0heau6wl6fp6 with 258.5 GNK,
and you can then send them to your main address.</p>
<p>If you're unsure about the exact steps, any guide on "import private key
into Keplr" covers it, or you can ask an AI assistant to walk you through
it. Please never share the key itself with anyone, including here.</p>
<p>If you still prefer the CLI on Termux, --keyring-backend test avoids the
keyring password prompt.</p>
<p>—
Reply to this email directly, view it on GitHub
<a href="https://github.com/gonka-ai/gonka/issues/2192?email_source=notifications&amp;email_token=CTS6GTTRX6FWAAE26GIGDCT5XGD5PA5CNFSNUABFM5UWIORPF5TWS5BNNB2WEL2JONZXKZKDN5WW2ZLOOQXTMNJZHAYTIMJVHEZKM4TFMFZW63VHNVSW45DJN5XKKZLWMVXHJLDGN5XXIZLSL5RWY2LDNM#issuecomment-6598141592">https://github.com/gonka-ai/gonka/issues/2192?email_source=notifications&amp;email_token=CTS6GTTRX6FWAAE26GIGDCT5XGD5PA5CNFSNUABFM5UWIORPF5TWS5BNNB2WEL2JONZXKZKDN5WW2ZLOOQXTMNJZHAYTIMJVHEZKM4TFMFZW63VHNVSW45DJN5XKKZLWMVXHJLDGN5XXIZLSL5RWY2LDNM#issuecomment-6598141592</a>,
or unsubscribe
<a href="https://github.com/notifications/unsubscribe-auth/CTS6GTQUYY34632PJQ5BM2T5XGD5PAVCNFSNUABFKJSXA33TNF2G64TZHM4DENZQGYYTAOJSHNEXG43VMU5TMMJTGE2DCNRQGM3KC5QC">https://github.com/notifications/unsubscribe-auth/CTS6GTQUYY34632PJQ5BM2T5XGD5PAVCNFSNUABFKJSXA33TNF2G64TZHM4DENZQGYYTAOJSHNEXG43VMU5TMMJTGE2DCNRQGM3KC5QC</a>
.
Triage notifications, keep track of coding agent tasks and review pull
requests on the go with GitHub Mobile for iOS
<a href="https://github.com/notifications/mobile/ios/CTS6GTV77PM7IPOZKQ2GUP35XGD5PA5CNFSNUABFM5UWIORPF5TWS5BNNB2WEL2JONZXKZKDN5WW2ZLOOQXTMNJZHAYTIMJVHEZKM4TFMFZW63VHNVSW45DJN5XKKZLWMVXHJKTGN5XXIZLSL5UW64Y">https://github.com/notifications/mobile/ios/CTS6GTV77PM7IPOZKQ2GUP35XGD5PA5CNFSNUABFM5UWIORPF5TWS5BNNB2WEL2JONZXKZKDN5WW2ZLOOQXTMNJZHAYTIMJVHEZKM4TFMFZW63VHNVSW45DJN5XKKZLWMVXHJKTGN5XXIZLSL5UW64Y</a>
and Android
<a href="https://github.com/notifications/mobile/android/CTS6GTQABVTVNJSG3OTOODD5XGD5PA5CNFSNUABFM5UWIORPF5TWS5BNNB2WEL2JONZXKZKDN5WW2ZLOOQXTMNJZHAYTIMJVHEZKM4TFMFZW63VHNVSW45DJN5XKKZLWMVXHJLTGN5XXIZLSL5QW4ZDSN5UWI">https://github.com/notifications/mobile/android/CTS6GTQABVTVNJSG3OTOODD5XGD5PA5CNFSNUABFM5UWIORPF5TWS5BNNB2WEL2JONZXKZKDN5WW2ZLOOQXTMNJZHAYTIMJVHEZKM4TFMFZW63VHNVSW45DJN5XKKZLWMVXHJLTGN5XXIZLSL5QW4ZDSN5UWI</a>.
Download it today!
You are receiving this because you were mentioned.Message ID:
<strong><em>@</em></strong>.***&gt;
</p>
</blockquote>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/AkSwiss573">@AkSwiss573</a></span>
    <span class="issues-meta-item">commented 2026-11-03 09:03 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@cyberdelamain </p>
<p>Thank you very much for your help; I have recovered my GNK and successfully transferred it to MetaMask by bridge it into wGNK.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #2192](https://github.com/gonka-ai/gonka/issues/2192) every hour.
