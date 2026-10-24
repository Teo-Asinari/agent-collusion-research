
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

<source path="research/workstreams/architecture/proposal.md">
## 9. Closed abstract retrieval machine (revision 1)

This is the normative revised operational specification. It is an exact search hybrid with a bounded neural predictor, not a claim to satisfy the owner's general language-model ambition. The graph example remains an independent correctness sanity vehicle.

**Input domain and authority.** Public x specifies fixed record count N, record width b, descriptor width d, neural fuel B, predicate bound K, public readout bound J, query q and public task ID. Integers lie within declared finite bounds and N≥1. An external task authority fixes these facts and the query allowlist. The receiver may choose allowed queries adaptively using its public history and fixed auxiliary information k. Sender-controlled query selection, fact falsification and changing x are excluded from the no-extra-flow claim. Private frames contain N b-bit records z_i, d-bit descriptor c, bounded payload m, private neural weights/state theta,H and private optimizer state. Decoding is total on all fixed-length private bitstrings; variable-length private inputs are outside this version. There is no private parsing-error status.

**Authorized release.** A total exact predicate P(q,z_i) has worst-case bound K; its code is fixed trusted task semantics, and q supplies arguments rather than arbitrary executable code. F(x,z)=OR_i P(q,z_i). All records, descriptor, payload, private parameters and private histories are protected except this declared Boolean disclosure. Any property inferable from F itself is permitted. Holding public phi fixed does not protect a secret already encoded in phi.

**Machine state.** Public registers are (x,session,t,L,phi); private registers are (z,c,m,theta,H,private optimizer,evaluation registers,j,v); phase and loop counters follow x's fixed control schedule. Only the transitions below exist; no tools, files, heap-allocation interface, exceptions, callbacks or network operations exist in this abstract machine. Records and registers are fixed-size bitvectors. Every transition emits the blank symbol until the one prescribed release frame.

| Fixed phase | Total transition and permitted reads/writes | Public observation |
| --- | --- | --- |
| B neural ticks | Evaluate the allowed bounded transformer graph with read signature T_theta(q,c,m,H); it has no direct read access to current records z_i or predicate registers. It writes only H and private evaluation registers. Neural primitive arithmetic is a total fixed-bit operation, with specified rounding and exceptional-value encoding. Finished computations idle; fuel exhaustion discards partial output. Decode output to j in 1..N, using j=1 for exhaustion/invalid encoding. Only private registers change. | Blank each tick |
| K candidate ticks | Evaluate P(q,z_j) in private registers, padding its abstract evaluation to K ticks; initialize v to that exact bit. | Blank each tick |
| N blocks of K ticks | For i=1..N: if v=1 or i=j, perform K idle ticks; otherwise evaluate P(q,z_i) in K ticks and set v := v OR result. Private memory only. | Blank each tick |
| J readout ticks | Freeze a=v. Total bounded public G(phi,L,x,a,U) writes new L and a fixed-width response containing a; unused ticks idle. U is a session-indexed public random tape independent of all protected state, with its law fixed conditional on public history and k. G has no access to private registers or private random counters. | Blank until final tick; then the response and fixed success status |

Release occurs at T(x)=B+(N+1)K+J. Then erase ephemeral private evaluation registers; persistent H/theta/private optimizer may remain private but cannot affect any later public state except through a future exact F. Public state/parameter updates, if enabled, are part of G and depend only on (L,phi,x,a,U). No private gradient, norm, checkpoint statistic or optimizer accumulator is shared. Any private numerical failure already has total bitvector semantics or the default candidate rule; it cannot suppress or change the release slot/status. A malformed **public** x is rejected by a public total parser at a public fixed reject slot. The two compared worlds have the same raw public x, so this behavior is identical. Hardware faults are not modeled.

This table closes the *abstract* transition relation; it does not implement total floating-point kernels, bounded transformer evaluation or private physical resources. Allowing an omitted external effect would require a new theorem/refinement argument.

## 10. A useful role with explicit limits (revision 1)

The predictor reads only (q,c,m,H,theta), not current record contents; exact record reads occur in the candidate/fallback predicate blocks. A successful candidate avoids predicate evaluations, unlike the graph full-sweep construction. Every predictor remains correct: a true candidate proves F=1; a false candidate triggers bounded exhaustive remainder. On records with predicate values (0,1,0), j=2 takes one predicate evaluation and returns true; j=1 takes the false check and then the matching second record, still returning true. An all-false frame needs N evaluations and returns false for every j. This is a concrete sound shortcut and bad-prediction recovery, **not a demonstrated learned advantage against a strong symbolic baseline**.

The abstract machine starts with a supplied descriptor c and private H. It does not assume a cheap informative descriptor exists. If c or H was built by scanning/embedding the records, charge that full preprocessing and memory-access cost; if rebuilt on each query, charge it on each query. If amortized across queries, specify build/update costs, number of uses and immutable record snapshots. During each invocation the record frame is immutable. A stale descriptor changes prediction accuracy rather than correctness, since each witness is checked against the current frame; any freshness benefit or refresh work must be measured. Record mutation during an invocation is outside this specification. No descriptor construction, freshness mechanism or favorable amortization regime has been demonstrated.

Let C_N include actual neural inference, descriptor acquisition, decoding, memory access and private update costs; C_P include exact predicate/checking cost. On a declared one-match distribution where an uninformed scan sees a uniformly placed match and a miss leaves it uniform among remaining records, the sequential scan uses (N+1)/2 expected predicates. Predictor-first costs C_N+C_P[1+(1-p)N/2], with hit probability p; it helps this baseline only if C_N/C_P < (pN-1)/2. Negative instances add C_N overhead with no predicate savings. No p, C_N or C_P has been measured, and the distribution assumptions have not been validated. The numerical scenario in revision-preparation.md is algebra, not experimental evidence.

An end-to-end ledger must separate C_descriptor/build/update + C_transformer + C_decode/access + C_predicate/fallback + C_public_readout. The first three comprise C_N above; common public readout costs cancel in that restricted comparison only when the baseline uses the identical readout. Training/setup costs and any amortization horizon must be reported separately. Moving a full record scan into descriptor acquisition cannot establish an end-to-end work reduction.

Strong comparisons must include a conventional exact index when the query/predicate admits one, context-aware symbolic retrieval, and the best task-specific solver. If an index already gives O(1) lookup, a transformer can be redundant or worse. No nontrivial instance beating these baselines, including its full neural/checking/preprocessing costs, is established. **A1's useful-architecture acceptance gate therefore remains open.**

The fixed abstract slots conceal early private completion only in the defined receiver projection. They do not improve public response latency; exclusive reservation may prevent throughput gains. Billing, power, cache contention and private-work counts are excluded. If observed, a sender can intentionally predict correctly/incorrectly to encode a bit even when F is unchanged. Padding or isolation may remove savings. Thus a conditional work-saving mechanism is not a deployed cost-saving anti-stego architecture.

An important existing comparator is [Polak–Schmidt, Warm-Starting APSP with Predictions, v1](https://arxiv.org/html/2607.00857v1). Their Theorem 1 combines estimates, verification and recovery with runtime O(n^2(q+log n)+n^3.66/p+eta*n), specializing to O(n^2.83+eta*n). Prediction generation must be added; a naive neural certificate generator can erase the gain. This is prior algorithmic correctness/cost work, not their proof of our receiver-view property, and not a new algorithm proposed here.

## 11. Conditional-history invariant and proof obligations (revision 1)

Define h_t as the whole receiver transcript including public task/query history, all released frames/statuses and their logical slots; receiver side information k is explicit. Define a_t=F(x_t,z_t). For every reachable h_{t-1}, equal x_t, equal authorized a_t, equal public state and k, the next-frame kernel must be the **same** K_public(frame,L' | h_{t-1},x_t,a_t,k), regardless of protected inputs/state/weights. Public random tapes are fresh across sessions, or generated by a public-state transition with this same conditional independence; independent marginals alone do not qualify.

Exact F follows from the candidate/remainder argument. All pre-release observations are fixed blanks; the release/readout transition reads only the equal public state and exact a_t. Coupling U gives equal next frame and public state. Induct on the transcript: the same receiver policy chooses the same distribution of the next public query from equal histories/k; whenever the two private worlds give the same authorized answer to that query, the next-frame condition applies. This is an interactive no-extra-flow claim relative to an ideal F oracle. If authorized answers differ, the theorem does not demand identical transcripts. Equality of only the *final* F is insufficient.

**XOR history counterexample.** Release r in session 1 and r XOR m in session 2 for a uniform private r. Each marginal is uniform; their XOR reveals m. After h_1=r is observed, the session-2 conditional distribution depends on m, violating the invariant. In this machine it also requires an illegal private-register read by G, a forbidden private update to public sampling state, or a sender-controlled value substituted for exact F. Reusing a public random tape is not itself forbidden if the conditional kernel remains independent of protected state; the leak is dependence of the public transition on m.

Three different proof stages remain: (i) exact algorithmic correctness, for which informal proofs are supplied; (ii) noninterference of this closed abstract transition system, for which the induction above is an outline; (iii) executable/hardware refinement, not established. No mechanical proof at any stage has been completed.

## 12. Boundary examples and revised novelty claim

Positive authorized flow: for fixed query and N=3, frames with predicate values (0,0,0) and (0,1,0) intentionally release different F values. Same-F protection: frames (0,1,0) and (1,0,0), different private descriptors/payloads and arbitrary private predictors both release true at the same slot; G cannot reveal the matching index. Repeated allowed queries may reveal many facts through their authorized answer history. This architecture does not prevent that intended information flow.

[Pandey et al., v1, §V-C](https://arxiv.org/html/2610.25032v1) already gives task-only canonicalization, including a zero-error ideal and key-aware leakage bounds with stated distributional assumptions. Our per-history/per-key specification is not identical to its average balanced-attribute bound, but restating canonical task-only release supplies no novelty. LLMbda already has a total-program specialization; Tiwari already changes learned architecture/training for IFC. Classical guided search, delimited release and algorithms with predictions already supply the main construction ingredients. The current contribution is a clarified candidate and its limitations; a useful novel transformer architecture remains an explicit research blocker.

## 13. Extension rule (revision 2)

The closed machine certifies no arbitrary learned semantic extractor, generated program, free-form private release, graph/record mutation or additional shared state. Before adding a primitive, specify its admitted inputs, total finite transition semantics and budget, all state reads/writes/observations, numerical/error behavior, parameter/optimizer update effects, and semantic contract relative to the authorized release. Then establish confinement and the conditional-history kernel condition under composition; if it changes F, update the ideal authorization explicitly. A primitive that merely preserves task validity is insufficient when it can select among distinguishable valid releases. Any executable/hardware refinement and cost claim also needs rechecking. Until these obligations are discharged, the extension is a research proposal rather than part of the architecture's guarantee.

</source>

<source path="research/workstreams/architecture/sources.md">
# Architecture source and reading ledger

Access date: 2026-10-24. All links below are primary author/publisher sources. Targeted verification only; no full proof audit, released-code audit, training or reproduction of the papers. No third-party material is vendored.

| Source/version | Inspected in this pass | Relevant scope and limit |
| --- | --- | --- |
| [Tiwari et al., USENIX Security 2024 published PDF](https://www.usenix.org/system/files/usenixsecurity24-tiwari.pdf) | Introduction, §2.3 definition, §3 architecture/training/gating passages, limitations | Transformer training-domain IFC, independent experts and access-aware aggregation. Does not establish general malicious-agent steganography prevention. The PDF's explicit training-independence requirement informed the training-state obligation. |
| [Garby, Gordon & Sands, LLMbda arXiv 2602.20064v2, July 10 2026](https://arxiv.org/html/2602.20064v2) | §3.4 confinement discussion, §4 definitions/theorem statements, total specialization Lemma 4.2, Appendix B.3 interpreter correspondence overview | Machine-checked calculus/interpreter result is author-reported; Lean code not inspected/executed. Termination-insensitive property must not become a claim of no termination/timing channels. Total-program specialization is already present. |
| [Daggitt et al., Vehicle, FSCD 2025](https://drops.dagstuhl.de/storage/00lipics/lipics-vol337-fscd2025/html/LIPIcs.FSCD.2025.2/LIPIcs.FSCD.2025.2.html) | Abstract, introduction and §2.1–2.2 decomposition/embedding gap | Supports distinctions between a symbolic system property, a neural contract, and the encoding/decoding bridge. Example safety proof is not a covert-channel proof. Tool not installed/executed. |
| [Chong & van der Meyden, Using Architecture to Reason about Information Security, TISSEC 2015](https://people.seas.harvard.edu/~chong/abstracts/ChongM2015.html) | Author abstract only | Architectural causal constraints, local trusted properties and refinement precede this proposal. Full formal model/proofs remain unread. |
| [Sabelfeld & Myers, A Model for Delimited Information Release, 2004](https://research.chalmers.se/en/publication/2026) | Author institutional abstract only | Explicit permitted disclosures and anti-laundering guarantees are prior art. The proposed F-equivalence target should not be described as a new information-flow definition. Full text not audited. |
| [Cousot & Cousot, Fixed Point Approach to the Approximate Semantic Analysis of Programs, June 1977 manuscript](https://cs.nyu.edu/~pcousot/COUSOTpapers/Unpublished-FP-77.shtml) | Author abstract/bibliography only | Chaotic iteration/fixed-point semantics are classical. No import of a particular theorem's assumptions without separate checking; our bounded graph argument is supplied explicitly. |
| [Anderson, Verma, Dillig & Chaudhuri, Neurosymbolic Reinforcement Learning with Formally Verified Exploration, NeurIPS 2020](https://papers.neurips.cc/paper_files/paper/2020/hash/448d5eda79895153938a8431919f4c9f-Abstract.html) | Published abstract only | Verified safe exploration via neurosymbolic policy updates is adjacent architecture/learning precedent, not a steganography guarantee. |
| [Kalyan et al., Neural-Guided Deductive Search, arXiv 1804.01186v2, September 9 2018](https://arxiv.org/abs/1804.01186v2) | Primary abstract only | Neural guidance of deductive computation precedes this design seed. Completeness/cost/security details need a deeper review before claiming a new neural-guided solver. |

Representative searches used: neural/transformer architectural information-flow control; neural-guided algorithms with formal correctness; delimited release; chaotic/fixed-point iteration and scheduling; verified neurosymbolic exploration. This is not an exhaustive citation-index audit. The absence of an exact match in this pass does not establish novelty.

## Revision 1 primary additions

- [Polak & Schmidt, Warm-Starting All-Pairs Shortest Paths with Predictions, arXiv 2607.00857v1, July 1 2026](https://arxiv.org/html/2607.00857v1): accessed 2026-10-24. Read abstract, §1.1/Theorem 1, Algorithm 1 and targeted §§3–4 verification/recovery passages. Predictive certificates can reduce exact APSP work while maintaining unconditional correctness. Its bound accounts for verification and recovery but not an arbitrary neural predictor's cost. No proof audit, code inspection or reproduction. Author-linked release identified in paper, not inspected. This directly prevents novelty claims for merely combining prediction, certification and fallback.
- [Pandey et al., Don't Judge an Agent by Its Messages, arXiv 2610.25032v1, October 18 2026](https://arxiv.org/html/2610.25032v1): accessed 2026-10-24. Read §V-C including Proposition V.3 and surrounding key-aware framing. Task-only canonicalization and zero-error release are direct precedents. Balanced conditional attributes and a key independent of private state qualify the advertised bounds; these are not silently substituted for a per-history/per-key system theorem. Full paper/proofs not audited.

## Our executable artifact (scope unchanged)

`check_small_model.py` is newly authored standard-library code for a bounded analytical check, not copied upstream. It abstracts a scheduler as an arbitrary permutation, so no neural implementation is claimed. Run command and observed result are recorded in `proposal.md`. No credentials, external datasets or model endpoints are used.

</source>