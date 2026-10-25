# Assessment: Approach A batch-1 critique calls

2026-10-25 UTC (2026-10-24 local). Three calls, one per family, single stage, no revision. **Actual reported cost $0.26759225** of the $5 batch cap (reservation $0.889). No retries.

| Call | Model / provider | Tokens (prompt / completion) | Cost USD | Outcome |
| --- | --- | --- | --- | --- |
| critique-anthropic | claude-sonnet-4.6 / Anthropic | 15,600 / 6,000 (all reasoning) | 0.1368 | `finish_reason=length`, **no visible text**. Low reasoning effort was requested; the provider still consumed the full output budget on reasoning. Wasted spend; ledger halted as designed. Not retried. |
| critique-google | gemini-3.1-pro-preview / Google AI Studio | 14,684 / 2,998 | 0.065344 | sound-with-repairs |
| critique-openai | gpt-5.2 / OpenAI | 12,943 / 3,057 | 0.06544825 | sound-with-repairs |

Packet: `packet.md` (formal-model.md, ir.py, programs.py, learned_task.py, prove.json excerpt; 46,216 bytes; SHA-256 in `plan.json`). Exact requests, visible responses and the ledger are in this directory.

## Objection dispositions (independently checked)

| Objection | Source | Verdict | Action |
| --- | --- | --- | --- |
| `secondary` not joined unless also in `args`; a `secondary`-only private wire yields a public label | GPT-5.2 (high) | **Valid mismatch, not an exploit.** `run` and z3 ignore `secondary`, so semantics and labels agreed; the document's wording overstated the field. | `ir.check` now rejects `secondary ⊄ args`; doc clarified. |
| `impl_out` may name a wire defined outside `impl` | Gemini | Valid hygiene issue. Not an exploit: the contract is semantic, so a wrong outside wire fails the z3 contract. | Enforced: `impl_out` and `cost` must be defined inside `impl`. |
| Contract keyed by names could be reused in a program where the read wires mean something else | Gemini (low) | Partially valid. Keys include spec args and impl text, but contracts were proved inside the original program. A proof is portable only if all external reads were free. | Contracts are now proved in an isolated context (every external read free). Results unchanged. |
| Lemma 2 is not enforced by tooling; re-importing private values as public inputs launders them | GPT-5.2 (medium) | Valid. Lemma 2 is a meta-level statement about linking. | Caveat added; a label-preserving linker is future work. |
| Capacity bound overgeneralized | both | Gemini correct: the bound needs a single global radius. GPT's claim that per-query cost vectors multiply capacity is **false for the implemented global-radius padding** (all per-query costs are equal), but true for per-leaf radii. | Scope sentence added. |
| Value/visible-work split is standard constant-time practice | Gemini (medium) | Accepted. | Downgraded to an application of the standard principle; the remaining combination is stated as a hypothesis needing a literature search. |
| mask_only ablation not diagnostic because `secondary` has no semantics | GPT-5.2 | Partly valid. The ablation models a checker that ignores some real args, which is how a mask-only analysis fails. It does not model the mechanics of attention. | Wording clarified. |

Neither critic produced a well-typed counterexample to Theorem 1. That is weak evidence: these were model reviews, not proof checks. No critic claim was adopted without the checks above. After the repairs, all z3 sections, the 5,000-program fuzz and the learned task were rerun with identical numbers.
