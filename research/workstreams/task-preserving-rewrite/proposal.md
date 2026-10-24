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
