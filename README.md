# AI Agent Collusion Research

Private exploratory research workspace for the Apart Research AI Collusion Research Sprint, October 23–25, 2026.

**Status: no research question or experiment selected.** Compare alternatives before implementation. No inference expenditure has been incurred by this workspace.

- [Research brief](research/brief.md): enduring context and constraints.
- [Literature](research/literature.md): source-verified claims, assumptions, and limitations.
- [Shared-knowledge assumptions](research/shared-knowledge.md): which approaches require pre-shared secrets, and which do not.
- [Starter inventory](research/starter-map.md): external code and research-track mapping.
- [Questions](research/questions.md): unresolved conceptual and empirical questions.
- [Candidates](research/ideas.md): hypotheses, designs, controls, feasibility, and negative results.
- [Decisions](research/decisions.md): explicit choices and their rationale.
- [Compute ledger](research/compute.md): proposed budgets and actual spending.

`experiments/` is reserved for selected experiments; `results/` for documented outputs; `references/` for source provenance. There is no experiment implementation yet.

## External starting points

- [Official sprint](https://apartresearch.com/sprints/ai-collusion-research-sprint-2026-10-23-to-2026-10-25)
- [Official starter repository](https://github.com/poseidon-research/collusion_hackathon)

The starter is an external reference, not a dependency or fork. Incorporate code selectively only after checking attribution and licenses. This repository must remain private unless the owner explicitly approves a visibility change.

## Secrets and compute

Copy `.env.example` to `.env` only when an experiment needs it. Never commit secrets or `compute.env`. Prefer local orchestration with hosted APIs; use Modal/GPUs only when justified by the selected question. Check model availability and pricing before any run. Record estimated and actual usage.
