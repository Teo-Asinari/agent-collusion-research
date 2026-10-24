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
