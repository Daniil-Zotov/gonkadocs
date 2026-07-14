Gonka Epochs 132-133 CPoC Compensation Analysis

Complete analysis and compensation calculations for participants affected by the Confirmation Proof of Compute (CPoC) bug in Gonka blockchain epochs 132-133.

Overview

This repository contains the complete statistical analysis proving that epochs 132-133 were abnormal, identification of affected participants, and fair compensation calculations based on median reward coefficients from successful participants.

Key Findings:

Epochs 132-133 were statistically abnormal: Confirmation ratios dropped 14-22% below baseline

45 affected participants: 13 in epoch 132, 32 in epoch 133

Total compensation: 24,799.48 GONKA

Selection criteria: CR 25-50%, miss rate 
Quick Start - Verify the Findings

Option 1: Review Final Results (Recommended)

Read the Summary:

cat COMPENSATION_SUMMARY.md

This provides the complete overview, methodology, and final compensation amounts.

Review Compensation Details:

JSON format: compensation_epoch_132.json and compensation_epoch_133.json

CSV format (Excel-friendly): compensation_epoch_132.csv and compensation_epoch_133.csv

Check Affected Participants Lists:

Epoch 132: affected_participants_epoch_132.json (13 participants)

Epoch 133: affected_participants_epoch_133.json (32 participants)

Option 2: Re-run the Entire Analysis

If you want to verify the calculations from scratch:

# Install Python dependencies
pip install -r requirements.txt

# Configure environment (first time only)
cp .env.example .env
# Edit .env to set your archive node URL and inferenced binary path

# Run analysis
# Phase 1: Fetch epoch data and analyze confirmation ratio distributions
python3 fetch_epoch_data.py 132 133

# Phase 2: Identify affected participants (those who received no rewards)
python3 identify_affected.py 132 133

# Phase 3: Calculate compensation amounts
python3 calculate_compensation.py 132 133

Requirements:

Python 3.x

Python packages: pip install -r requirements.txt

.env file configured with:

ARCHIVE_NODE_URL (archive node endpoint)

INFERENCED_BINARY (default: /Users/fixtwin/gonka/gonka/inferenced)

Option 3: Spot-Check Individual Participants

Verify specific participants manually using the archive node:

 0 → participant received rewards (not affected)"># Set up environment
INFERENCED="/Users/fixtwin/gonka/gonka/inferenced"
ARCHIVE_NODE="$ARCHIVE_NODE_URL" # From .env file

# Example: Check if a participant received rewards in epoch 132
ADDRESS="gonka14ued4vcdeluj9v9vmsmteap7vtg7t50640hvmf"

# Query their epoch performance summary (after settlement at height 2,060,000)
$INFERENCED query inference show-epoch-performance-summary-by-participant \
 132 $ADDRESS --node $ARCHIVE_NODE --height 2060000 -o json | jq '.'

# Look for "rewarded_coins" field:
# - If absent or "0" → participant received NO rewards (affected)
# - If present with value > 0 → participant received rewards (not affected)

Key Files Overview

Analysis Scripts

File
Purpose

fetch_epoch_data.py
Phase 1: Fetch raw epoch data from archive node

identify_affected.py
Phase 2: Filter participants by criteria (25-50% CR, 

calculate_compensation.py
Phase 3: Calculate compensation based on median coefficient

Output Files

File
Description

COMPENSATION_SUMMARY.md
START HERE - Complete analysis summary

compensation_epoch_*.json
Detailed compensation records (ngonka amounts)

compensation_epoch_*.csv
Same data in CSV format for spreadsheets

affected_participants_epoch_*.json
Lists of qualified affected participants

analyzed_participants_epoch_*.json
All candidates analyzed (including those rejected)

epoch_*_data.json
Raw epoch data from Phase 1

Raw Data Files

File
Description

epoch_132_data.json
All 609 participants in epoch 132 with weights

epoch_133_data.json
All 594 participants in epoch 133 with weights

Validation Checklist

Use this checklist to verify the analysis:

 Verify affected participant criteria:

 All have confirmation_ratio between 25% and 50%

 All have miss_rate All have rewarded_coins = 0 (received no epoch rewards)

 Verify compensation calculation:

 Coefficient calculated from median of successful participants

 Expected reward = confirmation_weight × coefficient

 Compensation = expected_reward - actual_reward (0)

 Spot-check sample participants:

 Pick 3-5 random affected participants

 Query their EpochPerformanceSummary from archive node

 Confirm rewarded_coins = 0

 Verify their confirmation_ratio is in 25-50% range

 Verify totals:

 Epoch 132: 13 participants, ~6,970 GONKA

 Epoch 133: 32 participants, ~17,830 GONKA

 Total: ~24,800 GONKA

Sample Verification Commands

Check a specific participant's qualification

# Participant address
ADDR="gonka1hec2h63xkf9qf7gn07uwucveuhjfrqks8f4dmh"

# 1. Check their confirmation ratio (from epoch_132_data.json)
cat epoch_132_data.json | jq --arg addr "$ADDR" \
 '.participants[] | select(.address == $addr) | 
 {address, confirmation_ratio, base_weight, confirmation_weight}'

# 2. Check their performance stats (before epoch end)
$INFERENCED query inference show-participant $ADDR \
 --node $ARCHIVE_NODE --height 2058356 -o json | \
 jq '.participant.current_epoch_stats'

# 3. Check if they received rewards (after settlement)
$INFERENCED query inference show-epoch-performance-summary-by-participant \
 132 $ADDR --node $ARCHIVE_NODE --height 2060000 -o json | \
 jq '.epochPerformanceSummary.rewarded_coins // "NO REWARDS"'

Verify the reward coefficient calculation

# Sample a successful participant who DID receive rewards
SUCCESS_ADDR="gonka1w6wwv3wq25p8qge4lqsnfzs8lsd3s8ty6au65p"

# Get their epoch summary
$INFERENCED query inference show-epoch-performance-summary-by-participant \
 132 $SUCCESS_ADDR --node $ARCHIVE_NODE --height 2060000 -o json | \
 jq '{rewarded_coins, address}'

# Get their confirmation_weight
cat epoch_132_data.json | jq --arg addr "$SUCCESS_ADDR" \
 '.participants[] | select(.address == $addr) | 
 {confirmation_weight}'

# Calculate coefficient manually:
# coefficient = rewarded_coins / confirmation_weight
# Should equal ~52,796,590.93 for epoch 132

Questions or Issues?

If the verification reveals discrepancies:

Check archive node accessibility: Ensure the ARCHIVE_NODE_URL from .env is reachable

Verify block heights: Ensure querying at correct heights (see COMPENSATION_SUMMARY.md)

Check conversion factor: 1 GONKA = 1,000,000,000 ngonka (9 decimals)

Review selection criteria: Only participants with ALL three criteria qualify

Technical Details

Archive Node: Configured via environment variables (see .env.example)

Token Denomination: 1 GONKA = 1,000,000,000 ngonka (9 decimals)

Analysis Date: March 5, 2026

Epochs Analyzed: 132, 133

Total Affected Participants: 43 unique addresses (13 + 32 - 2 duplicates)

Recommended Compensation Pool: 24,799.48 GONKA

For questions or clarifications, refer to COMPENSATION_SUMMARY.md for detailed methodology.
