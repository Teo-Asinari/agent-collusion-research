# Architecture response to adversarial review round 2

2026-10-24. Final bounded revision responding to the architecture section of [round-2 review](../../reviews/round-2.md). No new training, inference, dependencies or experiment. No new source search was needed: these changes tighten the reviewed operational model and its claim boundaries.

| Request | Disposition | Concrete revision/evidence |
| --- | --- | --- |
| A5: predictor reads and descriptor cost | Accepted; specification tightened | Proposal §9 now fixes the predictor read signature to (q,c,m,H,theta), excluding direct current-record and predicate-register reads. §10 says how descriptor/H construction, full scans, refresh and amortization enter C_N and the end-to-end ledger. Record frames are immutable during an invocation; stale descriptors affect accuracy, not checked-witness correctness. No cheap informative descriptor or useful amortization has been demonstrated. |
| A6: extensions need contracts | Accepted | New §13 requires total finite primitive semantics, admitted inputs, budgets, all effects/observations, learning-state behavior, semantic release contract, confinement and conditional-history composition before any extension enters the guaranteed language. Arbitrary learned semantic extraction, generated code, private free-form release and mutable task data are not covered. |
| A1: useful radical architecture | Remains deferred/unresolved | Witness prediction has an explicit correctness-preserving role and conditional cost expression, but no actual learned speedup against strong symbolic retrieval/index baselines, measured end-to-end cost or general language capability exists. Full-sweep graph scheduling remains a proof vehicle. |
| A2/A3/A4: proof and deployment limits | Preserved | Restricted abstract specification and informal history induction remain the claims. No mechanized proof, executable refinement or physical side-channel guarantee; trusted facts/query authority and secrets in fixed public parameters are excluded rather than solved. |

**Changed claim:** the predictor can avoid exact predicate work only through a bounded, checked witness, using explicitly enumerated private context. Any descriptor acquisition is charged. This is a conditional guided-search mechanism inside a restricted abstract neural/verified machine—not an achieved novel anti-steganographic language model.

Remaining blockers are useful learned performance after preprocessing/checking/isolation, precise capability/novelty delta beyond the recorded precedents, mechanical verification and implementation refinement. The reviewer found the restricted argument defensible but did not certify it. No objection is converted into a success claim by labeling an unproved extension as future work.
