# Bounded cross-family research batch

Owner approved a **$5 total ceiling** for 12 OpenRouter research calls on 2026-10-24. This is exploratory proposal generation and criticism, not confirmatory steganography measurement, model training or a proof system.

Two model families each propose for both directions, the other family criticizes, and the original family revises: four chains × three calls. Prompts contain a fixed, hashed packet of prior workspace findings and source-reading limits. Models have no browsing or execution tools. Any new citations remain unverified leads until checked independently.

`run_batch.py --prepare` fixes models, provider tags, pricing, corpus hashes and a conservative 12-call reservation estimate without inference. `--run` performs the one authorized batch. It refuses duplicate attempts and automatic retries. Requests/visible outputs/accounting are saved under `results/openrouter-research-01/`; ignored local `.env` supplies the key and never enters a request log. Provider reasoning traces are excluded. Calls have fixed model/provider selection, no fallback, price caps, bounded outputs and two-request concurrency. Unknown costs/errors halt the batch; unresolved attempts retain their reservation. The reservation is a conservative operational estimate, not a formal theorem about provider billing.

Budget arithmetic and state transitions have local fake-client/unit checks. API pricing comes from model-specific endpoint metadata, not guessed token rates. Output cost includes provider-reported reasoning charges. No paid web search, plugins, tool execution or explicit cache writes are requested.

API references, accessed 2026-10-24: [provider routing and price caps](https://openrouter.ai/docs/guides/routing/provider-selection), [usage accounting](https://openrouter.ai/docs/cookbook/administration/usage-accounting), [reasoning token controls](https://openrouter.ai/docs/guides/best-practices/reasoning-tokens). Seed support differs; no deterministic-reproduction claim is made. Model self-agreement is not evidence of correctness or novelty.
