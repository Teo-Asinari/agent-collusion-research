# AI Agent Collusion Research

Private exploratory research workspace for the Apart Research AI Collusion Research Sprint, October 23–25, 2026.

**Status: no full hackathon study selected.** At the owner's request, a local scripted [anti-steganography prototype](experiments/anti_stego/README.md) now tests task-aware release protocols and an explicit surviving semantic channel. No model inference expenditure has been incurred.

**Current research agenda:** develop two approaches in parallel—[a ground-up learned/verified architecture and task-preserving steganography removal](research/two-approach-agenda.md). Specific theorem, task, full experiment and inference budget remain unselected.

First delegated research passes are complete: [architecture proposal](research/workstreams/architecture/proposal.md) and [task-preserving reconstruction proposal](research/workstreams/task-preserving-rewrite/proposal.md). Both record limitations and source-reading scope; neither establishes novelty or a general security theorem.

[Adversarial review outcome](research/reviews/outcome.md): two review/revision rounds sharpened both restricted mechanisms and their failure models. Useful efficiency, generality and novelty remain open.

- [Research brief](research/brief.md): enduring context and constraints.
- [Literature](research/literature.md): source-verified claims, assumptions, and limitations.
- [Shared-knowledge assumptions](research/shared-knowledge.md): which approaches require pre-shared secrets, and which do not.
- [Keyless construction](research/keyless-construction.md): assumptions and practical questions.
- [Active defenses](research/anti-steganography.md): prototype, literature context and verified cache-timing report.
- [Mathematical directions](research/mathematical-directions.md): equivalence classes, invariants, information flow and complexity.
- [iMEC reference check](research/imec-reference.md): concrete upstream encoder/decoder and a minimal executed round trip.
- [Synchronization](research/synchronization.md): probability calculation versus sampling, practical mismatch, and alternative secure schemes.
- [Secure steganography prior art](research/stego-prior-art.md): expanded primary-source comparison, code findings, active wardens and robustness.
- [Practical-barrier candidates](research/practical-barrier-candidates.md): revised falsifiable questions, controls, costs and novelty limits.
- [Semantic-choice channels and erasure cost](research/semantic-erasure.md): substantive task choices, replacement capability, mixing barriers and cryptographic counterexamples.
- [Novelty audit](research/novelty-audit.md): closer predecessors and explicit reasons the broad solution-choice/erasure-cost proposal is not yet a novel project.
- [Isolation and mediation](research/isolation-and-mediation.md): hardware/physical channels, robots and collusion-free interaction protocols, with explicit guarantee boundaries.
- [Starter inventory](research/starter-map.md): external code and research-track mapping.
- [Questions](research/questions.md): unresolved conceptual and empirical questions.
- [Candidates](research/ideas.md): hypotheses, designs, controls, feasibility, and negative results.
- [Decisions](research/decisions.md): explicit choices and their rationale.
- [Compute ledger](research/compute.md): proposed budgets and actual spending.

`experiments/` contains scoped feasibility work; `results/` holds documented outputs; `references/` records source provenance. The first prototype is scripted and does not evaluate autonomous collusion.

## External starting points

- [Official sprint](https://apartresearch.com/sprints/ai-collusion-research-sprint-2026-10-23-to-2026-10-25)
- [Official starter repository](https://github.com/poseidon-research/collusion_hackathon)

The starter is an external reference, not a dependency or fork. Incorporate code selectively only after checking attribution and licenses. This repository must remain private unless the owner explicitly approves a visibility change.

## Secrets and compute

Copy `.env.example` to `.env` only when an experiment needs it. Never commit secrets or `compute.env`. Prefer local orchestration with hosted APIs; use Modal/GPUs only when justified by the selected question. Check model availability and pricing before any run. Record estimated and actual usage.
