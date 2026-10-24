## Objection Disposition

**Objection 1 (microbenchmark of known asymptotic gap): Accepted.** Measuring O(V+E) vs O((V+E)log V) in Python produces no contribution beyond what McConnell et al. already establish. The timing proposal is withdrawn.

**Objection 2 (abandonment of rich-artifact objective): Accepted in part.** The shortest-path kernel is correctly characterized as a toy. However, the repair proposed—LLM-generated ASTs with certificate verification—smuggles in the unsolved problem as a precondition. No known unique-certificate structure exists for rich code that is both cheap to verify and canonical enough to strip steganographic choices. The objection identifies the bottleneck but not a solution.

**Objection 3 (rational-sender circularity): Accepted.** If the receiver can re-solve, the sender's certificate is unnecessary. The "rational sender" framing inverts the dependency. The assumption is withdrawn.

**Withdrawn claims:** efficiency motivation for the shortest-path construction; rational-sender framing as a deployment justification; the proposed Python timing experiment.

---

## Surviving Construction

The finite content guarantee from the verified construction survives intact: for the declared 280,000-record universe, maximum pairwise TV is zero. This is not withdrawn.

What does not survive: any efficiency argument, any extension to rich artifacts, any claim that certificate reuse is preferable to re-solving for this task.

---

## The Actual Technical Bottleneck

The critique's repair (Objection 2) requires a task where:

1. Re-solving is computationally intractable for the receiver.
2. Verification is cheap (poly-time certificate).
3. The certificate *uniquely determines* a canonical useful artifact, stripping sender-selected non-unique witnesses.

This is the gap between NP-hard search and P-time verification—the standard NP certificate framework. But standard NP certificates are not unique: for SAT, many satisfying assignments exist; for graph coloring, many valid colorings exist. Uniqueness of the certificate is a separate and strong requirement.

**Observation (not proved):** Problems with unique witnesses relative to a canonical ordering—e.g., lexicographically-first satisfying assignment, or minimum-cost spanning tree (unique under generic weights)—satisfy condition 3, but re-solving them is also efficient when the problem is in P. For NP-hard problems with unique witnesses (e.g., unique-SAT), verification is cheap but finding the witness in the first place requires the sender to do expensive work, and the receiver cannot verify uniqueness without solving. This is a circular dependency.

**Conjecture (model speculation, not proved):** No problem class simultaneously satisfies all three conditions without either (a) the receiver being able to re-solve efficiently, or (b) the uniqueness claim being unverifiable by the receiver. If true, certificate-reuse sanitization has no efficiency advantage over re-solving for any task where the content guarantee is also achievable by re-solving.

This is not established. A counterexample would require identifying a specific problem in the gap.

---

## Closest Predecessor Delta

Certifying algorithms (McConnell et al.): establish verification efficiency, not sanitization or uniqueness-of-witness for canonical output. Pandey et al.: canonical task interfaces with leakage bounds, not certificate reuse or computational intractability of re-solving. Neither addresses the three-condition requirement above.

The open question—whether any task satisfies all three conditions—is not answered by existing verified sources. This is a genuine technical gap, not a novelty claim from absence of evidence.

---

## Smallest Decisive Next Check

**Not an experiment. A classification task:**

Identify one candidate problem P such that:
- P is in NP but believed not in P (or provably requires superlinear time under a reasonable model).
- P has a polynomial-time verifiable certificate that is *unique given the problem instance* (not just a witness, but the unique witness).
- The unique certificate determines a canonical useful output—one that a sanitizer can reconstruct deterministically without re-solving.

**Rejection criterion:** If no such P can be identified, or if every candidate either (a) admits efficient re-solving, or (b) has non-unique certificates, then the reuse-efficiency framing has no valid target and should be permanently abandoned in favor of the purely content-theoretic result already established.

**If a candidate is found:** Verify that the uniqueness claim is checkable by the receiver (not just asserted by the sender), that the canonical output is actually useful (not a trivial encoding), and that the receiver's verification cost is strictly less than re-solving under a specified complexity assumption. Only then does efficiency motivation survive.

**Assessment:** I do not currently identify a compelling candidate. The most natural candidates (unique shortest path under generic weights, minimum spanning tree) are in P. Problems believed outside P with unique witnesses (Factoring with unique prime factorization, integer factorization) have re-solving costs that define the hardness—the receiver cannot verify uniqueness without factoring. This suggests the bottleneck may be fundamental.

**If no compelling design survives this classification check, the correct conclusion is:** the task-preserving-rewrite direction produces a content guarantee for a restricted toy model with no efficiency advantage, and the path to useful generalization requires a complexity-theoretic result that is currently out of reach. Report that and stop.
