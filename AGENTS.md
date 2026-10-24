# Research collaboration instructions

Read `research/brief.md`, `research/decisions.md`, and the current literature/candidate notes before continuing.

- Preserve exploratory scope. No full hackathon study has been selected. The owner explicitly authorized a local anti-steganography prototype; see `experiments/anti_stego/README.md`. Compare candidates and discuss a research question before expanding to a full experiment. Small feasibility checks are allowed when they discriminate between candidates.
- Be skeptical: challenge weak assumptions, confounded designs, and novelty claims. Do not optimize for implementation convenience over contribution.
- Verify claims against primary papers and author repositories. Record URLs, versions/commit SHAs, inspected sections, and access dates. Separate paper claims, verified code behavior, our interpretations, and untested hypotheses. Mark incomplete reviews explicitly.
- Distinguish channel capacity, instructed use, independent discovery, chosen exploitation, harmful coordination, and adaptation under monitoring. Do not label all cooperation or correlated behavior collusion.
- Theoretical undetectability depends on a specified cover distribution, monitor, secrets, computational bounds, and implementation assumptions. A detector failure is not proof of universal undetectability. A working demonstration is not a general theorem.
- Define falsifiable hypotheses, independent units, primary outcomes, controls, and analysis before confirmatory runs. Include benign coordination, disconnected/shuffled channels where valid, and an instructed positive control.
- Log all observable actions, configurations, prompts, model/provider/version identifiers, sampling parameters, supported seeds, tool versions, and costs. Distinguish exploratory from confirmatory analysis. Report uncertainty and negative findings honestly.
- Favor reproducible local orchestration and hosted model APIs. No unlimited-credit assumption. Estimate expenditure before runs; record actual usage and missing cost data. Use GPUs or Modal only for a stated experimental need.
- Keep the official starter external. Before selective code reuse, verify the specific upstream license and preserve attribution; a bundled repository does not establish a common license for all subprojects.
- Repository visibility MUST remain private. Do not change it without explicit owner approval. Never commit keys, credentials, `.env`, `compute.env`, or secret-bearing files. Inspect staged changes before committing.
- Maintain the literature, questions, ideas, decisions, and compute ledger as living documents. Do not silently convert a candidate into a commitment.
