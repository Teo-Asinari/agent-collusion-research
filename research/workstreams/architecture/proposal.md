# Architecture approach: learned computation with a verified observable quotient

2026-10-24. Completed first research pass. **An architecture specification and informal proof outline, not an implemented secure model or mechanized theorem.** No full study, training run or inference budget selected. Primary-source review depth is recorded in [sources.md](sources.md).

## Outcome

A defensible small starting point is to **let learned computation change the internal route to a result while verified operations ensure that every permitted route produces the same specified observable information**. This requires changing the model's internal state transitions, learning boundaries and public readout, rather than attaching an output classifier to an ordinary LLM.

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
