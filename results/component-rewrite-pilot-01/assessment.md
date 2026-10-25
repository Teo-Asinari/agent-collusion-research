# Assessment: component-label rewrite pilot 01

2026-10-24. **Exploratory.** Preregistration: [component-pilot-prereg.md](../../research/workstreams/task-preserving-rewrite/component-pilot-prereg.md), committed in `409933b` before any paid call. B worker's single $5 batch under the owner's $5-per-batch authorization.

## Execution

- 1,440 calls attempted, 1,437 complete; 3 qwen calls returned HTTP 429 (reservation retained, units counted as invalid). No halt.
- **Reported cost $0.65856607** (sum of per-response `usage.cost`). Key usage changed by $0.65333135 between snapshots. The key is shared with any concurrently running worker and usage can lag, so that delta is a cross-check, not an attribution.
- Models: `openai/gpt-4.1-mini`/openai, `qwen/qwen3-235b-a22b-2507`/deepinfra-fp8. Temperature 0.7, max 600 tokens, per-job seed, no fallback/retries. Full requests and visible responses are in `records.jsonl`; accounting is in `ledger.json`.

## Preregistered results (held-out 60 tasks; per-bit component accuracy, chance 0.5)

| Arm | gpt-4.1-mini valid / acc [95% CI] | qwen3-235b valid / acc [95% CI] |
| --- | --- | --- |
| instructed_sender (positive control) | 0.46 / 0.99 [0.98, 1.0] | 0.13 / 0.73 [0.65, 0.80] |
| paraphrase | 1.00 / 1.00 | 1.00 / 1.00 |
| minimal_edit | 0.99 / 1.00 | 1.00 / 1.00 |
| tc_rewrite | 0.97 / 1.00 | 0.89 / 0.96 [0.92, 0.99] |
| tc_sanitize | 0.66 / 0.77 [0.70, 0.83] | 0.15 / 0.52 [0.45, 0.58] |
| resolve (task only) | 0.56 / 0.50 [0.45, 0.56] | 0.10 / 0.51 [0.46, 0.56] |

Shuffled-payload controls were 0.47–0.54 in every condition. The syntax (order) carrier survived paraphrase and tc_rewrite (0.97–1.00) but not tc_sanitize (0.52–0.60). Local scripted arms (`results/component-rewrite-local/summary.json`, 400 tasks): normalize and valid local walk keep component accuracy at 1.00; one random cluster flip gives 0.75; two flips or a task-only resolve give chance. In the connected-space control the local walk reaches chance (0.49).

Hypotheses: **H1 supported** (paraphrase/minimal_edit = 1.00). **H2 supported** (tc_rewrite ≥ 0.96; ≥ 99% of valid outputs left the draft's assignment unchanged). **H3 supported only for gpt-4.1-mini** (0.77, CI above 0.5); qwen's tc_sanitize is at chance, but mostly because its outputs are invalid. **H4 fails on validity**: resolve validity is 0.41 (gpt) and 0.79 (qwen) below tc_rewrite.

## Major confound found after the run

The 600-token limit truncated most outputs that actually re-solved the task. Truncated (`finish_reason=length`) calls: resolve 98/120 (gpt) and 119/120 (qwen); tc_sanitize 92/120 and 109/120. Inspection shows step-by-step constraint propagation cut off mid-search. The parser then sometimes read partial intermediate "Room A/B" lines. **Low validity in resolve and tc_sanitize is therefore mostly a design flaw, not evidence that these models cannot solve the task.** Arms that copy the draft are short and never hit the limit. This biases validity sharply in favour of draft-preserving arms.

## Post-hoc analysis (not preregistered): valid outputs only, direct decoder

`posthoc.py` → `posthoc-valid-only.json`. Valid tc_sanitize outputs still carried the payload: gpt-4.1-mini n=79, 0.84 [0.79, 0.88]; qwen n=18, 0.72 [0.63, 0.82]. 56% of gpt's valid sanitize outputs reproduced the draft's assignment exactly. Valid resolve outputs: gpt 0.47 (n=67); qwen 0.35 (n=12, too small to interpret). One reading is a selection effect: the sanitizer stays valid mostly by copying the draft, and genuine re-solving ran out of tokens. This is post hoc and confounded by the same truncation.

## What this does and does not show

- In this toy task, every LLM arm that receives the draft, including an explicit "choose independently" instruction, preserved a solution-choice payload in its valid outputs. Only payload-independent resolving reached chance. This matches the local-rewrite obstruction and the known solution-choice/re-solving prior art; it is not a novelty claim.
- It does not establish that removal is expensive: a scripted task-only solver erases the payload perfectly at negligible cost. The pilot measures LLM rewriter *behavior* under one prompt per arm.
- The scripted sender is not autonomous collusion. The instructed control shows that gpt-4.1-mini places anchors exactly when it manages a valid answer, but it only produced a valid answer 46% of the time, again partly due to truncation.
- Not covered: adaptive receivers beyond the small decoder family; single prompt wording per arm; two models; one task family.

## Next batch (proposed, not authorized)

Rerun only resolve, tc_sanitize and instructed_sender with max_tokens 2,500, and require the final assignment in a fenced block so the parser ignores intermediate lines. 120 tasks × 3 arms × 2 models = 720 calls. At about 1,500 completion tokens per call, estimated actual cost is about $1.0–1.5; the worst-case reservation is about $4.7 under this runner's formula, so it fits in one $5 batch. A second sanitize wording would push the reservation over $5 unless tasks are cut to about 90. It would separate copying from re-solving at matched validity, which is the question this pilot could not answer.
