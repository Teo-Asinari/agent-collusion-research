# Two approaches to anti-steganography

**Latest exploratory continuation:** [bilinear network](workstreams/architecture/bilinear-network/report.md)
replaces weight enumeration with exact linear algebra on a structured quadratic
family, learns hidden maps, tests unseen inputs and checks generic and concrete
Lean statements. This resolves a bounded learning limitation without establishing
novelty or stronger security. No full study or paid run selected.

**Current EOD focus, explicitly reaffirmed by owner:** neural architecture design
and proof on a small set, not a pivot to the rewrite study. The first bounded
[residue-network design loop and report](workstreams/architecture/residue-network/report.md)
are complete, with learned hidden weights, finite checks and Lean certificates.
Scalable learning, utility beyond tiny truth tables and novelty remain open.

Operation-level follow-up: [candidate factorization-quotient primitive](workstreams/architecture/quotient-primitive.md)
now has equations, an exact-arithmetic identity, local checks and explicit floating-
point/training counterexamples. Close GL-equivariant and polynomial prior art
means novelty remains unestablished; this is not a selected experiment.

Current A continuation: owner explicitly endorsed both operation-level neural
design and the candidate-generator/chooser implementation. See
[equations, prototype and recovery evidence](workstreams/architecture/operator-and-choice.md).
The chooser is a baseline and possible finite release module; it does not replace
the requirement to develop the underlying neural computation. B remains active.

2026-10-24. Owner endorsed developing two research approaches: (A) a ground-up learned/verified architecture and (B) post-creation rewriting with task preservation. This is a chosen research agenda, not selection of a particular benchmark, proof theorem, full experiment, model or spending budget. Novelty must be established separately for concrete results.

## Shared objective and boundary

Prevent an unauthorized payload from affecting information available to a receiver, while preserving explicitly required task utility. Let x denote the externally specified task and authorized information, m a sender-private payload, and k receiver side information including any shared key. The sender must not control x through an unmodeled path. Include repeated messages, state, status and timing in the receiver view when the claim covers them.

For exact prevention, compare receiver-view distributions across m, with x and k fixed, under a specified initial-state/randomness model. For controlled release of private task information, specify an ideal release function F first, and compare worlds agreeing on its permitted disclosure. Merely conditioning on a sender-selected output or labeling a learned summary as authorized would make the guarantee misleading.

Task preservation means meeting the original user's specification, with a declared quality tolerance. It does not necessarily mean preserving every choice or meaning in the submitted artifact. If the task requires preserving the very feature carrying the payload, erasure and preservation can conflict.

## A. Ground-up learned/verified architecture

**Question.** Can an architecture interleaving transformer computation and verified operations provide useful computation while preserving an information-flow invariant for every permitted set of learned weights?

**Design seed.** Define a small computational language whose primitives include compartmentalized attention/MLP blocks, labeled memory and verified cross-compartment operations. Private and public streams have explicit dependency rules. The type/proof discipline covers residuals, routing, normalization, recurrence and parameter updates, not only attention masks. A private-to-public transition must implement a specified permitted release, rather than an arbitrary learned projection. This is an internal computational architecture, not an ordinary LLM plus an output inspector.

**Proposed theorem shape, not an achieved theorem.** Given well-formed architecture A, admissible parameters and initial states, and stated execution semantics, changes to protected information cannot change the receiver view beyond F. Prove primitive preservation and composition; state termination and randomness assumptions. A universal-over-weights result would avoid relying on training to learn compliance. Some useful modules may instead require weight-specific contracts; label that weaker target explicitly.

**Critical obstacle.** If a protected neural stream can freely choose between two public task-valid results, the channel remains. Moving that decision inside the network does not remove it. Avoid a vacuous success in which private neural computation is disconnected from every useful output: show a task needing a nonconstant authorized function of private information, alongside the forbidden payload.

**Falsifiable research claims.** The proposed primitives support the global information-flow theorem; an explicit useful task can be represented without bypassing it. A counterexample invalidates the first claim; inability to express the useful task falsifies the intended capability claim. A small mechanized proof could be valuable; random testing alone is insufficient to establish universality.

**Baselines/controls.** Unrestricted transformer; attention-mask-only ablation with other dependencies retained; corresponding verified symbolic task solution. Remove one architectural invariant and construct an explicit payload channel. Verify that the permitted task information still influences the result while the forbidden payload does not. These are proposed controls, not executed results.

**Prior art.** [Architecture notes](formal-hybrid-architectures.md): Tiwari et al. already alter transformer training/expert routing for training-data IFC. LLMbda already mechanizes agent-level probabilistic information-flow guarantees. Vehicle connects neural and symbolic specifications/proofs; Chong–van der Meyden provides architectural proof methodology. A candidate contribution needs a specific new primitive, theorem or useful capability/guarantee combination beyond them. No claim of the first verified hybrid architecture.

**Feasibility/cost.** Near-term output: formal model, counterexample search and one compositional lemma/proof attempt for a small architecture. Training a general language model from scratch is a separate, much larger project. No model inference is needed to test initial structural claims; proof-engineering/toolchain costs remain unestimated. Do not label a bounded numerical check a proof of an unbounded architecture.

**Informative negative.** A covert dependency through a supposedly safe primitive; training-state contamination; an unrealizable release contract; a guarantee that removes useful capability. Record which assumption failed rather than claiming formal methods generally cannot help.

## B. Rewrite with task preservation

**Question.** Can a defender transform a sender-created artifact into a task-successful replacement that removes payload transfer, including after sender/receiver adaptation, at a useful computational cost?

**Design seed: task-conditioned reconstruction.** Give the defender the original task x and submitted artifact y. Extract/check task-relevant content, discard optional sender choices where possible, and construct a fresh task-valid artifact. The target is to preserve task success while changing the encoding-relevant features. Extraction and reconstruction can themselves preserve the signal; they are interventions to test, not trusted information-flow boundaries by definition.

**Proposed mathematical target.** A rewrite kernel R(x,y) maps valid inputs to task-valid output distributions. A sufficient strong property is that, for fixed x, the entire released distribution is identical for every admissible sender artifact y, including selection/failure behavior. A common task-conditioned distribution independent of y supplies this property in the stated model. Approximate distance bounds are an alternative, but require stated adversary observations and composition. Fresh randomness alone does not establish independence from y.

**Interventions/baselines.** Identity; syntax normalization; ordinary paraphrase or refactor; task-conditioned rewrite; stronger structural or solution replacement; independent solving from x alone. Include independent solving even when expensive: without it, local rewrite failure cannot establish that removal is hard. Include a cheaply rerandomizable task. Public task controls and artifact-independent solver randomness must be verified.

**Hypotheses.** Task-conditioned rewriting reduces residual transfer more than meaning-preserving paraphrase at matched task quality. Any apparent gain persists against an adapted decoder and substantive-choice encoders. Reuse of expensive submitted work can retain payload-dependent structure, while independent reconstruction may remove it at higher cost. These are bounded empirical hypotheses, not universal hardness claims.

**Measurements.** Task success and quality against an independent specification/oracle; exact and partial payload recovery against chance and disconnected controls; receiver access to keys and multi-output history; defender compute, latency and inference spend. Hold out payloads and task instances for evaluation. Freeze a decoder only for one baseline, then allow receiver refitting and joint adaptation in separately budgeted conditions. Failure of all tested decoders remains weaker than an information-flow proof.

**Confounders.** A sanitizer may suppress both task information and payload. Tests may miss functional regressions. Freshly solved artifacts can still depend on sender-controlled prompts, warm starts, stopping decisions or caches. The receiver may have uncontrolled observations. Multiple variants of one task are not independent task instances. A signal mandated by x is not evidence of an unauthorized extra channel.

**Prior art.** [Semantic erasure](semantic-erasure.md) and [novelty audit](novelty-audit.md): Roger–Greenblatt already discuss replacement capability; constraint-based watermarking already discusses solution choice and re-solving; SrcMarker tests functional code removal; random-walk work studies quality-preserving erasure; Hand and Brain directly overlaps agentic decision interventions. Generic rewriting, removal-cost curves and a SAT toy are not established novelty. Hand and Brain full-text/release access remains a material review gap.

**Feasibility/cost.** A controlled task with an exact oracle can support local scripted comparisons first. Hosted-model rewriting/adaptation is a later option after selecting task, models, call limits and expenditure. No inference count, statistical power or dollar budget has yet been established. Existing assignment prototype supplies a boundary demonstration, not the new study.

**Informative negative.** Cheap task-valid replacement defeats all tested semantic encoders; rewriting retains recoverable payload; or removal costs too much task utility. Each identifies a useful boundary. Neither successful examples nor unsuccessful attacks establish general channel closure.

## Compare before implementation

| Dimension | A: architecture | B: task-preserving rewrite |
| --- | --- | --- |
| Intervention point | Training and internal computation | Artifact after generation |
| Intended evidence | Compositional theorem plus useful task | Strong adaptive evaluation; theorem only for specified rewrite families |
| Main scientific risk | A sound property with little useful expressiveness | A failed decoder mistaken for erased information |
| Main resource risk | Proof/architecture engineering and eventual training | Strong reconstruction and adaptive attack inference cost |
| Nearest initial output | Primitive semantics, proposed invariant, theorem/counterexample | Task contract, explicit encoders, intervention and adaptation protocol |

Shared task-family shortlist: small constraint/planning tasks offer exact validity checks but have close watermarking precedent; executable programs offer richer utility but tests do not prove general equivalence; unrestricted prose has the weakest semantic preservation oracle. Do not pick the easiest family without stating the novelty and inference tradeoff.

These approaches can share an information-flow target and later benchmark, but should retain independent success criteria. A does not need B to work; B need not assume A is deployed. Next preparation: exact claim-versus-prior-art tables and a short specification for each. User endorsement of the two approaches is not authorization to start large training, paid inference or a full benchmark.
