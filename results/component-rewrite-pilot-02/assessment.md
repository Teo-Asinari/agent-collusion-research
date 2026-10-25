# Assessment: component-label rewrite pilot 02

2026-10-24. **Exploratory; the run halted early.** This is the owner-approved $5 batch 2 for the B worker. The preregistration addendum is in [component-pilot-prereg.md](../../research/workstreams/task-preserving-rewrite/component-pilot-prereg.md) (commit before the run).

## Execution

- **Halted as designed after 21 failures**, all HTTP 429 rate-limit errors from qwen on deepinfra/fp8; the failure limit is 20. 294 of 720 calls were attempted and 273 completed. No retries or restart; the remaining 426 calls were not sent.
- **Reported cost $0.31721780.** Key usage rose $0.77444070 over the same window. The key is shared with the concurrently running A worker, so the delta is not attributable to this run.
- Jobs ran in task order, so only tasks 0–48 were reached, all from the training split. **No held-out test task ran, so the preregistered fitted-receiver analysis is empty.** `summary.json` is uninformative (identical rows) and must not be cited.
- Only 25 completed calls hit the 2,500-token limit, against 98–119 per arm in pilot 01. The truncation fix worked.

## Salvaged analysis (deviation: direct decoder on tasks 0–48)

`posthoc.py component-rewrite-pilot-02` → `posthoc-valid-only.json`. The direct decoder (bit = anchor in Room A) is fixed by the encoding rule and has no fitted parameters. Evaluating it on training-split tasks therefore does not overfit, but this was not the preregistered primary analysis. n = 49 tasks per arm; task-level bootstrap 95% CIs. Validity counts the 429 failures as invalid.

| Arm | gpt-4.1-mini validity | gpt acc among valid | gpt unchanged from draft | qwen3-235b validity | qwen acc among valid | qwen unchanged |
| --- | --- | --- | --- | --- | --- | --- |
| instructed_sender | 0.96 | 1.00 (n=47) | — | 0.90 | 1.00 (n=44) | — |
| tc_sanitize | 1.00 | **0.73 [0.64, 0.81]** (n=49) | 0.41 | 0.67 | 0.61 [0.52, 0.71] (n=33) | 0.24 |
| resolve (task only) | 1.00 | 0.54 [0.47, 0.61] (n=49) | 0.08 | 0.76 | 0.54 [0.47, 0.61] (n=37) | 0.08 |

"Unchanged" for resolve is about 0.08, close to the 1/16 = 0.0625 expected by chance.

Hypotheses (on this partial sample): **H5** is supported for gpt-4.1-mini and fails qwen's validity threshold (0.76 < 0.8, partly because of the 429s); resolve accuracy CIs include 0.5 for both. **H6 is supported for gpt-4.1-mini:** at full validity, the "choose independently of the draft" sanitizer still recovers 0.73 and copies the draft exactly 41% of the time. For qwen the lower bound is only 0.52, so this is weak. **H7 is supported:** under instruction both models encode exactly when valid, with 0.90–0.96 validity.

## Interpretation

- Removing truncation removes the validity confound for gpt-4.1-mini. With matched, perfect validity, task-only resolve sits at chance, while an explicitly warned task-conditioned rewriter still leaks about a quarter of the excess over chance on each bit. Pilot 01's conclusion survives: giving the defender the draft lets the payload through, even with a direct instruction not to use it.
- Erasure is cheap here: resolve costs about the same per call as sanitize (gpt about $0.0014 each) and reaches chance. The useful defender lesson for this task family is not to show the draft to the re-solver, rather than any hardness result.
- Limits: one toy task, two models, one prompt wording, a scripted sender, a partial sample from the training split only, a deviated analysis, and n=49.

## Next batch (proposed, not authorized)

Complete the remaining held-out tasks 49–119 for the same 3 arms: 426 calls. Run qwen at concurrency 2 or switch it to a provider without rate limits, keep the 20-failure halt, and interleave tasks so a halt does not drop the whole test split. The reported cost of this run implies about $0.5 actual; the worst-case reservation is about $2.6.
