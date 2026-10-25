
<source path="research/workstreams/architecture/formal-model.md">
# Formal model: labeled learned/verified dataflow with contracted release

2026-10-24, Approach A batches 1–2. **Status: a small formal model whose core noninterference theorem, payload corollary, composition lemma and witness-cell contract (all N) are machine-checked in Lean 4 (§2a). Also: per-instance z3 checks over every interpretation of the learned functions, explicit ablation counterexamples, one non-vacuous task, and a timing-channel analysis.** Not a trained language model, not a novelty claim. Code: [`experiments/verified_arch/`](../../../experiments/verified_arch/README.md). Results: `results/arch-a-batch-01/`.

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

## 2a. Lean mechanization (batch 2)

[`experiments/verified_arch/lean/Arch.lean`](../../../experiments/verified_arch/lean/Arch.lean) is core Lean 4.35.0 with no mathlib. It contains no `sorry`, and `#print axioms` reports only `propext` (plus `Quot.sound` for the witness lemma). Check it with `~/.elan/bin/lean experiments/verified_arch/lean/Arch.lean`; it takes about 1 s.

| Lean declaration | Statement |
| --- | --- |
| `WT κ Γ p Γ'` | The typing judgment: fresh (SSA) outputs; an op's label is the join over all args, with weights passed as args; a release is public only with (R1) readable spec args and (R2) a **Lean proof** `∀ ι ρ, impl ι ρ = spec (specArgs.map ρ)`; observe requires a public wire |
| `ni`, `ni_init` | Theorem 1: for every interpretation `ι` of every function symbol, worlds that agree on public inputs and on every declared release value give identical observations |
| `payload_ni` | Corollary: worlds that agree on public inputs and authorized data give identical observations, whatever the payload, private weights, private randomness and private state |
| `wt_append`, `releases_append`, `ni_compose` | Lemma 2: concatenation (e.g. unrolled sessions) is well-typed, and noninterferent modulo all components' releases |
| `witness_contract` | Lemma 3, witness cell, all N: candidate-first evaluation equals `any` for every candidate index j |
| three `example`s | Necessity: dropping (R1), the contract, or the join rule each gives a concrete payload leak, and the full `WT` rejects each program |

Modeling differences from the Python IR, which make the Lean theorem neither weaker nor easier in the directions we found:
- *All* function symbols, trusted ones included, are arbitrary in `ι`, so the theorem is uniform over trusted code as well as weights.
- A release `impl` is an arbitrary Lean function of `ι` and the whole environment. Its internal wires never enter the outer environment, which matches `observe_internal` being forbidden.
- Values are `Int` and wires `Nat`; overwriting is excluded by the freshness premise.
- Only R0 observations are modeled: no cost, timing or probabilistic sampling. Public randomness is an input wire.
- Not mechanized: the learned-index contract for general N, and the type checker's correspondence to `ir.check` (it is a hand translation).

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

Honest limits: the learned model is a regression index, not a transformer (the theory treats it as an opaque function, so this is a choice of test vehicle). A 32-unit tanh MLP on raw keys certified only e=10,820, with no saving. Learned indexes with error bounds are prior art (Kraska et al., SIGMOD 2018: §2 and §3.4 primary-checked in batch 2; min/max error over stored keys guarantees that existing keys are found). Per-query model evaluation, fit and the O(N) certificate are extra costs not counted in probes. No wall-clock comparison is made.

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

**Conclusion.** Exact values are guaranteed for all weights. Visible work is not. Visible learned speedup survives only if the parameters that determine work are not sender-controlled: a trusted, deterministic, sender-independent training procedure whose output depends on z alone, with its cost profile declared as an authorized disclosure. Otherwise padding (worst case or fixed slot) removes the visible benefit, and radius-dependent padding leaves a bounded per-parameter-choice channel. For agent collusion, an untrusted agent's own learned heuristics cannot buy receiver-visible efficiency without opening a channel of that size. This mirrors classical timing-channel mitigation. Askarov–Zhang–Myers (CCS 2010, §2.2–2.3, primary-checked) bound leakage by the log of the number of distinguishable timing outcomes, with O(log²T) for their doubling mitigator, and our per-parameter-choice bound is the same counting argument at a coarser grain. Agat (POPL 2000) removes timing leaks by type-directed padding; only the thesis abstract was read, and the details are unverified. The observation is not claimed new; see `sources.md`.

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

- Theorem 1, the payload corollary, composition and the witness contract are mechanized in Lean for the Lean model (§2a). The learned-index contract for general N and the correspondence between the Lean `WT` and Python `ir.check` are not. z3 covers instance sizes N≤8 (witness), N≤16 (index), n=3 (sweep counterexample), plus 5,000 random N=2 programs.
- Deterministic semantics only. Public randomness is a public input wire, so the coupling argument is built in, but probabilistic programs with private sampling feeding releases are not modeled.
- No hardware refinement. R1 uses a deterministic probe proxy.
- The authorized function is trusted. Sender-chosen queries or falsified z are out of scope.
- The scripted adversary shows channel capacity, not autonomous discovery or exploitation.
- The useful task is a learned index, not language generation. The architecture admits any opaque public model *after* the release, but a private learned model may only influence values through a verified contract, which excludes free-form private generation.

</source>

<source path="experiments/verified_arch/lean/Arch.lean">
/-
Mechanized core of research/workstreams/architecture/formal-model.md (Theorem 1,
Lemma 2, payload corollary, witness-cell contract for all N). Core Lean 4 only.

Modeling choices relative to the Python IR (ir.py):
* Every function symbol is interpreted by an arbitrary `ι : Interp`, so the
  theorems quantify over all learned weights AND all "trusted" code at once.
  Weights are ordinary wires passed as arguments, as in the Python IR.
* `secondary` args are just args (the full rule joins over all of them).
* A release's implementation is an arbitrary function of the interpretation and
  the whole environment; its internal wires never enter the outer environment.
  The typing rule demands a Lean proof of the contract `impl = spec ∘ args`.
* Observations are values of `observe` nodes only (receiver model R0). Cost or
  timing is not modeled here.
-/
namespace Arch

abbrev Val := Int
abbrev Wire := Nat
abbrev Env := Wire → Val
abbrev Interp := String → List Val → Val

inductive Label where
  | pub
  | priv
  deriving DecidableEq

def Label.join : Label → Label → Label
  | .pub, .pub => .pub
  | _, _ => .priv

inductive Kind where
  | publicTask | publicRand | publicWeight
  | authorized | payload | privateWeight | privateRand | privateState
  deriving DecidableEq

def Kind.label : Kind → Label
  | .publicTask | .publicRand | .publicWeight => .pub
  | _ => .priv

/-- Rule (R1): a release spec may read only public task data and authorized data. -/
def Kind.specReadable : Kind → Bool
  | .publicTask | .authorized => true
  | _ => false

inductive Node where
  | op (out : Wire) (fn : String) (args : List Wire)
  | release (out : Wire) (spec : List Val → Val) (specArgs : List Wire)
      (impl : Interp → Env → Val)
  | observe (w : Wire)

abbrev Prog := List Node

def upd (ρ : Env) (w : Wire) (v : Val) : Env := fun x => if x = w then v else ρ x

/-- Big-step semantics: observations and final environment. -/
def run (ι : Interp) : Prog → Env → List Val × Env
  | [], ρ => ([], ρ)
  | .op out fn args :: p, ρ => run ι p (upd ρ out (ι fn (args.map ρ)))
  | .release out _ _ impl :: p, ρ => run ι p (upd ρ out (impl ι ρ))
  | .observe w :: p, ρ => ((ρ w) :: (run ι p ρ).1, (run ι p ρ).2)

def obs (ι : Interp) (p : Prog) (ρ : Env) : List Val := (run ι p ρ).1

abbrev Ctx := Wire → Option Label

def joinAll (Γ : Ctx) : List Wire → Label
  | [] => .pub
  | a :: as =>
    match Γ a with
    | some l => l.join (joinAll Γ as)
    | none => .priv

def setCtx (Γ : Ctx) (w : Wire) (l : Label) : Ctx :=
  fun x => if x = w then some l else Γ x

/-- Initial context: input wires carry the label of their kind. -/
def ctx0 (κ : Wire → Option Kind) : Ctx := fun a => (κ a).map Kind.label

/-- Typing judgment `WT κ Γ p Γ'`: p is well typed from context Γ, ending in Γ'.
Outputs must be fresh (SSA), op labels join over all reads, a release output is
public only with readable spec args and a proof of its contract, and only public
wires may be observed. -/
inductive WT (κ : Wire → Option Kind) : Ctx → Prog → Ctx → Prop where
  | nil (Γ : Ctx) : WT κ Γ [] Γ
  | op {Γ Γ' : Ctx} {out : Wire} {fn : String} {args : List Wire} {p : Prog} :
      Γ out = none →
      WT κ (setCtx Γ out (joinAll Γ args)) p Γ' →
      WT κ Γ (.op out fn args :: p) Γ'
  | release {Γ Γ' : Ctx} {out : Wire} {spec : List Val → Val} {specArgs : List Wire}
      {impl : Interp → Env → Val} {p : Prog} :
      Γ out = none →
      (∀ a ∈ specArgs, ∃ k, κ a = some k ∧ k.specReadable = true) →
      (∀ ι ρ, impl ι ρ = spec (specArgs.map ρ)) →
      WT κ (setCtx Γ out .pub) p Γ' →
      WT κ Γ (.release out spec specArgs impl :: p) Γ'
  | observe {Γ Γ' : Ctx} {w : Wire} {p : Prog} :
      Γ w = some .pub →
      WT κ Γ p Γ' →
      WT κ Γ (.observe w :: p) Γ'

/-- The declared releases of a program: (spec, spec args). -/
def releases : Prog → List ((List Val → Val) × List Wire)
  | [] => []
  | .release _ s sa _ :: p => (s, sa) :: releases p
  | _ :: p => releases p

/-! ### Helper lemmas -/

theorem map_congr' {f g : Wire → Val} :
    ∀ (l : List Wire), (∀ a ∈ l, f a = g a) → l.map f = l.map g
  | [], _ => rfl
  | a :: l, h => by
    simp only [List.map_cons]
    rw [h a (List.mem_cons_self ..), map_congr' l (fun b hb => h b (List.mem_cons_of_mem _ hb))]

theorem join_pub {l m : Label} (h : l.join m = .pub) : l = .pub ∧ m = .pub := by
  cases l <;> cases m <;> simp_all [Label.join]

theorem joinAll_pub (Γ : Ctx) :
    ∀ (args : List Wire), joinAll Γ args = .pub → ∀ a ∈ args, Γ a = some .pub
  | [], _, a, ha => by cases ha
  | b :: bs, h, a, ha => by
    unfold joinAll at h
    split at h
    · rename_i l hl
      have ⟨h1, h2⟩ := join_pub h
      cases ha with
      | head => rw [hl, h1]
      | tail _ hmem => exact joinAll_pub Γ bs h2 a hmem
    · cases h

/-! ### Theorem 1: noninterference modulo declared release, for every interpretation -/

theorem ni (κ : Wire → Option Kind) (ι : Interp) {Γ Γ' : Ctx} {p : Prog}
    (h : WT κ Γ p Γ') (ρ1₀ ρ2₀ : Env)
    (hrel : ∀ s sa, (s, sa) ∈ releases p → s (sa.map ρ1₀) = s (sa.map ρ2₀)) :
    ∀ (ρ1 ρ2 : Env),
      (∀ w, Γ w = some .pub → ρ1 w = ρ2 w) →
      (∀ a, κ a ≠ none → Γ a ≠ none) →
      (∀ a, κ a ≠ none → ρ1 a = ρ1₀ a ∧ ρ2 a = ρ2₀ a) →
      obs ι p ρ1 = obs ι p ρ2 := by
  induction h with
  | nil => intro ρ1 ρ2 _ _ _; rfl
  | @op Γ Γ' out fn args p hfresh _ ih =>
    intro ρ1 ρ2 hpub hdef hin
    simp only [obs, run]
    apply ih (fun s sa hm => hrel s sa (by simpa [releases] using hm))
    · intro w hw
      simp only [setCtx] at hw
      simp only [upd]
      by_cases hwo : w = out
      · simp only [hwo, ite_true] at hw ⊢
        have hargs := joinAll_pub Γ args (Option.some.inj hw)
        rw [map_congr' args (fun a ha => hpub a (hargs a ha))]
      · simp only [hwo, ite_false] at hw ⊢
        exact hpub w hw
    · intro a ha
      simp only [setCtx]
      by_cases hao : a = out
      · simp [hao]
      · simp only [hao, ite_false]; exact hdef a ha
    · intro a ha
      have hne : a ≠ out := fun he => hdef a ha (he ▸ hfresh)
      simp only [upd, hne, ite_false]
      exact hin a ha
  | @release Γ Γ' out spec specArgs impl p hfresh hread hcon _ ih =>
    intro ρ1 ρ2 hpub hdef hin
    simp only [obs, run]
    apply ih (fun s sa hm => hrel s sa (List.mem_cons_of_mem _ hm))
    · intro w hw
      simp only [setCtx] at hw
      simp only [upd]
      by_cases hwo : w = out
      · simp only [hwo, ite_true]
        rw [hcon ι ρ1, hcon ι ρ2]
        have e1 : specArgs.map ρ1 = specArgs.map ρ1₀ :=
          map_congr' specArgs (fun a ha => by
            obtain ⟨k, hk, _⟩ := hread a ha
            exact (hin a (by simp [hk])).1)
        have e2 : specArgs.map ρ2 = specArgs.map ρ2₀ :=
          map_congr' specArgs (fun a ha => by
            obtain ⟨k, hk, _⟩ := hread a ha
            exact (hin a (by simp [hk])).2)
        rw [e1, e2]
        exact hrel spec specArgs (List.mem_cons_self ..)
      · simp only [hwo, ite_false] at hw ⊢
        exact hpub w hw
    · intro a ha
      simp only [setCtx]
      by_cases hao : a = out
      · simp [hao]
      · simp only [hao, ite_false]; exact hdef a ha
    · intro a ha
      have hne : a ≠ out := fun he => hdef a ha (he ▸ hfresh)
      simp only [upd, hne, ite_false]
      exact hin a ha
  | @observe Γ Γ' w p hw _ ih =>
    intro ρ1 ρ2 hpub hdef hin
    simp only [obs, run]
    rw [hpub w hw]
    have := ih (fun s sa hm => hrel s sa (by simpa [releases] using hm)) ρ1 ρ2 hpub hdef hin
    simp only [obs] at this
    rw [this]

/-- Theorem 1 from the initial context: two worlds that agree on public inputs and
on every declared release value give identical observations, for every
interpretation of every function symbol (all weights). -/
theorem ni_init (κ : Wire → Option Kind) (ι : Interp) {p : Prog} {Γ' : Ctx}
    (h : WT κ (ctx0 κ) p Γ') (ρ1 ρ2 : Env)
    (hpubin : ∀ a k, κ a = some k → k.label = .pub → ρ1 a = ρ2 a)
    (hrel : ∀ s sa, (s, sa) ∈ releases p → s (sa.map ρ1) = s (sa.map ρ2)) :
    obs ι p ρ1 = obs ι p ρ2 := by
  apply ni κ ι h ρ1 ρ2 hrel ρ1 ρ2
  · intro w hw
    simp only [ctx0] at hw
    cases hk : κ w with
    | none => simp [hk] at hw
    | some k =>
      simp only [hk, Option.map_some] at hw
      exact hpubin w k hk (Option.some.inj hw)
  · intro a ha
    simp only [ctx0]
    cases hk : κ a with
    | none => exact absurd hk ha
    | some k => simp
  · intro a _; exact ⟨rfl, rfl⟩

/-! ### Rule (R1) makes the release condition a condition on authorized data only -/

theorem releases_readable (κ : Wire → Option Kind) {Γ Γ' : Ctx} {p : Prog}
    (h : WT κ Γ p Γ') :
    ∀ s sa, (s, sa) ∈ releases p → ∀ a ∈ sa, ∃ k, κ a = some k ∧ k.specReadable = true := by
  induction h with
  | nil => intro s sa hm; cases hm
  | op _ _ ih => intro s sa hm; exact ih s sa (by simpa [releases] using hm)
  | @release Γ Γ' out spec specArgs impl p _ hread _ _ ih =>
    intro s sa hm
    simp only [releases] at hm
    cases hm with
    | head => exact hread
    | tail _ hm' => exact ih s sa hm'
  | observe _ _ ih => intro s sa hm; exact ih s sa (by simpa [releases] using hm)

/-- **Payload corollary.** If two worlds agree on all public inputs and on all
authorized data, then for every interpretation (all weights, all predictors,
all readouts) observations are identical, whatever the payload, private
weights, private randomness and private state. -/
theorem payload_ni (κ : Wire → Option Kind) (ι : Interp) {p : Prog} {Γ' : Ctx}
    (h : WT κ (ctx0 κ) p Γ') (ρ1 ρ2 : Env)
    (hpubin : ∀ a k, κ a = some k → k.label = .pub → ρ1 a = ρ2 a)
    (hauth : ∀ a, κ a = some .authorized → ρ1 a = ρ2 a) :
    obs ι p ρ1 = obs ι p ρ2 := by
  apply ni_init κ ι h ρ1 ρ2 hpubin
  intro s sa hm
  congr 1
  apply map_congr' sa
  intro a ha
  obtain ⟨k, hk, hr⟩ := releases_readable κ h s sa hm a ha
  cases k with
  | publicTask => exact hpubin a .publicTask hk rfl
  | authorized => exact hauth a hk
  | _ => simp [Kind.specReadable] at hr

/-! ### Lemma 2: composition (sequential programs, multi-session unrolling) -/

theorem wt_append (κ : Wire → Option Kind) {Γ Γ' Γ'' : Ctx} {p q : Prog}
    (hp : WT κ Γ p Γ') (hq : WT κ Γ' q Γ'') : WT κ Γ (p ++ q) Γ'' := by
  induction hp with
  | nil => exact hq
  | op hf _ ih => exact WT.op hf (ih hq)
  | release hf hr hc _ ih => exact WT.release hf hr hc (ih hq)
  | observe hw _ ih => exact WT.observe hw (ih hq)

theorem releases_append : ∀ (p q : Prog), releases (p ++ q) = releases p ++ releases q
  | [], _ => rfl
  | .op .. :: p, q => by simp [releases, releases_append p q]
  | .release .. :: p, q => by simp [releases, releases_append p q]
  | .observe .. :: p, q => by simp [releases, releases_append p q]

/-- Composed (e.g. k unrolled sessions) programs are noninterferent modulo the
concatenated releases of all components. -/
theorem ni_compose (κ : Wire → Option Kind) (ι : Interp) {p q : Prog} {Γ' Γ'' : Ctx}
    (hp : WT κ (ctx0 κ) p Γ') (hq : WT κ Γ' q Γ'') (ρ1 ρ2 : Env)
    (hpubin : ∀ a k, κ a = some k → k.label = .pub → ρ1 a = ρ2 a)
    (hrel : ∀ s sa, (s, sa) ∈ releases p ++ releases q → s (sa.map ρ1) = s (sa.map ρ2)) :
    obs ι (p ++ q) ρ1 = obs ι (p ++ q) ρ2 :=
  ni_init κ ι (wt_append κ hp hq) ρ1 ρ2 hpubin (by rw [releases_append]; exact hrel)

/-! ### Lemma 3 (witness cell contract, all N, every predictor)

Predictor-first existential check: evaluate the candidate j chosen by any learned
predictor, then scan every other index. The value equals `ps.any id` for every
j and every predicate-value list. -/

def scanOthers (j : Nat) : List Bool → Nat → Bool
  | [], _ => false
  | p :: ps, i => ((i != j) && p) || scanOthers j ps (i + 1)

def witness (j : Nat) (ps : List Bool) : Bool := ps.getD j false || scanOthers j ps 0

theorem scan_any (j : Nat) :
    ∀ (ps : List Bool) (i : Nat),
      ((ps.getD (j - i) false && decide (i ≤ j)) || scanOthers j ps i) = ps.any id
  | [], i => by simp [scanOthers]
  | p :: ps, i => by
    have ih := scan_any j ps (i + 1)
    simp only [scanOthers, List.any_cons, id]
    by_cases hij : i = j
    · subst hij
      have h1 : decide (i + 1 ≤ i) = false := by simp
      rw [h1, Bool.and_false, Bool.false_or] at ih
      simp [ih]
    · have hne : (i != j) = true := by simp [hij]
      rw [hne, Bool.true_and]
      by_cases hle : i ≤ j
      · have hlt : i + 1 ≤ j := by omega
        have hsub : j - i = (j - (i + 1)) + 1 := by omega
        rw [hsub, List.getD_cons_succ]
        simp only [hle, hlt, decide_true, Bool.and_true] at ih ⊢
        rw [← ih]
        cases p <;> cases (ps.getD (j - (i + 1)) false) <;> simp
      · have hlt : ¬ (i + 1 ≤ j) := by omega
        simp only [hle, hlt, decide_false, Bool.and_false, Bool.false_or] at ih ⊢
        rw [ih]

theorem witness_contract (j : Nat) (ps : List Bool) : witness j ps = ps.any id := by
  have := scan_any j ps 0
  simp only [Nat.sub_zero, Nat.zero_le, decide_true, Bool.and_true] at this
  exact this

/-! ### Necessity examples (concrete counterexamples when a rule is dropped) -/

/-- Wire 0: public task, wire 1: payload. -/
def κex : Wire → Option Kind
  | 0 => some .publicTask
  | 1 => some .payload
  | _ => none

def ρm (m : Val) : Env := fun w => if w = 1 then m else 0

/-- (R1) dropped: a release whose spec reads the payload, with a valid contract. -/
def leakSpec : Prog :=
  [.release 2 (fun l => l.headD 0) [1] (fun _ ρ => ρ 1), .observe 2]

example (ι : Interp) : obs ι leakSpec (ρm 0) ≠ obs ι leakSpec (ρm 1) := by
  simp [obs, run, leakSpec, upd, ρm]

/-- Contract dropped: release claims spec "constant 0" but outputs the payload. -/
def leakImpl : Prog :=
  [.release 2 (fun _ => 0) [0] (fun _ ρ => ρ 1), .observe 2]

example (ι : Interp) : obs ι leakImpl (ρm 0) ≠ obs ι leakImpl (ρm 1) := by
  simp [obs, run, leakImpl, upd, ρm]

/-- Join rule dropped: an op reading the payload labeled public. Here, with
the identity interpretation of "id". -/
def leakOp : Prog := [.op 2 "id" [1], .observe 2]

example : obs (fun _ l => l.headD 0) leakOp (ρm 0) ≠
    obs (fun _ l => l.headD 0) leakOp (ρm 1) := by
  simp [obs, run, leakOp, upd, ρm]

/-- And the full checker rejects each of them: R1, the contract, and the join rule. -/
example : ¬ ∃ Γ', WT κex (ctx0 κex) leakSpec Γ' := by
  rintro ⟨Γ', h⟩
  cases h with
  | release _ hread _ _ =>
    obtain ⟨k, hk, hr⟩ := hread 1 (by simp)
    simp [κex] at hk; subst hk; simp [Kind.specReadable] at hr

example : ¬ ∃ Γ', WT κex (ctx0 κex) leakImpl Γ' := by
  rintro ⟨Γ', h⟩
  cases h with
  | release _ _ hcon _ =>
    have := hcon (fun _ _ => 0) (ρm 1)
    simp [ρm] at this

example : ¬ ∃ Γ', WT κex (ctx0 κex) leakOp Γ' := by
  rintro ⟨Γ', h⟩
  cases h with
  | op _ h2 =>
    cases h2 with
    | observe hw _ =>
      simp [setCtx, joinAll, ctx0, κex, Kind.label, Label.join] at hw

end Arch

</source>

<source path="experiments/verified_arch/programs.py">
"""Concrete IR programs: the witness cell, its public readout, and one-invariant ablations.

Values are integers; booleans are 0/1. `P` is the fixed trusted task predicate;
names starting with `Net` or listed in OPAQUE are learned/opaque functions.
"""
from ir import Input, Op, Release, Observe

OPAQUE = {'NetPred', 'NetPub', 'NetGrad', 'NetH', 'Norm', 'Sgd'}


def witness_impl(n, pred_args=('q', 'c', 'm'), out='v', cost='cost'):
    """Predictor-first existential check with early-exit fallback scan."""
    impl = [Op('j', 'NetPred', list(pred_args), kind='neural', weight='theta'),
            Op('jc', f'clamp1_{n}', ['j'])]
    impl += [Op(f'p{i}', 'P', ['q', f'z{i}']) for i in range(1, n + 1)]
    impl += [Op('v0', f'select_{n}', ['jc'] + [f'p{i}' for i in range(1, n + 1)]),
             Op('k0', 'one', [])]
    for i in range(1, n + 1):
        impl += [Op(f'ji{i}', f'neq_{i}', ['jc']),
                 Op(f'nv{i}', 'not', [f'v{i-1}']),
                 Op(f'ev{i}', 'and', [f'nv{i}', f'ji{i}']),
                 Op(f'hit{i}', 'and', [f'ev{i}', f'p{i}']),
                 Op(f'v{i}', 'or', [f'v{i-1}', f'hit{i}']),
                 Op(f'k{i}', 'add', [f'k{i-1}', f'ev{i}'])]
    impl += [Op(out, 'id', [f'v{n}']), Op(cost, 'id', [f'k{n}'])]
    return impl


def inputs(n):
    nodes = [Input('q', 'public_task'), Input('r', 'public_rand'),
             Input('phi', 'public_weight'), Input('c', 'private_state'),
             Input('m', 'payload'), Input('theta', 'private_weight')]
    nodes += [Input(f'z{i}', 'authorized') for i in range(1, n + 1)]
    return nodes


def spec_args(n):
    return ['q'] + [f'z{i}' for i in range(1, n + 1)]


def full(n):
    """Accepted architecture: private witness cell, exact release, public readout.

    Private training of theta is allowed and stays private.
    """
    return inputs(n) + [
        Op('g', 'NetGrad', ['c', 'm'] + [f'z{i}' for i in range(1, n + 1)],
           kind='neural', weight='theta'),
        Op('theta2', 'Sgd', ['theta', 'g']),
        Release('a', f'exists_{n}', spec_args(n), witness_impl(n), 'v', cost='cost'),
        Op('y', 'NetPub', ['q', 'a', 'r'], kind='neural', weight='phi'),
        Observe('a'), Observe('y')]


def ablation(name, n):
    """Program rejected by the full checker; accepted when `name` is ablated."""
    base = inputs(n)
    rel = Release('a', f'exists_{n}', spec_args(n), witness_impl(n), 'v', cost='cost')
    if name == 'mask_only':
        # Public token normalized with statistics that include a private activation.
        return base + [rel,
                       Op('h', 'NetH', ['c', 'm'], kind='neural', weight='theta'),
                       Op('y', 'NetPub', ['q', 'a', 'r', 'h'], kind='neural',
                          weight='phi', secondary=['h']),
                       Observe('a'), Observe('y')]
    if name == 'weights_not_wires':
        # Shared public readout fine-tuned on a private, payload-dependent gradient.
        return base + [rel,
                       Op('g', 'NetGrad', ['c', 'm'], kind='neural', weight='theta'),
                       Op('phi2', 'Sgd', ['phi', 'g']),
                       Op('y', 'NetPub', ['q', 'a', 'r'], kind='neural', weight='phi2'),
                       Observe('a'), Observe('y')]
    if name == 'trust_release':
        # Claims the exists spec but releases the predictor-chosen index.
        bad = witness_impl(n) + [Op('leak', 'id', ['jc'])]
        return base + [Release('a', f'exists_{n}', spec_args(n), bad, 'leak'),
                       Op('y', 'NetPub', ['q', 'a', 'r'], kind='neural', weight='phi'),
                       Observe('a'), Observe('y')]
    if name == 'spec_reads_anything':
        # Contract holds for a declared spec that itself reads the payload.
        impl = witness_impl(n) + [Op('vx', 'xor', ['v', 'm'])]
        return base + [Release('a', f'existsxor_{n}', spec_args(n) + ['m'], impl, 'vx'),
                       Op('y', 'NetPub', ['q', 'a', 'r'], kind='neural', weight='phi'),
                       Observe('a'), Observe('y')]
    if name == 'observe_internal':
        # Correct release, but the receiver sees its internal work count.
        return base + [rel,
                       Op('y', 'NetPub', ['q', 'a', 'r'], kind='neural', weight='phi'),
                       Observe('a'), Observe('y'), Observe('cost')]
    raise ValueError(name)


def py_trusted(n):
    """Python semantics for trusted (non-opaque) functions used above."""
    fns = {
        f'clamp1_{n}': lambda j: min(max(int(j), 1), n),
        f'select_{n}': lambda j, *p: p[j - 1],
        'one': lambda: 1, 'id': lambda x: x,
        'not': lambda x: 1 - x, 'and': lambda x, y: x & y,
        'or': lambda x, y: x | y, 'xor': lambda x, y: x ^ y,
        'add': lambda x, y: x + y,
    }
    for i in range(1, n + 1):
        fns[f'neq_{i}'] = (lambda i: lambda j: int(j != i))(i)
    return fns

</source>