# Compute and expenditure ledger

Before the approved batch below, no model inference or cloud compute had been run for this project. Local standard-library scripted feasibility tests have run. Literature browsing and development assistant service costs are outside this experimental ledger.

An OpenRouter credential was supplied by the owner and stored only in the ignored local `.env` with mode 0600. Its value is never recorded in research notes. Initial corrected-credential authentication reported key limit USD 100 and usage USD 0. These are key-level limits, not independent account credit balance. That historical zero-spend status is superseded by the approved completed batch below. The earlier invalid credential was replaced locally. Do not silently treat unknown usage as free.

Before a pilot record model/provider, input/output token estimates, current unit prices and timestamp, calls, retries, maximum output/context, concurrency, and stop condition. Formula: `input_tokens * input_price_per_million / 1e6 + output_tokens * output_price_per_million / 1e6`, plus applicable tool, cache, hosting, and compute costs.

| Run | Status | Estimated USD | Actual USD | Tokens / compute | Notes |
| --- | --- | --- | --- | --- | --- |
| Initial literature work | No inference | — | 0 | 0 | Later credential verification used only the authentication endpoint |
| anti_stego/local-smoke | Scripted feasibility complete | 0 | 0 | 7,680 local records; no model tokens | Eight tests; no API calls |
| openrouter-research-01 | Complete: 12/12 calls | Conservative reservation ceiling 4.822524; authorized cap 5 | **0.601760** | 88,602 prompt + 28,061 completion tokens, provider reported | Per-response costs reconciled with key usage; qualitative proposal/critique/revision, not a stego benchmark |
| component-rewrite-local | Scripted feasibility complete | 0 | 0 | 5,600 local records per carrier set; no model tokens | B worker; `experiments/component_rewrite/local_eval.py` |
| component-rewrite-pilot-01 | Authorized, prepared | Worst-case reservation 2.516130; authorized cap 5 | pending | 1,440 planned calls | Owner $5-per-batch authorization, B worker; exploratory pilot, preregistered |

## Authorized first hosted research batch

Owner explicitly approved one **$5 total cap** for 12 OpenRouter research calls: two model families × two directions × proposal/critique/revision. No continuing inference, full experiment or training budget follows. Status: **complete, $0.601760 actual**; exact execution/accounting is in `results/openrouter-research-01/`.

Read-only authentication succeeded. Pre-batch key usage was $0; post-batch reconciliation reports usage **$0.601760** and key limit remaining **$99.398240**. These are still key-level values, not independent account-balance verification. The full model catalog timed out; targeted endpoint records succeeded. Fixed model/provider pairs: `anthropic/claude-sonnet-4.6` / `anthropic`, $3 input and $15 output per million tokens; `google/gemini-3.1-pro-preview` / `google-ai-studio`, $2 input and $12 output per million. Endpoint snapshots include dated underlying model names and supported parameters. Both completed all six assigned calls.

Runner settings: max 5,000 output tokens per request, low reasoning effort, temperature 0.5, no seed, no tools/plugins, no fallback, pinned providers, price ceilings at snapshot rates, concurrency two, no automatic retries. The operational worst-case reservation for 12 requests is **$4.822524**, using a deliberately generous 95,000-byte prompt ceiling plus framing allowance, doubled output allowance and 5% contingency. This is conservative budgeting, not a formal provider-billing guarantee. Actual responses and account snapshots will provide expenditure evidence. An unknown cost or reservation overrun halts subsequent calls. Six local accounting/bound tests passed without network or credentials.

Source packet and output claims remain research suggestions. Hosted models had no source-retrieval tools; additional citations require independent verification. The primary agent independently rejected several invalid reviewer arguments and unsupported final impossibility claims. No new architecture/sanitizer or novelty was validated. See [assessment](../results/openrouter-research-01/assessment.md) and [runner documentation](../experiments/openrouter_research/README.md). The 12-call authorization is exhausted even though expenditure was below its dollar ceiling; no automatic continuation is implied.

## B worker batch 1 (component-rewrite-pilot-01)

Owner authorized $5-per-batch spending for parallel A/B workers on 2026-10-24; this is the B worker's single batch. Endpoint pricing snapshot 2026-10-24: `openai/gpt-4.1-mini`/openai $0.40 input, $1.60 output per million tokens; `qwen/qwen3-235b-a22b-2507`/deepinfra/fp8 $0.09/$0.55. Max 600 output tokens, temperature 0.7, per-job seed, concurrency 8, no retries or fallback, provider price caps. Reservation = (UTF-8 prompt bytes + 512) × input price + 1,200 × output price, + 5%. Execution details are in `results/component-rewrite-pilot-01/`.
