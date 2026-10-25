# Exact residue-network experiment

[Plain-English report and proof scope](../../research/workstreams/architecture/residue-network/report.md).
CPU-only finite polynomial network. Internal arithmetic is modulo 9; the
declared observer sees remainders modulo 3. Both hidden and output weights learn.

```bash
python -m experiments.residue_network.run_loop \
  --hidden-units 1 --output results/residue-network-repeat
python -m experiments.residue_network.verify_results \
  --output results/residue-verification-repeat
```

The loop refuses output overwrites. `verify_results` checks the saved rounds,
source hashes, gradient-state agreement and Lean certificates; its chosen
result directory must not already exist. Lean 4.35.0 is currently installed at
`/home/tasinari/.elan/bin/lean`. PyTorch is used only for bounded int64 enumeration,
not floating-point training. Finite search fits all sixteen truth tables; the
formal-gradient attempts do not. No held-out generalization, scalable training,
physical isolation or established originality is claimed.
