# Revised candidates after the secure-steganography review

2026-10-24. **No study selected.** These refine the owner's interest in practical barriers and active prevention. [Prior-art review](stego-prior-art.md) supplies the qualifications. Cost estimates below are planning sketches, not approved spend or a power analysis.

**Novelty downgrade:** the [latest audit](novelty-audit.md) finds closer predecessors in constraint-based watermarking, code watermark removal and Hand and Brain. The provisional comparisons below do not establish novelty. In particular, a generic solution-choice/rewriting-cost study should not be selected without an explicit contribution beyond those sources.

**Subsequent focus:** the owner requested prior art on substantive task choices and the cost of replacing useful work. [Semantic erasure](semantic-erasure.md) records the direct predecessors, counterexamples and a further replacement-cost candidate. The comparison below remains exploratory; token-sampling schemes are not the only research scope.

## A. How much receiver-side assistance does a successful demonstration require?

**Question.** Do isolated receivers recover payloads as reliably as same-process or encoder-assisted evaluations?

**Why it matters / prior art.** SparSamp's v4 experimental decoder uses saved encoder intervals, while its basic demo recomputes them. ANStega already acknowledges numerical synchronization limits; finite-precision detection is already researched. Reporting this dependency is useful, but another “floating point exists” demonstration has low novelty. The contribution would have to quantify the actual interoperability gap under explicitly reproducible interfaces.

**Falsifiable hypotheses.** H1: removing encoder-side interval assistance reduces exact recovery in at least one specified runtime condition. H2: model-free Zamir decoding is less sensitive to receiver inference-runtime changes than shared-model coding. Freeze conditions and a meaningful difference before confirmatory runs; neither hypothesis is assumed true.

**Design and controls.** Compare original assisted path, isolated matched-runtime decoder, and deliberately perturbed receiver calculations on the same fixed carrier instances. Positive control: exact original token IDs and matched state. Then separate tokens-to-text-to-tokens ambiguity from numerical drift. Log seed, PRNG, weights, tokenizer, prompt/template, probabilities where needed, software and hardware. Do not merge arithmetic changes, tokenization and context truncation into one treatment. Use cryptographic randomness for security claims; retain original demo randomness as a labeled reproduction arm only.

**Inference / feasibility.** First use synthetic probability vectors for mechanism checks; they cannot estimate real-model failure rates. A small open model enables a local end-to-end check if resources allow. Proposed pilot: 50 independent payloads/prompts across 2 schemes and 3 decoder conditions. Some carrier generation can be reused across decoder arms; cluster uncertainty by original carrier. Hosted text-only APIs are insufficient for many encoders because arbitrary sampling/probability access is required. Local numerical checks cost $0 in API calls; GPU time/model downloads remain unestimated.

**Negative result.** Stable isolated decoding would weaken the supposed barrier in those conditions and demonstrate that the saved-interval workaround is unnecessary there. A failure confined to corrupted model settings is not evidence of normal deployment unreliability.

## B. What is the repair cost of surviving a task-preserving active warden?

**Question.** Can a defender reduce delivered covert information with small legitimate-task cost, even after the sender uses an edit-resilient scheme or repairs its protocol?

**Prior-art boundary.** Wang–Moulin already studies constrained active attacks. Paraphrasing, semantic channels and resynchronization also have direct predecessors. Codetta explicitly leaves mitigation evaluation open, but being named future work does not establish novelty. A defensible contribution would compare actual robust and fragile schemes under a common, independently checked task-utility budget.

**Falsifiable hypotheses.** H1: interventions that disable a fragile codec do not achieve the same suppression against a robust codec at matched task utility. H2: repair restores some delivery but measurably increases total sampling, visible tokens or latency. The intervention could fail both hypotheses; report that.

**Design.** Start with one task that has an executable correctness oracle: a small structured report with required facts, or a bounded software artifact. Compare identity, task-valid sham, syntax normalization and one semantic regeneration policy. Sweep a preregistered perturbation budget. Test a functioning fragile encoder and an edit-resilient baseline before claiming prevention. Keep fixed-codec and repair-enabled phases separate; cap and log repair effort. Measure exact message recovery, partial payload leakage, covert bits per total computation, task success, valid-output/abort rate, and latency. Exact-message failure alone can conceal substantial surviving information. For a binary control channel, include balanced payloads and independent payload/receiver pairing.

**Confounders / requirements.** A random token edit is often invalid code or an altered fact. A paraphraser seeing a secret must be a trusted component, resistant to sender instructions. Semantic encoding may survive and be harder to replace than syntax. Framing and alignment must be tested rather than silently given to one codec. Repair search must not contaminate held-out evaluation instances. Choose a representation every baseline genuinely supports; Alkaid's sequence codebook may not fit strict code/report requirements without adaptation.

**Feasibility.** A bounded local scripted pilot is plausible; a fair multi-codec adaptive study is substantially larger and may exceed the sprint. Planning sketch: 30 carriers × 2 codecs × 4 transformations, with paired task checks; adaptive search and paraphraser inference additional. Estimate dollars only after selecting a model and measuring token usage. The existing assignment prototype is a control environment, not a substitute for these stronger encoders.

**Negative result.** If every effective intervention violates task constraints, that is an informative utility boundary. If a robust baseline wins, characterize the defender's failure rather than adding post-hoc harsher edits. No general impossibility conclusion follows from either outcome.

## C. Can control of the final sampler prevent a specified covert encoder?

**Question.** If a trusted broker rather than the agent controls release randomness, what covert influence remains through prompts, task choices and rejection/retry behavior?

**Prior-art boundary.** Codetta already proposes verifiable sampling; our projection/replanning prototype already illustrates discarded versus retained choices. Simply moving randomness to a broker is not new. The unresolved engineering question is whether a precisely bounded interface actually removes sender control, rather than shifting it into context or selective retries.

**Falsifiable hypotheses.** H1: with a fixed authenticated probability vector and broker-owned randomness, the tested sampling-steering encoder cannot convey its payload. H2: allowing sender-controlled context or selective rejection restores a measurable channel. H1's fixed-vector case is a basic control, not the main research finding.

**Design and controls.** Compare ordinary agent-controlled sampling, broker release with fixed approved input, broker release with agent-selected input, and broker release with bounded rejection. Log all proposals and failures; delivered output alone misses selective aborts. Use several equally valid task solutions to make semantic choice explicit. Positive controls prove capacity through allowed context/retry choices; a fixed-input baseline proves the restricted interface functions. Specify whether execution time, shared state and tool actions are observable or excluded.

**Inference / feasibility.** A standard-library finite sampler can establish the mechanism without spending credits. Extending to an LLM requires interception of the actual sampling interface and authenticated control over model/context; a normal chat API often cannot provide this. Production proof machinery is far beyond a sprint. A small finite task is tractable but its scientific value depends on a nontrivial residual-channel result.

**Negative result.** If retained task choices carry the payload at nearly unchanged rate, the broker does not meet the proposed boundary. If restrictions remove most legitimate usefulness, report the cost rather than a universal anti-steganography success.

## Comparison, not selection

| Candidate | Novelty confidence | Scientific value if executed well | Tractability | Primary risk |
| --- | --- | --- | --- | --- |
| A: isolated receiver fidelity | Low–medium, pending code/literature comparison | Clarifies evidence and practical compatibility | Highest for a small mechanism check | A mundane mismatch with little external relevance |
| B: active interference versus repair | Unestablished; strongest question of these three | Direct prevention/utility evidence | Medium–low with robust baselines | Unfair transformations or weak adversary |
| C: broker-owned randomness | Low for the basic principle | Tests a precise pre-creation boundary | High for a toy, low for deployment | Covert influence moves into inputs or aborts |

B currently poses the most direct research question for the owner's goal; A can be a feasibility gate, and C a complementary control. This is a comparative assessment, not authorization to launch a full study. Do not choose A solely because it is easy. A genuinely novel experiment still needs a narrower task, a working strong baseline and explicit resource limits.
