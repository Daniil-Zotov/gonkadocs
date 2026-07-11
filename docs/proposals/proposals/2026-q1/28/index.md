---
title: "#28 – Collateral Parameters Update"
description: "0.032 GNK per 1 unit of power, 0.01% slashing for miss rate or jail, 0.5% slashing for invalid inference"
template: proposals-proposals-main.html
---

# #28 – Collateral Parameters Update

<div class="prop-detail-header" markdown="1">

<span class="prop-badge prop-rejected">Rejected</span>

**Proposal ID:** `28`

**Type:** Update Params

**Submit:** 2026-02-18 07:27 UTC

**Voting:** 2026-02-18 07:27 UTC → 2026-02-19 07:27 UTC

**Proposer:** [`gonka18lluv53n4h9z34qu20vxcvypgdkhsg6nn2cl2d`](https://gonka.gg/address/gonka18lluv53n4h9z34qu20vxcvypgdkhsg6nn2cl2d){:target="_blank"}

**Failed reason:** proposal did not get enough votes to pass



[View on gonka.gg](https://gonka.gg/network/proposals/28){:target="_blank"}

</div>

0.032 GNK per 1 unit of power, 0.01% slashing for miss rate or jail, 0.5% slashing for invalid inference

---

## Final Tally


<div class="prop-tally">
  <div class="prop-tally-bar">
    <div class="prop-tally-yes" style="width:96.5%"></div>
    <div class="prop-tally-no" style="width:3.5%"></div>
    <div class="prop-tally-veto" style="width:0.0%"></div>
    <div class="prop-tally-abstain" style="width:0.0%"></div>
  </div>
  <div class="prop-tally-stats">
    <span class="prop-tally-yes-text">Yes 314,460 (96.5%)</span>
    <span class="prop-tally-no-text">No 11,504 (3.5%)</span>
    <span class="prop-tally-veto-text">Veto 0 (0.0%)</span>
    <span class="prop-tally-abstain-text">Abstain 0 (0.0%)</span>
    <span class="prop-tally-total-text">Total 325,964 votes</span>
    
  </div>
</div>


---

## Messages

| # | Type |
| :- | :--- |
| 1 | `/inference.inference.MsgUpdateParams` |

<details class="prop-contracts" markdown="1">
<summary markdown="1">Contract Details</summary>

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
        "poc_validation_duration": "480",
        "set_new_validators_delay": "120",
        "inference_validation_cutoff": "2",
        "inference_pruning_epoch_threshold": "2",
        "inference_pruning_max": "5000",
        "poc_pruning_max": "1000",
        "poc_slot_allocation": {
          "value": "1",
          "exponent": -1
        },
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
        "expiration_blocks": "150",
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
        "timestamp_expiration": "300",
        "timestamp_advance": "30",
        "estimated_limits_per_block_kb": "0",
        "invalid_reputation_preserve": {
          "value": "0",
          "exponent": 0
        },
        "bad_participant_invalidation_rate": {
          "value": "1",
          "exponent": -1
        },
        "invalidation_h_threshold": {
          "value": "4",
          "exponent": 0
        },
        "downtime_good_percentage": {
          "value": "98",
          "exponent": -2
        },
        "downtime_bad_percentage": {
          "value": "99",
          "exponent": -2
        },
        "downtime_h_threshold": {
          "value": "1",
          "exponent": 2
        },
        "downtime_reputation_preserve": {
          "value": "0",
          "exponent": 0
        },
        "quick_failure_threshold": {
          "value": "1",
          "exponent": -6
        },
        "binom_test_p0": {
          "value": "1",
          "exponent": -1
        },
        "claim_validation_enabled": false,
        "logprobs_mode": ""
      },
      "poc_params": {
        "default_difficulty": 5,
        "validation_sample_size": 200,
        "poc_data_pruning_epoch_threshold": "1",
        "weight_scale_factor": {
          "value": "262",
          "exponent": -3
        },
        "model_params": {
          "dim": 1792,
          "n_layers": 64,
          "n_heads": 64,
          "n_kv_heads": 64,
          "vocab_size": 8196,
          "ffn_dim_multiplier": {
            "value": "1",
            "exponent": 1
          },
          "multiple_of": 8192,
          "norm_eps": {
            "value": "1",
            "exponent": -5
          },
          "rope_theta": 10000,
          "use_scaled_rope": false,
          "seq_len": 256,
          "r_target": {
            "value": "1398077",
            "exponent": -6
          }
        },
        "model_id": "Qwen/Qwen3-235B-A22B-Instruct-2507-FP8",
        "seq_len": "1024",
        "poc_v2_enabled": true,
        "confirmation_poc_v2_enabled": true,
        "stat_test": {
          "dist_threshold": {
            "value": "2",
            "exponent": -1
          },
          "p_mismatch": {
            "value": "1",
            "exponent": -1
          },
          "p_value_threshold": {
            "value": "5",
            "exponent": -2
          }
        },
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
          "value": "5",
          "exponent": -3
        },
        "slash_fraction_downtime": {
          "value": "1",
          "exponent": -4
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
          "value": "32",
          "exponent": 6
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
        "grace_period_per_token_price": "100"
      },
      "bandwidth_limits_params": {
        "estimated_limits_per_block_kb": "53760",
        "kb_per_input_token": {
          "value": "23",
          "exponent": -4
        },
        "kb_per_output_token": {
          "value": "64",
          "exponent": -2
        },
        "invalidations_limit": "500",
        "invalidations_sample_period": "120",
        "invalidations_limit_curve": "250",
        "minimum_concurrent_invalidations": 1,
        "max_inferences_per_block": "1000"
      },
      "confirmation_poc_params": {
        "expected_confirmations_per_epoch": "4",
        "alpha_threshold": {
          "value": "5",
          "exponent": -1
        },
        "slash_fraction": {
          "value": "0",
          "exponent": 0
        },
        "upgrade_protection_window": "500"
      },
      "genesis_guardian_params": {
        "network_maturity_threshold": "15000000",
        "network_maturity_min_height": "3000000",
        "guardian_addresses": [
          "gonkavaloper1y2a9p56kv044327uycmqdexl7zs82fs5lyang5",
          "gonkavaloper1dkl4mah5erqggvhqkpc8j3qs5tyuetgdc59d0v",
          "gonkavaloper1kx9mca3xm8u8ypzfuhmxey66u0ufxhs70mtf0e"
        ]
      },
      "developer_access_params": {
        "until_block_height": "2459367",
        "allowed_developer_addresses": [
          "gonka10fynmy2npvdvew0vj2288gz8ljfvmjs35lat8n",
          "gonka1v8gk5z7gcv72447yfcd2y8g78qk05yc4f3nk4w",
          "gonka1gndhek2h2y5849wf6tmw6gnw9qn4vysgljed0u",
          "gonka1z66ec2zedwpapp6jrj9raxgl93e5ec9z5my52h",
          "gonka1jw6xg0wun3g8m2fjm8lula82dw5p6jl8yp28mn",
          "gonka15sjedpgseutpnrjx2ge3mgau3s8ft5qzym9waa",
          "gonka1l4a2wtls9rgd2mnnj6mheml5xlq3kknngj4p7h",
          "gonka1f3yg5385n3f9pdw2g3dcjcnfqyej67hcu9vfet",
          "gonka15g5pu70k7l6hvdt8xl80h4mxe332762csupaeg",
          "gonka1uyqp5z3dveamfw4pmw7p7rfvwdvgzewnqrzhsu",
          "gonka18lluv53n4h9z34qu20vxcvypgdkhsg6nn2cl2d",
          "gonka1x7zh2277spp7jfqjhv0g5mnezg290xdr4kpfnk",
          "gonka1ddswmmmn38esxegjf6qw36mt4aqyw6etvysy5x",
          "gonka1kx9mca3xm8u8ypzfuhmxey66u0ufxhs7nm6wc5",
          "gonka1dkl4mah5erqggvhqkpc8j3qs5tyuetgdy552cp",
          "gonka1y2a9p56kv044327uycmqdexl7zs82fs5ryv5le",
          "gonka1p0uanq0aay6n3l4gtnshg63cy6vx3zgvkyc5lc",
          "gonka1khca2ht3m0nvpfghrxwgvnmj74t0sx6qzc2edd"
        ]
      },
      "participant_access_params": {
        "new_participant_registration_start_height": "2475000",
        "blocked_participant_addresses": [
          "gonka1blockedxxxxxxxxxxxxxxxxxxxxxx"
        ],
        "use_participant_allowlist": true,
        "participant_allowlist_until_block_height": "2475000"
      },
      "transfer_agent_access_params": {
        "allowed_transfer_addresses": [
          "gonka1y2a9p56kv044327uycmqdexl7zs82fs5ryv5le",
          "gonka1dkl4mah5erqggvhqkpc8j3qs5tyuetgdy552cp",
          "gonka1kx9mca3xm8u8ypzfuhmxey66u0ufxhs7nm6wc5",
          "gonka1ddswmmmn38esxegjf6qw36mt4aqyw6etvysy5x",
          "gonka10fynmy2npvdvew0vj2288gz8ljfvmjs35lat8n",
          "gonka1v8gk5z7gcv72447yfcd2y8g78qk05yc4f3nk4w",
          "gonka1gndhek2h2y5849wf6tmw6gnw9qn4vysgljed0u"
        ]
      },
      "devshard_escrow_params": null,
      "fee_params": null,
      "delegation_params": null
    }
  }
]
```

</details>

---