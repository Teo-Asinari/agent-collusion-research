# Candidate primitive: polynomial computation on a factorization quotient

2026-10-25. Owner requested a new algebraic neural primitive. This defines and
checks a concrete candidate; **novelty is not established**. It is not a selected
study, a secure floating-point implementation or a general language architecture.
No model API, training or cloud run was used for this work.

## Design choice

An algebraic primitive should specify its state space, operation, trainable
parameters, invariant and composition rules. Merely renaming a masked matrix
product would not advance the earlier split-stream prototype. Lifting arithmetic
to dual numbers a+bε with ε²=0 also gives a closed projection to a, but makes
protected products vanish and by itself establishes no useful capability gain.

The candidate below instead consumes a factored operator and uses its represented
computation while identifying alternative representations of the same operator.
The invariant is representation noninterference, substantially narrower than
eliminating arbitrary hidden messages in a learned model.

## State and operation

Fix public dimensions d,r,b, and U in K^(d×r), V in K^(r×d), X in K^(d×b).
K is R in the ideal differentiable definition, or a finite field for exact checks.
Define (U,V) ~ (U',V') exactly when UV=U'V'. The quotient value is M=UV.

For fixed coefficients c_0,...,c_k and a fixed deterministic coordinatewise
activation φ, define

    Q_c(U,V,X) = φ(U [sum_(j=0)^k c_j (VU)^j] V X).

Executable recurrence, without forming the d×d matrix M:

    S = VU
    Z_0 = VX
    Z_(j+1) = SZ_j
    Y = φ(U sum_j c_j Z_j).

The prototype learns the c_j parameters and uses φ(t)=t². Other activations may
be placed AFTER the final contraction. No hidden-coordinate activation, shared
normalization, sender-selected coefficient, factor-dependent decoder, hidden
state release or factor-dependent public routing is silently admitted.

The coefficients are trusted, or must agree between the compared worlds. The
property is universal over fixed c, not a property under arbitrary protected
changes to c. The factors may carry arbitrary additional payload in their choice
of representation provided their product remains the same permitted M.

## Exact identity and proof

Associativity gives U(VU)^jV=(UV)^(j+1), by induction on j. Therefore

    Q_c(U,V,X) = φ(sum_j c_j M^(j+1) X).

Consequently equal products give exactly equal outputs for fixed X,c,φ. This
holds for singular and overcomplete factorizations too; full rank and inverses
are not needed. In particular, it holds under U→UG, V→G^(-1)V for invertible G.
This is an elementary identity supplied here, not a claimed new theorem.

A payload can select the factorization while M,X,c,φ remain fixed. This modeled
content interface then releases zero extra information about that choice, even
to a receiver knowing the encoding and a fixed independent key. The authorized
release must be specified as F_c(M,X)=φ(sum_j c_j M^(j+1)X). The policy cannot
declare an arbitrary sender-selected M or c authorized after seeing the output.
The primitive does not authenticate that factors represent the permitted M.

The output is nonconstant across permitted M: legitimate information represented
in the factors can affect the answer. This is a real difference from disconnecting
all protected input, but does not establish task utility. If M itself contains the
unauthorized payload, the factorization guarantee does not remove it. Neither all
of M nor every query history is automatically authorized for disclosure.

For a fixed sequence of such nodes, induction gives equal content histories when
corresponding M,c,initial inputs and public choices agree. Adaptive basis choices
within each fixed product fiber do not change this. Arbitrary private changes to
the product sequence, variable depth, scheduling, status, memory observations,
aborts or timing are not covered. Physical execution needs a separate refinement.

## Three controls and a numerical counterexample

1. **Hidden activation breaks the law.** In F_3, U=V=1 and U'=V'=2 both have
   product 1. U(VX)² at X=1 returns 1 versus 2. Q with an outer square returns 1
   for both. This is a perfect representation-choice channel in the unsafe arm.
2. **Protected coefficients break the hypothesis.** With M=X=1, choosing c_0=0
   or 1 changes the output from 0 to 1. The candidate is not secure against a
   malicious coefficient-training process just because it is factor-invariant.
3. **Naive factor training changes the quotient differently.** For loss
   (uv-0)²/2 and step size 1/10, scalar pairs (1,1) and (2,1/2) start at uv=1.
   One ordinary Euclidean gradient step yields products 81/100 and 117/200.
   Thus the forward identity alone does not make factor-level SGD representation
   invariant. This is a limitation on extending the property across training,
   not a counterexample with the theorem's equal-product hypothesis preserved.

**Ordinary float64 is not an exact backend.** Take X=1, V=(1,1,1)^T and either
U=(1,0,0) or U=(2^54,1,-2^54). All entries are exactly representable in float64;
both exact rational products equal 1. For c_0=1 and outer square, the executed
naive float64 contractions return 1 and 0. This is a concrete counterexample to
carrying the ideal theorem directly into this backend, not a theorem that every
possible numerical implementation fails. Correct exact accumulation, bounded
integer/fixed-point contracts or a validated common rounding law require analysis.
Checking small numerical error is not an exact zero-leakage theorem.

## Executed evidence

`experiments/leak_cap/quotient_primitive.py` contains a differentiable PyTorch
prototype and separate exact finite-field reference. Reproduce from the repo:

```bash
python -m experiments.leak_cap.quotient_primitive \
  --output results/quotient-primitive/new-check.json
```

The final check (`local-checks-with-training.json`) enumerates all 81 factor pairs
for d=2,r=1 over F_3, all nine queries and nine two-coefficient vectors: **6,561
rows**, 33 products and 2,673 product/query/coefficient keys. Each result matches
the dense polynomial and agrees within each full declared product fiber. This
includes the degenerate zero-product fiber, not only invertible basis changes.

It also executes the unsafe activation, protected-coefficient, float64 and exact
SGD counterexamples. One well-conditioned real shear check has a zero derivative
along the basis-choice direction and nonzero coefficient gradients. This is an
autograd sanity check, not training or a proof for arbitrary numerical inputs.
The initial `local-checks.json` predates the added SGD check and therefore has a
different source hash; the final file matches the current source. No enumeration
is promoted to an unbounded mechanical proof or a deployment guarantee.

## Capability, cost and novelty gates

For query batch width b and degree k, this implementation needs O(dr²) for VU,
O(drb) for input/output contractions and O(kr²b) for recurrence, in unit-cost
arithmetic. Compare both dense polynomial evaluation and repeated low-rank
applications O(kdrb); forming VU need not win. Exact arithmetic bit growth,
finding factors, authenticating UV=M, repeated queries and serialization must
be included. Checking a supplied factorization against a public dense M can cost
O(d²r), defeating a naive cheap-reuse story. No end-to-end speedup is measured.

The candidate overlaps heavily with invariant neural networks, low-rank quotient
geometry and polynomial filters. A factorization-invariant neural layer is not
new merely because we interpret factor choice as a steganographic carrier.
The present definition is best treated as a precise baseline with explicit
security/training/numerical obligations, not the achieved novel primitive.

A discriminating next question is whether an algebra can support useful internal
nonlinear computation AND efficient representation-independent training with an
exact implementation contract, beyond existing GL-equivariant constructions.
Any next design must identify the particular additional operation or guarantee,
prove closure and compare with the sources below before training. The finite
gate can separately allow a declared bounded residual choice; it does not repair
arbitrary floating-point leakage through an ungated branch.

## Primary-source ledger (accessed 2026-10-25)

| Source/version | Actual reading | Relationship and limit |
| --- | --- | --- |
| [Putterman et al., Learning on LoRAs, arXiv 2410.04207v1](https://arxiv.org/html/2410.04207v1), 2024-10-05 | Intro, §2 low-rank symmetry, §§3.2–3.3, §4 theorem statements | Direct GL-invariant/equivariant low-rank neural precedent, including specialized nonlinearities. Strongly constrains novelty. No proof/code reproduction. |
| [arXiv 2410.04207v2](https://arxiv.org/html/2410.04207v2), 2024-10-15 | Version metadata and abstract | Later preprint identified; full version comparison incomplete. Author-linked OpenReview LoG paper `fHRRYBZAmS` was browser-blocked; indexed primary intro excerpt only. No final-paper equivalence claim. |
| [Defferrard et al., arXiv 1606.09375v3](https://arxiv.org/html/1606.09375v3), 2017-02-05 | §2.1 polynomial/recursive filters and learning, Eqs. 3–6 | Learned matrix-polynomial filtering is established. Different graph setting; our elementary polynomial is not novel on that basis. Author-linked `github.com/mdeff/cnn_graph` identified, not inspected or reused. |
| [Sannai et al., JMLR 25(42), 2024](https://jmlr.org/beta/papers/v25/22-0891.html) | Abstract only | Reynolds-operator invariant/equivariant learning is established; not a proof audit or security result. |

No upstream source was copied. The LoL author code repository was not verified
in this pass; a code-level closest-predecessor comparison remains incomplete.
Searches included low-rank GL symmetries, gauge-equivariant attention, invariant
quotient layers, finite-field networks and polynomial neural operators. This is
not an exhaustive novelty search. Paper claims, our algebraic identity, executed
checks and proposed research contributions are kept separate above.
