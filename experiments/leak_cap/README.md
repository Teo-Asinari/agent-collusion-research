# Leak-capped transformer (toy CPU scale)

Design, results and limits: [research/workstreams/architecture/leak-cap.md](../../research/workstreams/architecture/leak-cap.md). Capacity proof: [`../verified_arch/lean/Choice.lean`](../verified_arch/lean/Choice.lean). Larger-run plan (not executed): [MODAL_PLAN.md](MODAL_PLAN.md).

```bash
python3 leakcap.py train   # CPU, PyTorch; writes results/leak-cap-01/{proposer,chooser}.pt, train.json
python3 leakcap.py eval    # writes results/leak-cap-01/eval.json
~/.elan/bin/lean ../verified_arch/lean/Choice.lean
```

Data: `data/google-10000-english-no-swears.txt` from [first20hours/google-10000-english](https://github.com/first20hours/google-10000-english), fetched 2026-10-24. It is derived from the Google Web Trillion Word Corpus; the repository README permits research use (LDC license, Norvig MIT for his contributions).
