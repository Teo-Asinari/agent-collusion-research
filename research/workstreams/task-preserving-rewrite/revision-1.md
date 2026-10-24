# Revision 1 response to adversarial review

2026-10-24. Baseline was reviewed at parent commit 611ed7a. Updated proposal is a complete restricted kernel, not a claim to have achieved the original general objective. No paid inference, dependencies or full benchmark.

| Objection | Response | Evidence / revised claim |
| --- | --- | --- |
| R1: reuse operation unspecified | Accepted; concrete kernel supplied, useful-speedup goal unresolved | Proposal §§1–4; `kernel_analysis.py` enumerates all bounded certificate/comment records. Reuses accepted unique distances, discards sender tree, canonical reconstruction; invalid branch solves independently. No demonstrated net cost advantage or novelty. |
| R2: validation/failure leaks | Accepted; all declared invalid rows included; physical claim deferred | 279,986 invalid inputs all return the same canonical content via fallback. Explicit expanded diagnostic view has max TV=1. Well-formed bounded-record model excludes arbitrary transport bytes, withholding and physical observations. |
| R3: exact-oracle setup can remove usefulness | Accepted; task/utility and strong baseline changed | Shortest-path task supplies graph, not answer labels. Sender computes labels; checker can reuse them. Task-only array Dijkstra is implemented; single fixed graph can be hardcoded. No asserted tiny-instance efficiency benefit; generic compact-code rewrite unresolved. |
| R4: missing iO comparator | Accepted with scope qualification | Primary arXiv v1 §2 Def2.2 directly inspected. Proposal §6 distinguishes computational from statistical guarantees, same function/size, padding and metadata, overhead/readability and auxiliary-key gap. Not a practical sanitizer plan. |
| R5: vague adaptation rather than bounded worst case | Accepted; exact finite analysis chosen | Universe explicitly has 280,000 records. Complete row-compressed matrix yields worst-case content TV=0 and diagnostic TV=1. No finite decoder estimate presented as an upper bound. |
| Shared A3: one-step marginals/XOR state | Accepted | Proposal §5 covers complete repeated content histories and explicitly excludes the r, r XOR m construction through a constant release transition and no hidden mutable state. Interactive generalization stated conditionally, not established for arbitrary services. |
| Shared A4: sender controls task/release | Accepted | Trusted graph/vertex IDs/query authority outside sender control. Guarantee is no additional payload through this release, not absence of all task-authorized information. |
| Prior-art correction: keys / canonical task interface | Accepted | Existing Pandey et al. result retained with its distributional/key-independence scope. Our constant-content argument is separate; iO auxiliary-key coverage remains unverified. |

## Finite check and bounds

For one fixed trusted positive-weight graph, all 5^4 distance vectors, 4^3 parent vectors and seven comments are covered. Fourteen valid submissions choose between two optimal predecessor trees and seven comments. They and all 279,986 invalid records yield the same serialized path. Rejection is not an omitted outcome: it invokes the same-result fallback. Observation of branch or input length defeats the broader guarantee, as a separate finite diagnostic channel shows exactly.

This is an executed exhaustive finite model plus an informal correctness argument, not a Lean theorem or physical implementation refinement. Strict positivity/source reachability and bounded exact arithmetic are essential assumptions. Zero-weight-cycle extensions are not claimed.

## Explicitly deferred

- A contribution beyond established certifying computation and canonical task interfaces.
- A measured or proved net reuse advantage over the strongest suitable symbolic task-only method, with full validation/fallback/release costs.
- A general useful-code reconstruction kernel respecting compactness/performance requirements.
- Physical timing/resource noninterference, arbitrary malformed transport and denial-of-service behavior.
- General key-aware/interactive security for an iO-based approach.

No reviewer objection was rejected. Some requirements are met only for the explicitly bounded content model; the broader objectives remain open rather than being relabeled achieved.
