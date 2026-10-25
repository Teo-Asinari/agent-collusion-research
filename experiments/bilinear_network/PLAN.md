# Exploratory bilinear-network feasibility check

Written before execution, 2026-10-25. Owner authorized a different local
architecture/experiment and Lean verification. CPU only; no hosted/cloud spend.

## Question and architecture

Can exact linear algebra replace exponential weight search while learning hidden
weights and predicting unseen inputs under the same restricted content contract?

    h_j = (u_j^T x)(v_j^T x) mod 9
    output = (c + l^T x + sum_j h_j) mod 9
    release = output mod 3

Both hidden maps are learned by finite-field rank factorization of a fitted
quadratic interaction matrix. This differs from the preceding square-neuron
network, but polynomial neurons, lifting and factorization are prior art.
Soltani & Hegde, AISTATS 2018, abstract and author extended-paper §I-A/B inspected
2026-10-25: https://proceedings.mlr.press/v84/soltani18a.html and
https://chinmayhegde.github.io/assets/papers/neural_TSP18.pdf . They lift real
quadratic networks to low-rank matrices and recover weights by decomposition.
We use exact ternary arithmetic and rank factorization, not their recovery
algorithms. No upstream code audited/reused. No new primitive/learning theorem
is claimed. Security still factors through direct modulo-3 computation.

## Fixed design and falsifiable outcomes

- Dimensions 4, 6, 8; teacher ranks 1, 2, d; seeds 20261025..20261028:
  36 task instances, not independent evidence about real-world tasks.
- Targets are noiseless quadratic functions over F3 with random linear/bias
  terms. Teacher rank-r maps have an identity block plus random remaining
  columns, ensuring full row rank; diagonal coefficients are nonzero.
- Training inputs are zero, e_i, 2e_i and e_i+e_j. They identify all degree<=2
  coefficients: 15, 28, 45 examples. No teacher parameters are given to fit().
  Evaluate all remaining 66, 701, 6516 inputs respectively. These are designed
  identification queries, not an iid sample or generalization to arbitrary tasks.
- Recover quadratic coefficients by finite differences, then use Gaussian
  elimination/rank factorization over F3 to learn hidden U,V. Fail if any
  held-out prediction differs or recovered matrix/rank differs from the target.
- Controls: direct fitted quadratic model; exhaustive empirical-risk-minimizing
  affine model using the SAME training data (lexicographic ties); train-table
  lookup with default 0 on unseen inputs. No neural advantage over the direct
  quadratic solver is expected or claimed. Parameter-search space is recorded
  descriptively; do not equate comparison to an optimized brute-force baseline.
- Negative target: cubic x0*x1*x2, outside the quadratic family, using the same
  training design. Retain held-out errors rather than imply universal learning.
- Attack checks: 128 seeded independent extra-part perturbations of inputs and
  all learned parameters per task; 32 training-data perturbations per task;
  require identical releases and identical fitted semantic models respectively.
  These joint checks are sampled, not exhaustive. Positive control: changing
  raw output bias by 0,3,6 carries a trit if raw output is exposed.
- Source/configuration hashes, task weights, training data, held-out metrics,
  baseline metrics, fit runtimes, environment versions and proof logs are saved.

## Lean scope

Compile generic arbitrary-depth polynomial noninterference from Residue.lean and
instantiate it for the bilinear computation with inputs AND all weights modeled
as mutable words. Produce kernel-checked certificates for each learned d=4
model on all 81 ternary inputs (including held-out points), using actual hidden
weights and independent quadratic targets. d=6/8 domain checks are Python-only.
Save all Lean logs and axiom reports; no sorry, added axioms or native_decide.
This does not prove the Python trainer, general coefficient-recovery algorithm,
hardware, timing or arbitrary private semantic changes secure/correct.

Success resolves finite-search training on this realizable structured family.
It does not establish scalable language learning or architecture novelty.
