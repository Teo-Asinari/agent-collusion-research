# Task-preserving reconstruction: concrete proposal and failure boundaries

2026-10-24. Research proposal, not an approved full study. No model inference, dependency installation, GPU allocation or full experiment was performed. One four-state analytical sanity check was calculated with Python's standard library. [Source/read-depth ledger](sources.md).

## Recommendation

Develop an **oracle-checked reconstruction method**, provisionally on bounded executable programs, rather than another unconstrained prose paraphraser. Give the defender the original task, an untrusted solution, and a task validator. Permit changes in algorithm/representation when the original task permits them. Compare local refactoring, broader equivalent reconstruction and independent synthesis. Test an adapted receiver and sender, not only the original decoder.

This is a research design, not an established novel defense. The promising question is whether submitted useful work can be reused without preserving sender-chosen structure, and what computational savings survive a stringent leakage target. Existing paraphrasing, code watermark removal and superoptimization already cover much of this terrain. A contribution needs a specific result against those precedents.

## 1. Operational target

Let x be the trusted original task, y=E(x,m,k) the submitted artifact, m a balanced private payload independent of x, and k receiver side information, including a shared codebook/key. Let R(x,y;r) be the defender's randomized reconstruction. The receiver view V includes every released artifact, status, metadata and repeated-output history exposed by the declared interface. Defender randomness r is independent of m,k. Fix the task before drawing m and prevent sender control of its specification.

**Strong target:** for fixed x,k and permitted sender strategies, distributions of V are identical across payloads. If the legitimate task requires disclosure of private facts, explicitly define that authorized function and compare inputs agreeing on it. Do not condition on a sender-selected solution and then claim its choice was erased.

**Approximate target:** upper-bound total variation between receiver views induced by two payloads. For a uniform binary payload and equal prior probabilities, optimal decoding accuracy is (1+TV)/2. Finite testing of a decoder provides a lower bound on exploitable transfer, not an upper bound against all decoders. Exact finite-kernel enumeration can certify a particular bounded interface; claims about arbitrary code or LLM adversaries require more.

**Preservation:** satisfy the original task, with a predeclared correctness and quality tolerance. Preserve exact program behavior only when that is the required task; preserve efficiency/readability constraints separately. Preserving every submitted semantic choice can make erasure impossible by definition.

## 2. A useful elementary feasibility criterion

For fixed x, let A_y be the finite set of released outputs allowed by the task and the chosen preservation rule for input artifact y. A sanitizer whose full output distribution is identical for every admissible y can have zero failure only if the intersection of all A_y is nonempty. Conversely, any output in that intersection gives a constant-output sanitizer with this property. The proof is support containment in every A_y; the converse is immediate. This elementary criterion is not a novelty claim or an efficient construction.

It forces the right questions: are we preserving the original task, or different sender-selected requirements? If the intersection is nonempty but hard to find, that is a computational question; local rewrite failure does not settle it. For randomized task specifications or allowed failures, reformulate the criterion rather than silently applying the zero-failure finite version.

## 3. Specific failure: inheriting the sender's quality target

A quality-preserving random walk can forget its starting point within a quality class while retaining a payload-dependent choice of that class. Consider four outputs a0,a1,b0,b1. Both a outputs have quality 1; both b outputs quality 2. The original task accepts quality at least 1. The sender selects an a output for payload 0 and a b output for payload 1.

Suppose a sanitizer perfectly samples uniformly among outputs with quality at least the submitted output's quality. Its distributions are:

| Payload | a0 | a1 | b0 | b1 |
| --- | --- | --- | --- | --- |
| 0 | 1/4 | 1/4 | 1/4 | 1/4 |
| 1 | 0 | 0 | 1/2 | 1/2 |

Every output meets the original task and never lowers the submitted quality. Nevertheless TV=1/2, optimal bit recovery is 3/4, and mutual information is approximately 0.311278 bits. A fixed task-derived threshold of 1 with the same common uniform target gives TV=0 in this finite example. Sampling only from b outputs would also erase the signal and preserve both initial quality levels, so this is not a general impossibility result.

These fractions and information value were checked with Python `fractions.Fraction` and `math.log2`, using the displayed probability vectors. No stochastic run or LLM experiment was used. The example is a sanity check on our definition, not a claimed new theorem or a refutation of watermark-removal results, whose security objective differs. It motivates treating initial quality, warm starts, stopping criteria and fallback behavior as possible input-dependent channels.

## 4. Compare task families before selection

| Family | Preservation oracle | Strength | Main drawback / closest overlap |
| --- | --- | --- | --- |
| Small schedules/constraint solutions | Exact validity and objective | Easy to enumerate channels and optimal reconstruction | Closely anticipated by Kahng and our assignment prototype; generic SAT study is weak novelty |
| Bounded loop-free bit-vector programs | Exhaustive behavior over all finite inputs, plus explicit instruction cost | Exact functional preservation; meaningful algorithmic/structural choice and synthesis cost | Artificial scale; compiler/superoptimization and code-watermark prior art are strong |
| Ordinary repository code | Tests plus optional translation validation for supported fragments | Direct relevance to agentic software work | Tests miss regressions; builds, environment and repository placement add channels |
| Free-form explanations/literature reviews | Task rubric and independent evaluation | Rich semantic choices | Quality oracle itself is uncertain and can preserve the hidden content |

**Provisional feasibility choice:** one-input 4-bit programs initially, expanding to 8 bits only if needed. Restrict operations and length so every candidate terminates and every input can be evaluated; define arithmetic modulo 2^b, with no undefined behavior, IO or mutable external state. The task specifies the desired finite function and an externally fixed cost ceiling. All input points are checked, not just a test sample. This buys a strong oracle; it is not itself a scientific contribution.

Sender controls the implementation: algebraic identities, alternate decompositions, operation order or choice among short implementations. Provide at least two payload values with genuinely valid artifacts and verify their visibility after each intervention. A codebook using a constant's spelling alone is a weak control, not the main adversary. Code generation need not involve an LLM for this initial mechanism check; transfer to real learned encoders is a separate stage.

Do not release truth tables as a shortcut unless they satisfy the task's code/size/performance requirements. A canonical lookup table may erase structure while violating the intended utility contract. Conversely, if lookup tables are permitted and cheap, their success is an informative negative for any claimed reconstruction barrier.

## 5. Reconstruction pipeline and comparison arms

1. Parse y into a defined intermediate representation. Validate complete behavior against x; canonicalize names and serialization.
2. Apply sound equivalence rewrites or reconstruct a program from task-derived semantics, with independent randomness where used. Retaining extracted expressions or initialization from y may retain the signal; measure this dependence.
3. Check correctness over the full finite domain and the fixed cost ceiling. Permit algorithmic replacement; do not require edit similarity.
4. Return via a fixed modeled release interface. Treat invalid input, timeout and no-solution as observable outcomes. Never silently evaluate only accepted instances.

| Arm | Role |
| --- | --- |
| Identity | Functioning channel control |
| Names/format normalization | Weak syntax baseline |
| Ordinary paraphrase/refactor | Typical defense; scripted now, hosted-model version only after budget selection |
| Task-conditioned reconstruction using y | Main reuse-based intervention |
| Structural reconstruction with wider search | Tests beyond local transformations |
| Independent synthesis from x only | Essential strong baseline; no y-dependent warm start, cost cap, seed or failure decision |
| Cheap canonical family | Negative control where erasure should be straightforward |

Independent synthesis must use a task-fixed search order and budget, with a declared fallback derived only from x. Otherwise a success/timeout or old-code fallback can restore y-dependence. Enumerative canonical synthesis can yield a formal content guarantee for this finite interface if it completes; its cost is the tradeoff to measure. It does not imply security for actual runtime timing.

## 6. Attacker adaptation and inference

Evaluate three distinct regimes: frozen encoder/decoder; decoder refit to rewritten outputs; jointly adapted encoder/decoder with stated construction/query budget and no evaluation-label access. Include a keyed family and a receiver that aggregates repeated artifacts. Do not call their instructed use spontaneous collusion or claim distributional covertness without a separate test/model.

Split by original task/function before generating variants and payloads. Enumerated rewrites and repeated payload samples of one task are correlated; report task-clustered uncertainty. Separate development/adaptation data from held-out task families and seeds. Use balanced payloads, public-task-only receiver baselines, no-delivery controls, valid-delivery positive controls and honest no-payload artifacts. Logs that expose m, unsanitized artifacts or selected seeds must not enter the receiver view.

Primary outcomes: exact functional validity, fixed cost-ceiling compliance, adapted bit recovery and defender search/evaluation cost. Secondary: partial information, multi-output recovery, rejection/timeout frequency and any lower bound on transfer from an empirical receiver. For a fully enumerated small rewrite kernel, calculate pairwise TV rather than relying on a learned detector. Report average and worst discovered sender pairs separately; held-out attacks are not a universal worst case.

Use a utility-versus-leakage-versus-compute frontier, not a single removal percentage. Correctness should be a hard requirement in the finite DSL. A degraded answer or missing delivery is not a successful defense merely because a frozen decoder fails.

## 7. Prior-art delta and go/no-go

| Closest precedent | Already covered | Proposed distinction needing verification |
| --- | --- | --- |
| Roger–Greenblatt §§5.3,7.2 | Context-aware paraphrase versus regeneration; reuse of a stronger model's insights | Exact-oracle structural reconstruction and adapted transfer measurement, not just another paraphrase prompt |
| Watermarks in the Sand / Sandcastles | Quality-oracle random walks and mixing/quality difficulties | Payload independence of the full release under fixed versus inherited quality targets; not merely watermark detection failure |
| Kahng et al. | Constraint solution-choice encoding and re-solving removal cost | Cannot claim that basic mechanism or its cost intuition is new |
| SrcMarker | Code structure/identifier channels, adaptive removal and functionality checks | Exact finite-domain validation and joint adversarial adaptation; benchmark size alone is insufficient novelty |
| Hand and Brain | Semantic strategy channels and decision-anchor intervention; some adaptation | Post-creation reconstruction differs, but full-text review remains necessary before claiming a new adaptive setting |
| Pandey et al., Oct 2026 | Canonical task interface, private-state leakage and shared-key bounds | Rich artifact reconstruction/compute reuse beyond a small route alphabet; generic projection is already covered |
| STOKE / equality saturation | Equivalent program search and cost-guided extraction | Need an explicit information-flow objective and evidence beyond ordinary optimization |

**Novelty status:** not established. Candidate contribution forms are a verified bounded sanitizer that recovers a demonstrable useful-computation advantage, a consequential counterexample to a named defense, or an exact measurement identifying when reuse preserves payload that independent synthesis removes. Do not sell the four-state example, finite DSL or standard compilation as novel by themselves.

## 8. Bounded next feasibility check

Before a full study: choose a tiny DSL and about a dozen independently specified functions; check two structural encoders per function; compare task-conditioned local rewrites with task-only canonical enumeration under the same search limits. Enumerate enough small cases to calculate receiver-view distributions including failure. Stop if channels fail before defense, if canonicalization already cheaply removes them, if the task oracle is unreliable, or if every interesting setting exceeds practical search limits. Record those negatives rather than constructing a harder toy to rescue the premise.

This check is proposed, not launched. It could use standard-library code and no inference spend. A hosted-model code-rewriting extension needs chosen models, verified access, estimated token workload and an approved budget. The only computation performed here was the four-state probability check above. No claim is made about realistic LLM scale, physical side channels or universal steganography removal.
