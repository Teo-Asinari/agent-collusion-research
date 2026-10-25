# Modal plan for a larger leak-capped run (NOT executed; needs owner approval)

Prices are from [modal.com/pricing](https://modal.com/pricing), fetched 2026-10-24, per second: L4 $0.000222 (≈ $0.80/h), A10 $0.000306 (≈ $1.10/h), A100-80GB $0.000694 (≈ $2.50/h), H100 $0.001097 (≈ $3.95/h). CPU costs $0.0000131 per core-second and memory $0.00000222 per GiB-second. The Starter plan includes $30/month of compute credit. Recheck the prices before launching.

## Goal

Take the CPU toy result (word denoising) to a task where an untrusted model's freedom clearly matters: **grade-school math word problems**. Measure utility (accuracy) against the leak cap k, and compare with the same untrusted model answering freely.

- **Public proposer** (trusted, public weights): a small open model, about 0.5B parameters. It samples 2^k solutions per problem from the problem text and a public seed. Fixed sampling budget: 2^kmax samples, always generated.
- **Untrusted chooser**: an open model of about 1.5B parameters, fine-tuned to output a k-bit index c given the problem and all candidates. It always scores every candidate, so its work is fixed.
- **Trusted decoder**: outputs candidate c verbatim. Lean `Choice.view_count` gives the at-most-k-bits bound for this wiring.
- **Baseline**: the same 1.5B model answering directly (unrestricted).
- **Adversary**: a scripted chooser that sets c = payload. Measure the bits recovered, which should be ≈ k minus duplicate loss. Also train a chooser with a payload objective and check that it cannot exceed k.

## Steps and cost estimate

| Step | Hardware | Work | Time est. | Cost est. |
| --- | --- | --- | --- | --- |
| 1. Sample 64 candidates per problem, train set (7.5k problems) + test set (1.3k), 0.5B proposer with vLLM | 1× L4 | ≈ 565k samples × ~250 tokens ≈ 140M generated tokens at ~5k tok/s batched | ~8 h | ~$6.5 |
| 2. Fine-tune the 1.5B chooser (LoRA) as a selector on train candidates (16 per problem) with correctness labels | 1× A100-80GB | ≈ 120k sequences × ~300 tokens, 2 epochs | ~2–3 h | ~$5–7.5 |
| 3. Evaluate k = 0..6, unrestricted baseline, scripted and trained adversaries on test | 1× L4 | Scoring 1.3k × 64 candidates plus 1.3k free generations | ~1 h | ~$0.8 |
| CPU/memory overhead, retries, storage | — | — | — | ~$2 |
| **Total** | | | **~12 h** | **~$15–17** (fits in the $30 monthly credit) |

A cheaper variant is to sample 16 instead of 64 candidates in step 1 (kmax = 4): ≈ $2 for step 1, ≈ $10 total.

Optional, to train the architecture from scratch: a 100M-parameter proposer plus chooser pretrained on a small story corpus (~0.5B tokens). That is ≈ 6·N·D ≈ 3×10¹⁷ FLOPs, ≈ 20–30 min on one H100 (≈ $2), plus the same evaluation.

## Controls and stop rules

- Fixed seeds; the public seed is part of the logged input. Log every candidate list, so a receiver can recompute it.
- Hard spend cap set in Modal (budget alert at $10, hard stop at $20). One run per step, no automatic retries.
- Report negative results: if utility at small k stays far below the unrestricted baseline, that is the price of the cap.
- Physical timing is out of scope: fixed work is enforced in code, but GPU timing is not measured as a side channel.
