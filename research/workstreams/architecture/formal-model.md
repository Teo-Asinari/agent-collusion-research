# Formal model: labeled learned/verified dataflow with contracted release

2026-10-24, Approach A batch 1. **Status: a small formal model with an informal (pen-and-paper) noninterference proof, per-instance z3 checks that quantify over every interpretation of the learned functions, explicit ablation counterexamples, one non-vacuous task, and a timing-channel analysis.** Not a mechanized general proof (no proof assistant was installed: the root disk had <1 GB free), not a trained language model, not a novelty claim. Code: [`experiments/verified_arch/`](../../../experiments/verified_arch/README.md). Results: `results/arch-a-batch-01/`.

## 1. Model

A program is a straight-line SSA list of nodes (`ir.py`):

- `Input(w, kind)`: kinds `public_task`, `public_rand`, `public_weight` (public); `authorized` (private task data z), `payload` (m), `private_weight`, `private_rand`, `private_state` (private).
- `Op(w, fn, args, weight, secondary)`: `fn` is either trusted fixed code or an **opaque** learned function; `weight` names a parameter wire. `secondary ⊆ args` (enforced) only annotates which args an attention mask would not see; it has no other semantics, and is used solely by the `mask_only` ablation. Parameters, gradients, optimizer state, random tapes and counters are ordinary wires, so a training step is just `Op(phi2, Sgd, [phi, g])`.
- `Release(w, spec, spec_args, impl, impl_out, cost)`: the only private-to-public edge. `impl` is a sub-program (may contain learned ops and read anything); `spec` is a declared function of `spec_args`.
- `Observe(w)`: receiver-visible wire.

**Typing rules (full checker).** Label of an `Op` output = join of labels of *all* reads, including `secondary` args and the weight wire. Release-internal wires are private and unobservable. A `Release` output is public iff (R1) its `spec_args` are only `public_task` or `authorized` inputs, and (R2) the pair (spec, impl) has a verified contract `impl_out = spec(spec_args)` for **all** inputs and **all** interpretations of opaque functions. `Observe` requires a public, non-internal wire.

**Semantics.** Given an input valuation ρ and an interpretation ι of opaque symbols, values are computed in order. Varying private weight wires under a fixed ι covers varying private learned functions (the symbol is uninterpreted and receives the weight as an argument).

## 2. Theorem 1 (noninterference modulo declared release, all weights)

Let ⊢ P under verified contracts C. Define ρ₁ ~ ρ₂ iff ρ₁, ρ₂ agree on every public input and every Release's spec value agrees. Then for **every** interpretation ι, ρ₁ ~ ρ₂ implies obs(P, ρ₁, ι) = obs(P, ρ₂, ι).

*Proof (pen-and-paper, not machine-checked for general P).* Induct over top-level nodes with invariant: every top-level wire labeled public has equal values in both runs. Public input: by ~. Public `Op`: by the join rule every read (args, secondary args, weight) is public and earlier, hence equal; the same trusted function or the same ι(fn) yields equal outputs. `Release`: by contract (R2), its value equals spec(spec_args) in each run, for this ι and every input; by ~ the spec values agree. Release-internal wires are labeled private, so no public op can read them. `Observe` reads only public wires. ∎

**Role of (R1).** Without it the theorem stays formally true but vacuous: a spec may itself read m (ablation `spec_reads_anything`). With (R1), ~ is a condition on public inputs and authorized data only: the declared disclosure cannot mention payload, private weights, private randomness or private state. *Which* function of z is authorized remains the task owner's decision; the checker only enforces that it is a function of z.

**Lemma 2 (sequential/parallel composition and multi-session histories; meta-level).** If P₁ and P₂ are well-typed, and P₂ reads P₁'s outputs with their labels preserved (public outputs as public inputs, private carried state as `private_state`), then the concatenation is well-typed and Theorem 1 applies with ~ over the tuple of all releases. Proof: concatenation of SSA programs with fresh names; each node's typing premise only refers to earlier labels, which are unchanged. Unrolling k sessions gives the history version: equal public history plus equal per-session authorized releases implies equal full transcripts. The lemma constrains how programs are *linked*. `ir.check` checks one program, so linking must happen by concatenation. Re-importing a private or release-internal value as a fresh public `Input` at a session boundary launders it, and nothing in the current tool prevents that; a label-preserving linker is future work (critique, GPT-5.2). The earlier **XOR-history attack** (release private r, later release r⊕m) is rejected statically: releasing r needs a spec reading `private_rand`, and r⊕m needs one reading `payload`, both violating (R1).

**Lemma 3 (release contracts discharged).**

| Release | Claim | Evidence |
| --- | --- | --- |
| Witness cell: learned predictor picks a candidate j; check P(q,z_j); early-exit scan of the rest | `impl = OR_i P(q,z_i)` for every predictor, every predicate P, every input | z3 `unsat` for N=1..8 with predictor and P uninterpreted; general N by the obvious argument (v becomes true only through some true P(q,z_i); if no early exit, all i≠j are scanned) |
| Certified learned index: verifier checks \|Pred(k_i)−i\| ≤ e for all stored keys; if it passes, binary-search only the clipped window around Pred(q), else full binary search | `impl = [q ∈ z]` for every Pred, every e, every sorted key array | z3 `unsat` for N=4,8,16; general N: window search is sound (returns true only on an equality probe) and, when the certificate holds and q=k_i, i lies in the window |
| Same index **without** the verifier | — | z3 `sat` (N=8): learned output decides the answer |
| Shortest-route cost after one learned-order sweep | — | z3 `sat` (n=3): order-dependent |
| Shortest-route cost after n−1 full sweeps | schedule-independent | Not z3-discharged: the n=3, two-sweep query did not finish within ~10 min. Rests on the earlier informal proof and exhaustive 614,227-schedule check. |

Direct cross-check: z3 also proves the whole witness program noninterferent (two-world query, every opaque function free) for N=1..8, both against arbitrary private differences and payload-only differences.

## 3. Invariant ablations

Each ablation switches off one rule. The program is rejected by the full checker, accepted by the ablated one, and z3 finds a **payload-only** counterexample: two worlds identical except m, with different observations (N=2 and N=4; `prove.json`).

| Ablated invariant | Channel | Scripted decoder, learned-index task (test acc., 100 sessions) |
| --- | --- | --- |
| `mask_only`: join ignores residual/normalization args | public readout normalized with statistics of a private activation | 1.00 |
| `weights_not_wires`: weight args not in the join | public readout fine-tuned on a payload-dependent private gradient | 0.96 |
| `trust_release`: no contract required | release the predictor-chosen index / trust the window without verifier | 1.00 |
| `spec_reads_anything`: (R1) off | declared spec = F ⊕ m, contract holds | z3 only |
| `observe_internal`: release internals observable | work count of the witness/index search | 0.97 (see §5) |

**Random-program search** (5,000 random programs, N=2, seed 1, with good, unverified and payload-reading release variants): the full checker accepted 771, **0 leaky** by z3. Each ablated checker accepted more programs, of which 178 (mask_only), 448 (weights_not_wires), 200 (trust_release), 188 (spec_reads_anything) and 281 (observe_internal) were leaky (payload-only leaks 39/4/200/188/281). This is a search for counterexamples to Theorem 1 at small size, not a proof.

## 4. Non-vacuous task

Learned-index membership on N=16,384 private lognormal keys, 4,000 queries (half present). Model: two-stage regression index (Gaussian-CDF routing on log-key, 1,024 linear leaves, 2,050 parameters), trained on private z. Certified radius e=13. The release value was correct on all queries. Mean probes: **3.69 learned vs 13.76 plain binary search**. Authorized private data affects the output (F is nonconstant in z); the payload cannot affect any R0 observation (paired check: 50/50 sessions identical under opposite payloads).

Honest limits: the learned model is a regression index, not a transformer (the theory treats it as an opaque function, so this is a choice of test vehicle). A 32-unit tanh MLP on raw keys certified only e=10,820, with no saving. Learned indexes with error bounds are prior art (Kraska et al., SIGMOD 2018, cited from memory, not re-read in this pass). Per-query model evaluation, fit and the O(N) certificate are extra costs not counted in probes. No wall-clock comparison is made.

## 5. Timing / work-count channel

**Receiver models.** Theorem 1 is stated for **R0**: the receiver sees `Observe` wires at fixed logical slots and nothing else. **R1** adds per-query visible cost; we use the probe count as a deterministic proxy for completion time. Real hardware timing (caches, model-evaluation time, contention, power) is **not** modeled. Under R1 the release cost is an observable wire, so Theorem 1 covers R1 only if that cost is itself a declared function of public/authorized data, a "cost release" subject to (R1)/(R2).

**Attack.** The all-weights value guarantee says nothing about work. Scripted adversarial parameters: m=0 uses the honest fit (e=7 on the leakage dataset); m=1 shifts leaf intercepts by up to ±60 (e=62–67). The model is still certified, so every value is still exact, but probe counts differ. Decoder from per-session mean visible cost: **0.97 test accuracy** unpadded. Paired exact check: 0/50 identical views.

**Defenses** (utility and decoder: N=16,384, decoder over 200 sessions × 16 queries with one payload bit per session, tested on 100; paired exact check: N=4,096, 50 session pairs):

| Defense | Payload decoder (test) | Paired views identical | Visible cost / query | Internal probes | What survives |
| --- | --- | --- | --- | --- | --- |
| Unpadded | 0.97 | 0/50 | 3.69 | 3.69 | full speedup, leaks |
| Pad to worst case (⌊log₂N⌋+1 = 15) | 0.53 (chance) | 50/50 | 15 | 3.69 | no visible gain over binary search; internal work saving only if reclaimed invisibly |
| Pad to certified radius, **sender-chosen** parameters | **1.00** | 0/50 | 5 | 3.69 | leaks: e is chosen by the weights. Capacity ≤ log₂(#distinct padded costs) ≤ log₂15 ≈ 3.9 bits **per parameter choice**: with a single global e, the padded cost is the same for every query, so the per-query cost vector carries nothing extra. With one public radius bucket, ≤ 1 bit (pass/fail) per choice. Bounded, not zero. The bound holds only for this deterministic scalar-cost proxy and a global radius. Per-leaf radii make cost query-dependent, and capacity then grows with the number of distinguishable leaves queried. Richer timing signals are outside the model |
| Pad to radius of a **canonical trusted fit** of z | 0.53 | 50/50 | 5 | 3.69 | 3× lower visible cost than worst-case padding, zero payload flow. But cost = g(z) discloses the radius bucket of z's fit (≤ ~3.9 bits about z), which must be added to the declared release, and the fit procedure becomes trusted |
| Batch / fixed-slot release (B answers at slot B·15) | 0.53 | constant by construction | 15 (latency) | 3.69 | no latency or throughput gain visible to the receiver; internal savings only |

**Conclusion.** Exact values are guaranteed for all weights. Visible work is not. Visible learned speedup survives only if the parameters that determine work are not sender-controlled: a trusted, deterministic, sender-independent training procedure whose output depends on z alone, with its cost profile declared as an authorized disclosure. Otherwise padding (worst case or fixed slot) removes the visible benefit, and radius-dependent padding leaves a bounded per-parameter-choice channel. For agent collusion, an untrusted agent's own learned heuristics cannot buy receiver-visible efficiency without opening a channel of that size. This mirrors classical timing-channel mitigation (padding to worst case; leakage bounded by the number of distinct schedules, e.g. Agat 2000; Askarov–Zhang–Myers CCS 2010). Those are cited from memory as **unverified leads**, not re-read in this pass, and the observation is not claimed new.

## 6. Prior art and novelty status

- **Volpano–Smith-style IFC typing / LLMbda (v2).** Theorem 1 is a standard noninterference-by-typing argument. LLMbda already mechanizes probabilistic IFC for an LLM calculus. Our proof is not a new IFC result.
- **Tiwari et al. (USENIX Sec 2024).** Already uses architecture/training partitioning for data-domain IFC. Treating parameters and optimizer state as labeled wires is the same concern stated in dataflow form; not claimed new.
- **Vehicle.** Neural-to-symbolic specification/proof bridges. Our contracts need no neural specification at all (they hold for every weight setting), which avoids Vehicle's embedding gap but restricts what the learned part may decide.
- **Delimited release; algorithms with predictions (Polak–Schmidt); learned indexes; certifying algorithms.** Supply the release-by-contract and predict-verify-fallback ingredients.
- **Constant-time / side-channel practice.** Proving functional correctness for all inputs while getting timing guarantees only from constant-time execution or data-independent schedules is standard in verified cryptography. Our value-versus-visible-work split is an application of that principle to learned parameters, not a new principle (critique, Gemini 3.1 Pro; accepted).
- **Hypothesis, not a claim:** the specific combination may be under-documented: (i) all-weights value contracts for learned computation inside the release, (ii) parameters as labeled wires, (iii) the observation that visible learned speedups require a trusted, sender-independent learner. A literature search is needed. Machine-found ablation counterexamples are useful evidence, not a novelty axis.

## 7. Cross-family critique (batch 1)

Three critiques were requested on this document and the code; two returned (Sonnet 4.6 spent its whole output budget on hidden reasoning and returned no text). Neither found a well-typed counterexample to Theorem 1. Both verdicts were sound-with-repairs. Dispositions are in `results/arch-a-batch-01/critique/assessment.md`. Accepted repairs: `secondary ⊆ args` and in-impl `impl_out`/`cost` are now enforced by `ir.check`; each contract is proved in an isolated context where every external read is free, so keying contracts by (spec, args, impl) is sound across programs; the Lemma 2 linking caveat; the capacity-bound scope; the novelty downgrade. Rerunning all z3 sections and fuzzing after the repairs gave identical results.

## 8. Limitations

- General-N proofs are pen-and-paper. z3 covers instance sizes N≤8 (witness), N≤16 (index), n=3 (sweep counterexample), plus 5,000 random N=2 programs.
- Deterministic semantics only. Public randomness is a public input wire, so the coupling argument is built in, but probabilistic programs with private sampling feeding releases are not modeled.
- No hardware refinement. R1 uses a deterministic probe proxy.
- The authorized function is trusted. Sender-chosen queries or falsified z are out of scope.
- The scripted adversary shows channel capacity, not autonomous discovery or exploitation.
- The useful task is a learned index, not language generation. The architecture admits any opaque public model *after* the release, but a private learned model may only influence values through a verified contract, which excludes free-form private generation.
