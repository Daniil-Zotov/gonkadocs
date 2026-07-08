---
title: "#3 – Increase PoC Validation Length"
description: "Proposal updates poc_validation_duration from 20 to 100."
template: proposals-proposals-main.html
---

# #3 – Increase PoC Validation Length

<div class="prop-detail-header" markdown="1">

<span class="prop-badge prop-passed">Passed</span>

**Proposal ID:** `3`

**Type:** Update Params

**Submit:** 2025-09-20 05:16 UTC

**Voting:** 2025-09-20 05:16 UTC → 2025-09-20 17:16 UTC

**Expedited:** Yes

**Proposer:** [`gonka18lluv53n4h9z34qu20vxcvypgdkhsg6nn2cl2d`](https://gonka.gg/address/gonka18lluv53n4h9z34qu20vxcvypgdkhsg6nn2cl2d){:target="_blank"}

**Metadata:** [https://github.com/gonka-ai/gonka/blob/2bf281cec95eaef061e2dfe46d4d104a7e1c2229/proposals/poc-validation-length/README.md](https://github.com/gonka-ai/gonka/blob/2bf281cec95eaef061e2dfe46d4d104a7e1c2229/proposals/poc-validation-length/README.md)



[View on gonka.gg](https://gonka.gg/network/proposals/3){:target="_blank"}

</div>

Proposal updates poc_validation_duration from 20 to 100.

---

## Final Tally


<div class="prop-tally">
  <div class="prop-tally-bar">
    <div class="prop-tally-yes" style="width:100.0%"></div>
    <div class="prop-tally-no" style="width:0.0%"></div>
    <div class="prop-tally-veto" style="width:0.0%"></div>
    <div class="prop-tally-abstain" style="width:0.0%"></div>
  </div>
  <div class="prop-tally-stats">
    <span class="prop-tally-yes-text">Yes 162,514 (100.0%)</span>
    <span class="prop-tally-no-text">No 0 (0.0%)</span>
    <span class="prop-tally-veto-text">Veto 0 (0.0%)</span>
    <span class="prop-tally-abstain-text">Abstain 0 (0.0%)</span>
    <span class="prop-tally-quorum-text">Quorum 25.0%</span>
  </div>
</div>


---

## Messages

| # | Type |
| :- | :--- |
| 1 | `/inference.inference.MsgUpdateParams` |

<details class="prop-contracts">
<summary>Contract Details</summary>

```json
[
  {
    "@type": "/inference.inference.MsgUpdateParams",
    "authority": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "params": {
      "epoch_params": {
        "epoch_length": "15391",
        "epoch_multiplier": "1",
        "epoch_shift": "16980",
        "default_unit_of_compute_price": "100",
        "poc_stage_duration": "60",
        "poc_exchange_duration": "5",
        "poc_validation_delay": "5",
        "poc_validation_duration": "120",
        "set_new_validators_delay": "120",
        "inference_validation_cutoff": "80",
        "inference_pruning_epoch_threshold": "2",
        "inference_pruning_max": "0",
        "poc_pruning_max": "0",
        "poc_slot_allocation": null,
        "confirmation_poc_safety_window": "0"
      },
      "validation_params": {
        "false_positive_rate": {
          "value": "5",
          "exponent": -2
        },
        "min_ramp_up_measurements": 10,
        "pass_value": {
          "value": "99",
          "exponent": -2
        },
        "min_validation_average": {
          "value": "1",
          "exponent": -2
        },
        "max_validation_average": {
          "value": "1",
          "exponent": 0
        },
        "expiration_blocks": "20",
        "epochs_to_max": "30",
        "full_validation_traffic_cutoff": "10000",
        "min_validation_halfway": {
          "value": "5",
          "exponent": -2
        },
        "min_validation_traffic_cutoff": "100",
        "miss_percentage_cutoff": {
          "value": "1",
          "exponent": -2
        },
        "miss_requests_penalty": {
          "value": "1",
          "exponent": 0
        },
        "timestamp_expiration": "60",
        "timestamp_advance": "30",
        "estimated_limits_per_block_kb": "0",
        "invalid_reputation_preserve": null,
        "bad_participant_invalidation_rate": null,
        "invalidation_h_threshold": null,
        "downtime_good_percentage": null,
        "downtime_bad_percentage": null,
        "downtime_h_threshold": null,
        "downtime_reputation_preserve": null,
        "quick_failure_threshold": null,
        "binom_test_p0": null,
        "claim_validation_enabled": false,
        "logprobs_mode": ""
      },
      "poc_params": {
        "default_difficulty": 5,
        "validation_sample_size": 200,
        "poc_data_pruning_epoch_threshold": "1",
        "weight_scale_factor": null,
        "model_params": null,
        "model_id": "",
        "seq_len": "0",
        "poc_v2_enabled": false,
        "confirmation_poc_v2_enabled": false,
        "stat_test": null,
        "validation_slots": 0,
        "poc_normalization_enabled": false,
        "poc_stronger_rng_enabled": false,
        "models": []
      },
      "tokenomics_params": {
        "subsidy_reduction_interval": {
          "value": "5",
          "exponent": -2
        },
        "subsidy_reduction_amount": {
          "value": "2",
          "exponent": -1
        },
        "current_subsidy_percentage": {
          "value": "9",
          "exponent": -1
        },
        "work_vesting_period": "180",
        "reward_vesting_period": "180"
      },
      "collateral_params": {
        "slash_fraction_invalid": {
          "value": "2",
          "exponent": -1
        },
        "slash_fraction_downtime": {
          "value": "1",
          "exponent": -1
        },
        "downtime_missed_percentage_threshold": {
          "value": "5",
          "exponent": -2
        },
        "grace_period_end_epoch": "180",
        "base_weight_ratio": {
          "value": "2",
          "exponent": -1
        },
        "collateral_per_weight_unit": {
          "value": "42",
          "exponent": -1
        }
      },
      "bitcoin_reward_params": {
        "use_bitcoin_rewards": true,
        "initial_epoch_reward": "323000000000000",
        "decay_rate": {
          "value": "-475",
          "exponent": -6
        },
        "genesis_epoch": "1",
        "utilization_bonus_factor": {
          "value": "5",
          "exponent": -1
        },
        "full_coverage_bonus_factor": {
          "value": "12",
          "exponent": -1
        },
        "partial_coverage_bonus_factor": {
          "value": "1",
          "exponent": -1
        }
      },
      "dynamic_pricing_params": {
        "stability_zone_lower_bound": {
          "value": "4",
          "exponent": -1
        },
        "stability_zone_upper_bound": {
          "value": "6",
          "exponent": -1
        },
        "price_elasticity": {
          "value": "5",
          "exponent": -2
        },
        "utilization_window_duration": "60",
        "min_per_token_price": "1",
        "base_per_token_price": "100",
        "grace_period_end_epoch": "90",
        "grace_period_per_token_price": "0"
      },
      "bandwidth_limits_params": {
        "estimated_limits_per_block_kb": "10752",
        "kb_per_input_token": {
          "value": "23",
          "exponent": -4
        },
        "kb_per_output_token": {
          "value": "64",
          "exponent": -2
        },
        "invalidations_limit": "0",
        "invalidations_sample_period": "0",
        "invalidations_limit_curve": "0",
        "minimum_concurrent_invalidations": 0,
        "max_inferences_per_block": "0"
      },
      "confirmation_poc_params": null,
      "genesis_guardian_params": null,
      "developer_access_params": null,
      "participant_access_params": null,
      "transfer_agent_access_params": null,
      "devshard_escrow_params": null,
      "fee_params": null,
      "delegation_params": null
    }
  }
]
```

</details>

---