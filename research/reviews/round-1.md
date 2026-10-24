# Adversarial review, round 1

2026-10-24. Independent review of the first architecture and task-preserving-rewrite proposals. No full experiment, neural training, paid inference or proof-assistant verification performed. Primary reading/access limits are in [sources.md](sources.md).

## Verdict

**Architecture:** the stated complete-sweep graph construction has a coherent informal correctness/noninterference argument within its deliberately restricted observation model. I found no counterexample to that bounded mathematical claim. It is not yet a useful new transformer architecture: removing the transformer leaves the same exact work and output. This limitation is already acknowledged, not a newly discovered flaw. Revision should distinguish a sound proof vehicle from the unfulfilled capability/contribution objective.

**Rewrite:** the proposal correctly distinguishes task preservation from retaining all submitted choices, includes independent synthesis and adapted decoders, and does not overclaim its four-output example. It is a well-specified evaluation direction, not yet a concrete reuse-based sanitizer or novel result. Its strongest formal endpoint currently discards the submitted implementation. Revision should supply an actual bounded reuse kernel or admit that the reuse question remains open.

The objections below are acceptance gates, not a demand to declare either approach successful. “Already acknowledged” means the draft honestly states the issue but has not resolved it. “New precision” means the reviewer supplies a concrete stronger obligation or comparator; it does not imply the underlying idea is novel.

## Architecture objections

### A1 — Blocking contribution gap: the neural component has no demonstrated purpose

**Location:** architecture §§3,7–8. **Status:** already acknowledged; blocks a capability/novelty claim, not the graph proposition.

Every sweep processes all padded edges, and there are always N−1 sweeps. Learned ordering can change intermediate distances but not reduce that exact work. The method adds neural inference to a standard solver. Nonconstant private release avoids total disconnection, but does not establish a useful role for learning.

**Repair:** retain this as a proof vehicle. Specify one proposed certified shortcut with a sound acceptance condition, bounded fallback and an exact cost ledger. An invalid predictor must not change correctness or release behavior; well-trained prediction may improve expected work without implying an all-weights speedup. Compare with a strong symbolic algorithm, not only a deliberately slow full-sweep baseline.

**Acceptance:** a worked nontrivial instance where predictor evaluation + checking + fallback costs less than the stated strong symbolic baseline, and a bad-prediction case showing correct bounded recovery. If no such instance exists, mark the useful-architecture objective unresolved and do not substitute “contains a transformer” for that objective.

**New prior-art comparator:** [Polak–Schmidt, Warm-Starting All-Pairs Shortest Paths with Predictions, arXiv 2607.00857v1](https://arxiv.org/abs/2607.00857) already studies prediction-assisted shortest-path computation with optimality certification and recovery. Abstract only reviewed here; it is not a direct anti-stego theorem. The cost/correctness combination needs comparison with algorithms-with-predictions work, in addition to neural-guided synthesis.

### A2 — High: the proposed theorem needs a closed operational model

**Location:** §§1–2,4–5. **Status:** acknowledged in prose, missing theorem-level closure.

The graph proof establishes equality of an exact answer. Global noninterference also needs the permitted transition relation, public initial-state relation, randomness coupling and receiver projection. Total neural evaluation and fixed logical release are assumptions, not an implemented guarantee. Observable parsing/validation failures, numerical exceptions, allocations or mutable shared state could bypass the argument. This is a scope defect if omitted from a system claim; it does not refute the scoped mathematical proposition.

**Repair:** write a compact formal specification of the primitive signatures and state partitions, with explicit admissible-input domain and total behavior. State whether malformed inputs and physical observations are excluded. Separate (i) algorithmic correctness, (ii) noninterference of an abstract machine, and (iii) implementation refinement.

**Acceptance:** a reader can identify all sources of public observations and prove equal observations by induction over the specified transitions without relying on the English phrase “no other path.” A rejected or nonterminating private neural computation must have a specified public outcome.

### A3 — High, shared with rewrite: marginal one-step equality is insufficient

**Status:** composition is already required; the following is a concrete acceptance test.

Let a secret bit be m and a hidden random bit be r. Release r in round 1 and r XOR m in round 2. Each individual marginal output is uniform and independent of m; the joint transcript reveals m exactly. Reused hidden state, sampling counters or caches can produce this pattern. The counterexample does not refute a theorem that already covers the complete view; it refutes replacing that theorem with per-output marginal checks.

**Repair/acceptance:** state a conditional-history invariant or a joint-transcript theorem, and show the toy counterexample violates an explicit architectural rule. Include authorized-release history, not just equality of the final F. Public adaptive query selection must be derived from equal visible histories; fixed-query tests cannot establish interactive security.

### A4 — High: do not infer unrestricted anti-stego from approved release

**Status:** already acknowledged, needs prominent claim boundary.

If the sender chooses the graph or queries, it can sometimes select F to carry a payload. A theorem allowing F correctly permits that signal. Public learned weights are fixed across compared worlds; secrets embedded in those weights are not protected by a theorem that calls those weights public and holds them fixed.

**Repair/acceptance:** explicitly list protected inputs/weights, trusted task facts and query authority. State that the guarantee is no extra transfer beyond the authorized release, not absence of every possible encoded message. Supply a positive example of required private information influencing the output and a same-F pair where a forbidden payload cannot do so.

## Rewrite objections

### R1 — Blocking contribution gap: specify the reuse operation

**Location:** rewrite §§4–5,7–8. **Status:** already acknowledged research gap; current “apply rewrites or reconstruct” leaves the proposed intervention underdefined.

Task-only canonical synthesis has a straightforward input-independence argument. Rewriting that retains an expression, e-graph component, initialization, candidate list or learned hint can retain payload-dependent structure. Complete functional equivalence says nothing about equality of artifact distributions. A set of compiler passes is not automatically an erasing kernel.

**Repair:** define one finite rewrite/search kernel completely: admissible syntax, trusted task specification, seed law, transition probabilities, stop/fallback rule and output serialization. Either calculate its worst-case contraction/TV over all valid input artifacts in a declared small universe, or make the narrower empirical claim against declared encoders. Show how reuse changes computation cost relative to a task-only method.

**Acceptance:** at least one nontrivial equivalence class with multiple structural encodings, a complete matrix R(y,output), row-distance calculation, and a cost comparison. If the only zero-distance result ignores y, report that instead of calling it a reuse success.

### R2 — High: validation and unsuccessful reconstruction remain part of the channel

**Status:** failure handling is acknowledged; validation is a concrete missing edge.

Even a task-only synthesizer can be placed after sender-dependent validation. Two valid equivalent input programs may have different lengths or verification costs. If the interface exposes different status, completion slots or budget exhaustion, the composite pipeline depends on y even when the synthesized code does not. Rejecting a failed rewrite and returning the original program restores an obvious channel.

**Repair/acceptance:** state input size bounds and which validation costs/statuses enter V. For the exact finite interface, include all failure outcomes in the row distributions and test a pair with unequal validation/search costs. Restricting attention to successful outputs is unacceptable. A content-only theorem is acceptable if labeled as such; no physical timing claim follows.

### R3 — High: current exact-oracle setting can remove the claimed source of usefulness

**Status:** partially acknowledged; needs sharper accounting.

If x already contains the complete small truth table and the release language permits a lookup-table program, a trusted canonical implementation may make both reconstruction and y unnecessary. If lookup tables are forbidden, that restriction needs task justification and the strongest permitted canonical construction as a baseline. A dozen handpicked functions where one solver happens to struggle would not establish a generic replacement-cost barrier.

**Repair/acceptance:** declare which task information is supplied independently, why the code/size/cost constraint matters, and what work y can save. Choose the permitted representation before observing results. Include cheap canonical families, strong deterministic baselines and failed searches; identify an actual reuse benefit rather than equating artifact complexity with synthesis hardness.

### R4 — High: add indistinguishability obfuscation as a theoretical comparator

**New prior-art gap in the current table.** For exact equivalent programs, the target of hiding which implementation was submitted is directly related to iO. [Jain–Lin–Sahai, arXiv 2008.09317v1](https://arxiv.org/pdf/2008.09317), introduction and §2, defines correctness plus computational indistinguishability of obfuscations of equal-size equivalent circuits. This is a conditional computational result, not statistical zero leakage, a usable sprint implementation, or preservation of arbitrary source-code readability/runtime budgets. The construction relies on stated cryptographic assumptions; proof not audited.

**Repair/acceptance:** add a precise comparison: exact versus computational indistinguishability; same function and padded size; allowed decoder/auxiliary information; randomness and metadata; function evaluation overhead and readability. Do not claim equivalent-program rewriting cannot theoretically hide implementation choice. Conversely, do not claim iO automatically solves task-equivalent programs that compute different functions allowed by a loose task.

### R5 — High: replace vague adaptation with an explicit bounded worst-case target

**Status:** adaptation is already present; missing operational budget/domain.

Testing two structural encoders per function does not bound all sender pairs. In a small enumerated universe, the stronger target is the maximum distance between R's rows over all admissible sender artifacts (or an explicitly bounded encoding class). Empirical decoder recovery supplies a lower bound, not an upper certificate. Repeated observations can amplify a small residual channel.

**Repair/acceptance:** choose whether the next check is exact finite-channel analysis or empirical red teaming. For the former, list all allowed sender artifacts and receiver-visible outcomes; compute max TV and a repeated-use analysis under stated independence/history assumptions. For the latter, fix attacker construction/query budgets, splits and aggregation opportunities and retain the lower-bound interpretation.

## Prior-art corrections applicable to both

1. Pandey et al.'s [§V-C](https://arxiv.org/html/2610.25032v1) already gives task-only canonicalization and key-aware bounds. Proposition V.3 uses an attribute balanced conditional on task state and a shared key independent of private state. This average/distributional statement is not identical to our desired per-task/per-key joint-history guarantee. Its ideal zero-error task-only interface is nevertheless a direct predecessor; saying “shared keys” or “task preservation” does not add novelty.
2. LLMbda v2 [§4.2, Lemma 4.2](https://arxiv.org/html/2602.20064v2) already relates its termination-insensitive guarantee to exact noninterference for total programs. “Make the machine bounded/total” alone is not a newly discovered route.
3. Tiwari et al. [§§2–3](https://www.usenix.org/system/files/usenixsecurity24-tiwari.pdf) already alter transformer training/experts/routing for IFC. The new architecture would need an exact capability/security delta, not just interleaved verified code.
4. Roger–Greenblatt [§§5.3,7.2](https://arxiv.org/html/2310.18512v2), Kahng §4 and SrcMarker §IV-E already cover regeneration, substantive-choice replacement limits and useful-code removal. The four-state quality example is correctly labeled elementary and is not itself a contribution.
5. Equality saturation and superoptimization are adjacent tools, not automatic secrecy results. STOKE's author PDF failed retrieval in this review; I retain the earlier ledger's introductory attribution and do not claim a new direct methods review. Hand and Brain full-text access is still unresolved; do not declare a specific adaptive gap from that absence.

## Ordered revision requests

1. Each author produce a short response table mapping IDs above to accepted/rejected/deferred, evidence and exact revised claim.
2. Architecture: formalize the restricted machine, retain the graph proof as a sanity vehicle, and choose either a specific certified useful primitive or an explicit “capability still unresolved” verdict. Do not train a redundant network to make the sketch look implemented.
3. Rewrite: define a complete tiny reconstruction kernel, add iO comparison, and separate exact finite-channel guarantees from empirical/adaptive estimates. Clarify the trusted task/cost contract before implementation.
4. Both: add the two-round XOR-state counterexample and explain how the actual system specification rules it out. Keep model-level and hardware-level guarantees separate.
5. Reviewer round 2 should check actual revisions against these gates. Unsupported ambition may remain deferred; a candid negative verdict is preferable to a narrower theorem presented as the original goal achieved.

## Late preparation notes: assessment of proposed repairs

These notes do not change the baseline verdicts. They identify concrete tests for the next revision rather than requiring the authors to remain with the initial toys.

**Architecture witness-index prediction.** The written `architecture/revision-preparation.md` replaces decorative permutation scoring with predicting a record satisfying a verified predicate, then exhaustive fallback on a miss. This gives the predictor an actual potential semantic/cost role: a successful positive witness can save predicate evaluations. The supplied break-even expression is coherent under its explicitly assumed distribution and cost model. It repairs “no possible useful role,” but proves neither trained-model benefit nor novelty. Ordinary short-circuit evaluation, learned retrieval and verified/neural-guided search are close conceptual predecessors. Acceptance also needs the conventional-index/strong symbolic heuristic baseline, descriptor cost, negative-instance workload and a clear admission that a fixed release deadline gives no client-visible latency gain. Predicate count, branch status or billing must remain outside the receiver view, otherwise intentional hit/miss restores a channel. A cell-level predictive shortcut is not yet a general radical language architecture.

**Rewrite verified unique-distance statistic.** The primary agent relayed an in-progress repair: verify exact shortest-distance labels supplied by an artifact, then reconstruct a deterministic path from the trusted graph and labels. I did not find a written rewrite preparation file at review time, so this is a test specification for the reported idea, not approval of unseen details. If a sound verifier ensures every accepted certificate yields the same exact distance vector, reconstruction from that vector can reuse computation without retaining the submitted predecessor choice. That resolves a real R1 gap for accepted certificates, while falling squarely within classical certifying-algorithm methodology. The next draft must address:

- Local tight-edge predecessor checks alone are unsound in the presence of zero-cost cycles disconnected from the source: finite labels can justify one another without an actual source path. Require source-rooted witnesses/ranks or equivalent reachability evidence, plus Bellman inequalities and unreachable-node checks.
- Deterministic tight-edge traversal needs an explicit terminating visited/ranking rule for zero-cost cycles and a canonical order based on trusted vertex/edge identifiers. Do not silently exclude zero weights unless the task contract says so.
- Rejecting invalid certificates creates a one-bit status channel if invalid submissions are in the sender's permitted strategy class. Either state an accepted-valid-input conditional guarantee, or provide a total task-only fallback and account for its observable work/failure behavior. The conditional claim is useful but weaker than zero leakage against arbitrary submissions.
- Compare verifier + reconstruction + all preprocessing with a strong task-only shortest-path baseline; no general asymptotic or practical advantage follows from linear certificate checking by itself.

Round 2 should evaluate the exact authored repair, source attribution and these counterexamples. A secure certificate-to-canonical-output map is an interesting construction to analyze, but its classical pieces and narrower accepted-input scope must remain explicit.
