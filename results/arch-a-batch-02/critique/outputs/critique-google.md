Here is a skeptical review of the Lean 4 mechanization (`Arch.lean`) against the claims in `formal-model.md`.

### 1. Theorem 1 and Semantic Choices (Gap Analysis)
**Finding 1: `impl` is a shallow Lean function, not a sub-program.**
*   **Severity:** High.
*   **Location:** `Node.release`, `run`, `WT.release`.
*   **Mismatch:** The document claims `impl` is a "sub-program (may contain learned ops and read anything)" and that "Release-internal wires are private and unobservable." However, in Lean, `impl` is modeled as a native Lean function `Interp → Env → Val`. It does not consist of `Node`s, it does not execute via `run`, and it generates no intermediate wires. 
*   **Consequence:** The mechanization completely bypasses proving that a sub-program's internal wires are isolated from the outer environment. The isolation is trivially true by the type signature of `impl`. This makes the noninterference proof significantly easier than the Python IR semantics demand.
*   **Smallest Repair:** Change `impl` in `Node.release` to `Prog`. Update `run` to execute the sub-program in a local environment and return its final output.

**Finding 2: Overwriting via `upd` vs SSA freshness.**
*   **Severity:** Low.
*   **Location:** `run` uses `upd` which overwrites; `WT` enforces `Γ out = none` (freshness).
*   **Mismatch:** The semantics (`run`) allow overwriting, but the type system (`WT`) rejects it. Because the theorems assume `WT`, the proofs only apply to strictly SSA programs. This matches the doc's "straight-line SSA list" claim, so it is sound, but the operational semantics are slightly looser than the IR definition.

### 2. `payload_ni` Satisfiability and "All Weights"
**Finding 3: `payload_ni` is satisfiable and correctly quantifies over weights.**
*   **Severity:** None (Verified).
*   **Location:** `payload_ni`.
*   **Assessment:** The theorem correctly quantifies over `ι : Interp` outside the hypotheses. Because `Interp` is `String → List Val → Val`, and weights are passed in the `List Val` arguments, this genuinely covers all interpretations of learned functions and all weight values. The hypotheses only require the initial environments `ρ1` and `ρ2` to agree on `.publicTask`, `.publicRand`, `.publicWeight`, and `.authorized` wires. This is easily satisfiable by constructing two environments that differ only on `.payload` or `.privateWeight` indices.

### 3. Composition Lemma (`ni_compose`)
**Finding 4: `ni_compose` evaluates all releases in the *initial* environment.**
*   **Severity:** Medium.
*   **Location:** `ni_compose` hypothesis `hrel`.
*   **Mismatch:** The lemma concatenates `p ++ q`. The hypothesis `hrel` requires agreement on the specs of all releases in `p ++ q`, evaluated using `sa.map ρ1` (the *initial* environment). In a standard sequential composition, `q` might release a value based on an intermediate wire computed by `p`. If `sa` contained an intermediate wire, evaluating it in the initial environment `ρ1` would yield a default/garbage value, making the theorem mathematically true but practically vacuous for linked programs.
*   **Why it currently holds:** Rule (R1) (`Kind.specReadable`) restricts `specArgs` strictly to `publicTask` or `authorized` wires, which are *initial inputs* defined in `κ`. Therefore, they never refer to intermediate wires, and evaluating them in `ρ1` is sound.
*   **Consequence:** The composition lemma is tightly coupled to (R1). If the architecture is ever extended to allow intermediate public wires in `specArgs`, `ni_compose` as stated will break.

### 4. Witness Contract (`witness_contract` vs `programs.py`)
**Finding 5: The Lean witness contract does not mechanize the IR nodes.**
*   **Severity:** High.
*   **Location:** `witness`, `scanOthers`, `witness_contract`.
*   **Mismatch:** The document claims "Lemma 3, witness cell, all N... machine-checked in Lean 4". The Python IR (`witness_impl` in `programs.py`) implements this using a specific graph of `clamp`, `select`, `neq`, `and`, `or`, and `add` nodes. The Lean mechanization proves a theorem about `scanOthers`, a pure recursive Lean function over `List Bool`. 
*   **Consequence:** The Lean code proves the *algorithmic logic* of an early-exit scan, but it does *not* prove that the SSA node graph in `witness_impl` actually computes this logic. The translation from the IR nodes to `scanOthers` is entirely unverified.
*   **Smallest Repair:** Write a Lean function that generates the `Prog` for `witness_impl(n)` (matching `programs.py`), and prove that `run` on this specific `Prog` yields `ps.any id`.

### 5. What is NOT Covered
As acknowledged in the document, the Lean mechanization omits several realities of the Python IR:
*   **Timing/Cost:** The `cost` wire in `Release` is absent from `Node.release`. `obs` only collects `.observe` values (R0 receiver model). The timing channel analysis in §5 is entirely unmechanized.
*   **Probabilistic Semantics:** `run` is purely deterministic. Public randomness is modeled as an input wire, which forces a coupling argument (the same random tape in both worlds).
*   **Release-Internal State:** As noted in Finding 1, `impl` has no internal wires in Lean, so the ablation `observe_internal` cannot even be expressed in the Lean model.

### Verdict
**Faithful-with-caveats.** 
The core noninterference logic (Theorem 1) and the payload corollary are faithfully mechanized and mathematically sound. However, the mechanization takes significant shortcuts: abstracting sub-programs as native Lean functions bypasses the mechanics of internal-wire isolation, and the witness contract proves a functional algorithm rather than the actual IR node graph. The claims of "machine-checked" should be scoped to the *logic* of the architecture, not the concrete IR implementation.
