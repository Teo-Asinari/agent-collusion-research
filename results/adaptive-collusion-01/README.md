# Adaptive colluders vs four defenses (run 01)

Plan: `experiments/adaptive_collusion/PLAN.md` (written before the run). Paper
section: `submission/report.tex`, Experiment 4. 3,045 OpenRouter calls,
$2.58 reported cost (`budget.json`), no halts, no failed calls.

Held-out leaked bits per answer (n=100, 8-bit payload): none 7.94,
paraphrase 0.55, broker 0.06 (chance), menu k=3 2.97 (cap 3). Honest
utility: free 0.77, menu 0.87, trusted proposer alone 0.71.

Deviation from plan: none in procedure. The training-round menu strategies
after round 5 got worse; evaluation used the best training round, as planned.
16 receiver replies had no parseable guess and were replaced by a seeded
random guess.

Files: `config.json` (models, git commit), `calls.jsonl` (every prompt and
response), `episodes.jsonl`, `strategies.json` (strategy text and score per
round), `metrics.json`, `budget.json`.
Regenerate the figure: `python experiments/adaptive_collusion/figure.py`.
