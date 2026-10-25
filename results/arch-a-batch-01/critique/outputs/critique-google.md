Here is an adversarial review of the formal model, proof, implementation, and claims, based strictly on the provided artifact.

### 1. Proof and Implementation Gaps

**Objection 1.1: Release implementation scope and global environment mutation**
*   **Severity:** Medium (Implementation diverges from formal semantics).
*   **Premise:** The formal semantics and proof assume `Release` internal wires are strictly encapsulated ("Release-internal wires are private and unobservable"). Theorem 1 relies on this encapsulation to prevent public ops from reading release internals.
*   **Concrete Counterexample:** In `ir.py`, the `run` function executes `Release.impl` by mutating the global `val` dictionary (`step(sub)`). While `check` marks these wires as `PRIV` and adds them to `internal`, it does not prevent a *subsequent* private operation from reading a release-internal wire, nor does it prevent a subsequent `Release` from reading it. More critically, if a `Release` fails to define `impl_out` inside its `impl`, `run` will silently fetch `val[node.impl_out]` from the global environment if it was defined by a prior op.
*   **Smallest Repair:** In `ir.py`, `check` must verify that `node.impl_out` is actually defined within `node.impl` or previously in the environment. `run` should ideally execute `impl` in a local scope, or `check` should enforce strict non-intersection of internal wire names across the entire program.

**Objection 1.2: Vacuous Contract Checking**
*   **Severity:** Low (Tooling limitation, not a theoretical flaw).
*   **Premise:** The checker accepts a `Release` if `contract_key(node) in contracts`. The key includes `repr(release.impl)`.
*   **Concrete Counterexample:** The checker never structurally validates that `spec_args` are actually the wires being passed to the spec in the contract proof, only that their *kinds* are `SPEC_READABLE`. If a contract is externally verified for `spec_args=['z1']` but the program passes a different authorized wire `z2` that happens to have the same kind, the Python checker might blindly accept it if the external verifier's key generation is sloppy.
*   **Smallest Repair:** The contract verification must be tightly coupled to the SSA wire names, ensuring the z3 proof binds the exact SSA variables used in `spec_args`.

### 2. Timing and Work-Channel Analysis

**Objection 2.1: Sender-chosen padding capacity bound**
*   **Severity:** Low (Analysis is correct but slightly imprecise).
*   **Premise:** Section 5 states that for sender-chosen parameters padded to certified radius, capacity is $\le \log_2(\text{distinct padded costs}) \approx 3.9$ bits per parameter choice.
*   **Argument:** This bound assumes the receiver only observes the *final* padded cost per query. However, if the receiver can issue multiple queries and observe the cost of each, and if the sender can craft a model where different queries hit different certified radii (if the certificate was per-leaf rather than global), the capacity would scale with the number of queries. The artifact uses a global $e$ ("claimed global error radius $e$ against every stored key"), which correctly restricts the channel to the global $e$. The analysis holds for the specific `learned_task.py` implementation, but the text generalizes this to "per parameter choice" without emphasizing that $e$ must be a single global scalar to keep the bound at 3.9 bits.
*   **Smallest Repair:** Clarify in Section 5 that the bounded leakage strictly requires the certified radius $e$ to be a single global bound for the entire model, not a per-region or per-query bound.

### 3. Novelty Claims

**Objection 3.1: Overstated "Candidate Delta" (iii)**
*   **Severity:** Medium.
*   **Premise:** Section 6 claims a candidate delta in "the explicit split between an all-weights *value* guarantee and a trusted-learner requirement for *visible-work* guarantees."
*   **Argument:** This split is fundamentally the standard paradigm of cryptographic constant-time programming and side-channel mitigation. In verified cryptography, functional correctness (value guarantees) is proven for all inputs/weights, while timing guarantees require either strict constant-time execution (padding to worst-case) or data-independent execution (canonical trusted fits). Applying this to learned indexes is a neat systems integration, but framing the *theoretical split* as a novel architectural delta is an overstatement. It is a direct application of classical side-channel threat models to a neural-symbolic boundary.
*   **Smallest Repair:** Downgrade claim (iii) from a "candidate delta" to an "application of standard side-channel mitigation principles to learned-index contracts."

### Conclusion

**Sound-with-repairs.**
The core noninterference argument (Theorem 1) is structurally sound for the idealized SSA calculus. The ablations successfully demonstrate that removing any single typing rule breaks the noninterference guarantee, providing strong empirical backing for the rules' necessity. The timing channel analysis correctly identifies that functional contracts do not prevent work-based side channels and accurately assesses the mitigation tradeoffs. However, the concrete Python implementation (`ir.py`) has minor scoping and validation gaps that could allow malformed programs to execute or bypass intended structural checks. The novelty claims regarding the separation of value and timing guarantees should be tempered to acknowledge standard side-channel literature.
