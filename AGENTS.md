# Research collaboration instructions

- Latest owner direction (2026-10-25): explicitly insists on a neural architecture
  with proof on a small set by EOD and intelligent design iteration; rejects the
  proposed pivot to rewriting. First finite residue-network loop is complete:
  `research/workstreams/architecture/residue-network/report.md`. Learned hidden
  weights, all 16 two-bit Boolean functions, exact declared finite checks and
  Lean certificates. Gradient attempts fit only 10/16 (two units) and 6/16 (one);
  exhaustive weight search fits 16/16. This is a restricted content/encoding
  guarantee, not scalable training, a language model or established originality.
  No new API/cloud budget follows. Keep this EOD focus while preserving B notes.

Read `research/brief.md`, `research/decisions.md`, and the current literature/candidate notes before continuing.

- Current owner-endorsed agenda: develop both approaches in `research/two-approach-agenda.md`. Architectural prevention includes neural operations down to linear algebra, alongside the endorsed candidate-generator/chooser baseline. The second approach is post-creation task-preserving rewriting. Both Claude worker branches have been integrated. No full study selected or continuing inference/cloud budget. Six batches' recorded response costs sum to $2.30376687, excluding unknown Modal costs. The approved $1 Modal setup/run reservation produced one usable T4 checkpoint after manual corrections; all four attempted apps are stopped. See `results/modal-operator-01-t4/assessment.md`, `experiments/leak_cap/PLAN.md` and `research/compute.md`. The trained 137k-parameter split-attention model solves an easy synthetic public lookup task; no useful private-computation advantage or novel language architecture is established. Model critiques contain independently corrected errors; do not adopt their impossibility claims as established facts.

- Preserve exploratory scope. No full hackathon study has been selected. The owner explicitly authorized a local anti-steganography prototype; see `experiments/anti_stego/README.md`. Compare candidates and discuss a research question before expanding to a full experiment. Small feasibility checks are allowed when they discriminate between candidates.
- Be skeptical: challenge weak assumptions, confounded designs, and novelty claims. Do not optimize for implementation convenience over contribution.
- Verify claims against primary papers and author repositories. Record URLs, versions/commit SHAs, inspected sections, and access dates. Separate paper claims, verified code behavior, our interpretations, and untested hypotheses. Mark incomplete reviews explicitly.
- Distinguish channel capacity, instructed use, independent discovery, chosen exploitation, harmful coordination, and adaptation under monitoring. Do not label all cooperation or correlated behavior collusion.
- Theoretical undetectability depends on a specified cover distribution, monitor, secrets, computational bounds, and implementation assumptions. A detector failure is not proof of universal undetectability. A working demonstration is not a general theorem.
- Define falsifiable hypotheses, independent units, primary outcomes, controls, and analysis before confirmatory runs. Include benign coordination, disconnected/shuffled channels where valid, and an instructed positive control.
- Log all observable actions, configurations, prompts, model/provider/version identifiers, sampling parameters, supported seeds, tool versions, and costs. Distinguish exploratory from confirmatory analysis. Report uncertainty and negative findings honestly.
- Favor reproducible local orchestration and hosted model APIs. No unlimited-credit assumption. Estimate expenditure before runs; record actual usage and missing cost data. Use GPUs or Modal only for a stated experimental need.
- Keep the official starter external. Before selective code reuse, verify the specific upstream license and preserve attribution; a bundled repository does not establish a common license for all subprojects.
- Repository is public as of 2026-10-25 (owner approved, for the sprint submission). Never commit keys, credentials or account tokens; everything pushed is world-readable. Never commit keys, credentials, `.env`, `compute.env`, or secret-bearing files. Inspect staged changes before committing.
- Maintain the literature, questions, ideas, decisions, and compute ledger as living documents. Do not silently convert a candidate into a commitment.
