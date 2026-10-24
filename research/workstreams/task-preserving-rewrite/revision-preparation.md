# Revision preparation: efficient reuse versus hidden sender dependence

2026-10-24. Prepared while round-one adversarial review reads the baseline proposal. This file does not modify that baseline. No benchmark, paid inference, dependency installation or git mutation. The constructions below are restricted mathematical examples, not a new practical general sanitizer or a novelty claim.

## 1. There is a real positive case: reuse a uniquely certifiable intermediate result

Consider a finite directed graph G with publicly labeled vertices, strictly positive bounded integer edge weights, source s, target t, and every vertex reachable from s. The task is to return a shortest path. A sender submits distances D and a shortest-path tree. A standard certificate checks D(s)=0, triangle inequalities on all edges, and a tight incoming justification edge for each non-source vertex. Positivity makes justification chains decrease to s; accepted D is the unique true distance vector. This certificate and its correctness argument are established in [McConnell et al., Certifying Algorithms, §2.4](https://people.mpi-inf.mpg.de/~mehlhorn/ftp/master-final.pdf), inspected directly.

To sanitize, discard the submitted tree and reconstruct it by choosing the lowest-public-ID tight predecessor at each vertex. Release only the reconstructed path in one serialization. Thus valid certificates yield a unique result C(G); any shared receiver key cannot recover an independent payload from that constant result. Verification and reconstruction take O(V+E) arithmetic operations, versus the usual binary-heap Dijkstra baseline's O((V+E)log V). This is a baseline comparison, not an optimal-algorithm lower bound or a bit-complexity claim.

The new application reasoning here is that a verified *unique intermediate* permits reusing sender computation without reusing the sender's nonunique witness. It is closer to certifying computation followed by canonical reconstruction than to stochastic rewriting. It does not establish a novel algorithm; certifying shortest paths is old. Its usefulness is to disprove an overly strong premise that erasure always requires solving from scratch.

**Fixed example.** G has edges s→a=1, s→b=1, a→t=1, b→t=1 and s→t=4, with a<b. Both sender paths s,a,t and s,b,t are optimal and can encode a bit. Accepted labels must be D=(0,1,1,2). Reconstruction always releases s,a,t. The defender verifies the supplied labels rather than rerunning shortest-path search. On this single fixed graph one could hardcode the answer, so the example establishes the mechanism only; cost claims concern the graph-family algorithms.

**Task scope.** This works when the legitimate requirement accepts any shortest path. If it requires the sender-selected path or a particular tie-dependent explanation, replacing that choice may violate utility. It also requires a correct, complete distance certificate. An optimal path alone need not furnish the verification/reconstruction advantage.

**Invalid inputs and all-attempt guarantees.** A sender can signal by submitting a valid certificate for 0 and an invalid one for 1 if the receiver observes rejection. Extending beyond the valid-submission domain requires a task-only fallback that computes the same C(G) on failure, and a fixed modeled release protocol hiding branch/status differences. Then content is independent of the submission, but worst-case compute includes independent solving. Padding the release time does not hide cache/energy/resource observations; those require separate assumptions. Deliberately crashing the sender, withholding the message and overrunning its input slot must also lead to the same fallback if covered.

This separates three claims: valid-input content erasure with cheap reused certificates; all-input content erasure with a potentially expensive fallback; and full-observation noninterference requiring enforced execution assumptions. They are not interchangeable. Timing padding can preserve a computation/energy saving while eliminating a latency saving; even that depends on resource isolation and what is measured.

## 2. For arbitrary executable artifacts, cheap common reconstruction is not supplied for free

For the baseline's b-bit total-function DSL, an exact canonical representation is obtained by evaluating y on all 2^b inputs and rendering the truth table with a fixed interpreter. Cost is O(2^b·T_y), with table size Θ(2^b) output words. Every accepted implementation of the same function yields identical released content. This reuses execution of y; it does not search for a new algorithm. A full finite task specification still has to establish which function is correct.

This construction is inadmissible if the original task requires a compact program or low evaluation cost that a lookup implementation violates. Obtaining a small canonical program from the table becomes synthesis, with no generic cheap construction established here. An exhaustive search with fixed order supplies a conceptual endpoint only when its time budget and fallback are independent of y. Treating b as tiny makes enumeration feasible, not novel.

Ordinary equivalence-preserving rewrites are much weaker. For instance, if the implemented rewrite rules do not connect x+x to x<<1, a sender can select those two equivalent expressions, and a normalizer can deterministically preserve the bit. Equality saturation only explores the closure of the supplied rules within its resources. Even complete exploration of that closure is not completeness for semantic equivalence. Random selection from two different explored sets also need not yield a common distribution.

A sanitizer need not be uniform, canonical or select a shortest program. It needs a *common output law* across the protected inputs in its guarantee domain. A shared law can be arbitrary and nonuniform. Uniform sampling of all task-valid programs is one sufficient special case only when its domain, size bounds and sample generation are well defined. Neither sound rewriting nor fresh RNG establishes it.

For fixed task x, if some submitted programs implement different task-acceptable functions, functional equivalence within each class cannot erase the choice between those classes. Requiring preservation of each program's behavior may make this an impossible objective. The preservation relation must say whether behavior or only the broader original-task objective is fixed.

## 3. Computational alternative: indistinguishability obfuscation

[Jain–Lin–Sahai, arXiv 2008.09317v1, §2 Definition 2.2](https://arxiv.org/html/2008.09317v1) specifies functional preservation and computational indistinguishability for equivalent polynomial-size circuits with equal size, input length and output length. Thus exact statistical equality/canonicalization is not the only formal route to hiding implementation choice. Their result is conditional on cryptographic hardness assumptions; it is not a practical sanitizer here.

The comparison requires public size bounds/padding, circuit conversion, and a declared evaluation/size overhead budget. Task-valid but functionally different circuits are outside this equivalence guarantee. Shared keys/auxiliary receiver information must appear in a matching security experiment: the displayed definition does not explicitly state an auxiliary-input game, so arbitrary keyed-channel closure is not certified by this inspection. Statistical zero and unbounded-receiver security do not follow. Runtime, aborts and release-selection behavior are separate.

Access: primary arXiv HTML and PDF readable; ePrint 2020/1003 PDF returned 403. Definition/introduction inspected, construction proof and concrete performance not audited. Do not rebrand this comparator as a practical implementation plan or a new result.

## 4. What should change after review

- Make the intended result **a scoped construction**, not merely a proposed measurement protocol. A certifiable unique intermediate followed by deterministic reconstruction is an implementable positive case, but established techniques make novelty doubtful.
- State which of three objectives is sought: exact statistical removal, computational suppression for bounded receivers, or failure of tested decoders. All require different evidence.
- Keep arbitrary program classes distinct from a finite DSL, a rewrite closure, and a common-target sampling distribution.
- Identify receiver side information and task inputs outside sender control. Independence of a bare artifact marginal is insufficient if the receiver has a correlated key. A key that already contains the payload is not new leakage, so specify baseline knowledge.
- Require an explicit counterexample when claimed utility or runtime assumptions fail. If the only provable reusable case reduces to established certifying computation, say so and decide whether to pursue a narrower empirical contribution or another construction.

No positive novelty delta or general efficient solution is established. This preparation strengthens the proposal by naming a genuine positive construction and the exact boundary where its guarantee/cost disappears.
