# Exact bilinear network

[Report and scope](../../research/workstreams/architecture/bilinear-network/report.md)
and [pre-execution plan](PLAN.md).

Hidden neurons multiply two learned projections over exact modular integers.
Finite differences and finite-field rank factorization learn both hidden maps
without enumerating model weights. The structured quadratic family is identified
from deliberately selected examples, not iid training data. This is not a novel
primitive or a language model.

```bash
python -m experiments.bilinear_network.run --output results/bilinear-network-repeat
python -m experiments.bilinear_network.verify \
  --results results/bilinear-network-repeat \
  --output results/bilinear-network-repeat/verification.json
```

Requires Python with NumPy and Lean 4.35.0. Set `LEAN_BIN` for a different executable
location. The runner performs training, controls, attacks and three Lean commands.
The verifier independently recomputes scalar predictions and checks provenance
and recorded proof results. It does not repeat compilation. Existing output paths
are never overwritten. No API credentials, external datasets or cloud jobs.
