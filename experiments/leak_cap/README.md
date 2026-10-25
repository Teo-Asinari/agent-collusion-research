# Neural operation and finite-choice feasibility

New exploratory algebraic candidate: [quotient polynomial neuron](../../research/workstreams/architecture/quotient-primitive.md).
Run `python -m experiments.leak_cap.quotient_primitive --output /tmp/quotient-check.json`
for exact finite-field checks and numerical/training counterexamples. This is not
an established novel primitive or secure float implementation; no training/cloud
run is part of that check.

See [equations and claim boundaries](../../research/workstreams/architecture/operator-and-choice.md).
`operators.py` implements separate public/private attention and a finite gate.
`leakcap.py` preserves the Claude worker's trained generator/chooser baseline.

```bash
python -m unittest experiments.leak_cap.test_operators -v
/home/tasinari/.elan/bin/lean experiments/leak_cap/lean/Choice.lean
python experiments/leak_cap/leakcap.py eval \
  --checkpoint-dir .claude/worktrees/agent-ad39c5a2861e07835/results/leak-cap-01 \
  --data .claude/worktrees/agent-ad39c5a2861e07835/experiments/leak_cap/data/google-10000-english-no-swears.txt \
  --n-test 64 --kmax 4 --output results/leak-cap-recovery/smoke.json
```

Requires PyTorch. Output refuses overwrites; choose a new path to repeat. The
merged worker checkpoints and corpus are also available under `results/leak-cap-01`
and `experiments/leak_cap/data`. Use `--proposer prop2 --kmax 8` for its larger
proposer. Evaluation resamples corruptions of training words. Lean covers an
abstract content channel, not Python refinement or timing isolation.

The corpus was supplied by the A worker from first20hours/google-10000-english.
Its upstream README describes provenance but does not itself contain the blanket
research-use license claimed by the worker's original README. Redistribution
terms remain incompletely reviewed; do not infer a common upstream code license.

Operation training: [plan and execution contract](PLAN.md),
[completed Modal assessment](../../results/modal-operator-01-t4/assessment.md).
A 20-step local smoke run and a usable 1,000-step T4 run completed. The synthetic
task uses no external corpus. The Modal launcher now returns plain JSON plus
checkpoint bytes, records the spawned call ID and bounds the whole wait at 600
seconds. The successful run does not establish a private-computation advantage.
