# Assessment: Approach A batch-2 critique of the Lean mechanization

2026-10-25 UTC (2026-10-24 local). Three calls, one per family, with a 12,000-token output limit. Reasoning was capped at 3,000 tokens for Anthropic and Google (`reasoning.max_tokens`); OpenAI used low effort. All three finished normally (`stop`). **Actual reported cost $0.2218205** (Sonnet 4.6 $0.082719, Gemini 3.1 Pro $0.075636, GPT-5.2 $0.0634655) against a $1.358 reservation and the $5 cap. No retries.

Packet: formal-model.md (with §2a), `lean/Arch.lean` as it stood before the concrete instance was added, and programs.py. 39,092 bytes; SHA-256 in `plan.json`.

All three verdicts: **faithful-with-caveats**. None found a soundness error or a vacuous hypothesis. Two independently confirmed that `payload_ni` genuinely quantifies over all weights and is satisfiable.

| Objection | Source | Verdict | Action |
| --- | --- | --- | --- |
| Release `impl` is a Lean function, not a sub-program, so internal-wire isolation holds by construction rather than by proof | Gemini (high), Sonnet (caveat) | Valid as a scope point; not a soundness gap. A sub-program run in a local scope *is* such a function, and the theorem holds for every impl satisfying its contract. The Python IR shares the environment but labels internal wires private. | Added `localImpl`; doc states that isolation is semantic (local scope), not a typing result. |
| Witness contract proved for a Lean function, not for the IR node graph in programs.py | Gemini (high) | Valid. The node graph was z3-checked for N≤8 only. | Added a concrete Lean instance (`witnessProg`) whose release *is* the witness cell with the learned predictor via `ι`. Proved its contract, its well-typedness, and `witnessProg_payload_ni`. The node-graph correspondence remains unmechanized; this is stated. |
| Weight is not a separate field, so "weights join into the label" is not enforced | GPT-5.2 (high) | **Rejected as a soundness gap.** In the Lean semantics `ι` sees only `args.map ρ`, so an op *cannot* depend on a wire that is not an arg, and every arg is joined. A hidden weight dependence is unrepresentable, not unlabeled. Faithfulness of the model to a real system is a modeling obligation that applies to every arg equally. | Doc clarification only. |
| `ni_compose` is sequential composition, not multi-session histories | Sonnet, Gemini, GPT | Partly valid. Sessions with fresh inputs fit by giving each session its own wires in one κ, which is unrolling. **Adaptive** receiver queries (later public inputs chosen from earlier outputs) are not modeled, and neither is a label-preserving linker. | Doc narrowed to "non-adaptive unrolled sessions". |
| Composition relies on (R1) reading only initial inputs | Gemini (medium) | Correct observation, not a bug. | Noted. |
| "Public iff" wording vs Lean rejecting bad releases | GPT-5.2 | Phrasing. | Doc now says releases are admitted only if (R1) and (R2) hold. |
| 0- vs 1-indexing, out-of-range j | Sonnet, GPT | Harmless: the Lean contract holds for every j, including out of range. | None. |

These are model reviews, not proof checks; the proofs are checked by Lean. The critiques were useful mainly for scoping the claims.
