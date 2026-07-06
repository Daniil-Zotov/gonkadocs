---
title: "#714 — Bug Report: New Nodes Fail to Sign Transactions (Keyring Backend Mismatch)"
source: https://github.com/gonka-ai/gonka/issues/714
issue_number: 714
synced_at: 2026-07-06T09:52:55Z
template: issues-main.html
---

> 🔄 **Auto-synced:** from [Issue #714](https://github.com/gonka-ai/gonka/issues/714) every 6 hours. 

# 🔴 Bug Report: New Nodes Fail to Sign Transactions (Keyring Backend Mismatch)

**Author:** [@moro3one](https://github.com/moro3one) · **State:** Closed · **Created:** 2026-02-07 08:47 UTC · **Updated:** 2026-02-10 00:33 UTC

---

## 📝 Описание

*(empty)*

---

## 💬 Comments (4)

### Комментарий 1 — [@moro3one](https://github.com/moro3one)

*2026-02-07 08:52 UTC*

Bug report: New nodes fail to sign transactions due to Keyring Backend mismatch in Docker config. Fix included in description.

### Комментарий 2 — [@moro3one](https://github.com/moro3one)

*2026-02-07 08:58 UTC*

FULL BUG REPORT:
Severity: High
Environment: Mainnet / Docker Compose

Summary:
The current Docker deployment setup for new join nodes fails to initialize the api service correctly due to a configuration mismatch in how KEYRING_BACKEND is handled. The init-docker.sh entrypoint fails to source config.env variables because of export prefixes, causing the api container to default to keyring-backend=file. However, the onboarding process generates keys using keyring-backend=test.

This results in the api service being unable to find the operator's private key, leading to a loop of 'account does not exist' errors. The node appears 'Active' in the explorer

### Комментарий 3 — [@gmorgachev](https://github.com/gmorgachev)

*2026-02-07 21:18 UTC*

Current onboarding pipeline uses manually creating warm key with `file` keyring backend:
https://gonka.ai/host/quickstart/#31-server-create-ml-operational-key

Explicitly suggest:
```
printf '%s\n%s\n' "$KEYRING_PASSWORD" "$KEYRING_PASSWORD" | inferenced keys add "$KEY_NAME" --keyring-backend file
```

`export` prefixes work with current onboarding pipeline as it uses explicit loading of environment variables via:
```
source config.env
```

> However, the onboarding process generates keys using keyring-backend=test

Are you refering to?
```
if [ "${CREATE_KEY:-false}" = "true" ]; then
  echo "Creating account key: $KEY_NAME"

  if command -v inferenced >/dev/null 2>&1; then
    APP_NAME="inferenced"
  else
    APP_NAME="decentralized-api"
  fi

  $APP_NAME keys add "$KEY_NAME" \
    --keyring-backend test \
    --keyring-dir /root/.inference

  ACCOUNT_PUBKEY=$($APP_NAME keys show "$KEY_NAME" --pubkey --keyring-backend test --keyring-dir /root/.inference | jq -r '.key')
  export ACCOUNT_PUBKEY
  echo "Generated ACCOUNT_PUBKEY: $ACCOUNT_PUBKEY"
fi
```

That part is used only during automatic testing in local testnet and is not used in onboarding pipeline

If i'm not missing smth, the `source config.env` step was skipped which caused unexpected behaviour.

### Комментарий 4 — [@AlexeySamosadov](https://github.com/AlexeySamosadov)

*2026-02-08 14:13 UTC*

PR created: https://github.com/gonka-ai/gonka/pull/715

Fixes keyring backend mismatch for new join nodes.
