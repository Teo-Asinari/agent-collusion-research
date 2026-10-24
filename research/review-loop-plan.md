# Adversarial review and improvement loop

2026-10-24. Owner authorized an adversarial review/improvement loop incorporating prior art for both active approaches. Initial scope: two independent review rounds, with an author revision after each. This does not select a full experiment or authorize inference/training expenditure.

Baseline proposals are preserved in commit `611ed7a`; author revisions should identify concrete changes against that baseline and the review that prompted them.

- [x] Round 1: independent reviewer audits both proposals for counterexamples, specification loopholes, usefulness, and closest primary prior art; writes `reviews/round-1.md`.
- [x] Architecture author resolves or explicitly defers round-1 objections, revises proposal/source ledger and writes `workstreams/architecture/revision-1.md`.
- [x] Rewrite author resolves or explicitly defers round-1 objections, revises proposal/source ledger and writes `workstreams/task-preserving-rewrite/revision-1.md`.
- [x] Round 2: reviewer checks the revisions against original objections, challenges new claims and writes `reviews/round-2.md`.
- [x] Both authors make final bounded revisions and write `revision-2.md` in their respective directories.
- [x] Primary agent inspects the final artifacts, records unresolved issues and evidence limits, validates changes and saves the results privately. See `reviews/outcome.md`; source/claim checks, relative links, Python syntax, JSON/count consistency and whitespace checks passed. Repository privacy verified before committing.

Review standard: distinguish fatal counterexamples, scope defects, missing proof obligations, unsupported novelty and optional extensions. Cite exact assumptions and primary-source sections when accessible. A revision must not silently weaken the user's ground-up architecture objective or replace task preservation with frozen-decoder failure. Rejection or narrowing is an acceptable scientific result. No requirement that either proposal emerge novel or successful.

Ownership: reviewer edits `research/reviews/` only; each author edits its own workstream only; primary agent owns shared indexes and this plan. Workers do not commit/push or spawn additional agents. No secret access, paid inference, dependency installation, GPU/cloud deployment or full benchmark. Small standard-library counterexample checks are permitted and must be labeled as such.
