# Adversarial review, round 2

2026-10-24. Completed second-round review of architecture revision 1 and rewrite revision 1. This is a review of informal specifications and a finite executable kernel, not mechanical certification or deployment verification. See [round 1](round-1.md) and [source ledger](sources.md).

## Architecture revision 1

Reviewed normative proposal §§9–12 and `architecture/revision-1.md`, together with the retained baseline and preparation analysis. **Verdict: the restricted abstract security/correctness claim is defensible as an informal construction; the useful novel architecture objective remains unresolved.** I found no new counterexample to the closed machine under its declared admissible-input and observation assumptions. This is not acceptance of a deployed system or a proof assistant result.

| Round-1 objection | Review outcome | Residual obligation |
| --- | --- | --- |
| A1: decorative neural scheduling | Partially repaired and honestly deferred. Predictor-first existential search can avoid expensive predicate evaluations; the old full-sweep graph remains redundant. | No trained predictor, real descriptor/predicate cost or advantage against the strong symbolic/index baseline is established. Useful radical language architecture is not achieved. |
| A2: operational closure | Adequately repaired for an abstract specification: fixed-size inputs/registers, total default candidate, fuel bound, exact bounded predicate, fixed blank observations and release slot, restricted public G. | Semantics of executable neural arithmetic and implementation refinement remain unproved/unimplemented. Private physical cost is intentionally excluded. |
| A3: history composition | Repaired at the right level: next-frame kernel depends only on public history/state, current authorized answer and fixed receiver side information; adaptive receiver queries are covered by the induction sketch. | Mechanize the induction if a theorem claim is desired. Any new state/update primitive must preserve that kernel condition. |
| A4: authorized release/query authority | Repaired by explicit role and protected-state lists, positive authorized-flow and same-answer examples. | Facts/query authority and secrets already in fixed public parameters are excluded rather than solved. Keep this boundary in summaries. |
| Prior-art scope | Correctly narrowed. Existing architectural IFC, total-program LLMbda, task-only release and learned/verified search are retained as predecessors. | Per-history wording and interleaving alone do not establish novelty. |

### Checked reasoning

The exact candidate test returns true only on a genuine witness. Otherwise exhaustive checks of all remaining records compute the same OR for every candidate, including default candidates from fuel exhaustion or malformed neural numerical output. No predictor controls the release value, status or slot. With equal exact authorized answers and equal public state, G has equal permitted inputs. A common conditional public random tape therefore gives equal next frames/public state. Induction over receiver-chosen queries supports the stated no-extra-flow relation against the ideal authorized-answer history. The XOR two-round example violates this condition and is now explicitly ruled out, rather than dismissed using uniform marginals.

The cost expression compares **actual predicate evaluations** with a sequential scan under an assumed one-match distribution; it does not count the fixed idle schedule as a free throughput or response-latency improvement. The revised prose explicitly says fixed releases remove client-visible latency gains and observable resource padding may remove savings. This is an important correct limitation, not a proof defect to conceal.

### Two final precision requests

**A5 — small specification tightening.** Section 10 says the predictor does not first scan all records, while the phase table permits unspecified “private inputs.” Give the predictor's read signature explicitly, such as `(q,c,H,theta)` with no direct read of the records, or admit record reads and account for them in C_N. This is a cost/architecture precision issue, not a new confidentiality counterexample: reading private records within a private phase remains confined. If the descriptor is built from those records, charge its acquisition/update work and explain freshness. A cheap informative descriptor must not be assumed into existence.

**A6 — do not promote future optional primitives to achieved properties.** The finite construction permits only its exact OR witness predicate and bounded public G. A general learned semantic extractor, arbitrary generated code, free-form learned release or graph-data mutation is not covered by the same proof. Add a short “extension rule”: each new primitive needs a total semantic contract and a confinement/composition argument before entering the certified language. This prevents a plausible small construction from being narrated as a proven general transformer architecture.

These requests can be repaired by a bounded final clarification. A1 may remain explicitly unresolved; no training run is warranted merely to decorate the safe abstract machine. No new primary source was needed for this architecture recheck because it tests the revised operational argument and prior review acceptance gates.

## Rewrite revision 1

Reviewed the new seven-section proposal, response table, `kernel_analysis.py`, `kernel-analysis.json` and source additions. **Verdict: the deterministic content-channel claim is supported for the complete declared finite input universe. General useful-code reconstruction, efficiency and novelty remain unresolved.** No new counterexample was found within that finite content model.

| Round-1 objection | Review outcome | Residual obligation |
| --- | --- | --- |
| R1: unspecified reuse kernel | Repaired for a restricted certifying-computation example. Every valid certificate has the same exact distance vector; sender predecessor/comment choices are discarded before deterministic reconstruction. | This is no longer a general source-code rewrite method. A reusable compact-program sanitizer and useful computation savings remain open. |
| R2: failures/validation in the channel | Repaired for bounded-record content: invalid certificates invoke task-only solving and produce the same bytes. Expanded diagnostics explicitly reveal a channel. | Arbitrary malformed transport, nonarrival, physical time/resources and a real fixed-slot service are excluded. |
| R3: trivial canonical/strong baseline | Correctly acknowledged. Task supplies the graph rather than its distance labels, but the actual fixed graph can be solved/hardcoded without y. | No speed or novelty follows from checking 280,000 inputs; this is a proof/control example only. |
| R4: iO missing | Repaired with primary definition and limitations, including computational versus statistical security and unverified general auxiliary-key/interactive claims. | No practical iO sanitizer or efficiency statement is established. |
| R5: only selected encoders | Repaired for the explicit finite universe: every row is analyzed, not a finite learned decoder sample. | No inference about arbitrary code or unbounded artifacts. A larger graph-family or randomized kernel needs its own analysis. |
| Zero-weight cycles/reachability | Repaired by a stated strictly-positive, source-reachable graph restriction, with no claim of the zero-weight extension. | An extension must add the missing source-reachability/canonical traversal rules rather than reuse this proof unchanged. |
| Keys/history | Repaired for this stateless constant-content kernel. Conditioning on arbitrary receiver side information does not change its constant row. | General service composition requires equal conditional-history kernels; no arbitrary interactive iO theorem is inferred. |

### Checked finite argument and code

There are 625 distance vectors, 64 parent vectors and seven comments, giving 280,000 declared input records. The graph forces accepted distances (0,1,1,2). Parents of vertices 1 and 2 must be 0; the parent of 3 may be 1 or 2. Thus two parent choices times seven comments yield 14 valid rows. All remaining 279,986 rows use the independent solver. The code's `rewrite` function does not hardcode the returned path: it validates, selects either supplied labels or solver labels, reconstructs from the trusted graph and serializes the result. Both branches yield the same bytes `[0,1,3]`. The reported counts and constant-output channel matrix are consistent with the code and direct finite reasoning. I inspected code/results; I did not rerun the author's exhaustive enumeration in this review.

The strictly-positive graph condition makes every tight predecessor decrease the distance. Together with a predecessor for each non-source vertex, this rules out disconnected self-justifying cycles. Triangle inequalities and tight source paths establish exact labels. A public lowest-ID predecessor rule then determines the released path independently of the submitted tree. The implementation's fixed four-node graph is within that domain. This is substantively different from preserving the sender's chosen valid witness, although it uses a classical certificate.

All content-channel rows are the same point mass, so the maximum row TV is zero for all admissible encoders/decoders and arbitrary receiver key information. This is stronger than frozen-decoder failure but much narrower than a real-service information-flow theorem. When `(comment_length,fallback)` is included, at least two rows become distinct point masses, so max TV is one. The diagnostic result correctly exposes the observation-boundary limitation; it is not something the content-only claim silently covers.

### Cost and novelty verdict

The finite construction demonstrates **how unique verified intermediate information can be reused while a nonunique submitted witness is replaced**. It does not demonstrate a cost advantage: task-only hardcoding solves this fixed task, and validation plus reconstruction may cost more than direct shortest-path solving. The author now says this explicitly. For a positive-weight graph family, linear certificate checking is classical; [Certifying Algorithms §2.4](https://people.mpi-inf.mpg.de/~mehlhorn/ftp/master-final.pdf) directly gives the same shortest-distance certificate conditions. I inspected the abstract and §2.4, not the entire 94-page preprint. The citation adequately downgrades novelty.

The original useful-artifact objective is therefore still an open research direction. Accept the finite example as a transparent reusable-statistic mechanism and a test of failure/channel definitions; do not describe it as successful general task-preserving code rewriting or a new steganography-removal algorithm. No additional code correction is required for the declared kernel. Final author response should preserve these open gates and the exact content-only scope.

## Overall second-round assessment and final revision gate

The loop has improved precision and supplied real restricted mechanisms. It has **not** delivered a proven general language architecture, a task-preserving rich-code sanitizer, measured useful learned speedups, physical channel closure or established novelty. Both authors now acknowledge those limits rather than burying them.

For a final bounded revision: architecture should address A5/A6 above; rewrite should record acceptance of its finite-only verdict and keep the original compact-code/cost/contribution objectives marked unresolved. No further experiment is justified merely to turn these scoped successes into a stronger headline. The next substantive work must select a new useful capability or identify a consequential counterexample against a named prior system, with an exact contribution claim first.

### Final architecture clarification checked

After writing the architecture objections above, I inspected `architecture/revision-2.md` and the corresponding proposal edits. A5 is resolved at specification level: the predictor read signature is now explicit, records are immutable during an invocation, and descriptor/state build, refresh, scan and amortization costs must enter the ledger. A stale descriptor can harm prediction quality but not the exact checked witness result. A6 is resolved by §13's required primitive contracts and composition/refinement obligations. These are clarification repairs, not new measured capability or a mechanized proof. A1's useful-performance/contribution gate remains open. The rewrite author needs only a final response preserving the accepted finite-only verdict and unresolved original objectives; no material implementation correction was identified in the declared kernel.
