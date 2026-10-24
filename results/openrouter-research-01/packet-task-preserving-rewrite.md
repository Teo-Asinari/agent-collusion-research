
<source path="research/reviews/outcome.md">
# Outcome of two adversarial review and improvement rounds

2026-10-24. Owner authorized an adversarial loop incorporating prior art. An independent reviewer inspected both proposals; each author revised after round 1 and supplied a final round-2 response. This document separates improvements in the research artifacts from achievement of the original goals.

## Architecture approach

**Before:** learned edge scheduling inside fixed complete graph sweeps. The exact result was schedule-independent, but the transformer did not avoid work.

**After:** an explicit bounded private predictor, verified witness evaluation and exhaustive fallback; public release depends only on the specified authorized result. The specification now enumerates state partitions, primitive accesses, total numerical/default behavior, fixed logical observations, public query authority and conditional-history composition. Predictor inputs and descriptor/preprocessing costs are explicit. Extensions require new semantic/confinement contracts.

**Surviving claim:** a defensible informal correctness/noninterference argument for this closed abstract machine, relative to the authorized answer history and declared receiver observations. The reviewer found no counterexample under those assumptions. No mechanized theorem or deployed implementation exists.

**Unresolved:** useful learned advantage against strong symbolic indices/solvers; novelty beyond architectural IFC, learned/verified search and delimited release; general language capability; executable/hardware refinement. The predictor can conditionally avoid predicate evaluations, but no measured overall benefit is established. Fixed releases and resource isolation may consume apparent savings. This remains a restricted architectural seed rather than the requested useful new language architecture.

## Task-preserving rewrite approach

**Before:** an evaluation agenda for equivalent program reconstruction, without a fully specified reusable-work sanitizer.

**After:** a concrete restricted construction verifies a uniquely determined shortest-distance certificate, discards the sender's chosen predecessor tree/comments and reconstructs one deterministic task-valid path. Invalid certificates invoke independent solving, yielding the same released content. Strictly positive weights and source reachability are explicit assumptions.

**Executed finite check:** all 280,000 bounded records for one fixed graph, including 14 valid and 279,986 invalid certificates, produce the same serialized path. Maximum pairwise content-distribution total variation is zero. If comment length and fallback status are exposed, maximum variation becomes one. This is an exact finite content-channel analysis, not a timing-secure service or an arbitrary-program result. Author executed the enumeration; reviewer and primary agent inspected the code/result and finite reasoning without rerunning it.

**Unresolved:** a general compact/useful-program reconstruction method, measured net reuse advantage, deployment observations and novelty. The fixed graph can be solved/hardcoded independently, so the enumeration does not demonstrate computational savings. Distance certification/canonical task release have close predecessors. The construction is a positive example of reusing unique checked information while replacing a nonunique witness, not a new general sanitizer.

## Prior art materially incorporated

The [review ledger](sources.md) and author ledgers record actual reading scope. Architectural IFC, LLMbda's total-program specialization, canonical task interfaces, delimited release, learned/verified search, certifying algorithms, regeneration/removal work and compiler search constrain contribution claims. New comparators include prediction-assisted certified shortest paths and indistinguishability obfuscation. The latter is a conditional computational result for equivalent size-matched circuits, not a practical statistical-zero sanitizer; general auxiliary-key/interactive coverage was not certified by the inspected definition.

No absence-of-prior-art or novelty claim follows from the searches. Inaccessible Hand and Brain full text remains a recorded review gap.

## What the loop accomplished

| Gate | Outcome |
| --- | --- |
| Concrete architecture rather than generic wrapper | Restricted internal computation specified; general capability unresolved |
| Precise information-flow target | Whole declared history, key/authority assumptions and failures specified |
| Concrete task-preserving removal | Executable finite certificate reconstruction supplied |
| Adversarial checks | Marginal-only/XOR, validation/fallback, quality thresholds and observable diagnostics addressed |
| Useful efficiency | Not established for either approach |
| Novelty | Not established for either approach |
| General or physical no-steganography guarantee | Not established |

Next substantive work must identify a useful capability and exact contribution beyond a named closest predecessor, or a consequential counterexample to an existing system. More toy enumeration or training a redundant neural component would not resolve those gates. Both approaches remain research directions; no full study or spending budget was selected.

Artifacts: [round 1](round-1.md), [round 2](round-2.md), [architecture proposal](../workstreams/architecture/proposal.md), [rewrite proposal](../workstreams/task-preserving-rewrite/proposal.md). No paid inference, training, dependencies or cloud deployment occurred in this loop.

</source>

<source path="research/workstreams/task-preserving-rewrite/proposal.md">
# Task-preserving reconstruction — final bounded revision 2

2026-10-24. Revised against [round-one review](../../reviews/round-1.md) and [round-two review](../../reviews/round-2.md). This is an exact finite-model construction plus a research proposal, not a general steganography-removal system. No paid inference, training or dependencies. [First response](revision-1.md), [final response](revision-2.md), [source scope](sources.md), [preparation](revision-preparation.md).

## Revised verdict

A complete, restricted sanitizer can reuse a sender-computed unique intermediate result, discard a nonunique witness carrying a payload, and reconstruct a canonical task-valid artifact. The construction below has identical content-channel rows over all 280,000 inputs in its declared universe, including invalid certificates. It uses established certifying-computation ideas; novelty and an efficiency advantage over a strong symbolic baseline are **not established**. Generic rich-code rewriting remains unresolved.

Round two found no material correction needed for this declared kernel. Acceptance is limited to the finite content model and informal argument; it is not proof-assistant certification, a deployment guarantee, or achievement of the original useful-artifact objective. The fixed graph can be solved or hardcoded without the submitted artifact, so enumerating its input records does not establish a useful computational advantage.

## 1. Fixed finite task and complete kernel

Trusted task x is a directed graph on vertices s=0,a=1,b=2,t=3 with edges (s,a,1),(s,b,1),(a,t,1),(b,t,1),(s,t,4). Vertex IDs, positive integer weights, source and target are public and outside sender control. Return a shortest s-to-t path. Both [0,1,3] and [0,2,3] meet the task; retaining the sender's selected path can carry a bit. The task does not require retaining that selection.

A submission y=(D,P,c) consists of four proposed distances D in {0,1,2,3,4}^4, three parent IDs P in {0,1,2,3}^3 for vertices 1,2,3, and a comment c in {0,1}^{≤2}. Thus the entire universe has 5^4·4^3·7=280,000 records. No extra files, RNG, persistent hidden state or sender-selected task facts are part of this model. Arbitrary malformed byte strings and transport withholding are outside this finite universe, not silently covered by the theorem.

The deterministic kernel R does:

1. Check D(0)=0, every public-edge inequality D(v)≤D(u)+w(u,v), and that each submitted parent edge exists and is tight. Evaluate all checks; do not return after the first failure.
2. If valid, retain D. If invalid, compute true distances from x using task-only, deterministic array Dijkstra. Never return the original artifact, an error symbol or a sender-dependent fallback.
3. Scan public edges. For each non-source vertex choose the lowest-ID predecessor satisfying D(v)=D(u)+w(u,v). Reconstruct the target's predecessor chain and serialize the path as exactly the UTF-8 bytes `[0,1,3]`, without extra whitespace or newline.

R has no random seed; all transition probabilities are 0 or 1. Its abstract outcome is exactly those bytes after a fixed logical release event. The supplied script computes and serializes those bytes. It is not an implemented transport or a physical timing guarantee.

## 2. Correctness and why this actually reuses something

For strictly positive weights and source-reachable vertices, the certificate conditions force D to equal the true shortest distances: triangle inequalities give the lower bound along any source path, and tight predecessor chains strictly decrease D until reaching the source, furnishing a matching path. The standard certificate is established prior art, not our theorem innovation. See the primary §2.4 reading in [sources.md](sources.md).

After validation, reconstructing from the unique D removes the sender's parent/tree choice. Positivity implies every reconstructed predecessor has smaller D, so it cannot cycle; at most |V|−1 predecessor steps are needed. Zero-weight cycles would require stronger certification and reconstruction rules, and are excluded here. The fixed graph has unique distances (0,1,1,2), although shortest paths are nonunique.

On a valid submission, the kernel consumes the computed distance labels and does not run an independent shortest-path solver. This is actual computational reuse through a unique checked intermediate, rather than copying a sender-selected subexpression. The invalid branch deliberately solves independently. It is a known-method composition, not a general transformation of arbitrary programs.

## 3. Complete row matrix, including failures

The following is the complete content-channel matrix in row-compressed form. Every record falls in exactly one category. A cell is its conditional probability, not its frequency in a random experiment.

| Input-row category | Number of rows | Release `[0,1,3]` | Any failure outcome |
| --- | ---: | ---: | ---: |
| Valid, comment length 0 | 2 | 1 | 0 |
| Valid, comment length 1 | 4 | 1 | 0 |
| Valid, comment length 2 | 8 | 1 | 0 |
| Invalid, comment length 0 | 39,998 | 1 | 0 |
| Invalid, comment length 1 | 79,996 | 1 | 0 |
| Invalid, comment length 2 | 159,992 | 1 | 0 |

All pairwise content-row TV distances are zero, hence their maximum is zero. This holds over all 280,000 declared records, not just two encoders or successful reconstructions. Two nontrivial valid structural encodings choose parent a versus b for t; both yield the same sanitized path. The seven optional comments provide additional syntax/payload choices. Fourteen rows pass validation and 279,986 invoke fallback; accepted distances have exactly one possible vector.

**Expanded-observation counterexample:** if V also contains (comment length, fallback flag), the six categories become six distinct deterministic outcomes; maximum row TV is 1. Two valid submissions of different lengths already distinguish perfectly in that diagnostic view. Invalid certificates that fail different checks also entail different comparison outcomes internally, even though the checker runs all listed constraints. We do not certify constant-time execution, memory access, exception behavior, resource effects or parsing.

## 4. Verification performed and cost accounting

[kernel_analysis.py](kernel_analysis.py) exactly enumerates the finite universe and verifies counts, unique accepted D, reconstructed outputs and row classes. Command: `python research/workstreams/task-preserving-rewrite/kernel_analysis.py`. It completed with all assertions satisfied. This is exhaustive analysis of a small executable mathematical model, not a proof-assistant result or a benchmark of learned encoders. Reported worst-case TV follows directly from the deterministic row classes; no quadratic pairwise loop is needed.

For the graph-family algorithm, valid-certificate checking and canonical reconstruction use O(V+E) arithmetic operations and no shortest-path search. Parsing adds O(L) for bounded submission length L. A binary-heap Dijkstra comparison baseline takes O((V+E)log V) operations, but this is not a lower bound on all symbolic algorithms or a bit-complexity statement. Small integers, heap overhead and task-family structure can eliminate any practical advantage.

For the actual four-node task, a strong baseline is task-only array Dijkstra, or a hardcoded answer if this single graph is the entire deployment. The latter needs no submitted work at all. We have **not** shown a net speedup on this task; certificate checking plus reconstruction may be slower than direct solving. Generalizing over many graphs would require fresh analysis and the strongest suitable baseline, including algorithms with predictions. Do not infer an efficiency contribution from the asymptotic comparison alone.

| Branch / guarantee | Reused work | Added cost and limitation |
| --- | --- | --- |
| Valid-record content theorem | Checked true distances | Parse, full certificate check, reconstruction; no established net speedup |
| All-record content theorem | Same fast path; independent solve on invalid records | Worst case includes full fallback; content guarantee still holds |
| Fixed logical release | Same content computation | Scheduler specification hides branch/status; not an implemented timing defense |
| Physical receiver view | Not established | Cache, energy, process behavior and wall time need additional enforced assumptions |

## 5. Keys, repeated use and conditional-history guarantee

For any key/side information k, each row releases the same C(x). Therefore this artifact adds no information about the payload conditional on x,k, even if a key already contains information about the payload. This is a property of the constant content kernel, not a cryptographic secrecy claim or an inference from independent marginals.

Repeated calls to this exact stateless kernel produce (C(x),…,C(x)), independent of every submitted record history. More generally a conditional-history formulation requires equal next-release distributions whenever authorized task/query histories and receiver histories agree. Public adaptive queries must be selected from those equal visible histories; sender-controlled secret-dependent queries are not allowed by this guarantee. Private caches, random-state reuse or hidden output-selection state would require new rules and proof.

The counterexample V1=r, V2=r XOR m has uniform individual marginals but reveals m jointly. It is not an execution of this kernel: neither output can be arbitrary r or r XOR m because every release must equal C(x), and no retained r exists in its state. A randomized extension would need a joint/conditional-history proof, not just single-message tests.

## 6. iO is a different formal route, not a practical fix

[Jain–Lin–Sahai, arXiv 2008.09317v1 §2 Definition 2.2](https://arxiv.org/html/2008.09317v1) gives function preservation and computational indistinguishability for equivalent circuits of the same size and input/output lengths. This undermines any claim that exact-program implementation choice can only be hidden by canonicalization or re-solving. Their result is conditional and computational, not statistical zero against unbounded receivers.

A comparison must specify public padding bounds, circuit conversion, randomness/metadata, evaluation and size overhead, and loss of source readability. Task-valid circuits computing different functions do not qualify. The displayed definition does not explicitly state an auxiliary-input/key game; we have not verified arbitrary key-aware or interactive extensions from it. No practical iO implementation or concrete runtime guarantee is proposed here.

## 7. What remains open and what to do next

The original rich-artifact objective remains open: an efficient reusable rewrite preserving useful code structure/cost while making all protected sender choices statistically or computationally unavailable. The finite-program candidate in the baseline is now a comparison setting, not a demonstrated sanitizer. Truth-table canonicalization costs exponential space in input width and may violate a compact-code contract; incomplete rewrite/e-graph closures need not have a common output law. A stationary law may be nonuniform: uniformity is not necessary, independence from protected choices is.

Closest precedents remain certifying algorithms, canonical task interfaces, Roger–Greenblatt regeneration, code watermark removal, quality-preserving random walks, superoptimization and iO. No novelty claim survives merely by combining their vocabulary. The earlier four-quality-output example remains an elementary definition check, not a contribution.

A next *proposed* check would compare valid-certificate reconstruction with strong task-only solving over a prespecified bounded graph family, including bad certificates and full diagnostic observations, before bringing in an LLM. If no useful cost advantage remains under the required observation model, report that negative and reconsider the task/construction. Do not expand into a full benchmark or paid model adaptation without choosing the scientific claim and budget.

</source>

<source path="research/workstreams/task-preserving-rewrite/sources.md">
# Primary sources and access scope

Accessed 2026-10-24. Targeted review, not exhaustive citation coverage or a proof/code audit. Prior workspace observations are cross-checked where indicated; source retrieval is not reproduction. No upstream code or PDFs are copied into this directory.

| Source / version | Scope inspected this pass | Relevance and limits |
| --- | --- | --- |
| [Roger & Greenblatt, Preventing Language Models From Hiding Their Reasoning, arXiv 2310.18512v2](https://arxiv.org/html/2310.18512v2) | §§5.2–5.3 and §7.2, evaluation framing | Already compares context-aware paraphrase with fresh answering and discusses generation/understanding limits. Bounded mitigation evidence, not universal closure. |
| [Zhang et al., Watermarks in the Sand, ICML 2024 primary paper](https://raw.githubusercontent.com/mlresearch/v235/main/assets/zhang24o/zhang24o.pdf); [ePrint version](https://eprint.iacr.org/2023/1776.pdf) | Indexed primary proof overview, quality-threshold random walk and Lemma 3 / theorem assumptions | Efficient mixing and quality-oracle assumptions matter. Watermark detectability/removal is distinct from full hidden-payload independence. Full proof not audited. |
| [Harel-Canada et al., Sandcastles in the Storm, arXiv 2505.06827](https://arxiv.org/abs/2505.06827) | Primary abstract; author [publication page](https://fabrice.harel-canada.com/publication/sandcastles/) | Tests practical rapid-mixing and quality-oracle assumptions. No new deep methodology or reproduction claim this pass. An attempted guessed ACL ID resolved to unrelated AgentRM and was discarded; no claim uses it. |
| [Kahng et al., Watermarking Techniques for Intellectual Property Protection, DAC 1998](https://www.cs.ucla.edu/~miodrag/papers/Kahng_DAC_98.pdf) | Primary PDF abstract/overview; prior workspace's §3.1/§4 findings retained with explicit attribution | Solution-choice constraints and removal by re-solving are established. Does not imply all practical sanitization is computationally hard. |
| [Yang et al., Towards Code Watermarking with Dual-Channel Transformations, arXiv 2309.00860v2](https://arxiv.org/html/2309.00860v2) | §§IV-A/B/D/E and discussion passages | Structural/identifier channels, adaptive removal and MBXP execution tests; unit tests are used instead of full semantic-equivalence proofs. No code execution. |
| [Krzyzanowski et al., Hand and Brain, OpenReview PDF](https://openreview.net/attachment?id=P7fHU7ZNFQ&name=pdf) | Search-indexed primary passages on semantic/syntactic decomposition; direct forum and attachment redirected to browser verification | Full text and released artifacts still unverified. Retain prior workspace's indexed §5/App A.6 adaptation observations; do not infer a missing adaptive setting from access failure. |
| [Pandey et al., Don't Judge an Agent by Its Messages, arXiv 2610.25032v1](https://arxiv.org/html/2610.25032v1) | Abstract, §V-C / Proposition V.3, §VI-D canonical interface | New close precedent: task-only canonical output yields leakage bounds, including keys independent of private state. Synthetic routing, not arbitrary rich-code reconstruction. Proof derivation not audited; model not reproduced. |
| [Mironov & Stephens-Davidowitz, Cryptographic Reverse Firewalls, ePrint 2014/758](https://eprint.iacr.org/2014/758) | Primary abstract only this pass | Protocol-specific replacement/rerandomization counters a universal recomputation requirement. No generic prose/code guarantee inferred. |
| [Schkufza, Sharma & Aiken, Stochastic Superoptimization, ASPLOS 2013](https://theory.stanford.edu/~aiken/publications/papers/asplos13.pdf) | Primary abstract/introduction | Equivalent program search with correctness and performance goals is established. No optimizer implementation or proof audit. |
| [Willsey et al., egg, POPL 2021 primary proceedings entry](https://popl21.sigplan.org/details/POPL-2021-research-papers/23/egg-Fast-and-Extensible-Equality-Saturation); [author PDF](https://homes.cs.washington.edu/~cnandi/docs/popl21-cr.pdf) | Proceedings abstract and indexed primary extraction overview | Equality saturation/extraction already searches equivalent expressions with a cost model. Saturation is relative to rules and resources; it is not automatically a globally canonical, input-independent sanitizer. |

Related workspace detail: [semantic erasure](../../semantic-erasure.md), [novelty audit](../../novelty-audit.md), [existing scoped prototype](../../../experiments/anti_stego/README.md). The latter was read, not rerun; its accepted-message projection property leaves semantic assignment choice and external observations outside the guarantee.

Search topics included exact paper titles, task-preserving reconstruction, adaptive code watermark removal, context-aware paraphrasing versus regeneration, canonical task interfaces, and compiler/superoptimization reconstruction. Search results on secondary summaries were used only to discover primary sources. The earlier task-preservation novelty concerns remain; the newly found canonical-interface paper makes generic projection an even weaker novelty claim.

Local analytical check: Python standard library, probability vectors p0=(1/4,1/4,1/4,1/4), p1=(0,0,1/2,1/2). Calculated TV=1/2, optimal binary recovery=3/4, MI=0.3112781244591328 bits. This is exact finite-model reasoning with a numerical logarithm, not empirical evidence about LLMs and not a claim of novel information theory.

## Revision-one additions and evidence limits

- [McConnell, Mehlhorn, Näher & Schweitzer, Certifying Algorithms, author preprint dated Aug 30, 2010, §2.4](https://people.mpi-inf.mpg.de/~mehlhorn/ftp/master-final.pdf): primary abstract and shortest-path certification conditions/proof read directly on 2026-10-24. The positive-edge distance certificate is established; our use of unique checked labels followed by deterministic witness reconstruction is a restricted composition, not a new shortest-path method. No formal-proof artifact executed.
- [Jain, Lin & Sahai, Indistinguishability Obfuscation from Well-Founded Assumptions, arXiv 2008.09317v1](https://arxiv.org/html/2008.09317v1), [primary PDF](https://arxiv.org/pdf/2008.09317): introduction, §2 Def2.2 and assumptions overview directly inspected on 2026-10-24. Equivalent equal-size/input/output-length circuits, function preservation, computational indistinguishability; no construction-proof audit or implementation. The displayed definition does not explicitly state an auxiliary-input game, so general shared-key/interactive claims are not certified here. ePrint 2020/1003 PDF retrieval returned 403.
- Executed `kernel_analysis.py` in this directory: exhaustive 280,000-record deterministic kernel analysis, full finite input universe and invalid/fallback records included. This is a scoped mathematical model, not a model/encoder benchmark or timing-secure service. Exact returned artifacts and row counts, rather than decoder trials, support its finite content claim.

</source>