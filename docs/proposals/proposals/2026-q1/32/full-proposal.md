# Simple Coin Amount Explanation (Epoch 158)

For epoch 158, we first take the total amount distributed by the reward simulation for that epoch: **252,286,759,171,835 ngonka**.
Then we divide it by the total non-preserved (confirmation) weight used for epoch 158: **4,981,565**.
This gives a single conversion rate: **50,644,076.544586889446 ngonka per 1 weight unit**.
In simple terms, this is the average value of one weight unit in epoch 158.

After that, we calculate lost preserved weight for each participant.
We restore historical preserved weight from the chain snapshot at block **2,443,438** (the effective block of epoch 158), and compare it to the preserved weight of epoch 158 in current-state epoch data (after reset).
If historical value is higher, the difference is the lost preserved weight; otherwise loss is zero.
Compensation is computed as this lost preserved weight multiplied by the single per-weight rate, then rounded to whole ngonka.

Example: if lost preserved weight is **4,663**, then
**4,663 × 50,644,076.544586889446 = 236,153,328,927.39...**,
so final compensation is **236,153,328,927 ngonka** (**236.153328927 GNK**).
If lost preserved weight is zero, compensation is zero.

Finally, after all participant compensations are calculated, an additional fixed payment of **500 GNK** is added to the proposal author.

Also, `MsgBatchTransferWithVesting` has a minimum payout of **10 GNK**. Because of that, all payouts below this threshold in `epoch_158_compensation_proposal_batch_vesting.json` were raised to **10,000,000,000 ngonka** after the chain rejected smaller amounts.

Generated governance proposal JSON:
https://github.com/huxuxuya/epoch158/blob/main/artifacts/epoch_158/epoch_158_compensation_proposal.json
