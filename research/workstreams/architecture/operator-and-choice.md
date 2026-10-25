# Neural operations and bounded choice

2026-10-24. Owner endorsed developing neural operations alongside the existing
generator/chooser. Local feasibility proceeds; no paid inference, Modal launch or
full study is selected. Post-creation rewriting remains a separate active approach.

## First operational specification

Let P denote public token states and H protected token states. For stream s:

    A_s(X,C) = softmax((X W_Qs+b_Qs)(C W_Ks+b_Ks)^T / sqrt(d))
               (C W_Vs+b_Vs) W_Os+b_Os
    U = P + A_P(P,P)
    P' = U + FF_P(LN_P(U))
    V = H + A_H(H,concat(stopgrad(P'),H))
    H' = V + FF_H(LN_H(V))

FF is Linear–GELU–Linear. Each stream has independent weights, biases and
per-token normalization. The executable seed is single-head and noncausal.
Protected-to-public matrix blocks are structurally absent, rather than evaluated
and multiplied by zero (which would not exclude NaN propagation).

For fixed public parameters and P, P' is invariant under changes to H and private
parameters. Induction extends this property across a fixed stack. This is an
algebraic argument, not a mechanized proof of PyTorch or physical noninterference.
Cross-stream normalization, private queries/keys in public attention, shared
caches and private-controlled public routing violate the intended separation.

stopgrad prevents a private loss from backpropagating into the public branch.
Public parameters, optimizer state, schedules, data preprocessing, checkpoint
selection and public randomness must also be independent of protected data.
In particular, a private optimizer must exclude public parameters, including
weight decay and other objectives. Arbitrary parameter mutation is not covered.
This is a training obligation, not a guarantee enforced by stopgrad alone.

## Integrating finite choice

The public stream constructs D(P,R), a fixed array of 2^k candidates. The private
stream scores them, and the trusted gate releases exactly D(P,R)[argmax(scores)].
No hidden states or scores are released. This can serve as an internal finite-state
transfer or a final output gate; subsequent public computation may use the gated
state but no other protected values.

For fixed P,R, at most 2^k released values exist, bounding conditional payload
mutual information by k bits. A fixed sequence of gates has at most 2^(sum k_i)
possible content transcripts, even if later gates depend on earlier public releases.
Public randomness must be payload-independent, including conditional on history.
An allowance per token is not the same allowance per answer. Variable gate count,
timing, exceptions, resource use, nonarrival and output diagnostics are outside the
current API. Validation failures are not silently included in the content bound.

At k=0, public task computation and trusted random output variation remain possible;
protected influence through this gate vanishes. Useful authorized functions of
private data need a separately specified verified release contract. Calling a
learned feature task-relevant does not establish that contract.

## Evidence and limitations

- `experiments/leak_cap/operators.py` implements the explicit matrix operations
  and finite candidate gate. Four passing tests cover composed public invariance,
  private-gradient confinement, a cross-normalization counterexample and release
  behavior. No training of this new block has run.
- `experiments/leak_cap/lean/Choice.lean` preserves the Claude worker's abstract
  support-count theorem. Local Lean 4.35.0 accepted it. No executable-refinement
  proof connects this theorem to the Python implementation or neural block.
- `experiments/leak_cap/leakcap.py` recovers the trained worker baseline, adding
  bounded evaluation options, separate non-overwriting output and hashes.
  Checkpoints and external corpus remain in the worker worktree, not vendored here.

A 600-example worker evaluation appeared during recovery: unrestricted accuracy
29.67%, public greedy 5%, six-bit selection 15.5%, six-bit oracle coverage 24.33%.
Our separate 64-example smoke evaluation in `results/leak-cap-recovery/smoke.json`
gives 34.375% unrestricted, 6.25% public greedy and 10.9375% four-bit selection.
Measured scripted payload information at four bits is 3.776 bits per answer;
duplicate candidates reduce it below four. These evaluations use fresh corruptions
of training words, not held-out-vocabulary generalization. The chooser ranks by
language-model likelihood and was not jointly trained as a selector. Neither
result measures spontaneous coordination or supplies a deployment guarantee.
The first recovery attempt refused to overwrite the newly appeared worker output.

Next falsifiable question: at matched data and total computation, does internal
finite-state transfer improve utility over public-only computation and external
candidate selection at the same whole-answer content budget? Before training,
specify a useful task, protected/public input split, authorized output, independent
test units, strong symbolic baseline and failure behavior. Merely moving an existing
chooser inside a conventional model would not establish the architectural contribution.

## Closest verified predecessor

[Tiwari et al., USENIX Security 2024](https://www.usenix.org/system/files/usenixsecurity24-tiwari.pdf),
published PDF, re-accessed 2026-10-24: abstract and introduction, PDF pp. 1–2.
Author claims concern independent training-domain experts with secure gating and
aggregation. This is a direct architectural predecessor. This pass did not audit
proofs or code; earlier section-level reading is in `sources.md`. Our equations
are a design seed; no novelty beyond that work or classical IFC is established.
