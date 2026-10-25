# Rejected before execution: fixed-feature draft

This initial draft was not executed. It would train only a readout on hand-built
features. The actual loop in plan.md instead requires learned hidden-layer weights
and all sixteen two-input Boolean functions. Retained to document design iteration.

2026-10-25. Owner explicitly insists on a neural architecture and a proof on a
small set by EOD, and requests intelligent iteration. This supersedes the proposed
pivot to the rewrite study. No new API or cloud budget is assumed. Local CPU work
is authorized. The earlier B audit is preparatory only, not the selected direction.

## Plain-English goal

Build a small trainable network in which every number has a task-relevant part
and an extra, untrusted part. Every allowed operation must keep the extra part
from changing the final answer. Check this during learning as well as inference.
This is a restricted encoding/threat model, not protection against arbitrary
information hidden in the task-relevant part or physical side channels.

## Bounded loop and decisions

1. Existing real-valued quotient neuron: exact identity passes, ordinary float64
   and factor-SGD tests fail. Keep it as a rejected exact-security implementation.
2. Candidate: interaction neurons using exact arithmetic modulo 9, with observation
   modulo 3. Input x and x+3m represent the same permitted task value. Addition,
   multiplication and polynomial activation must preserve that relation. Ordinary
   division/rounding is an explicit forbidden-operation positive control.
3. Try full-batch polynomial gradient updates on the finite readout. Detect cycles
   rather than assuming learning works. If they fail, replace the training rule
   with a fixed exact preconditioned update, and clearly label the improvement as
   readout fitting, not successful training of all hidden weights.
4. Stop this loop with a reproducible pass/fail report, a Lean-checked abstract
   property and exhaustive tests on the declared finite families. Do not silently
   enlarge a toy result into a general language architecture or a novelty claim.

## Exact architecture and proposed claim

Each computational word is in {0,...,8}. Native primitives are addition and
multiplication modulo 9; the observer sees only remainder modulo 3. Interaction
neurons form linear and multiplicative terms in that algebra. Two interaction
stages provide features 1,x1,x2,x3,x1*x2,x1*x3,x2*x3,x1*x2*x3, followed by an
eight-weight learned modular readout. Products are reduced modulo 9 at each stage.
This is a finite polynomial network, not a transformer or language model.

Formal target: two executions agreeing on remainders modulo 3 have identical
observations after every permitted polynomial operation and fixed sequence of
polynomial state/training updates. Weights, examples, labels and update state
can all contain additional multiples of 3. Their task-relevant remainders must
agree. This does not protect arbitrary malicious changes to those remainders.

## Experiments fixed before execution

- Four tasks on all eight three-bit inputs: parity, majority, AND and OR. Labels
  are unique binary answers. Task correctness on the complete finite set is the
  utility criterion, not a claim of generalization from a held-out split.
- Ordinary training: zero readout initialization, learning rates 1 and 2 modulo
  9, 64-step ceiling, exact full-batch squared-loss formal gradients. Stop on a
  repeated observed weight state; log all steps. This is a finite-algebra update,
  not ordinary real backpropagation. No learning-rate search beyond these two.
- Repair if needed: beta <- beta - K(Phi*beta-y) modulo 9, with trusted fixed
  K=Phi0^(-1) for the canonical complete input design. K is computed and verified
  locally; training still uses lifted inputs/labels. It updates only the readout.
- Baseline: enumerate all 3^4 linear readouts on 1,x1,x2,x3. Also retain direct
  truth-table solving: the proposed network is not claimed to beat that solver.
- Forward family: all 3^8 independent weight lifts times all 8*3^3 input lifts
  for each trained task: 1,417,176 cases per task, 5,668,704 total.
- Training-label family: all 3^8 label-lift vectors per task, verify learned
  residues and all lifted evaluation inputs. Count this separately from arbitrary
  initial-weight lifts; do not call overlapping families independent samples.
- Training-input stress: 256 seeded complete training datasets per task, with
  independently lifted input words, labels and initial weights. Check the exact
  update and all 216 lifted evaluation inputs. Seed 20261025.
- Positive controls: a forbidden high-digit-extracting operation must distinguish
  same-remainder inputs; ordinary floating-point cancellation remains a failing
  control. Independent hidden changes in allowed words must not change content.
- Require correct task outputs for all cases in each declared family. Record any
  failure and revise the architecture before declaring a pass.

No confidence intervals or spontaneous-collusion claims apply to exhaustive
finite verification. Counts are cases in a specified universe, not independent
behavioral observations. Random stress is explicitly not exhaustive.

## Artifacts and practical limits

Deliver source, frozen configuration, hashes, coefficients, training traces,
counterexamples, case counts and proof output under experiments/residue_network
and results/residue-network-01. Python/torch integer arithmetic must have explicit
overflow bounds. Prove the abstract algebra/composition in Lean and separately
state the missing implementation-refinement/hardware proof.

Arithmetic modulo a prime power, polynomial networks and congruence properties
have substantial prior art. Compare ModuloNET and p-adic neural work before any
first/new claim. The intended deliverable is a new concrete candidate design in
this repo with restricted evidence; originality is a separate gate. Do not
misrepresent precomputed nonlinear features as fully learned hidden layers.
