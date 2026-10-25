# Learning a finite bilinear network without weight search

2026-10-25. Exploratory local continuation of the residue-network experiment.
No hosted-model calls or cloud jobs. [Plan written before execution](../../../../experiments/bilinear_network/PLAN.md).

## Plain-English result

The earlier network learned by trying possible weights. This version learns
which input interactions matter using exact linear algebra, then converts those
interactions into hidden-neuron weights. It correctly predicted every unseen
input in the small, deliberately structured task family. Lean checked its
restricted information-flow property and twelve concrete learned models.

This resolves brute-force fitting for this family. It does not establish a new
primitive, a general learning algorithm or an advantage over a direct quadratic
solver, which performs equally well. The same security limitation remains:
released answers depend only on the modulo-3 task information.

## Computation and learning

Each learned hidden neuron multiplies two learned linear projections:

    h_j = (u_j^T x)(v_j^T x) mod 9
    y   = (c + l^T x + sum_j h_j) mod 9
    released answer = y mod 3

Both U and V are learned, not fixed random feature maps. The learner first
identifies a quadratic function c+l^T x+x^T Qx over F3 from labeled examples.
It uses exact finite differences on zero, e_i, 2e_i and e_i+e_j queries, then
Gaussian elimination to factor Q=UV. The columns of U and rows of V supply the
hidden maps. Hidden width is the recovered matrix rank. This is algebraic
identification/decomposition training, not successful gradient descent.

Training uses 1+2d+d(d-1)/2 examples: enough to identify the complete quadratic
family. It receives no teacher parameters. Queries are deliberately selected,
not iid observations. Fitting and factorization require polynomial work in d;
there is no enumeration of possible network weights. Timings here are single
small local measurements, not a robust performance benchmark.

## Frozen task set and outcomes

For each dimension, four fixed seeds and teacher ranks 1, 2 and d yield twelve
tasks. Targets have random linear and bias terms and rank-controlled symmetric
quadratic interactions. Outputs have three possible values. All inputs outside
the training set are evaluated, rather than sampling a convenient test subset.

| Inputs | Training examples/task | Unseen inputs/task | Tasks | Bilinear unseen accuracy | Affine ERM unseen accuracy | Lookup/default-0 unseen accuracy |
| --- | --- | --- | --- | --- | --- | --- |
| 4 | 15 | 66 | 12 | 100% | 35.48% | 34.60% |
| 6 | 28 | 701 | 12 | 100% | 36.71% | 33.67% |
| 8 | 45 | 6,516 | 12 | 100% | 40.54% | 33.37% |

Total: 87,396/87,396 held-out predictions correct. These are finite-domain
correctness counts across related synthetic functions, not independent trials
or evidence of arbitrary out-of-distribution generalization. Direct fitted
quadratic evaluation also achieves 100%. The affine control uses exact empirical
risk minimization over every affine model on the same training data, with fixed
lexicographic tie breaking. Lookup stores the training table and emits zero for
unseen inputs. Both controls have weaker inductive assumptions than the target
family; beating them does not establish an advantage over known quadratic models.

Median learner fit times were approximately 0.093, 0.105 and 0.156 ms for the
three dimensions. This excludes controls, evaluation, proof generation and Lean.
Low-rank maps can reduce parameter storage: d=8, rank=1 has 25 neural parameters
versus 45 independent quadratic coefficients. Dense maps can increase storage:
d=8, rank=8 has 137 parameters. No universal compression gain is claimed.

The predeclared cubic negative target x0*x1*x2 is invisible on these identification
queries. It fails on held-out inputs: accuracy is 63.64%, 69.19% and 70.17%.
Thus the outcome depends on the quadratic-family assumption, and is not an
arbitrary-function learner. No cubic capability repair was attempted after seeing
these results.

## Lean checks and attack scope

Lean 4.35.0 accepted three commands: the existing generic polynomial semantics,
the new bilinear expression architecture and twelve learned-model certificates.

- `Bilinear.content_noninterference` applies to every input/weight environment
  with matching remainders, at any dimension and hidden width. All hidden,
  linear and bias weights are part of that relation.
- `Bilinear.direct_projection` explicitly confirms equivalence to direct
  modulo-3 computation. The extra parts do not improve released expressiveness.
- Each d=4 learned model has a kernel-checked theorem equating its actual hidden
  weights with the independent target on all 81 ternary inputs, including the
  66 held-out points. Certificates are not merely statements about training fit.
- These theorems depend on standard `propext`; no `sorry`, added axioms or
  `native_decide`. d=6/8 correctness is exhaustively tested in Python, not
  certified on every input in Lean. The general noninterference theorem still
  covers their abstract arithmetic.

All 4,608 sampled joint input/weight perturbations preserve released answers.
All 1,152 sampled training-data perturbations return identical learned models.
Neither attack family is exhaustive. Exposing raw output instead of its
remainder gives three distinct values through bias changes of 0,3,6 in every
task: a positive control demonstrating a real channel when release is weakened.

An independent standard-library scalar audit agrees on all 88,452 domain points
(training and held-out), reconstructs interaction matrices from saved hidden
weights, checks source hashes and matches the twelve certificates to those saved
models. Its audit reads recorded successful Lean logs rather than rerunning Lean.

The Python trainer and its correspondence to Lean are not generally verified.
Timing, failures, resource use, raw states and arbitrary changes to semantic
information remain outside the guarantee. Fixed finite examples do not establish
collusion prevention, independent discovery or harmful coordination.

## Prior art and interpretation

Soltani & Hegde's [AISTATS 2018 paper](https://proceedings.mlr.press/v84/soltani18a.html)
already learns quadratic neural networks through low-rank matrix estimation;
the [author's extended paper](https://chinmayhegde.github.io/assets/papers/neural_TSP18.pdf),
§I-A/B, explicitly recovers hidden weights by matrix decomposition. We inspected
those passages and the conference abstract on 2026-10-25, not the full proofs or
code. Their real-valued recovery algorithms differ from this exact finite-field
identification scheme. That difference alone does not establish novelty.
The existing [prior-art assessment](../residue-network/prior-art.md) supplies
additional polynomial, modular-arithmetic and information-flow precedents.

This is a successful learning-method feasibility change, not a security-theorem
advance. A further contribution needs practical learning beyond engineered
quadratic identification queries or a useful, differentiated computation/security
tradeoff. Neither a new paid run nor a full study is selected by this result.

## Reproduce

From the repository root, with NumPy and Lean installed:

```bash
python -m experiments.bilinear_network.run --output results/bilinear-network-repeat
python -m experiments.bilinear_network.verify \
  --results results/bilinear-network-repeat \
  --output results/bilinear-network-repeat/verification.json
```

Set `LEAN_BIN` to override `/home/tasinari/.elan/bin/lean`. Output directories
must be fresh. Results, configuration/source hashes, actual learned weights,
training observations, checked certificate and Lean version/logs are saved in
`results/bilinear-network-01/`. This is a Markdown experiment report, not yet the
official-template hackathon PDF.
