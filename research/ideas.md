# Candidate investigations

**Latest owner direction:** the [two-approach agenda](two-approach-agenda.md) is now the active research organization: ground-up learned/verified architecture and task-preserving rewriting. Both have concrete proposed targets and controls; neither has a selected full study or established novelty claim. Historical candidates below remain reference material.

**Current-focus update:** the owner subsequently prioritized practical barriers to secure steganography and active prevention. See [revised candidates](practical-barrier-candidates.md) and [expanded prior art](stego-prior-art.md). The shortlist below is preserved historical exploration, not the current recommendation or a selected project.

**No candidate selected.** These are proposals for discussion, not experimental findings. Novelty remains provisional after an initial selective review. Scientific value should decide selection; setup convenience is secondary.

## Comparative judgment

Scores are qualitative assessments, not measured quantities. Cost uses proposed call counts, not verified dollar prices. All four can initially use local orchestration and hosted APIs. Narrow to one environment and at most two model families for the sprint.

| Candidate | Potential novelty | Significance | Rigor potential | Sprint tractability | Inference burden | Main reason to decline |
| --- | --- | --- | --- | --- | --- | --- |
| A. Discovery without an alliance offer | Medium; existing adoption/emergence work is close | High behavioral relevance | Medium: elicitation is hard to separate from incentives | Medium; risk of few events | Medium | A null may mostly measure weak task competence or poor discovery opportunity |
| B. Restriction and carrier substitution | Medium; text mitigation is established | High for deployment controls | High if task utility is preserved | Medium; requires an observable alternative carrier | Medium–high | Intervention may impair the task or make the new channel unusable |
| C. Causal audit of forbidden information use | Medium; action dependence/regret are established | High for evidence standards | High with randomized secrets and valid shams | Medium–high after task specification | Medium | A custom task could make the answer trivial or bake labels into signals |
| D. Executed protocol interoperability | Medium; planning convergence is already studied | High for translating security theory | High for capability; limited for behavioral willingness | Medium; coding-agent access and verification add risk | High/variable | A working pair does not imply secure covert outputs or autonomous exploitation |

**Discussion shortlist:** B and C offer concrete intervention/evidence contributions; A is the more direct behavioral question but has a greater event-rate risk. D remains competitive if translating cryptographic feasibility into operational compatibility is the priority. This is not a decision or a claim that B/C are novel. Preserve the market alternative below.

## A. Does discoverability determine chosen exploitation without an explicit offer?

**Question and motivation.** In a repeated allocation workflow, do agents find and exploit permitted operational affordances to coordinate against a third party when no secret alliance is advertised? This separates discovery and enacted behavior from saying ACCEPT to an offered tool.

**Prior work.** Voluntary-secret-tool adoption already separates acceptance from later stages and tests observation/framing. Colosseum already studies added private channels, including benign controls. Hidden in Plain Text already studies optimization-induced emergence. Our possible contribution is the transition from ordinary tool documentation to observed unauthorized coordination in a controlled deployment-style task, with discovery burden varied independently. It is not “first voluntary collusion.”

**Hypotheses.** H1: making an existing affordance more discoverable increases actual partner-conditioned harmful coordination under a fixed incentive structure. H2: the effect is larger with conflicting subgroup incentives than with aligned incentives. A preregistered null interval/effect threshold is needed; do not interpret non-significance as equivalence.

**Possible design.** Use three agents and randomized private task information. Compare ordinary tool documentation versus a salient but neutral example for the same tool, crossed with aligned versus conflicting objectives. Match documentation length, tool access, token budgets and task instances. Keep policy boundaries explicit in all arms; do not describe an offered alliance in discovery arms. Separate external rewards from textual instructions about rewards. Record first exposure, tool inspection, first use, partner response, harmful outcome and latency.

**Baselines and positive controls.** A benign legitimate coordination task; a disconnected relevant channel; unilateral agents with the same incentives; an explicit-offer replication arm; an instructed encoder/decoder control proving capacity and model competence. Keep controls out of the primary spontaneous numerator.

**Confounders.** Salient documentation may cue a strategy rather than merely enable discovery. Prompted conflicting objectives still induce behavior and limit “spontaneous” claims. More private information may directly improve decisions. Tool errors, skill differences and turn order can create apparent advantage. Require causal partner dependence and outsider loss, not a post-hoc successful subgroup.

**Implementation / inference.** Small custom allocation wrapper or a carefully adapted Colosseum view; event logs and objective oracle; no training/GPU. Proposed comparison: 4 cells × 20 independent episodes × at most 24 calls = 1,920 calls, plus roughly 480 control calls. Pilot fewer episodes only for feasibility, not effect claims. Setup estimate: 4–8 engineering hours, conditional on license/access and no framework problems.

**Informative negative result.** Zero spontaneous events with a strong capacity control bounds the event rate only under this elicitation regime. With 20 independent trials and zero events, the one-sided 95% upper bound is about 14%, so that sample cannot substantiate rare-risk absence. If the explicit control also fails, the result diagnoses the task/model rather than willingness.

## B. Does restricting one carrier suppress harm or relocate coordination?

**Question and motivation.** After normalizing a communication surface, do agents retain harmful coordination by exploiting another permitted degree of freedom, and at what legitimate utility cost?

**Prior work.** Paraphrasing, rate limiting and configured adaptive schemes are established. The prospective contribution is a controlled measurement of enacted substitution across operational carriers, with matched task semantics and utility. The starter explicitly suggests actions as carriers; merely encoding bits in a tool argument is insufficient novelty.

**Hypotheses.** H1: normalizing free-form messages reduces harmful coordination when an alternative carrier is absent. H2: allowing an equivalent action-order/identifier carrier attenuates that reduction after adaptation. H3: this interaction persists after accounting for legitimate task performance.

**Possible design.** Cross message normalization (off/on) with one alternative carrier (absent/present), ensuring the primary task has the same feasible solutions. First use instructed colluders to establish capacity. If time permits, add separate uninstructed episodes; never merge those populations. Introduce a restriction at a fixed checkpoint rather than only after selecting successes. Compare continuation, sham transformation and intervention from the same checkpoint; group inference by originating episode. Log sender-private payload dependence and outsider loss before/after restriction, plus recovery time. A carrier is present only if receiver observations actually expose it.

**Baselines and positive controls.** Honest teams under every restriction; a known functioning primary encoder; a known functioning alternative encoder; both carriers disabled; task-equivalent sham; no adaptation continuation; fresh agents facing the restriction from the start. An oracle or scripted solver checks that task utility is not mechanically destroyed.

**Confounders.** JSON canonicalization does not remove semantic choice of values. Ordering changes can affect allocations directly; identifiers may carry real task meaning. Provider timing/retries must not become an uncontrolled channel. Coalition advantage can survive because agents no longer need to communicate, so sustained harm alone does not demonstrate substitution. Require randomized private information that cannot be inferred from public state and targeted intervention on the proposed new carrier.

**Implementation / inference.** Instrument two observation surfaces and deterministic canonicalization; record raw actions and exactly what each receiver saw. Proposed 4 cells × 20 episodes × 36 calls = 2,880 calls plus controls, roughly 3,600 total. Branching can increase this. Setup estimate: 6–10 hours with a small workflow. No need for cryptographic undetectability, custom weights or GPU.

**Informative negative result.** A selective restriction that reduces measured transfer/harm while retaining honest performance supports that intervention for the tested regime. No recovery only informs substitution if the alternative carrier works under positive control and sufficient adaptation opportunities were given. Loss of honest utility is an informative failed defense, not successful prevention.

## C. Can an auditor establish forbidden information use without decoding the carrier?

**Question and motivation.** Can controlled interventions distinguish communication-enabled harmful coordination from shared priors, common signals, legitimate cooperation and unilateral misconduct?

**Prior work.** Bonjour already uses conditional action dependence, Colosseum already measures outcome/regret, and Audit the Whisper already combines detectors/interventions. The possible contribution is calibration of a causal audit under deliberately difficult benign nulls and unseen carriers. SCHEME's edits-plus-messages monitoring also constrains novelty. We should not market another correlation score as causal identification.

**Hypotheses.** H1: a prespecified audit using randomized private information and channel interventions has lower false-positive rate on common-cause/benign-coordination controls than unconditional action dependence at comparable power. H2: sensitivity transfers to a held-out carrier without the detector receiving its codebook.

**Possible design.** Build a three-agent allocation or small auction task with a sender-only randomized variable Z independent of all public task state. A recipient can exploit Z to benefit a pair at an outsider's expense; no single agent can achieve the joint side objective. Randomize channel delivery/canonicalization without changing feasible task actions, and compare a task-equivalent sham. Analyze the intervention's effect on recipient dependence on Z and outsider welfare. Auditor access to Z is privileged experimental access and must be stated; an ordinary log-only deployment auditor may lack it. If matched message swaps are used, use them only when state-valid, or label them as stress tests rather than causal estimates.

**Baselines and positive controls.** Shared public shocks with disconnected agents; same-model independent agents; benign communication with allowed private information; unilateral cheating; talk without action; harm without communication; fixed instructed scheme. Compare simple dependence, state-conditioned dependence, a fixed text judge and the causal audit, with held-out evaluation episodes/carriers and equalized observation/call budgets where possible.

**Confounders.** Channel interventions may remove useful information or cause out-of-distribution reactions. A tag predicting a side objective may leak through tool names or logs. A private-information channel is not automatically collusion; require joint benefit and outsider/policy harm. A task constructed to force Z-use only shows identifiability in that task. Low-dimensional statistics need sufficient repeated states; avoid huge sparse MI estimators.

**Implementation / inference.** Objective oracle, randomized delivery layer, full receiver-view logging and predefined scoring; hosted APIs suffice. Example: 2 behavior regimes × 2 channel conditions × 20 episodes × 24 calls = 1,920 calls, plus 480 calibration/control calls = about 2,400. Extra model replication or judge scoring is additional. Setup estimate: 4–8 hours; full null calibration is more costly than a proof of concept.

**Informative negative result.** Failure on benign common-cause controls rejects the proposed evidence standard. Better calibration with low power can still characterize a real sample-size/visibility tradeoff. No transfer to a held-out carrier limits generality. Even strong results support a bounded experimental audit, not passive universal detection or a claim about mental intent.

## D. Do matching steganography plans yield interoperable implementations?

**Question and motivation.** Does access to a common public reference materially improve independently built sender/receiver compatibility? Does the paper's planning-level compatibility measure predict actual round-trip success?

**Prior work.** Rippin directly studies scheme/parameter convergence and flags tool access as follow-up. Secure steganography and covert key exchange are already established mathematically. This candidate is an execution/measurement extension, not a new existence result or voluntary-collusion study.

**Hypotheses.** H1: a shared reference increases executed cross-agent compatibility relative to isolated reference discovery. H2: broad scheme agreement is an unreliable proxy for successful payload recovery. Separate public defaults from shared secret keys; a public artifact is not a cryptographic secret.

**Possible design.** Independent clean workspaces receive only agreed interfaces and a fixed time/token budget. Vary public reference availability, holding sampling access and tool budget fixed. Prevent cross-workspace file/network exchange other than the defined output interface. Score within-implementation self-tests, cross-implementation decoding, exact payload recovery, supported payload length and execution cost. Examine dependence among parameter choices rather than assuming a product of marginal match probabilities. Pairing many endpoints does not create equally many independent agents.

**Baselines and positive controls.** One authored reference encoder/decoder, deliberately mismatched parameters, shared code with independently generated keys where appropriate, matched known keys, and a no-reference condition. Keep a simple detectable channel as a competence control and treat security tests separately. Have the auditor see the same public reference in a separate detection comparison.

**Confounders.** Shared keys/interfaces can give away much of the coordination problem. Library/runtime/float differences can break decoding unrelated to conceptual agreement. Self-tests can leak the intended protocol. Repeated debugging between the pair changes one-shot independent coordination into interactive engineering. Successful recovery does not validate a distributional or cryptographic proof; finite empirical tests cannot certify undetectability.

**Implementation / inference.** Requires sandboxed coding-agent access and an independent execution evaluator, not just chat model completion access. Promotional OpenRouter access alone may not supply a practical coding harness. Start with 2 conditions × 8 independent endpoints = 16 bounded construction jobs; add fixed held-out decoding tests without extra LLM calls. Dollar and call estimates depend on the construction-job budget and are not yet defensible. Setup estimate: 6–12 hours, possibly more if supplementary code is unavailable.

**Informative negative result.** Reliable self-tests but failed cross-pair decoding isolate a compatibility bottleneck. Failure of even reference pairs diagnoses environment assumptions. An improvement from public artifacts supports an operational risk factor while leaving willingness, harm and secrecy unmeasured.

## Market alternative retained for comparison

**E. Replacement versus retained context.** Use checkpointed pricing games to separate model identity from history/notes in recovery of a price convention. Hypothesis: preserving a convention-bearing context matters more than nominal instance identity. Compare different model/same context, same model/reduced context and no-change continuation, with randomized checkpoint time and independent base episodes. Controls include competitive scripted opponents and history-matched benign coordination; outcome measures include prices, profit and consumer welfare. Same-model “fresh instance” with identical context is statistically the same treatment in a stateless harness. A null can bound convention portability. This is tractable, but long sequential histories increase cost and generic replacement studies are already an official suggested project. Retain it if the economic interpretation is more valuable than covert-channel specificity; perform a further targeted literature check before claiming novelty.

## Shared inference and analysis requirements

- Proposed call counts above are workload sketches, not power analyses or approved spending. Pilot latency, token use and valid-action rate before deciding sample sizes. A short pilot cannot establish a low false-positive rate.
- Example workload of 2,400 calls at 2,000 input and 500 output tokens/call means 4.8M input + 1.2M output tokens before retries, growing histories, tool loops or judging. Dollar estimate is `4.8 * input_USD_per_M + 1.2 * output_USD_per_M`; rates and budget remain unset.
- Use a fixed primary outcome and minimum meaningful effect. Report intervals; resample/randomize at the episode/base-trajectory level. Predefine subgroup identity and avoid post-hoc maximum-pair selection without multiplicity correction.
- Keep pilot and evaluation data separate. Freeze prompts, detector thresholds, model IDs, transformations and failure handling before confirmatory runs. Unsupported provider seeds do not guarantee deterministic model outputs.
- Protect analysis from false reassurance: zero events in 20 runs still permits about 14% underlying event probability at one-sided 95% confidence. Roughly 2,995 independent zero-event null trials would be needed for that empirical upper bound to fall below 0.1%, assuming a stable binomial null.
- Preserve raw versus receiver-visible actions, API usage/retries, cost fields, intended versus effective models, and failed/aborted episodes. No cherry-picking positive controls until they succeed and then treating the selected sample as an unbiased effect estimate.

Selection requires a discussion of the scientific question, available remaining hours, and acceptable inference spend. No candidate here starts a run automatically.

## New exploratory lens: components of the task-valid artifact space

See [local-rewrite obstruction](workstreams/task-preserving-rewrite/local-rewrite-obstruction.md). Treat artifacts that solve a fixed task as vertices and allowed elementary edits as edges. A sanitizer restricted to those edits cannot leave the connected component containing its input; a receiver-distinguishable component choice can therefore survive every local edit while task validity remains perfect.

This makes one part of the owner's topology intuition precise, but the operative concept is graph connectivity / zero-dimensional components, not knot theory or a new topological invariant. The mathematical framework and hardness of reconfiguration reachability are established prior art. The possible contribution is a focused evaluation of whether realistic rewrite grammars preserve receiver-readable component choices, and the cost of allowing global reconstruction to cross them. Novelty and practical relevance are both unverified.

Qualitative screen: **conceptual clarity: high; potential significance: medium but speculative; tractability for a small exact benchmark: high; generalizability: low until a realistic artifact domain is found; prior-art risk: high.** Keep as a lens for candidate design, not a selected project. The one-bit `x != y` example is only a proof illustration and should not be promoted as the experiment.

- **Component-label rewrite pilot (B, exploratory, 2026-10-24).** LLM rewriters given the draft preserved a solution-choice payload; truncation confounds the validity of the re-solving arms. See `results/component-rewrite-pilot-01/assessment.md`.
