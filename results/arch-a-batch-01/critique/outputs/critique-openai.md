## Objection 1 (high): `secondary` is *not* part of “all reads” in the implementation, contrary to the stated typing rule

**Premise challenged (Formal model §1 / Typing rules):**  
“Label of an `Op` output = join of labels of *all* reads, including `secondary` args…”

**What the code actually does (`ir.check`):**
```py
reads = list(node.args)
# ... may delete some args if mask_only ablation ...
# it never does: reads += node.secondary
```
So the “full checker” only joins over `args` (plus `weight`), not over `secondary` unless the same wires are duplicated into `args`.

**Concrete counterexample program (well-typed under `ir.check` full rules, but violates the *stated* rules):**  
Take an op that semantically uses a private wire as a “secondary read” but does not list it in `args`.

```py
from ir import Input, Op, Observe

P = [
  Input('q', 'public_task'),
  Input('m', 'payload'),          # private
  Op('y', 'Leak', ['q'], kind='trusted', secondary=['m']),
  Observe('y')
]
```

- Under the **stated** typing rule, `y` should be `priv` because it reads `m` via `secondary`.
- Under the **implemented** rule, `reads = ['q']`, so `y` is labeled `pub` and `Observe('y')` is accepted.

**Does it violate Theorem 1 as executed?**  
Not with the current `run()`: `run()` ignores `secondary` completely, so `Leak` is called only on `q`. This makes the counterexample a **model/implementation mismatch**, not (yet) a semantic exploit.

**Smallest repair:**  
Make the artifact match the paper rule *and* make “secondary” real:
- In `check()`: set `reads = node.args + node.secondary` (then apply ablations appropriately).
- In `run()`: decide semantics: either remove `secondary` from the IR entirely (purely a labeling aid), or actually pass them to the function (or otherwise model their effect). Right now it’s neither: it affects labeling in some programs (where duplicated into args), but has no semantic meaning.

**Severity rationale:** high because it undermines the claim that the checker corresponds to the written IFC rule (“including secondary”), and it weakens the interpretation of the ablation results as isolating *exactly* that invariant.

---

## Objection 2 (medium): Lemma 2 (“composition and histories”) is not actually enforced by the checker; it’s a meta-claim that can silently fail in a naive composition pipeline

**Premise challenged (Formal model Lemma 2):**  
“If P₂ reads P₁’s outputs with their labels preserved … then concatenation is well-typed…”

**Gap:**  
The lemma assumes a correct “label-preserving wiring” discipline across sessions/program boundaries. But `ir.check` is per-program; it does not provide (or check) any mechanism that:
- carries labels forward as required, or
- prevents a user from re-introducing P₁’s outputs as fresh `Input(..., kind='public_task')` in P₂.

**Concrete failure mode (not a single well-typed SSA program, but a realistic two-stage integration bug):**
1) P₁ produces a private intermediate internally (fine), then releases a public output `a`.
2) A glue layer accidentally re-imports some internal/cost/state as a *public* `Input` to P₂.

Because kinds are attached only to `Input` nodes, a mis-wiring can “launder” a private value into a public kind at the boundary. Lemma 2’s conclusion then doesn’t apply, but nothing in the artifact prevents such a misuse.

**Smallest repair:**  
If Lemma 2 is part of the intended story, add a “linker” or “session composition” checker:
- a function that composes two IR programs *and* checks that every carried wire keeps its original kind/label, rather than being reintroduced with a different `Input.kind`.
- or represent cross-session carries not as `Input` but as explicit `Carry` nodes with enforced label continuity.

**Severity rationale:** medium: it’s not a logical flaw in Theorem 1 (which is for a single typed program), but it is a gap between the lemma’s stated applicability and what the tooling actually guarantees in a multi-session setting.

---

## Objection 3 (medium): The “cost channel capacity” discussion is directionally right but the stated bound is easy to misread as tighter/more general than justified

**Premise challenged (Formal model §5):**  
“Capacity ≤ log₂(#distinct padded costs) … per parameter choice.”

**Issue:**  
That bound is only for the *specific cost observation you model* (a single deterministic integer per session/query), and only when:
- the receiver observes exactly that scalar and nothing else about time, and
- the sender’s “choice” is restricted to selecting among models that map into a small discrete set of visible costs.

But several nearby variants break the bound without contradicting your model:
- If the receiver sees a **vector of per-query costs** (you often compute a mean in the decoder, but R1 could expose the full vector), then distinct patterns across queries can multiply the number of distinguishable observations even if each element lies in a small set.
- If the sender can induce **data-dependent certificate pass/fail** outcomes across sessions (e.g., by manipulating the definition of “cert” or its trustedness), the observation alphabet increases.

To be clear: within *your* `visible_cost()` definitions, the statement is fine; the objection is that it reads like a generally valid quantitative bound for “padding to radius” rather than a bound for this particular proxy.

**Smallest repair:**  
Clarify that the bound is for the *modeled observation* (scalar padded cost; or constant-over-queries in pad_radius), and state what breaks it (per-query vectors; richer timing signals).

**Severity rationale:** medium: not a refutation, but it’s an overgeneralization risk.

---

## Objection 4 (low-to-medium): “mask_only” ablation is not clearly isolating “mask-only” in the general IR because `secondary` has no semantics

**Premise challenged (Formal model §3 + `programs.py`):**  
“mask_only: join ignores residual/normalization args…”

**Issue:**  
In the IR, “secondary” is only a typing/checking concept, not a semantic one (`run()` ignores it). The ablation works in your crafted program only because you *also* include the “secondary” wire in `args`, so it affects join. That makes the ablation less diagnostic about “mask-only attention” and more about “ignoring a subset of explicit args.”

**Smallest repair:**  
Either:
- remove `secondary` as a field and model “mask-only” more directly (e.g., separate op ports with semantics), or
- give `secondary` real semantics in `run()` and z3 modeling so it actually corresponds to “residual/normalization reads that the mask wouldn’t see.”

**Severity rationale:** low-to-medium: doesn’t break Theorem 1 under the implemented semantics, but weakens the claim that the ablation corresponds to the intended phenomenon.

---

## Novelty check (low): mostly appropriately hedged, but one phrasing risk

Your §6 is generally careful. The main phrasing risk is the “candidate delta (unverified)” list: it could be read as a *compound novelty claim* even though you say a literature check is needed. Easiest fix is to phrase it as “hypothesis: this combination may be under-documented; needs search,” and avoid any implication that machine-found ablations are new as a concept (they are useful evidence, but not a novelty axis by itself).

---

# Bottom line: **sound-with-repairs**

- I did **not** find a concrete single-program counterexample to Theorem 1 **under the implemented semantics** (`run()` + `check()` + “Release is the only edge”)—the structure is a standard IFC-by-typing setup.
- But there is a **high-severity spec/implementation mismatch** around `secondary` (“all reads”) and a **composition/linking gap** for Lemma 2 in realistic multi-session use.
- Repairs are small and local (fix `secondary` handling; add/clarify a linker discipline; tighten timing-capacity scope statements).
