# Formal guarantees for hybrid LLM architectures

2026-10-24. Exploratory response to the owner's question about a hybrid architecture provably never using steganography or colluding. No project selected, experiment launched or verified architecture implemented.

## Claim worth investigating

A controlled system can enforce a precisely specified information-flow or joint-action property even when its LLM component is untrusted. This does not establish that the model never internally considers signaling, that arbitrary permitted task behavior cannot encode information, or that all harmful coordination is prevented.

An example target: for fixed authorized task information, varying a sender-only private payload does not change the distribution of the receiver's complete observable history. Define receiver side information, joint randomness, permitted releases, termination, deadlines, errors, retries and resource observations explicitly. A theorem restricted to one observation projection cannot be advertised as covering excluded channels. Initial shared strategies or shared training can coordinate behavior without fresh communication.

## Newly checked primary precedents

- [Garby, Gordon & Sands, LLMbda, arXiv 2602.20064v2](https://arxiv.org/html/2602.20064v2): machine-checked termination-insensitive probabilistic noninterference for a calculus/interpreter with LLM conversations and generated code. Inspected introduction, §4, and interpreter-correspondence overview; did not execute or audit Lean proofs. Termination leakage and retry composition are explicitly discussed, so these are not newly identified gaps. Always-terminating modeled programs obtain the stronger equality result (§4.2); that does not certify a real scheduler, provider or hardware.
- [Costa et al., Fides, arXiv 2505.23643v1](https://arxiv.org/html/2505.23643v1): inspected threat model and §§4.3–4.4. Explicit-secrecy guarantee omits indirect control-flow leakage; tool selection/order can leak. Timing and packet lengths are outside its model. Selective release and schema restrictions require care; deterministically checking a label is not universal anti-steganography. No reproduction or code audit.
- [Clarkson & Schneider, Hyperproperties, author manuscript dated 2009-10-16](https://www.cs.cornell.edu/fbs/publications/Hyperproperties.JCS.pdf): abstract/introduction inspected. Noninterference concerns relationships among possible executions. Individually acceptable outputs need not imply absence of signaling. Full proof not reviewed.
- [Cecchetti, Myers & Arden, Nonmalleable Information Flow Control, CCS 2017](https://www.cs.cornell.edu/andru/papers/nmifc/): author abstract only. Controlled release/downgrading requires stronger conditions than unrestricted declassification; no claim this language proves arbitrary LLM-agent collusion prevention.
- [Dalrymple et al., Towards Guaranteed Safe AI, arXiv 2405.06624v3](https://arxiv.org/abs/2405.06624v3): abstract only. World model, specification and verifier framework; agenda-level precedent, not a completed general anti-collusion system.
- [Alwen et al., Collusion-Preserving Computation, CRYPTO 2012](https://crypto.ethz.ch/publications/AKMZ12.html): author abstract only. Extends communication-resource and composition framing, including bounded outside communication. Important next reading before proposing a compositional novelty claim.

Access date for all six: 2026-10-24. LLMbda v1 HTML returned 404; v2 HTML was accessible and is the version reviewed. Sources remain external.

## Possible architecture, not an implemented guarantee

1. Treat LLM suggestions and generated programs as untrusted. Restrict their access and effects through an enforced interface.
2. State the authorized computation and forbidden flow, with separate constraints on prohibited joint outcomes.
3. Use a small trusted runtime, information-flow discipline and/or proof checker to admit only computations satisfying those specifications. Protect scheduling, failure behavior and output release as well as message bytes.
4. Prove the property for the composed system, then identify assumptions needed to connect the model to its actual deployment.

Proofs of ordinary task correctness alone are insufficient. If two distinct accepted answers are interchangeable for the task and visible to a receiver, choosing between them may encode a bit. A valid certificate can itself offer signaling choices if exposed. Stronger enforcement could require an independently chosen canonical release or a relational proof that private payloads cannot influence release. Rejecting invalid proposals also needs modeled failure behavior; secret-dependent success/fallback can signal.

## Research assessment

Generic verified wrappers, dual-model isolation, information-flow tracking and machine-checked LLM harnesses already have precedents. A meaningful investigation needs a specific missing guarantee and useful task, compared directly with these systems. No gap has yet been established. Proving lack of extra communication and ruling out harmful joint outcomes are different objectives; neither should silently substitute for the other.

See also [physical isolation and mediation](isolation-and-mediation.md) and [the novelty audit](novelty-audit.md).

## Owner clarification: redesign the learned architecture itself

The owner explicitly means a ground-up combination of transformer computation and formally verified code, with anti-steganography invariants built into the computational architecture. A conventional LLM monitored by a wrapper does not satisfy the intended scope. Focus is steganography, not general harmful coordination. The earlier runtime-oriented sketch is a comparison point, not the requested architecture.

**A stronger possible target:** prove an information-flow property for every allowed choice of neural weights, by construction of the permitted computation graph and state transitions. Training would improve task performance within that class. This is a proposed proof strategy, not an established theorem for a new design. If useful neural operations require semantic contracts beyond structural separation, those contracts need independent proofs or a narrower learned-module class.

Candidate proof obligations, to be refined before implementation:

| Obligation | Architectural consequences to investigate |
| --- | --- |
| Protected information has no unauthorized causal path | Partition neural state and attention; inspect residual paths, normalization, caches, routing and recurrence as well as attention masks |
| Only a specified task function may release protected information | Formally define that function; an unconstrained learned summarizer is not automatically a trusted semantic boundary |
| Learning preserves separation | Constrain parameter sharing, gradients, optimizer state and permitted online updates |
| Randomness cannot carry a sender-controlled choice | Specify joint randomness, receiver side information and how all random choices are generated and used |
| Repeated operation preserves the property | Prove composition over memory, steps and interactions; a one-step or marginal result is insufficient |
| Implementation matches abstract observations | Specify numerical semantics, scheduling, errors and hardware assumptions; code-level flow separation alone does not certify physical noninterference |

These obligations should imply a relational property over complete receiver views, rather than merely certify every individual output as task-valid. Preventing operational transfer does not require banning arbitrary internal encodings, which may be ordinary learned representations and require a separate definition.

### Additional architectural primary sources

- [Tiwari et al., Information Flow Control in Machine Learning through Modular Model Architecture, USENIX Security 2024](https://www.usenix.org/system/files/usenixsecurity24-tiwari.pdf): inspected introduction, §2 definitions, architecture overview and limitations. Separates training-domain influence into experts; restricts gating and aggregation to accessible domains. Direct transformer/training architectural precedent, not general malicious-agent steganography prevention. No mechanized-proof or implementation audit performed.
- [Chong & van der Meyden, Using Architecture to Reason about Information Security, 2015](https://people.seas.harvard.edu/~chong/abstracts/ChongM2015.html): author abstract only. Architectural causal constraints plus local trusted-component properties support information-flow proofs and refinement. Adjacent compositional methodology; not a neural architecture.
- [Daggitt et al., Vehicle, FSCD 2025](https://drops.dagstuhl.de/storage/00lipics/lipics-vol337-fscd2025/html/LIPIcs.FSCD.2025.2/LIPIcs.FSCD.2025.2.html): abstract/introduction inspected. Integrates neural specifications and symbolic proofs, addressing their embedding gap. Adjacent verification infrastructure; demonstrated controller safety is not anti-steganography.

All three accessed 2026-10-24. No new architecture implemented, experiment selected, budget spent or novelty established. Next useful theoretical artifact would be a small explicit architecture, an operational definition and a compositional theorem or counterexample—not a generic proof-of-correctness output filter.
