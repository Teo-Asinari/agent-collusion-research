# Neural operation and finite-choice feasibility

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

Requires the already installed PyTorch. Output refuses overwrites; choose a new
path to repeat. Checkpoints and external corpus are referenced in place: this is
not yet a portable artifact. Corpus redistribution permissions need review before
vendoring. Evaluation resamples corruptions of training words. The new operation
block has not been trained. Lean covers an abstract content channel, not a proof
of Python refinement or timing isolation. No cloud or model API calls are used.
