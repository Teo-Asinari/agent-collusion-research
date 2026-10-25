# Targeted prior-art assessment

Accessed 2026-10-25; compared against our implementation at `0bba861`.
This is a targeted review, not exhaustive novelty clearance. No new inference,
training, upstream execution or code reuse. Paper claims, inspected code and our
interpretation are distinguished below.

## Finding

No new neural primitive or security theorem has been established. Polynomial
neurons, modular neural arithmetic, congruence preservation and canonical task
interfaces have direct precedents. Our concrete implementation, checked proof,
finite tests and failure analysis remain useful artifacts; their independent
research novelty is unestablished.

Our own Lean `Residue.project` theorem gives:

    project(network_mod_9(weights, inputs))
      = network_mod_3(project(weights), project(inputs))

where project(z) = z mod 3. Thus the extra parts add no expressive power for the
released answer: computing directly modulo 3 produces exactly the same output.
This is our deduction from the checked theorem, not an additional experiment.

## Primary-source comparisons

| Source/version | Inspected scope | Prior-art implication and difference |
| --- | --- | --- |
| Livni, Shalev-Shwartz & Shamir, [An Algorithm for Training Polynomial Networks, arXiv:1304.7045v2](https://arxiv.org/html/1304.7045v2), revised 2014-02-20 | Introduction, §2, §3.1, §6 code passage | Linear operations and weighted products construct polynomial neural networks; finite-sample fitting is established. Their real-valued basis learner differs from our square network and finite search. |
| Dubey et al., [ModuloNET, author abstract](https://research.ece.ncsu.edu/aaysu/publication/modulonet-neural-networks-meet-modular-arithmetic-for-efficient-hardware-masking/), November 2021, TCHES 2022(1) | Abstract only | Explicitly proposes modular neural arithmetic and modified BNN training/inference for hardware masking. Modular arithmetic for neural security is already established. Protecting model internals against physical probing differs from restricting malicious extra-part influence on released content. |
| Mihara, [p-adic Character Neural Network, arXiv:2603.29905v1](https://arxiv.org/html/2603.29905v1), 2026-03-31 | Introduction, §4, §3 theorem statement | Character activation; finite-precision fitting reduces to polynomial equations modulo prime powers, with Gröbner-basis feasibility discussed. Our square activation and enumeration differ; ring-based neural fitting is not new. Full approximation proof and solver code not audited. |
| [mathlib ZMod/Basic.lean](https://raw.githubusercontent.com/leanprover-community/mathlib4/master/Mathlib/Data/ZMod/Basic.lean), unpinned master accessed on review date | `castHom`, `cast_add`, `cast_mul`, `cast_pow` declarations and proof bodies | Source defines projection to a ring whose characteristic divides the source modulus and preservation of arithmetic. This directly covers modulo 9 to modulo 3. Read, not compiled here; no SHA recovered, so upstream reproducibility audit remains incomplete. Our independent core-only Lean proof does not import this library. |
| Cégielski, Grigorieff & Guessarian, [Characterizing congruence preserving functions, arXiv:1506.00133v1](https://arxiv.org/html/1506.00133v1), 2015-05-30 | Introduction, definition/theorem statements, conclusion | Broader classification of congruence-preserving maps using rational polynomial-like functions. Our integer polynomial composition is simpler. Their rational evaluation conventions do not authorize arbitrary division in our safe operations. Full proofs not audited. |
| Pandey et al., [Don't Judge an Agent by Its Messages, arXiv:2610.25032v1](https://arxiv.org/html/2610.25032v1), 2026-10-18 | §V-C, Proposition V.3 and balanced-attribute/key assumptions | Explicit K-output/log2(K) capacity bound and canonical task-interface/error-leakage bounds. Finite choice and canonicalization are established. Our arithmetic propagation contract does not protect arbitrary semantic choices. Code and appendix proofs not audited. |
| Tiwari et al., [Information Flow Control in Machine Learning through Modular Model Architecture, USENIX Security 2024](https://www.usenix.org/system/files/usenixsecurity24-tiwari.pdf) | Abstract, §3.4–3.5; earlier repo notes cover §2.3 and §3 | Independently trained domain experts and access-policy gating establish architectural ML information-flow precedent. Domain separation differs from our same-remainder relation within words/weights. “Modular” means modules here, not integer arithmetic. Code not audited. |

## Incomplete access and implementation review

The [ModuloNET publisher page](https://tches.iacr.org/index.php/TCHES/article/view/9306)
was blocked by robots policy. No author implementation was located and inspected
in this pass; this does not establish that none exists. Exact operation/proof
comparison remains incomplete, and hardware security claims do not transfer to us.

Livni et al. link [BasisLearner.zip](https://www.wisdom.weizmann.ac.il/~shamiro/code/BasisLearner.zip).
Web access rejected ZIP content. A direct download failed with a connection reset
after retry outside the network sandbox. Contents, version/hash and license were
not inspected. No upstream implementation behavior is claimed verified.

## Claim disposition and next discriminator

- New polynomial neurons, modular neural arithmetic for security, projection
  theorem or canonical output defense: unsupported as novelty claims.
- Checked restricted information flow for our saved models: supported within
  the report's abstract-arithmetic and implementation/timing limitations.
- First exact proof/test package of this kind: unknown; this search does not
  establish absence of an existing match.
- Arbitrary malicious-model communication prevention: unsupported; semantic
  choices and other channels remain outside the contract.

An architectural contribution now needs a demonstrated capability or learning
advantage against direct modulo-3 computation, lookup tables and established
polynomial constructions. More tiny truth tables alone do not resolve this.
Alternatively, present this as a reproducible case study of a known principle,
including training failures and unsafe-operation counterexamples. Neither option
is a selected new paid experiment.
