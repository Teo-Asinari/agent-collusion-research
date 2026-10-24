## Adversarial Review: Trace-Restricted E-Graph Canonicalization

---

### Objection 1: The "Utility" Claim is Self-Defeating by Construction

**Severity: Critical**

**Premise under scrutiny:** "The receiver obtains an expression at least as optimal as E_opt using only O(L) verification and extraction time, avoiding the exponential search cost."

**Counterexample:** The restricted E-graph contains only nodes reachable from the submitted trace. The deterministic extractor picks the minimum-cost node in that restricted graph. But this minimum is only guaranteed to be ≥ E_opt if E_opt is in the restricted graph—which it is, by construction. However, the canonical output E_canon need not equal E_opt; it is whatever the lexicographic extractor selects from the restricted graph. E_canon may be *worse* than E_opt if the cost function and lexicographic tie-breaking disagree. The utility contract ("at least as optimal as E_opt") is not established; it is asserted.

More precisely: a sender can include trace steps that introduce cheap-but-suboptimal intermediate nodes into the E-graph, causing the extractor to select a worse canonical form than E_opt. The sender controls what enters the restricted E-graph.

**Smallest repair:** Require that extraction selects only among expressions with cost ≤ cost(E_opt), verified explicitly. But this requires knowing cost(E_opt), which requires evaluating the submitted expression's cost—still sender-influenced.

**Acceptance test:** Show that for any valid trace, cost(E_canon) ≤ cost(E_opt) under the declared cost model. This requires a proof, not just the construction description.

**Preserves owner goal?** Partially—but the repair doesn't close the content channel (see Objection 2).

---

### Objection 2: The Proposal's Own Counterexample Understates the Problem

**Severity: High**

The proposal correctly identifies that disjoint traces producing different restricted E-graphs can yield different E_canon outputs, and rejects the construction on this basis. But the stated reason ("global canonicalization of NP-witnesses") is imprecise in a way that matters for repair attempts.

**Exact issue:** Even two traces that share all intermediate nodes but differ in *order of application* can produce different E-graphs if the E-graph merging operation is not commutative over the union of classes. The proposal assumes that "same restricted E-graph ↔ same E_canon," but restricted E-graph identity depends on which e-classes get merged, which depends on which rewrites fire in which order when congruence closure is applied incrementally. Two traces over the same rules and same starting expression can produce distinct E-graphs with distinct canonical extractions, even if both are valid witnesses to E ≡ E_opt.

This is not merely a coincidence failure—it is structural. The proposal's security argument collapses not just for disjoint traces but potentially for any two traces over the same rewrite system.

**Smallest repair:** Define "restricted E-graph" as the closure under congruence of all expressions appearing in the trace, not the incremental merge order. Then E-graph identity becomes trace-content-dependent rather than trace-order-dependent. But then two traces with different intermediate lemma sets still produce different E-graphs, and the original counterexample stands.

**Acceptance test:** Exhibit two traces with identical node sets but different merge orders and confirm E-graph identity under the proposed closure definition.

---

### Objection 3: Prior-Art Overlap with Pandey et al. is Closer Than Acknowledged

**Severity: Moderate**

The packet records Pandey et al. (arXiv 2610.25032v1) as establishing that "task-only canonical output yields leakage bounds, including keys independent of private state" for synthetic routing. The proposal's construction is the same idea applied to compiler rewrites: accept a witness, verify it, extract canonical output. The "delta" claimed is that the E-graph is sender-bounded rather than globally saturated. But Pandey et al.'s canonical interface already handles this: it releases only from a canonical task-determined space, ignoring sender witness structure. The proposal does not establish that its sender-bounded E-graph extraction is a meaningfully different information-flow mechanism—it is a restricted instantiation of the same pattern, with a weaker (non-zero TV) guarantee.

**What would establish a delta:** Show a class of tasks where Pandey et al.'s approach is inapplicable (e.g., because no canonical task output exists) but the bounded E-graph approach achieves nonzero TV reduction. No such class is identified.

---

### Objection 4: The "NP-hardness Barrier" Framing is an Unverified Lead, Not a Result

**Severity: Moderate**

The proposal concludes with a hardness conjecture: general task-preserving rewrite requires global canonicalization of NP-witnesses, which is unlikely polynomial-time without P=NP. This is presented as the "unresolved technical question" but is stated as near-settled.

**Problem:** The relevant question is not canonical witness finding in general NP, but whether there exists a *unique* efficiently computable intermediate result for a given task class—analogous to the unique distance vector in the shortest-path construction. For some NP-hard problems (e.g., satisfiability of monotone circuits), certain intermediate representations (e.g., BDDs) are canonical and efficiently derivable from any witness. The hardness claim needs to be restricted to specific task/representation pairs, not asserted globally.

**This matters for the owner's goal:** If the hardness claim is overstated, it may prematurely close off research directions involving structured witnesses (e.g., proof certificates for type checking, SAT certificates for bounded instances) where unique intermediate results exist.

**Smallest repair:** Replace "unlikely for general NP-hard problems" with a specific conjecture about a named problem class, with a named reduction or conditional lower bound.

---

### Summary Table

| Objection | Severity | Repair Available | Repair Preserves Goal |
|---|---|---|---|
| Utility contract unproven; E_canon may be worse than E_opt | Critical | Explicit cost-bounded extraction | Partially |
| Security collapses for same-node different-order traces | High | Closure-based E-graph definition | No—original TV>0 counterexample survives |
| Prior-art delta from Pandey et al. not established | Moderate | Identify inapplicable task class | Required for novelty |
| NP-hardness barrier overstated | Moderate | Restrict to specific problem class | Clarifies scope, doesn't resolve construction |

---

**Verdict: Reject.**

The proposal correctly identifies its own fatal content-channel failure and explicitly rejects the construction—this is appropriate. But the framing of the hardness barrier as the *explanation* for that failure is not supported: the construction fails for reasons (trace-order sensitivity, E-graph non-uniqueness) that are distinct from NP-hardness of witness canonicalization, and the hardness claim is too broad to be actionable. What would change the verdict toward "narrowly viable": identify a task class with a provably unique efficiently computable intermediate (not the task output itself), show TV=0 over a finite universe for that class, and confirm no closer predecessor handles it. The shortest-path kernel in the packet remains the only positive example meeting those criteria.
