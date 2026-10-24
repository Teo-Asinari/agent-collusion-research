## Objection Disposition

**Objection 1 (false-positive initialization bug): Accepted.** The proposed update condition `z_i <_lex min_rec` with `min_rec` initialized to `0^b` fails when the candidate is a false positive: a true match with encoding `> 0^b` would not update `min_rec`, releasing a hallucinated record. The repair is the two-branch update: `if found==0 OR z_i <_lex min_rec`. This is a logic error, not a deep flaw; the repaired construction restores j-independence.

**Objection 2 (full-sweep eliminates neural utility): Accepted, and fatal to the proposal's motivation.** After the repair, the sweep must still visit all N records to guarantee minimum-finding. The predictor contributes nothing to cost; it adds B ticks of overhead. The proposal, as stated, is strictly worse than a plain scan. No adjustment to the min-finding accumulator rescues this—it is structural.

---

## What Does Not Survive

**Withdrawn:** The claim that this extension constitutes a useful next step for the architecture research direction. Releasing the lex-minimum record within the closed machine is a correct construction, but it provides zero learned advantage and is dominated by a trivial no-predictor scan. It is not a compelling design.

---

## The Exact Technical Bottleneck

The core unsolved problem is:

> **Can a neural predictor enable correctness-preserving early termination for minimum-finding, analogous to its role in existence-testing?**

For existence (Boolean F): the predictor guesses a witness j; if P(q, z_j)=1, the answer is immediately certified true without scanning remaining records. This is a genuine shortcut.

For minimum-finding: there is no analogous certificate. Even if the predictor correctly identifies a matching record z_j, certifying that no smaller matching record exists requires either (a) scanning all records with smaller encodings, or (b) a data structure that proves non-existence of smaller matches without full scan.

Path (b) reduces to a verified index problem. A sorted authenticated structure (e.g., a Merkle tree over records sorted by encoding) lets the predictor supply a logarithmic non-inclusion proof for the prefix below z_j. But this makes the neural component vestigial: the verifiable structure does all the work, and the predictor at best selects a candidate to verify against it. This is a standard verifiable database query, not a learned architecture contribution.

**The bottleneck is not an engineering gap—it is that minimum-finding lacks a cheap verifiable witness analogous to a satisfying assignment.** Existence is in NP; minimum under a predicate is harder to certify locally without global information.

---

## Best Surviving Construction (Narrowed Scope)

The Boolean machine from §9–11 remains the sound artifact. Its predicate shortcut is genuinely asymmetric: true-positive prediction avoids up to N-1 predicate evaluations; false-positive triggers bounded fallback with correct result. This is the only task where the predictor's role is architecturally non-vestigial within the closed machine.

**Surviving claim (observation, not proved theorem):** Within the closed abstract machine, existence queries are the unique task class where a neural candidate can provide a verifiable shortcut without requiring full-record-range coverage. Minimum-finding, k-th match, and counting all require Ω(N) predicate evaluations in the worst case regardless of predictor quality, unless the private frame is supplemented with a verified auxiliary index—at which point the neural predictor is redundant.

This is a conjecture, not a proof. A formal lower bound would require an adversarial argument that no certificate shorter than a full scan can verify minimum-ness under an arbitrary predicate P.

---

## Closest-Predecessor Delta (Unchanged Assessment)

Pandey et al. §V-C and the Boolean machine already cover the existence case. No new delta is established here. The minimum-finding extension does not open a gap; it closes one by demonstrating a limit of the predicate-shortcut approach.

---

## Smallest Decisive Next Check

**Not another construction.** The decisive next step is a lower-bound argument:

> **Conjecture:** For any predicate P and any predictor strategy, a machine releasing the lex-minimum matching record must evaluate P on at least the records with encodings ≤ z_min in the worst case, where z_min is the true minimum match.

A formal version: exhibit an adversary that, for any fixed j output by the predictor, constructs two record frames agreeing on all records except one with encoding between 0^b and z_j, such that skipping that record changes the released output. This is a straightforward information-theoretic argument—the minimum can shift to any unevaluated record—and does not require a computer check.

**If the conjecture holds:** minimum-finding is architecturally outside the predicate-shortcut regime. The research direction must either (a) restrict to existence queries and pursue the efficiency question for that case only, or (b) identify a different task class admitting cheap neural certificates.

**If the conjecture fails:** exhibit a task-predicate pair where a neural certificate enables sublinear minimum-finding with correctness. That would be a genuine new algorithmic idea and the actual research contribution.

---

## Research Decision

No compelling design for extending the architecture to content release survives this round. The bottleneck is structural: minimum-finding lacks cheap verifiable witnesses. Further specification work on the closed machine without resolving the witness-existence question for a richer task class would not advance the architecture gate. The open problem is now precisely stated; resolving it requires either a new certificate scheme or a lower-bound proof, not more machine description.
