# Compute and expenditure ledger

No model inference or cloud compute has been run for this project. Actual experiment spend: **$0**. Literature browsing and development assistant service costs are outside this experimental ledger.

An OpenRouter credential was supplied by the owner and stored only in the ignored local `.env` with mode 0600. Its value is never recorded in research notes. Corrected credential authenticated on 2026-10-24 via OpenRouter’s `/api/v1/auth/key` endpoint: HTTP 200. Endpoint reports key limit USD 100, limit remaining USD 100, usage USD 0, and no expiration. These are key-level limits, not independent verification of account credit balance or model availability. The earlier credential returned HTTP 401 and has been replaced locally. No inference request was made; model prices remain unverified. No budget ceiling has been selected. Do not silently treat unknown usage as free.

Before a pilot record model/provider, input/output token estimates, current unit prices and timestamp, calls, retries, maximum output/context, concurrency, and stop condition. Formula: `input_tokens * input_price_per_million / 1e6 + output_tokens * output_price_per_million / 1e6`, plus applicable tool, cache, hosting, and compute costs.

| Run | Status | Estimated USD | Actual USD | Tokens / compute | Notes |
| --- | --- | --- | --- | --- | --- |
| None | No experiment selected | — | 0 | 0 | No provider credentials accessed |
