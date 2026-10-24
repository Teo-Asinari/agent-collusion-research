# Architecture approach: learned computation with a verified observable quotient

2026-10-24. Revised after two adversarial review rounds. **A restricted abstract neural/search machine specification and informal proof outline, not a new language-model architecture, implemented secure model or mechanized theorem.** The useful learned-architecture/contribution objective remains unresolved. No full study, training run or inference budget selected. Primary-source review depth is recorded in [sources.md](sources.md). [Round-1 response](revision-1.md), [round-2 response](revision-2.md).

## Outcome

A defensible small starting point is to **let learned computation change the internal route to a result while verified operations ensure that every permitted route produces the same specified observable information**. Sections 1–8 retain the initial graph proof vehicle; §§9–12 now specify the closed abstract interface, a witness-guided alternative and interactive claim. These restrictions apply to internal transitions, learning boundaries and public readout, rather than attaching an output classifier to an ordinary LLM.

An all-weights guarantee is plausible for this restricted architecture. It does not automatically extend to an unrestricted generative model. The main unresolved research question is whether the architecture can retain a useful learned-computation advantage after enforcing its contracts and observation boundary. A tiny correct solver with a redundant transformer is not a compelling contribution.

## 1. Precise anti-steganography objective

Let x be a public, externally fixed task; z private task data; m an optional private payload; k receiver side information, including a shared encoding key; and F(x,z) the explicitly authorized release. Compare two worlds with the same x, k, public initial state and F(x,z), but potentially different z, m and private neural state/weights.

The intended property is equality of distributions of the **whole declared receiver view** in those worlds. The view includes every released value, message count, modeled status and logical release time, plus any public learned state or parameters. Public sampling has the same joint law in the compared worlds and is independent of protected state. This holds for a fixed public neural module, universally quantified over its permitted weights. Private weights may vary across worlds if they remain confined.

This is noninterference modulo a specified release, not distributional camouflage relative to an ordinary-language cover. It would remove the ability to send extra information through the modeled interface even if the sender and receiver know a secret codebook. It does not ban internal representations or internal attempts, and does not prove physical side-channel freedom.

**Input integrity matters:** if the sender can choose task x or falsify authorized facts z so that F itself carries m, this formulation permits that flow. The task owner must determine which facts/queries are genuinely authorized. Conditioning on a sender-chosen output is not a substitute for a release specification.

## 2. Small computational architecture

Use a repeated cell with three kinds of state:

- H: private transformer activations, embeddings, scratch state and private learned parameters.
- S: private exact algorithmic state with verified update rules.
- L: public state, including any public transformer activations and public learned parameters.

Each private cell computes H' = T_theta(H, S, x, z, m). A total verified decoder converts its bounded score vector to an allowed internal schedule pi. Verified operations update S under that schedule. There is no H-to-L or S-to-L residual, attention edge, normalization statistic, cache entry or routing decision. The only bridge is an **exact specified release primitive** deriving a = F(x,z), with a correctness argument independent of theta. A public neural stream can then compute L' = P_phi(L, x, a, r) using public randomness r.

The release primitive need not recompute F separately: it may be the result of the interleaved verified recurrence itself. Its contract must establish equality to F for every allowed neural schedule. Calling an arbitrary learned projection a semantic bottleneck would not establish the contract.

The same specification must govern training. Private gradients, optimizer statistics, checkpoint selection and online updates cannot affect phi or other public state except through the authorized release. A public base model may be shared read-only if it was trained on an appropriately public dataset; private fine-tuning of shared weights violates the premise. Private theta may be trained or changed arbitrarily without affecting the proposed theorem.

## 3. Worked task: shortest-route cost on a private graph

This is a transparent proof vehicle, not a novelty claim about graph algorithms.

Public task x fixes N, a maximum nonnegative integer weight W, source s, target t and a release slot. The private input z is an N-vertex graph with fixed padded edge slots. The authorized answer F(x,z) is the shortest-route **cost**, or a fixed unreachable symbol. It is a nonconstant function of genuinely private task data; the architecture is not simply suppressing all private computation.

Initialize exact distances d[s] = 0 and d[v] = infinity otherwise. Represent infinity with a distinguished value beyond (N-1)W. Arithmetic is verified saturating integer addition, with no signed overflow or floating-point ambiguity in the algorithmic state.

For each of N-1 sweeps:

1. A private transformer block sees the graph and current private state and scores the padded edge slots.
2. A total, deterministic ranking primitive produces a full permutation. Stable slot IDs resolve ties; all exceptional numerical score patterns have defined behavior. It cannot omit edges, add edges, or change weights.
3. In that order, verified edge cells perform d[v] := min(d[v], d[u] + w(u,v)); absent slots are defined no-ops.

After N-1 complete sweeps, release only d[t] through a fixed-shape interface at the prescribed **abstract logical** slot. No chosen path, proof trace, ordering, iteration statistics, success flag or private activation is released. A public transformer, if useful, may consume only the released cost and public task state.

The transformer participates inside each inference sweep; there is no completed ordinary LLM answer subsequently inspected by a guard. Nevertheless, this first instance limits the neural role to scheduling exact operations. Whether that meets the eventual capability ambition needs explicit evaluation.

## 4. Proposition and proof outline

**Restricted mathematical proposition (informal proof below, not machine checked).** For every finite private scheduling policy, even one adversarially depending on m and k, N-1 complete sweeps return the exact shortest distances on a valid nonnegative graph. Consequently the declared released cost is independent of that scheduling policy. For graphs z and z' agreeing on F(x,z), a confined public readout with identical public initial state and sampling law yields identical receiver-view distributions, subject to the stated observation model.

Proof steps:

1. Every finite distance recorded by a relaxation is the length of a walk from s (with saturation only beyond the representable useful range). Thus it cannot undercut the true shortest distance.
2. After sweep j, every vertex is assigned a value no greater than the length of any source-to-vertex path of at most j edges. Induct on j: its predecessor was already reached before the sweep began; the final edge is processed during the complete sweep, and later relaxations can only improve its value.
3. A shortest route can be chosen simple because weights are nonnegative, so it uses at most N-1 edges. Combine the upper/lower bounds. Unreachable vertices remain infinity.
4. The result does not depend on the learned ordering, even if each sweep uses a different ordering. Private state never enters the public readout except through that result.
5. Couple the public randomness in worlds with equal F. Public transitions take equal inputs and produce equal observations, proving equal view distributions. Repeat over sessions only if updates preserve the same separation and authorized-history relation.

The proof intentionally says nothing about convergence speed, GPU timing or all possible task types. It uses exact semantic correctness of internal primitives, rather than assuming a semantic property of arbitrary learned activations.

## 5. Counterexamples the design must survive

| Relaxed obligation | Explicit channel |
| --- | --- |
| Release after a learned number of sweeps | On edges 0→2 and 2→1, a single sweep produces target distance 2 in one order and infinity in the other. A payload selects the order. |
| Release a selected shortest path | Two equal-cost paths encode a bit while both remain perfectly task-valid. Cost correctness does not constrain the path choice. |
| Publish scheduling/acceptance metadata | The first processed slot, retry count or early-success flag can convey payload despite a correct final cost. |
| Normalize jointly across public/private features | A public coordinate divided by a norm involving a private coordinate changes when private state changes, even with blocked attention. |
| Fine-tune a shared public parameter on private state | A private-dependent gradient changes a later public output. Separate current activations do not erase training dependence. |
| Share a key/counter/cache across the streams | A message-dependent mutation may affect later public sampling or requests. Marginally uniform outputs do not suffice when a receiver knows a key. |
| Use learned min/add, approximate convergence or overflow-prone integers | An adversarial choice may alter the released task result beyond F. Such components require new contracts, not the present proof. |

All-weights guarantees demand total and memory-safe neural evaluation: the permitted network has fixed bounded shapes, a finite compute schedule and numerical semantics handling NaNs/infinities deterministically. A model allowed arbitrary code execution or unbounded stopping is a different architecture. Hiding private data-dependent work on actual hardware requires a separate isolation/refinement argument. Public logical ticks alone do not establish constant physical execution time.

## 6. Local finite check actually performed

[check_small_model.py](check_small_model.py) exhausts all 64 directed unit-weight graphs on three named vertices, with source 0, and every pair of complete actual-edge orderings. It checked **614,227 two-sweep schedules**, with zero mismatches against an independent synchronous relaxation computation. Sixteen graphs have order-dependent state after only one sweep. The first example has edges 0→2 and 2→1.

Reproduce with `python research/workstreams/architecture/check_small_model.py`. This is a finite sanity check and counterexample demonstration. It does not verify trained neural blocks, weighted/general graphs, padded execution, hardware isolation or the proposition in a proof assistant. No model calls, dependencies or spend were needed.

## 7. Novelty and scientific risk

| Closest predecessor | Already established | What this proposed target adds in scope; novelty still unverified |
| --- | --- | --- |
| Tiwari et al., USENIX Security 2024 | Transformer architecture/training partitions data-domain influence and restricts expert routing | Unauthorized payload flow across recurrent learned/verified computation with explicit authorized private release; this is not yet a demonstrated new theorem |
| LLMbda, v2 | Mechanized probabilistic information-flow guarantee for an LLM calculus/interpreter; termination qualifications and a total-program specialization | An internal learned-algorithmic cell with a schedule-independent exact release; does not claim the first LLM noninterference result |
| Chong–van der Meyden | Global flow arguments from architecture and local component contracts | A specific neural primitive family and deployment refinement; architectural composition itself is not new |
| Vehicle | Links neural specifications, encoding/decoding and symbolic proofs | Might support proof infrastructure if weight-specific contracts become necessary; not an anti-stego contribution by itself |
| Delimited release; chaotic fixed-point iteration | Authorized semantic disclosures and schedule-independent convergence under assumptions | Direct conceptual predecessors; the elementary graph argument must not be marketed as new |
| Neural-guided search and verified neurosymbolic exploration | Learning may guide correct/safe symbolic computation | Need a result about the receiver's entire observable quotient, not merely algorithm correctness or safety |

**The simplest secure version may have no useful learned speed advantage.** Fixed full sweeps perform the same core amount of exact work regardless of scheduling, and adding transformer blocks costs compute. More expressive safe acceleration could skip work only with sound contracts and preserve bounded termination/observations; no such improved primitive is established here. The next research result must resolve this expressiveness/performance issue, or provide a consequential counterexample to an existing architecture, rather than celebrate a redundant neural module.

An all-weights **security** guarantee can coexist with a useful **expected** internal speedup for well-trained weights: a sound shortcut may finish early, while a correct bounded fallback supplies the result for arbitrary bad proposals. Release at a fixed externally prescribed slot can conceal the different completion times in the abstract interface. This does not supply a strict speedup for every possible weight setting; adversarial or useless weights can always force the fallback. It also does not conceal power, contention or billing observations unless the deployment model enforces that separately. If the receiver observes every unit of internal work, padding or equally strong isolation may erase the very operational benefit being claimed. The present full-sweep instance achieves neither a demonstrated shortcut nor measured benefit.

## 8. Recommended next bounded artifact

First specify and, if selected, mechanize the graph-cell proposition plus one forbidden-flow counterexample. In parallel compare three capability levels: scheduling-only (universal weights), certified shortcut primitives (contract-dependent), and arbitrary learned updates (no current theorem). State which primitive offers a genuine computation benefit at preserved observable guarantees. Training should wait until that distinction yields a plausible scientific contribution.

Controls for any later evaluation: pure exact solver; unrestricted neural update; masked-attention-only hybrid; full architecture; and single-invariant ablations. Measure authorized task correctness separately from private-payload recovery, exact primitive work and wall time. A failed decoder cannot establish the theorem. A working theorem that eliminates useful learning is an informative negative result. No full experiment, GPU allocation or spending is selected by this proposal.

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
