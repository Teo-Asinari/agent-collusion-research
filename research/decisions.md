# Decision log

## 2026-10-25 — owner-approved local architecture evolution

- Owner requested commit/push plus a different architecture/experiment and Lean
  verification. Prior-art review committed/pushed as `e08e7ca` first.
- Pre-execution [bilinear plan](../experiments/bilinear_network/PLAN.md): learn
  quadratic coefficients from fixed identification queries, then rank-factorize
  to learn both hidden maps. Existing lifting/decomposition prior art is explicit.
- One CPU-only exploratory run fit all 36 predeclared quadratic tasks and all
  87,396 unseen inputs. Direct quadratic solver ties; affine/lookup controls and
  failed cubic targets retained. This addresses exponential fitting on this
  family, not novelty, general learning or stronger security.
- Lean accepted generic information-flow/projection theorems and all twelve d=4
  learned-model certificates. Independent scalar/provenance audit passed.
  [Report](workstreams/architecture/bilinear-network/report.md); no paid calls or
  new full-study commitment. Training algorithm/Python/hardware not formally
  verified in general.

## 2026-10-25 — targeted residue-network prior-art check

- Owner requested prior-art comparison. Read primary polynomial-network,
  finite-ring fitting, canonical-interface and architectural IFC sources, plus
  standard ZMod projection code; ModuloNET remains abstract-level because its
  publisher full text was blocked. Author BasisLearner archive download failed.
- Current protection is standard projection through polynomial computation;
  the released answer equals direct modulo-3 computation. No new neural primitive
  or security theorem established. Updated report and living literature with
  [scope/version ledger](workstreams/architecture/residue-network/prior-art.md).
- No paid calls, cloud jobs, upstream execution or new experimental selection.

## 2026-10-25 — owner reaffirms architecture; first finite design loop completed

- Owner rejected the suggested EOD pivot to rewriting and explicitly insists on
  a neural architecture with proof on a small set and intelligent design iteration.
  The current EOD work is architecture. The independently run B pilot audit is
  preparatory only and does not select or launch a rewrite experiment.
- Built an exact residue-polynomial neural family with learned hidden weights,
  using modulo-9 arithmetic and a modulo-3 observer. Two hidden units/nine weights
  and a pruned one-unit/five-weight model each fit all sixteen two-bit Boolean
  functions. The formal-gradient attempts fit 10/16 and 6/16 respectively;
  exhaustive weight search fits 16/16 and is explicitly unscalable.
- Two-unit forward family: 11,337,408 cases, zero wrong answers. Pruned family:
  139,968 cases, zero wrong answers. Same-family repeats are not independent data.
  Final training-input checks call the actual learner on observed data, with
  separately exhaustive input/label lifts plus sampled joint combinations.
- Lean accepts arithmetic/composition, update-state and observed-learner
  noninterference properties, plus all learned finite truth-table certificates.
  Abstract semantics, not Python/hardware refinement. Axioms printed and retained.
- Plain-English report: `workstreams/architecture/residue-network/report.md`.
  This is a bounded verified candidate, not an established novel/general language
  architecture. The required encoding/release policy, unique-answer task, training
  search cost and direct modular/p-adic prior art remain material limits.
- Local CPU only; no new API/cloud spend or continuing budget. No additional paid
  experiment selected. Preserve both original approaches without switching back
  to B merely because its existing pipeline is convenient.

## 2026-10-25 — candidate algebraic primitive defined and challenged

- Owner requested a new algebraic neural primitive. Defined a candidate polynomial
  operation on the quotient of matrix factorizations by equal product; it consumes
  nonconstant represented information while discarding factorization choice in
  exact arithmetic. This is not established novelty or a selected study.
- Added explicit identity, composition/authorization assumptions, differentiable
  prototype and exact finite-field reference. Final local check covers 6,561 rows
  and same-product fibers, including singular cases. Hidden activation, protected
  coefficient, float64 and factor-SGD counterexamples expose real limits.
- Direct GL-equivariant LoRA and polynomial-filter prior art prevents claiming a
  new invariant layer from this definition alone. Source versions and incomplete
  repository/final-paper review are recorded in `workstreams/architecture/quotient-primitive.md`.
- No training, paid inference or cloud compute; local API/cloud experimental spend
  USD 0. Further work needs an exact-backend/training/capability delta over named
  predecessors. The earlier trained split block and finite chooser remain baselines.

## 2026-10-25 — first usable Modal neural-operation training completed

- Approved $1 setup/run reservation used for the planned synthetic recall
  feasibility check, with manual fixes and a cheaper T4 fallback. Four app attempts
  occurred: import failure; completed L4 training with lost output; L4 queue/stop
  race with no recovered output; successful T4 training. These are not four
  independent replications. No more cloud/inference spending is authorized here.
- Usable result: 137,696-parameter two-block model, 1,000 steps, batch 128,
  9.13 seconds inside training/evaluation, 1,024 synthetic test draws. Public and
  private heads, all finite gates and exact symbolic lookup score 100%. Private
  bit flips leave public logits equal. CPU checkpoint reload reproduces the result.
- This trains conventional attention/affine/normalization operations with separate
  public/private connectivity. It is not a language model or established new
  primitive. The easy public-only task provides no evidence that private neural
  computation or the bottleneck adds useful capability.
- Fixed remote-path handling and TorchVersion serialization; return JSON text and
  checkpoint bytes. Record call IDs with spawn and bound the entire wait at 600
  seconds. All four apps confirmed stopped with zero tasks. Actual Modal charges
  remain unknown; estimates are not relabeled as actual costs.
- Assessment, failures, metrics and checkpoint: `results/modal-operator-01-t4/`.
  Further work needs a discriminating capability/task contract, not more runs of
  this solved toy. Both architectural and rewriting research directions remain open.

## 2026-10-24 — first Modal training estimate approved

- Owner explicitly accepted the prepared $1 reservation for one bounded L4
  operation-training run, including setup. No larger experiment or continuing
  cloud/inference budget follows. Existing time/resource limits remain in force.
- Started Modal browser authentication with credentials directed to a private
  `/tmp/agent-collusion-modal.toml` file, outside the repository. Authentication is
  required before cloud launch; no credential values are recorded here.

## 2026-10-24 — integrate both workers; prepare bounded Modal training

- Owner requested committing everything, confirmed interest in worker branches,
  and asked for a Modal training run. Both branches are merged with original
  histories preserved; conflicts combine both ledgers and keep the larger proposer
  plus the recovery evaluation controls. Worker branches/worktrees are retained.
- Corrected the imported zero-leakage/zero-freedom assertion and README corpus
  licensing overstatement. Original worker outputs remain evidence, not endorsed
  conclusions. Recorded response costs across all six batches sum to $2.30376687;
  this is not a separately reconciled account invoice.
- Prepared `experiments/leak_cap/PLAN.md` and launcher: one L4, 1,000 steps,
  no retries, 600-second timeout, requested execution resources approximately
  $0.154 with proposed $1 reservation including setup. Installed SDK 1.2.6 in an
  isolated /tmp environment; no authentication, image build or remote run occurred.
- A 20-step CPU operation-training smoke run completed. All 25 local tests pass;
  Lean accepts the abstract choice bound. No new paid API requests or cloud cost.
- Next required actions for Modal: owner approval of this concrete estimate and
  local authentication. Earlier scale-up estimate of $15–17 remains separate.

## 2026-10-24 — neural operations and finite-choice baseline jointly endorsed

- Owner requires architecture down to linear algebraic operations, and explicitly
  endorsed incorporating the candidate-generator/chooser implementation alongside
  that work and proceeding with both. Rewrite approach remains active.
- Recovered Claude worktrees; main's earlier status missed additional artifacts
  and spend. Their ledgers require reconciliation before reporting a current total.
- Added split attention, separated normalization and private-gradient confinement,
  with a finite candidate gate. Four operator tests pass. Local Lean accepted the
  recovered abstract capacity theorem. No PyTorch-refinement or novelty claim.
- A bounded 64-example CPU evaluation completed using existing checkpoints, with
  zero model API spend. Results, limitations and next question are recorded in
  `workstreams/architecture/operator-and-choice.md`. No new training, Modal launch
  or paid inference occurred. No full experiment has been selected.

## 2026-10-24 — workspace initialization

- Authorized: new private repository on the authenticated GitHub account; preserve brief and exploratory research process.
- Research question: **unselected**. Candidate comparisons are proposals, not commitments.
- No experiment implementation, dependency installation, provider setup, model inference, or GPU provisioning is authorized by a candidate appearing in notes.
- Official starter remains an external reference; no upstream code is incorporated.
- Source inspection and literature synthesis proceed before selection.

## 2026-10-24 — initial landscape completed

- Created `https://github.com/Teo-Asinari/agent-collusion-research`, committed/pushed the initial workspace, and verified GitHub reports `visibility: PRIVATE`, `isPrivate: true`.
- Reviewed the official starter at `e6fb1308dae9cf97ae42aec1c5f7889d9e2291e8`; kept source external in a temporary inspection directory. Did not install dependencies or run upstream experiments.
- Recorded a selective primary-source landscape, explicit review depth, source/code availability limitations, and comparative candidate designs. Candidate rankings are provisional judgments, not a selected project.
- A tiny arithmetic feasibility check found the audit starter's permutation-null statistic invariant to its shuffle. No upstream code modification was made.
- Owner subsequently supplied an OpenRouter credential. Stored it only in local ignored `.env` (0600); no provider requests or paid inference performed. No budget/model selected.
- Next scientific decision remains which uncertainty to prioritize; no full experiment should be built until that discussion selects a question.

## 2026-10-24 — OpenRouter authentication check

- At the owner’s request, checked the saved key against OpenRouter’s authentication endpoint. It returned HTTP 401 Unauthorized. A valid credential is needed before inference. No model calls or experimental expenditure occurred.

## 2026-10-24 — corrected OpenRouter credential verified

- Replaced the local ignored credential with the owner’s correction. Authentication endpoint returned HTTP 200; key-level limit and remaining limit both USD 100, usage USD 0. No paid inference was attempted. The key limit is not an approved experiment budget or independent account-balance verification.

## 2026-10-24 — clarified research focus and knowledge assumptions

- Owner clarified interest in practical barriers to theoretically undetectable steganography. Earlier candidate preferences for restriction/causal auditing are not the current research priority and were never a selection.
- Discussed speculative alternatives: auditor feedback aiding synchronization, interference between concurrent covert protocols, ambiguity from multiple public implementations, and detectability during channel formation. Novelty unverified; none selected.
- Owner requested primary-source verification of whether all approaches assume common private knowledge. Added `research/shared-knowledge.md`: pre-shared secrets are not universally required; distinguish public-key systems, covert establishment of session secrets, training-derived conventions and public decoding.
- Corrected conceptual framing: a secure setup transcript need not expose “courtship”; theoretical covert key exchange already addresses that possibility. Practical formation traces remain a conditional empirical proposal.
- No experiment or inference was run.

## 2026-10-24 — active-defense prototype authorized and implemented

- Owner requested research into assumptions of the keyless construction, then supplied the cache/RAM timing example and requested actual creation of anti-steganographic protocols. This authorizes the scoped prototype; earlier exploration-only instructions are updated for this action.
- Verified cache-timing example against OpenAI's primary Oct 23 report, including elicitation caveats. Recorded keyless assumptions separately.
- Built a local standard-library assignment-release broker with syntax normalization, semantic projection, defender-controlled rerendering and public-task replanning. All six scripted encoders work before intervention; task-choice encoding deliberately survives projection.
- Ran eight tests and 256 balanced trials per cell (six carriers × five modes, 7,680 logged records), with model spend USD 0. These are feasibility controls, not evidence of autonomous behavior, real hardware isolation, or a novel universal defense.
- Full hackathon question, model-based/adaptive evaluation and inference budget remain unselected. Prototype boundaries and reproduction instructions are recorded with the artifacts.

## 2026-10-24 — reference iMEC and mathematical framing

- Owner identified the original iMEC repository as a concrete example. Inspected pinned source and ran its original selected numerical/encoder/decoder definitions with our four-symbol carrier adapter. Recovered `Hi` exactly. This was not a GPT-2 reproduction, optimality/security certification, or autonomous-agent study. No dependencies installed; no inference spend.
- Added a reproducible inspection runner without vendoring upstream source. Documented stale standalone-demo calls, actual harness path, shared setup assumptions and approximate coupling implementation.
- Owner asked about knot theory, topology and complexity connections. Recorded equivalence-class release, transformation invariants/mixing, noninterference/hyperproperties and complexity distinctions. These are candidate tools, with existing literature acknowledged; no full study selected.

## 2026-10-24 — synchronization interest and terminology correction

- Owner expressed interest in disrupting synchronization and asked about LLM nondeterminism and alternative optimal schemes. Clarified deterministic ideal probability calculation versus random sampling and actual numerical reproducibility limits.
- Avoid labeling the practical iMEC implementation “theoretically optimal” without qualification: its approximate coupling routine is distinct from the optimality characterization. Added targeted alternative-scheme references and a possible synchronization study, without selecting or running a new experiment.

## 2026-10-24 — expanded secure-steganography review

- Owner authorized deeper review of Zamir, SparSamp, Shimmer, Wang–Moulin and related prior art. Completed a bounded primary-source comparison with an explicit reading-depth and provenance ledger; this is not an exhaustive survey, full proof audit or model reproduction.
- Inspected pinned Zamir source and retrieved SparSamp/Shimmer artifacts. Recorded research-code randomness caveats. Verified that the SparSamp v4 experimental path substitutes saved encoder intervals on mismatches, whereas Basic Test recomputes independently.
- Added Codetta, BAM, Alkaid, finite-precision detection, ANStega, classical active-warden theory and semantic/resynchronization defenses. Corrected the universal-model-matching framing and distinguished Codetta's algebraic key-exchange simulations from live exchanges.
- Revised candidate questions around isolated decoding, utility-constrained interference/repair costs, and trusted release randomness. No new experiment selected or run; no paid inference, model downloads, dependency installation or GPU allocation.
- Corrected a collaboration-status error: a final response saying work was underway did not correspond to any running background job. Future status reports must distinguish completed work, an actually running tool process and work that has not started. No background continuation is implied after a final response.

## 2026-10-24 — semantic choices and erasure-cost prior art

- Owner questioned the narrow focus on token-sampling schemes and authorized research into substantive choices and whether erasure requires redoing useful work.
- Found direct conceptual predecessors in Roger–Greenblatt, semantic-unit/codebook implementations, and Conceptual Steganography. The generic replacement-capability intuition is not new.
- Reviewed targeted primary sections of Watermarks in the Sand, Sandcastles in the Storm, Perry et al., steganography-free ZK, and a source-code transformation proposal. Inspected a pinned semantic-steganography manuscript and selected citation-channel source functions. Cryptographic reverse-firewall/unique-proof abstracts and solution-reconfiguration theory supply qualified adjacent leads, not completed proof audits.
- Recorded the distinction between preserving submitted meaning and preserving original-task quality. Added a candidate comparison of local edits, global replacement and cheap-rerandomization controls. No full experiment selected or run; no model calls, API expenditure, dependency installation or GPU allocation.

## 2026-10-24 — novelty audit materially downgrades broad proposal

- Owner explicitly requested further prior-art search to ensure new ground. Expanded into constraint-based IP/design watermarking, abstract interpretation, cryptographic program watermarking, code de-watermarking and AI control.
- Verified direct overlap with Kahng et al.'s 1998 SAT/solution-selection and re-solving-cost discussion. Located closer 2026 agentic-defense prior art (Hand and Brain) through indexed primary passages, while direct full-text/API access remained blocked. Recorded the synthetic math/particular-decoder qualifications and existing post-hoc codebook adaptation.
- Updated candidate/research headers: generic semantic-choice, SAT/local-search, and erasure-cost framing does not establish novelty. No full experiment should be selected on that premise. Future work needs an explicit extension/counterexample or narrower result against the closest prior art; no new project selected.
- Added source/access/query ledger. No inference spend or experiment execution; source inspection only.

## 2026-10-24 — physical isolation and constrained-interaction prior art

- Owner proposed physically preventing steganography and requested both isolation and useful constrained-interaction directions. Included robot embodiment as a separate interpretation.
- Reviewed targeted primary sources on deterministic execution, seL4 time protection, thermal and robotic motion channels, and collusion-free physical/mediated protocols. Added abstract-level formal time-protection, AutoCC and runtime-assurance references with explicit scope.
- Recorded key limits: 2019 hardware/time-protection assumptions, generic-model versus complete deployed-system verification, external timing rate limits, physical channels excluded by the 2005 protocol theorem, and the single abort-presence bit allowed in the 2009 mediated model.
- Both broad directions have established prior art. Preserved exploratory candidates with controls and feasibility limits; no claim of a novel universal steganography-free environment, no full project selected, no hardware deployment or model experiment.

## 2026-10-24 — formal hybrid architecture remains exploratory

- Owner asked whether formal methods could yield an LLM architecture that never uses steganography or colludes. Reviewed close primary precedents and recorded precise guarantee targets and assumptions in `formal-hybrid-architectures.md`.
- LLMbda already supplies machine-checked probabilistic noninterference with termination qualifications; Fides explicitly leaves control-flow/side channels outside its secrecy guarantee. No broad novelty claim, implementation or selected study follows.

## 2026-10-24 — clarified ground-up neural and verified architecture scope

- Owner clarified that the intended system interleaves/restructures transformer computation and verified code from the ground up, rather than monitoring an ordinary LLM with external tooling. Current focus is prevention of steganographic transfer.
- Recorded proposed architecture-preserved invariants covering inference, training, release, randomness, recurrence and deployment assumptions. Located transformer-level IFC precedent (Tiwari et al., USENIX Security 2024) and adjacent architectural proof/Vehicle work with reading limits.
- This clarification does not select a full study or establish a new theorem. Future proposals must respect the architectural scope and compare against learned-model IFC, not only agent wrappers.

## 2026-10-24 — two anti-steganography approaches endorsed

- Owner requested developing both a ground-up transformer/verified-code architecture and steganography removal by rewriting with task preservation. This is an active two-approach agenda; neither should displace the other by default.
- Added design seeds, prospective proof/evaluation targets, baselines, controls, confounders, costs and informative negatives. The architecture approach concerns internal computation/training; rewrite preservation is against the original task, not automatic retention of every submitted choice.
- Specific task/theorem/full experiment and model budget remain unselected. No inference, training or new experiment launched. Closest precedents continue to constrain novelty claims.

## 2026-10-24 — both delegated first research passes completed

- Owner explicitly authorized two agents, one per approach. Both produced proposals, reading-scope/source ledgers and completed checklists under `research/workstreams/`.
- Architecture: internal learned scheduling and verified exact updates support an informal authorized-release/noninterference argument. A finite 64-graph check covered 614,227 schedules. No general mechanized theorem or useful neural advantage was established; complete sweeps retain the exact work and add neural overhead.
- Rewrite: recommended bounded executable programs with exhaustive functional validation and a task-fixed cost ceiling. A four-output analytical example retains 75% optimal bit recovery when the preservation threshold depends on the submitted artifact. This is a sanity check, not a new theorem. Further canonical-interface prior art narrows novelty.
- Primary agent inspected the drafts and finite-check source. No paid inference, training, dependency installation or full experiment. Proposed next checks remain proposals; novelty is unestablished for both approaches.

## 2026-10-24 — two-round adversarial review and revision

- Owner explicitly requested an adversarial review/improvement loop incorporating prior art. Ran an independent reviewer across both workstreams, with two author revision rounds and source-scope ledgers.
- Architecture now specifies a closed bounded predictor/verified-witness machine and conditional-history argument, with explicit preprocessing cost and primitive extension obligations. Learned utility, novelty and mechanical/deployment verification remain open.
- Rewrite now supplies an executable finite certificate-reconstruction kernel: all 280,000 bounded content rows agree including invalid-input fallback; exposing length/fallback diagnostics creates a perfect distinguishing channel. This is not a general code sanitizer, cost advantage or physical-security result.
- Added close certifying-algorithm, prediction-assisted algorithm and iO comparisons without novelty claims. No paid inference, training, dependency installation or full study. Detailed disposition and unresolved original objectives are preserved in `research/reviews/outcome.md`.

## 2026-10-24 — first bounded OpenRouter research batch authorized

- Owner explicitly accepted the proposed $5 total ceiling for 12 cross-family proposal/critique/revision calls across both research approaches. This supersedes earlier no-budget status only for this batch, not a full experiment or training run.
- Verified authentication and targeted current endpoint pricing; selected Sonnet 4.6 and Gemini 3.1 Pro Preview with pinned providers. Built a conservative reservation/accounting runner; six local spending-state tests passed. Source packets exclude credentials and preserve prior-art/claim limits.
- Prepared plan and metadata under `results/openrouter-research-01/`; actual execution and independently assessed outcomes will be recorded next. No model-written proof or novelty claim will be accepted without checking.

## 2026-10-24 — approved OpenRouter batch completed and independently assessed

- All 12 planned calls completed with pinned Anthropic Sonnet 4.6 and Google AI Studio Gemini 3.1 Pro Preview. Actual charge $0.601760, reconciled with key usage after an initially delayed usage snapshot. No retries or further model requests.
- Critiques correctly caught selective proof-success signaling and a minimum-record initialization bug. They also made false mathematical objections and unsupported global complexity/utility claims; final model revisions sometimes accepted those errors. Primary-agent checks and primary AKS/mathlib references correct these claims.
- No useful novel architecture or general sanitizer was established. Neither original research direction is abandoned on the basis of model consensus. Assessment preserves exact prompts/responses, raw versus accepted claims, source-reading scope and reproducible elementary counterexamples.
- The one 12-call allowance is complete. Unspent dollars do not imply authorization for another batch, a full experiment or training. See `results/openrouter-research-01/assessment.md` and compute ledger.

## 2026-10-24 — parallel A/B workers and $5 batches

- Owner authorized parallel agents for Approach A and Approach B, with OpenRouter spend in **batches of $5 hard cap per batch per agent**. Each batch needs a stop-and-report before the next; this entry authorizes exactly one $5 batch for the B worker.
- B framing is the worker's default, not an owner selection: the component-label question from `research/workstreams/task-preserving-rewrite/local-rewrite-obstruction.md`. Preregistered in `research/workstreams/task-preserving-rewrite/component-pilot-prereg.md` before any paid call. The pilot is exploratory.
- Models: `openai/gpt-4.1-mini` (openai) and `qwen/qwen3-235b-a22b-2507` (deepinfra/fp8). They were chosen as cheap, non-reasoning, seed-supporting endpoints from different families, so the pilot can have 120 task units. The worst-case reservation is $2.52 for 1,440 calls.
- Deviation from the 01 runner: a failed HTTP call keeps its reservation and is recorded as a failed unit rather than halting at once; the run halts after 20 failures, on any reservation overrun, or on an answer without reported cost.

## 2026-10-24 — B batch 1 complete

- `component-rewrite-pilot-01` completed 1,437 of 1,440 calls for a reported $0.658566. The batch is exhausted as planned; unspent dollars do not authorize more calls. See `results/component-rewrite-pilot-01/assessment.md`.
- Exploratory finding: in valid outputs, paraphrase, minimal edit and task-conditioned rewrite preserved the component payload at about 1.00. An explicit "choose independently" sanitizer still left 0.72–0.84. Task-only resolve was at chance.
- Major confound: the 600-token limit truncated most re-solving outputs, so validity comparisons between arms are biased toward draft copying. A larger-token rerun of three arms is proposed as the next $5 batch, pending owner approval.

## 2026-10-24 — B batch 2 authorized (pilot 02)

- The owner, relayed by the coordinator, approved one new **$5 hard-cap batch** for the proposed 720-call rerun: task-only resolve, tc_sanitize and instructed sender; max_tokens 2,500; fenced final answer. Same rules apply: no retries or fallback, halt on unknown cost, no further batch without approval.
- Tasks, payloads, train/test split, models, prompts (apart from the answer-format line) and receiver are unchanged from pilot 01. The prereg addendum is in `component-pilot-prereg.md`. Worst-case reservation is $4.383743.

## 2026-10-24 — B batch 2 halted

- Pilot 02 halted by design after 21 qwen HTTP 429 errors: 294 of 720 calls, reported $0.317218. No retries or restart; batch 2 is closed.
- Only training-split tasks 0–48 ran, so the preregistered held-out analysis is empty. A deviated direct-decoder analysis (no fitted parameters) is in `results/component-rewrite-pilot-02/assessment.md`. At full validity, gpt-4.1-mini's warned sanitizer still recovered 0.73 [0.64, 0.81] against resolve's 0.54. Qwen's result was weaker.
- Proposed next batch: finish tasks 49–119 (426 calls, about $0.5, worst case about $2.6), with qwen concurrency reduced. Not authorized.
## 2026-10-24 — parallel A/B workers and $5 batch authorization

- Owner approved running Approaches A and B in parallel with separate agents, and OpenRouter spending **in batches of $5 hard cap per batch per agent**. Each agent may spend one $5 batch, then must stop and report before any further batch. Ample key credit is not a standing budget.
- Approach A worker (branch `worktree-agent-ad39c5a2861e07835`) is scoped to: a small formal model of a compartmentalized learned/verified architecture, at least one composition lemma, invariant-ablation counterexamples, and a non-vacuous useful task. OpenRouter use for A is optional and limited to discriminating critique.

## 2026-10-24 — Approach A batch 1 completed

- Built a labeled SSA dataflow model (parameters/optimizer state as wires; one contracted release edge), an informal noninterference-by-typing proof with a composition lemma, z3 instance checks over every interpretation of learned functions, five single-invariant ablations each with a z3 payload-only counterexample, and 5,000-program fuzzing (0/771 leaky accepted by the full checker). See `research/workstreams/architecture/formal-model.md`.
- Non-vacuous task: a certified learned index (N=16,384) answered every query exactly, using 3.69 vs 13.76 mean probes. Owner-requested timing analysis: the value guarantee holds for all weights, but visible work does not. Unpadded and radius-padded (sender-chosen parameters) costs leak the payload. Worst-case padding and fixed-slot release remove both the leak and the visible gain. Only a canonical trusted fit keeps a visible 3× gain with no payload flow, at the cost of declaring g(z) and trusting the learner.
- Spent $0.268 of the $5 cap on three cross-family critiques. Accepted repairs are implemented; no critic found a counterexample. No novelty claimed; the value/work split is standard constant-time practice applied to learned parameters.

## 2026-10-24 — Approach A batch 2 authorized

- Owner approved one new **$5 hard-cap** OpenRouter batch for Approach A: mechanize Theorem 1 (composition lemma if time permits) in Lean, primary-source check of timing-mitigation and learned-systems references, and 2–3 cross-family critique calls on the mechanized statement with a larger output limit and capped reasoning. Lean toolchain installed under `~` (core Lean, no mathlib unless needed; under ~3 GB).
- Batch 2 complete. Lean 4.35.0 core (elan under `~/.elan`, 3.0 GB, no mathlib) checks Theorem 1 (`ni`, `ni_init`), the payload corollary (`payload_ni`), composition (`ni_compose`), the witness contract for all N, a concrete well-typed witness architecture with a payload-noninterference proof, and necessity examples. No `sorry`; axioms are `propext` and `Quot.sound` only. Primary sources checked: Askarov–Zhang–Myers CCS 2010 §2.2–2.3 and Kraska et al. §2/§3.4; Agat 2000 abstract only. Three critiques ($0.222) all returned faithful-with-caveats with no soundness error. Scope narrowed (non-adaptive sessions; semantic release isolation) and the concrete instance added. Not mechanized: the timing analysis, the learned-index contract for general N, and the IR-to-Lean correspondence.

## 2026-10-24 — Approach A batch 3 authorized

- Owner approved one new **$5 hard-cap** OpenRouter batch (same rules) to lift the Lean model to multi-agent orchestration. LLM calls are opaque ops; tool calls are trusted ops; verified tool outputs are releases; scheduling and slot timing are a cost release. The model needs at least a sender, a receiver and an orchestrator with shared state as labeled wires. Deliverables: a primary-source comparison with CaMeL and FIDES, a Lean proof of agent-level payload noninterference, and private randomness handled where feasible.
- **Batch 3 stopped (2026-10-24) by owner instruction.** Committed as WIP: the Lean multi-agent section (`Arch.Agents`, compiles, no `sorry`) and the CaMeL/FIDES comparison (`research/workstreams/architecture/agents-camel-fides.md`). The three critique calls had already completed when the stop arrived ($0.23681025). Their outputs are saved **unassessed** in `results/arch-a-batch-03/critique/outputs/`. No further paid calls for this work.

## 2026-10-24 — Owner correction: new neural architecture with a provable leak cap

- Historical worker framing: the brief asked for a **new neural architecture**
  (ground-up transformer + verified computation), not a rules framework with a
  stand-in regressor. Its additional assertion that zero leakage forces zero
  freedom is rejected: trusted randomness and public task computation can vary
  without protected influence. Bounded leakage remains an endorsed design target,
  alongside operation-level architectural work, not an established necessity.
- New goal: design, implement and train (CPU, toy scale) a transformer architecture with real freedom and a **provable cap of k bits per answer**. Seed: every receiver-visible output is TrustedDecoder(public input, public randomness, c), where c is a k-bit code from the untrusted network. Prove in Lean that c is the only private-to-public path, plus the capacity bound. Measure utility versus k against an unrestricted transformer of matched size; show a scripted adversary gets about k bits and no more; check prior art first. Budget: the remainder of the batch-3 $5 (≈ $4.76). No Modal; write a Modal plan with a cost estimate.
- Delivered, with no paid calls (≈ $4.76 unspent).
  - Lean `Choice.view_count`: for every weight setting, the receiver's view has at most 2^(Σk) values.
  - CPU toy run on word denoising, trained from scratch: with a 105k-parameter public proposer, k = 5 bits per answer matches the unrestricted 605k model (29.2% vs 29.7%), and k = 8 reaches 35%.
  - The scripted adversary received ≤ k bits.
  - Modal plan (≈ $15–17) is written and not executed.
  - See `research/workstreams/architecture/leak-cap.md`.

## 2026-10-25 — submission report and public repository

- Owner asked to consolidate leak-cap and anti-stego work into the sprint
  submission: `submission/report.tex` / `report.pdf` (7 pages incl. appendices).
  Tables come from saved `results/leak-cap-01` and `results/anti_stego` JSON.
- Owner approved making the repository public. History scanned for keys/tokens
  before the change; only placeholder `.env.example` values and OpenRouter
  usage/limit snapshots were found.

## 2026-10-25 — adaptive LLM colluders (Experiment 4)

- Owner asked for an aggressive experiment with real LLMs and approved a $30
  cap. Ran `experiments/adaptive_collusion` per its pre-written plan.
- Held-out: none 7.94 bits, paraphrase 0.55, broker 0.06 (chance, 49%
  rejected), menu 2.97 (at the proved 3-bit cap). Menu raised honest utility.
- Added to the submission as Experiment 4. Instructed, in-context colluders
  only; the broker result is not a bound.
