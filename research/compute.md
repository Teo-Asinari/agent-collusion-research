# Compute and expenditure ledger

2026-10-25 finite architecture loop: three local CPU runs, exact enumeration,
formal-gradient attempts, finite weight-search fitting and four Lean checks.
Results in `results/residue-network-01..03/` and `results/residue-verification-01/`;
API/cloud experimental spend USD 0. The B pilot audit reused existing records
with zero API calls; owner then explicitly reaffirmed architecture as EOD focus.

2026-10-25 algebraic primitive exploration: local exact enumeration and numerical/
autograd counterexample checks only (`results/quotient-primitive/`), API/cloud
experimental spend USD 0. No training or new hosted/cloud job launched.

2026-10-25 Modal update: the approved $1 setup/run reservation produced one
usable T4 checkpoint (`results/modal-operator-01-t4/assessment.md`). Four app
attempts occurred, including startup and transport failures and a queued L4
cancellation race. All four are stopped. **Actual combined Modal billing remains
unknown**; the provider invoice has not been independently retrieved. The L4
600-second requested-resource estimate was $0.154248; the T4 equivalent is
$0.119448. These are per-attempt estimates, not actual charges or a dollar cap.
No new hosted-model API requests occurred. No further cloud budget follows.

Recorded per-response charge sum across the six hosted batches: **USD 2.30376687**.
This sums `cost_usd` entries, including the paid empty A response; it is not an
independent invoice reconciliation or a claim that failed calls have known costs.
Concurrent workers shared one key, so account-usage deltas are not summed.

Historical integration note, 2026-10-24 (superseded for Modal by the entry above): both Claude worker histories and their batch ledgers
are now integrated below. Per-response costs are available, but shared-account
snapshots should not be added as independent expenditures. Current local work ran
operator checks, Lean verification, a 64-example CPU chooser evaluation, and a
20-step CPU training smoke test with model API/cloud spend USD 0. First Modal
operation-training plan: `experiments/leak_cap/PLAN.md` (not launched; approximately
$0.154 requested execution resources at the 600-second timeout, with a proposed
$1 reservation including setup). Authentication and explicit estimate approval
remain pending. No actual Modal charge is recorded.

Before the approved batch below, no model inference or cloud compute had been run for this project. Local standard-library scripted feasibility tests have run. Literature browsing and development assistant service costs are outside this experimental ledger.

An OpenRouter credential was supplied by the owner and stored only in the ignored local `.env` with mode 0600. Its value is never recorded in research notes. Initial corrected-credential authentication reported key limit USD 100 and usage USD 0. These are key-level limits, not independent account credit balance. That historical zero-spend status is superseded by the approved completed batch below. The earlier invalid credential was replaced locally. Do not silently treat unknown usage as free.

Before a pilot record model/provider, input/output token estimates, current unit prices and timestamp, calls, retries, maximum output/context, concurrency, and stop condition. Formula: `input_tokens * input_price_per_million / 1e6 + output_tokens * output_price_per_million / 1e6`, plus applicable tool, cache, hosting, and compute costs.

| Run | Status | Estimated USD | Actual USD | Tokens / compute | Notes |
| --- | --- | --- | --- | --- | --- |
| Initial literature work | No inference | — | 0 | 0 | Later credential verification used only the authentication endpoint |
| anti_stego/local-smoke | Scripted feasibility complete | 0 | 0 | 7,680 local records; no model tokens | Eight tests; no API calls |
| openrouter-research-01 | Complete: 12/12 calls | Conservative reservation ceiling 4.822524; authorized cap 5 | **0.601760** | 88,602 prompt + 28,061 completion tokens, provider reported | Per-response costs reconciled with key usage; qualitative proposal/critique/revision, not a stego benchmark |
| component-rewrite-local | Scripted feasibility complete | 0 | 0 | 5,600 local records per carrier set; no model tokens | B worker; `experiments/component_rewrite/local_eval.py` |
| component-rewrite-pilot-01 | Complete: 1,437/1,440 calls (3 HTTP 429) | Worst-case reservation 2.516130; authorized cap 5 | **0.658566** | 1,440 calls; key usage delta 0.653331 (shared key, possible lag) |
| component-rewrite-pilot-02 | Halted: 294/720 attempted, 273 complete (21 HTTP 429) | Worst-case reservation 4.383743; authorized cap 5 | **0.317218** | Key usage delta 0.774441 includes concurrent A-worker spend; not attributable | Owner-approved B batch 2; rerun of 3 re-solving arms | Owner $5-per-batch authorization, B worker; exploratory pilot, preregistered |
| arch-a-batch-01 | Complete: 3 calls (1 empty, length-truncated reasoning) | Hard cap 5; reservation 0.889 | **0.26759225** | 43,227 prompt + 12,055 completion tokens, provider reported | Cross-family critique of formal model (Sonnet 4.6, Gemini 3.1 Pro, GPT-5.2); local z3/numpy work $0. See `results/arch-a-batch-01/critique/` |
| arch-a-batch-02 | Complete: 3/3 calls | Hard cap 5; reservation 1.358 | **0.2218205** | Provider-reported usage in `results/arch-a-batch-02/critique/ledger.json` | Lean-mechanization critique (Sonnet 4.6, Gemini 3.1 Pro, GPT-5.2), 12k output limit, reasoning capped at 3k tokens. Lean toolchain: elan + Lean 4.35.0 under `~/.elan` (3.0 GB), no mathlib |
| arch-a-batch-03 | **Stopped by owner** after 3/3 critique calls (outputs unassessed) | Hard cap 5; reservation 1.384 | **0.23681025** | see `results/arch-a-batch-03/critique/ledger.json` | Multi-agent Lean lift (WIP). Remaining ≈ $4.76 is reassigned by the owner to the leak-capped neural-architecture work |

## Authorized first hosted research batch

Owner explicitly approved one **$5 total cap** for 12 OpenRouter research calls: two model families × two directions × proposal/critique/revision. No continuing inference, full experiment or training budget follows. Status: **complete, $0.601760 actual**; exact execution/accounting is in `results/openrouter-research-01/`.

Read-only authentication succeeded. Pre-batch key usage was $0; post-batch reconciliation reports usage **$0.601760** and key limit remaining **$99.398240**. These are still key-level values, not independent account-balance verification. The full model catalog timed out; targeted endpoint records succeeded. Fixed model/provider pairs: `anthropic/claude-sonnet-4.6` / `anthropic`, $3 input and $15 output per million tokens; `google/gemini-3.1-pro-preview` / `google-ai-studio`, $2 input and $12 output per million. Endpoint snapshots include dated underlying model names and supported parameters. Both completed all six assigned calls.

Runner settings: max 5,000 output tokens per request, low reasoning effort, temperature 0.5, no seed, no tools/plugins, no fallback, pinned providers, price ceilings at snapshot rates, concurrency two, no automatic retries. The operational worst-case reservation for 12 requests is **$4.822524**, using a deliberately generous 95,000-byte prompt ceiling plus framing allowance, doubled output allowance and 5% contingency. This is conservative budgeting, not a formal provider-billing guarantee. Actual responses and account snapshots will provide expenditure evidence. An unknown cost or reservation overrun halts subsequent calls. Six local accounting/bound tests passed without network or credentials.

Source packet and output claims remain research suggestions. Hosted models had no source-retrieval tools; additional citations require independent verification. The primary agent independently rejected several invalid reviewer arguments and unsupported final impossibility claims. No new architecture/sanitizer or novelty was validated. See [assessment](../results/openrouter-research-01/assessment.md) and [runner documentation](../experiments/openrouter_research/README.md). The 12-call authorization is exhausted even though expenditure was below its dollar ceiling; no automatic continuation is implied.

## B worker batch 1 (component-rewrite-pilot-01)

Owner authorized $5-per-batch spending for parallel A/B workers on 2026-10-24; this is the B worker's single batch. Endpoint pricing snapshot 2026-10-24: `openai/gpt-4.1-mini`/openai $0.40 input, $1.60 output per million tokens; `qwen/qwen3-235b-a22b-2507`/deepinfra/fp8 $0.09/$0.55. Max 600 output tokens, temperature 0.7, per-job seed, concurrency 8, no retries or fallback, provider price caps. Reservation = (UTF-8 prompt bytes + 512) × input price + 1,200 × output price, + 5%. Execution details are in `results/component-rewrite-pilot-01/`.
## Approach A batch 1 authorization

Owner approved parallel A/B workers with OpenRouter spend in **$5 hard-cap batches per agent** (2026-10-24). This entry covers exactly one A batch. Reservation must stay within $5 before any call; unknown cost halts. No second batch without owner approval.

Status: **complete, $0.26759225 actual** (Anthropic $0.1368 for an empty reasoning-only response; Google $0.065344; OpenAI $0.06544825). Account usage snapshots before/after are in `results/arch-a-batch-01/critique/`; they may include concurrent Approach B spend on the same key. The A batch is exhausted. Further A spending needs a new owner-approved batch.
