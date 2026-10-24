# Revision preparation: can learned computation do useful work?

2026-10-24. Prepared while the baseline proposal is under adversarial review. Baseline proposal.md and sources.md are unchanged. This is a conditional construction and cost analysis, not a trained-model speedup result or novelty claim.

## Diagnosis of the baseline

The full-sweep shortest-path example does not establish a useful neural role. A learned permutation changes transient private state but every sweep still processes every edge; transformer scoring/ranking adds work. The all-weights correctness argument survives removal of the transformer. Improving this example requires a sound mechanism for avoiding actual work, not merely renaming an optimization as neural reasoning.

## A concrete alternative: bounded neural retrieval inside exact existential evaluation

Private input z contains N fixed-shape records and a descriptor c. Public task x asks whether any record satisfies an exact bounded predicate P(x,z_i). Authorized release is the Boolean F(x,z) = OR_i P(x,z_i). This is nonconstant private information. Neither a chosen record nor its index is an authorized release.

Inside a computational cell:

1. A bounded private transformer maps (x,c) to scores or a candidate record index j. It does **not** read all N records. A total verified decoder clamps/decodes every numerical output to one valid index.
2. A verified gather/predicate block checks P(x,z_j). If true, the exact answer is already known to be true.
3. If false, a bounded exact fallback checks remaining records and returns their OR. Early internal success is allowed; all return paths have the same declared external release slot and fixed output schema.

The learned component predicts where useful evidence is, so a successful prediction avoids evaluating many predicates. The verified component establishes semantic sufficiency of that evidence, rather than trusting the predictor. Every weight setting still returns F: bad weights can waste computation but cannot change the released answer. Private predicates, indices, branch status and cost remain private state. This is a cell-level architecture seed, not a claim to have built a new general language model.

The all-weights statement concerns security/correctness, **not performance**. Useful performance is conditional on prediction quality and cost. Public/private parameter and optimizer separation remains necessary.

## Explicit accounting

Let a predicate evaluation cost C_P and the entire neural inference plus decoding cost C_N. Descriptor acquisition/preprocessing must be included in C_N. Assume a positive-instance distribution with exactly one matching record, uniformly distributed to an uninformed sequential scan. Let the predictor hit with probability p. Conditional on a miss, assume the match is uniform among the remaining N-1 records. These are stated distributional assumptions, not measured facts.

- Sequential early-exit baseline: expected (N+1)/2 predicate checks.
- Neural candidate first: one check plus, on a miss, N/2 expected further checks; total expected cost C_N + C_P[1 + (1-p)N/2].
- Improvement requires C_N/C_P < (pN-1)/2.
- On negative instances, the candidate plus exhaustive remainder costs N checks, plus C_N overhead. Worst-case positive behavior also needs at most N checks plus C_N.

For N=1024, p=0.9 and an **assumed** neural/descriptor cost equivalent to 32 predicates, the expression is 84.2 predicate-cost units versus 512.5. These are algebraic scenario values, not measurements. If a predicate is cheap, a transformer reads the full dataset, the descriptor is expensive, or p is low, this gain can disappear. A trusted conventional index or context-aware symbolic heuristic may dominate; both must be baselines. This construction resembles learned indexing/guided search and is not asserted novel.

## Fixed termination versus observable cost

Reserve a release deadline covering the bounded neural computation and all N predicate checks. Internal completion may differ, but the abstract receiver sees only F at that slot. This permits fewer internal operations while preserving the stipulated receiver view. It does **not** improve client-visible latency when every client waits for that same slot, and reserving a whole exclusive device until release may prevent throughput gains.

If the receiver sees predicate counts, billing, shared-resource contention, power or early completion, the predictor can signal by intentionally hitting or missing. Padding all observable work can consume the apparent savings. Therefore the defensible claim is conditional internal-work reduction under a protected execution boundary. Actual deployment benefit and side-channel closure are separate unresolved obligations.

## What is and is not demonstrated

This provides a specific semantic role, an all-weights correctness argument and a testable break-even condition. It does not demonstrate a trained transformer advantage, a nontrivial new theorem, competitive utility against strong symbolic retrieval, or physical noninterference. The next useful check is whether an actual task supplies cheap predictive context and expensive exact predicates under an achievable isolation boundary. Without that, I cannot honestly claim the radical architecture has a useful learned advantage.
