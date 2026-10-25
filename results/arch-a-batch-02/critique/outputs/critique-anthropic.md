## Adversarial Review of Arch.lean Statements

### Finding 1 — `ni_init` silently restricts to programs with no private inputs (MODERATE)

**Declaration:** `ni_init`, hypothesis `hpubin : ∀ a k, κ a = some k → k.label = .pub → ρ1 a = ρ2 a`

**Mismatch:** The doc says Theorem 1 holds when ρ₁ ~ ρ₂, meaning "agree on public inputs and every release's spec value agrees." But `ni_init` requires agreement on *all* public-kind wires and separately requires `hrel`. Private wires are unconstrained. That is correct as far as it goes—but the hypothesis `hdef : ∀ a, κ a ≠ none → Γ a ≠ none` inside the inner `ni` lemma requires that every wire mentioned in κ is already in the context Γ. If a wire appears in κ but not in the SSA list (i.e., is an input that was never `Input`-declared in the SSA sense), `ni` can silently treat it as unlabeled (returns `none`) and the `hdef` side-condition may not hold. However, `ctx0 κ` maps every κ-defined wire immediately, so in `ni_init` this is satisfied vacuously. **Severity: low**; the path through `ni_init` is safe.

### Finding 2 — `release` impl reads the entire outer environment (SUBSTANTIVE)

**Declaration:** `Node.release`, field `impl : Interp → Env → Val`

**Mismatch:** The doc says "Release-internal wires are private and unobservable" and that internal computation may "contain learned ops and read anything." In `run`, `impl ι ρ` receives the *entire* outer environment ρ at evaluation time, not a restricted sub-environment. The contract `∀ ι ρ, impl ι ρ = spec (specArgs.map ρ)` must then hold for every ρ—so in principle impl could read payload wire 1 and still satisfy the contract by always returning `spec(specArgs.map ρ)`. The *statement* of `ni` is safe because the contract equality collapses impl to spec(specArgs.map ρ), and (R1) controls specArgs. But this means:

- The modeling *does not* enforce that impl's internal sub-wires are private in the sense of having their own SSA labels; they are invisible to the outer type system entirely.
- A impl that reads payload and happens to satisfy the contract is accepted. The contract check is purely extensional.

**Counterexample sketch:** `impl ι ρ = if ρ 1 = 0 then spec(specArgs.map ρ) else spec(specArgs.map ρ)` satisfies `∀ ι ρ, impl ι ρ = spec(specArgs.map ρ)` trivially but reads payload wire 1. The theorem is still sound (obs is unchanged), but the modeling claim that "release-internal wires are private" is not verified—it is simply not represented.

**Impact on soundness:** None—the theorem is still correct. **Impact on the claim "internal wires are private and unobservable":** The Lean model does not verify this; it relies entirely on the contract obligation. The doc's §2a is honest about this ("A release `impl` is an arbitrary Lean function of `ι` and the whole environment"), but the prose claim "internal wires are private" is architectural, not mechanized. **Severity: caveat, honestly stated in §2a but worth flagging.**

### Finding 3 — `payload_ni` hypothesis satisfiability and weight quantification (IMPORTANT)

**Declaration:** `payload_ni`, hypothesis `hauth : ∀ a, κ a = some .authorized → ρ1 a = ρ2 a`

**Question:** Does this really quantify over all weights?

**Analysis:** Weights are wires of kind `privateWeight`, `publicWeight`, etc. `payload_ni` says: if ρ1 and ρ2 agree on public inputs (`hpubin`) and authorized inputs (`hauth`), observations are equal for *every* `ι`. Since `ι` is universally quantified in `payload_ni`'s statement and ranges over all `Interp = String → List Val → Val`, this covers all learned functions at all weight settings (a weight wire `w` of kind `privateWeight` is an argument to `ι fn`—it's in `args.map ρ`, and ρ can set it arbitrarily between the two worlds). Private-weight wires can *differ* between ρ1 and ρ2 (they're not constrained), so the theorem says observations are equal even when private weights differ—which is exactly the "all weights" claim. **This is correctly stated.**

**Satisfiability:** For a non-trivial program (e.g. `full(n)` from programs.py), the hypotheses are satisfiable: set ρ1 = ρ2 on public and authorized wires, let payload and private weights differ freely. The release has specArgs of kind `publicTask`/`authorized`, so `hauth` is non-vacuous (it constrains z1..zN). ✓

### Finding 4 — `ni_compose` does NOT model multi-session histories as claimed (SUBSTANTIVE)

**Declaration:** `ni_compose`

**Claim (doc §2a):** "Unrolling k sessions gives the history version: equal public history plus equal per-session authorized releases implies equal full transcripts."

**Actual statement:** `ni_compose` takes two programs `p` and `q` typed from *the same* initial κ and input context, concatenates them, and shows noninterference modulo the union of their releases. It is a *single-run* composition theorem: one valuation ρ1 vs ρ2 over a flat SSA concatenation.

**Gap:** True multi-session histories require fresh input wires per session (each session has its own payload, authorized data, etc.). In `ni_compose`, κ is fixed and ρ is a single environment. The document's linking caveat ("Re-importing a private or release-internal value as a fresh public `Input` at a session boundary launders it, and nothing in the current tool prevents that; a label-preserving linker is future work") acknowledges this—but `ni_compose`'s *statement* does not capture the "multi-session" claim at all. It is a sequential composition lemma, not a session-history lemma. The doc's table row says "Lemma 2: concatenation (e.g. unrolled sessions) is well-typed, and noninterferent modulo all components' releases"—"e.g. unrolled sessions" is aspirational if sessions require fresh κ-bindings. **Severity: the statement is a valid composition lemma but is weaker than "multi-session histories."**

**Repair:** Either (a) remove the "multi-session histories" claim from the table, or (b) add a session-indexed version with fresh Wire namespaces and a label-preserving linker condition.

### Finding 5 — `witness_contract` vs `programs.py` semantic gap (MODERATE)

**Declaration:** `witness_contract (j : Nat) (ps : List Bool) : witness j ps = ps.any id`

**programs.py witness_impl:** The Python `witness_impl` uses 1-indexed candidates (`z1..zN`), `clamp1_n` clips `j` to [1,N] (1-indexed), and the predicate list is p1..pN. The Lean `witness` uses 0-indexed `ps.getD j false`. The scan in `scanOthers` uses 0-indexed `i` starting at 0.

**Concrete discrepancy:** If `j = 0` (predictor returns below the valid range), Python clamps to 1 (1-indexed first element), while Lean evaluates `ps.getD 0 false` (0-indexed first element). These agree on the *value* (both get the first element) but for different reasons. If `j = n+1` (above range), Python clamps to n; Lean's `witness` with `j ≥ ps.length` returns `ps.getD j false = false` (out of bounds default), then `scanOthers` covers all elements—so the result is `ps.any id` regardless. The theorem still holds because it states `witness j ps = ps.any id` for *all* j, including out-of-bounds. So the contract is verified for the Lean model. The Python IR uses a separate `clamp1_n` Op before the scan, meaning the Python predictor-chosen index j is always in [1,N] by the time the select/scan logic runs—the Lean model's out-of-bounds case has no Python counterpart. **Mismatch in scope, not in the cases Python exercises; severity: low.**

### Finding 6 — What is NOT covered (confirmed gaps, not new criticism)

**Timing/work-count (R1 receiver model):** `run` produces only `Observe` wire values; cost is not in the semantics. The `cost` wire in `programs.py` is observable in the `observe_internal` ablation but not in the Lean model. This is honestly stated in §2a.

**Probabilistic semantics:** No private sampling; public randomness is a wire. Stated limitation.

**Release-internal labeling:** As noted in Finding 2, internal sub-computation of impl is unmodeled structurally.

**Correspondence of Lean WT to Python `ir.check`:** Not mechanized. The Lean model is a hand translation.

---

## Summary Table

| # | Declaration | Severity | Nature |
|---|---|---|---|
| 1 | `ni_init` / `ni` `hdef` | Low | Vacuous in practice via ctx0 |
| 2 | `release` impl reads full env | Caveat | Honest in §2a; internal privacy not verified structurally |
| 3 | `payload_ni` weight quantification | None | Correctly stated |
| 4 | `ni_compose` as multi-session | Substantive | Weaker than "history" claim |
| 5 | `witness_contract` indexing | Low | Out-of-bounds cases not in Python |
| 6 | Timing, probabilistic, linker | Structural | Honestly stated |

---

## Verdict: **faithful-with-caveats**

The core noninterference statement (`ni_init`, `payload_ni`) is correctly mechanized and the hypotheses match the intended meaning. The weight quantification is genuine. The main substantive gap is `ni_compose` being presented as a multi-session history lemma when it is a single-environment sequential composition lemma—the linking problem (fresh session inputs) is unresolved in both the Lean statement and the Python tool. The impl-reads-full-environment modeling is a conscious simplification that preserves soundness but does not verify internal-wire privacy structurally. No finding invalidates the theorem; the mechanization is honest about its scope.
