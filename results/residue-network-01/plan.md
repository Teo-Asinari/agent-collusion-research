# Architecture design loop: exact neural arithmetic

2026-10-25. Owner insists on architecture design and proof on a small set by EOD,
and authorizes intelligent local iteration. The proposed rewrite pivot is rejected.
No new hosted/cloud budget. This is a scoped proof/learning feasibility study,
not evidence of a novel general language architecture.

## What will be built

A two-input, two-hidden-unit polynomial network with nine learned parameters.
All input words and weights are integers 0..8. Arithmetic is modulo 9; observations
are modulo 3. Words differing by a multiple of 3 represent the same permitted task
value. Every allowed operation must preserve that equivalence.

    h_i = (w_i1*x1 + w_i2*x2 + b_i)^2 mod 9
    y = (v1*h1 + v2*h2 + bo) mod 9
    released_answer = y mod 3

Both hidden affine maps, both hidden biases, the output weights and output bias
are trained: nine parameters total. This is not the earlier fixed-feature readout
draft. That draft was rejected before execution because hidden weights were fixed.

## Loop fixed before execution

1. Keep the float quotient neuron as a known failing exact-security baseline.
2. Prove modular polynomial operation/composition noninterference in Lean. Extend
   the abstract expression grammar to the concrete nine-weight network.
3. Try exact formal-gradient updates on the network: two learning rates (1,2),
   four fixed initial seeds (20261025..20261028), up to 64 steps per attempt.
   Stop on perfect truth-table fit or a repeated semantic weight state. Log every
   state and outcome. The gradient is the formal polynomial derivative of
   (1/2)*sum(error^2) in Z/9Z, not continuous real backpropagation. Loss modulo 9
   can be zero without correct answers; success requires all answers correct.
4. If some tasks fail, use finite weight search as an explicit training repair:
   enumerate all 3^9=19,683 semantic weight vectors, select the lexicographically
   first consistent network. Input and label observations determine selection.
   No assertion of scalable training or held-out generalization follows.
5. Attack the learned models exhaustively and record pass/fail. Stop this design
   loop with a report; do not add unrelated theory or tasks to this run.

## Fixed tasks, comparisons and finite universes

- All sixteen Boolean functions of two inputs. Each task supplies all four truth
  table rows for training and verification. There is no held-out-data claim.
- Compare gradient training, finite neural weight search, all 27 modular affine
  three-weight models, and a direct four-entry truth-table solver. The affine
  baseline is modular, not a real-valued linear-threshold classifier. No efficiency
  or expressivity gain over lookup-table solving is claimed.
- Forward attack: all 3^9 independent high-digit weight lifts and all 4*3^2=36
  input words, per learned task. Total 708,588 cases per task; 11,337,408 cases
  across sixteen tasks. Include all inputs, not just a favourable example.
- Training-label attack: all 3^4=81 independent label-lift vectors per task;
  selected semantic weights must be identical. Verify learning decisions use only
  remainders, rather than running expensive search for identical views.
- Training-input attack: all 3^8=6,561 independent lifts of the eight input words
  in each complete training table. Verify observed training data and hence the
  deterministic selected network are unchanged. This covers inputs and labels
  separately, not their full Cartesian product.
- Include 256 seeded joint input/label-lift training cases per task, with hashes.
  They stress joint combinations but are not exhaustive.
- Positive controls: releasing the raw output must transmit a scripted trit via
  the output bias; a forbidden high-digit extractor must break same-remainder
  equivalence. These are instructed channels, not spontaneous collusion.

## What counts as success

All sixteen tasks must be representable and exactly fitted; every forward case
must return the task answer; all declared training attacks must preserve semantic
training inputs and selection; Lean must accept the arithmetic/composition proof
and instantiated finite task certificates. Any failure is logged and repaired or
the corresponding claim withdrawn. No statistical confidence intervals are used
for exhaustive finite checks.

The proof is conditional on semantic remainders being fixed as the permitted
information. It does not stop an attacker changing them arbitrarily. The only
modeled output is one canonical residue. Timing, failures, raw states, retries,
physical resources and secret-dependent query selection are excluded. Exact task
answers are unique; correctness plus canonical release closes this tiny content
interface. That limitation must be prominent.

## Implementation and provenance

CPU only. Primitive products <=64; affine sums <=136; squares are reduced before
further use. All bounds are far below int64 capacity. Use Python integers and
torch int64 for enumeration. Log source/output hashes, configurations, learned
weights, gradient traces, coverage and costs. Record the missing Python-to-Lean/
hardware refinement separately; no generic constant-time claim is allowed.

ModuloNET (2021), finite-ring polynomial networks and p-adic neural methods are
close prior art; modular arithmetic itself is not new. The deliverable is this
concrete candidate, restricted proof and a clear learning/scalability result.
Any originality claim requires a named distinction beyond those predecessors.
