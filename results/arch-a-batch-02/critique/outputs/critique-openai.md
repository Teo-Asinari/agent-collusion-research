## 1) Theorem 1 statement vs Lean (`ni` / `ni_init` / `payload_ni`)

### Finding A (HIGH): Lean does **not** enforce “weights are reads that join into the label”
- **Where:** `Arch.Node.op` / `Arch.WT.op`, and the whole absence of a “weight wire” field.
  - `Node.op (out fn args)` has only `args : List Wire`.
  - `WT.op` labels `out` with `joinAll Γ args`.
- **Mismatch:** `formal-model.md` (and the Python IR) explicitly says an `Op` reads:
  1) its argument wires,
  2) its `secondary` args, **and**
  3) its weight wire, and the output label is the join of *all* reads.
  
  In Lean, there is no syntactic place where the checker can require the weight wire to be included in the join. You can simulate “weights-as-wires” only by manually including the weight wire in `args` in the program term—but the *typing rule* does not enforce that discipline.
- **Concrete counterexample (informal but direct):**
  - Let `w` be a private weight wire (`κ w = some .privateWeight`) and `x` be public.
  - Define an op `.op out "F" [x]` where the intended semantics is “uses weight `w` internally”.
  - In Lean, the label of `out` can become public (since it only joins `[x]`), and then `.observe out` is typable, while the interpretation `ι "F"` can depend on `w` *only if `w` is passed in the arguments*—but nothing forces that, so the Lean model simply **cannot represent** “an op uses a private weight without it being an explicit argument”.
- **Why this matters for the claim “quantifies over all weights”:**
  - Lean *does* quantify over all interpretations `ι : String → List Val → Val`, but `ι` only sees the explicit `args.map ρ`. So “all weights” holds **only for weights that are explicitly threaded as arguments everywhere they matter**.
  - This is weaker than the doc’s “weights are ordinary wires passed as args” *as an enforced invariant*.
- **Smallest repair (Lean-side):**
  1) Extend `Node.op` to carry an explicit `weight : Wire` (and optionally `secondary`), and update typing:
     ```lean
     | op (out : Wire) (fn : String) (args : List Wire) (weight : Wire)
     ...
     WT.op ... setCtx Γ out (joinAll Γ (weight :: args)) ...
     ```
  2) Or, if you want to stay minimal: define a *well-formedness predicate* `WF` requiring that for each op symbol `fn`, a designated weight wire is included in `args`. Then Theorem 1 would be for `WT ∧ WF`.

**Severity:** High, because it is exactly one of the ablations in the prose (“weights_not_wires”), and the Lean model currently cannot even *state* the stronger rule.

---

### Finding B (MED): Release output is always public in Lean
- **Where:** `Arch.WT.release` does `WT κ (setCtx Γ out .pub) ...`
- **Mismatch:** The doc says: “A `Release` output is public iff (R1) … and (R2) …”. That suggests it *could* be non-public if conditions don’t hold.
- **What Lean does instead:** A release node is only typable if (R1) and (R2) hold, and then it labels the output as public unconditionally. So “iff” is implemented as “only-if + constructors enforce the if-direction”. Net effect: any well-typed program has only “good releases”.
- **Is this a real semantic gap?** Possibly just presentation: your Lean `WT.release` encodes *the restricted language of valid releases*. If the prose intends that invalid releases exist but get a private label (rather than be rejected), Lean is stricter.
- **Smallest repair:** If you want literal “public iff …”, you’d need a release node that can type-check even when not public, e.g.:
  ```lean
  (if R1∧R2 then setCtx Γ out .pub else setCtx Γ out .priv)
  ```
  but that changes the metatheory surface significantly.

**Severity:** Medium (could be merely a phrasing mismatch, but it does change what “WT” ranges over).

---

### Finding C (LOW/MED): `ni` has extra hypotheses that are easy to misread
- **Where:** `Arch.ni` takes `ρ1₀ ρ2₀` and `hrel` over those, then proves a statement about arbitrary `ρ1 ρ2` under constraints.
- **Potential confusion:** This is not the doc’s Theorem 1 shape (which is about two complete runs from the same initial “input valuation”). Lean’s `ni_init` is the closer match.
- **Is it vacuous/too-strong?** Not vacuous, but `ni` is easy to misuse unless you stick to `ni_init`. In `ni_init`, the extra premises collapse cleanly.

**Severity:** Low/Med (mainly a “statement means something slightly different than the prose headline”, but `ni_init` matches the headline intent).

---

## 2) `payload_ni`: satisfiable? really “all weights”?

### Finding D (MED): “All weights” again depends on explicitly threading them as args
- **Where:** `payload_ni` quantifies over `ι : Interp` (good), but the same limitation from Finding A applies.
- **Satisfiable for realistic programs?** Yes, for programs that:
  - put all private learned parameters into the environment as wires, and
  - ensure every learned op takes those wires as explicit arguments.
  
  But Lean won’t enforce that discipline; you have to treat it as a meta-assumption.

**Smallest repair:** same as Finding A.

**Severity:** Medium (because it directly impacts the advertised “all weights” reading).

---

## 3) `ni_compose` and “multi-session histories”

### Finding E (MED): Composition lemma is only for *literal SSA concatenation*; no session interface discipline
- **Where:** `wt_append`, `releases_append`, `ni_compose`.
- **What it proves:** If `p` is well-typed from `ctx0 κ` to `Γ'` and `q` is well-typed from `Γ'` to `Γ''`, then `p ++ q` is noninterferent modulo combined releases.
- **What it does *not* prove (and cannot, as stated):**
  - Any guarantee about a “linker” that reclassifies wires across session boundaries.
  - Any constraint preventing the laundering issue described in the prose (re-importing private as a fresh public input).
- **Repair:** If you want the “multi-session histories” story formally, you likely need:
  - an explicit session-boundary constructor, or
  - an explicit linking judgment that enforces label preservation across boundaries.

**Severity:** Medium (it matches the doc’s *caveated* claim, but not a stronger one).

---

## 4) `witness_contract` vs `programs.py`

### Finding F (LOW): It matches the *value* contract, but not the work/early-exit structure
- **Where:** `witness_contract`, `scanOthers`, `witness`.
- **Match:** It proves `witness j ps = ps.any id`, i.e. existential correctness independent of predictor `j`. This corresponds to the doc’s “value guarantee”.
- **Differences from Python witness:**
  - Python clamps `j` into `[1..n]`; Lean uses `getD` so out-of-range `j` yields `false` for the candidate probe. Contract still holds.
  - Python’s `k` is a work counter; Lean ignores cost entirely (by design).
  - Python has an operational early-exit structure; Lean’s `scanOthers` is a pure fold-like computation. Value-equivalent, but not an operational model.

**Severity:** Low (given the doc’s explicit R0-only scope for Lean).

---

## 5) What is NOT covered (Lean model gaps)
- **Timing/cost channels:** explicitly absent (`run` has no cost; `WT` has no cost release). (Expected.)
- **Probabilistic semantics / private sampling:** absent; everything is deterministic `Int`. (Expected.)
- **Release internal state / internal observables:** release impl is a single pure function `Interp → Env → Val`. There is no notion of internal wires, so you cannot state/verify “observe_internal” style properties here at all.
- **“Trusted code” distinction:** Lean intentionally quantifies over arbitrary `ι` even for trusted functions, which is *stronger* than the Python model in one sense (fewer assumptions), but also means you can’t exploit algebraic properties of trusted primitives in proofs.

---

## Bottom line
**Verdict: faithful-with-caveats.**

The biggest caveat is **Finding A**: the Lean mechanization does not structurally encode “weights are wires that must be joined into labels”, so the “all weights” reading only holds under an external discipline (“every op that uses weights must receive them as explicit args”). Everything else is broadly consistent with the doc’s stated Lean scope (R0, deterministic, release-by-contract), with composition matching the intended “append/unroll” lemma but not a stronger session-linking story.
