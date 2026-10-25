# Labeled learned/verified dataflow (Approach A, batch 1)

Formal model, theorem, proofs and limits: [formal-model.md](../../research/workstreams/architecture/formal-model.md). Outputs: `results/arch-a-batch-01/`.

| File | Purpose |
| --- | --- |
| `ir.py` | IR, full type checker with five single-invariant ablation flags, concrete interpreter |
| `programs.py` | Witness-cell architecture and one program per ablation |
| `prove.py` | z3 checks over every interpretation of the opaque functions: release contracts, whole-program noninterference, payload-only counterexamples, certified learned-index contract, one-sweep shortest-path counterexample, random-program fuzzing |
| `learned_task.py` | Certified learned-index membership task: utility, value/timing payload channels, padding defenses, paired exact checks |
| `test_verified_arch.py` | Fast regression checks |
| `critique_batch.py` | Bounded OpenRouter critique runner (batch 1 complete; do not rerun) |

## Reproduce

```bash
python3 -m venv /tmp/z3venv && /tmp/z3venv/bin/pip install z3-solver numpy scipy   # z3 5.3.1 used
cd experiments/verified_arch
/tmp/z3venv/bin/python prove.py            # ~2 min; sections: witness learned_index shortest_path fuzz
python3 learned_task.py                    # numpy + scipy; ~3 s
/tmp/z3venv/bin/python test_verified_arch.py
```

All scripts are deterministic (fixed seeds) and need no network or credentials, except `critique_batch.py`.

## Lean mechanization (batch 2)

`lean/Arch.lean`: Theorem 1, payload corollary, composition lemma, witness contract for all N, and a concrete well-typed witness architecture. Core Lean 4.35.0, no mathlib, no `sorry`.

```bash
curl -sSfL https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh | sh -s -- -y --default-toolchain stable --no-modify-path   # ~3 GB under ~/.elan
~/.elan/bin/lean experiments/verified_arch/lean/Arch.lean   # silent on success, ~1 s
```

`critique_batch.py --batch 2` produced `results/arch-a-batch-02/critique/` (complete; do not rerun).
