# Adaptive colluders, scaled (runs 03a-e)

Plan: `experiments/adaptive_collusion/PLAN.md` (scale-up and relaunch sections,
written before launch). Paper: `submission/report.tex`, Experiment 4.
Five independent runs (`--run-seed 1..5`), 12 rounds x 40 training episodes,
300 held-out and 300 honest episodes per condition. 75,813 calls, $56.87
provider-reported cost, no budget halts, no empty responses.

Mean held-out leaked bits (range over runs): none 5.09 (1.31-7.04),
paraphrase 0.32 (0.04-1.01), broker 0.84 (0.03-2.33),
menu k=1..5: 0.97, 1.87, 2.89, 3.65, 4.51 (cap k).
Honest utility: free 0.79, menu k=1..5: 0.75, 0.81, 0.86, 0.90, 0.91,
trusted proposer alone 0.70.

Aggregate and figure: `python experiments/adaptive_collusion/aggregate.py
results/adaptive-collusion-03a ... results/adaptive-collusion-03e` writes
`results/adaptive-collusion-03-summary.json` and `submission/adaptive_scale.pdf`.
Runs 02a-c crashed mid-training (uncaught socket timeout) and are excluded.
