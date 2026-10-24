# Final response after adversarial review round 2

2026-10-24. Read [round-two report](../../reviews/round-2.md). Accepted its finite-only verdict. No material kernel correction was requested or made. No exhaustive run was repeated, and no additional experiment, paid inference, training, dependency or literature expansion occurred.

| Gate | Final outcome | Exact remaining boundary |
| --- | --- | --- |
| R1: specify actual reuse kernel | Met for classical certificate reuse and canonical witness reconstruction | This is not arbitrary source-code rewriting; useful compact-code reconstruction remains unresolved. |
| R2: include failures and validation | Met for every bounded record in the finite universe, including invalid certificates | Arbitrary transport errors, nonarrival, physical timing/resources and an implemented fixed-slot service are outside the result. |
| R3: show useful computation advantage and strong baseline | Not achieved; correctly deferred | Task-only hardcoding solves the single fixed graph. No net gain over strong symbolic solving, even though the valid branch reuses verified labels, is established. |
| R4: add iO comparison | Met as a theoretical comparator with scope limits | Conditional computational indistinguishability for same-size equivalent circuits is different from statistical zero. Practical performance and general auxiliary-key/interactive security were not established. |
| R5: bound all declared sender choices | Met for the complete finite content kernel | All 280,000 rows are point masses at the same bytes. No inference about arbitrary artifacts, larger task families or unbounded code. |
| Keys and repeated use | Met for the specified stateless constant-content release | A richer or stateful interface requires a conditional-history proof; single-output marginal equality is insufficient. |
| Positive weights and traversal | Retained as an essential restriction | Strict decrease along tight predecessors excludes cycles. Zero-weight or disconnected extensions need new rules and analysis. |

## Exact surviving claim

For the fixed trusted four-vertex graph and the complete declared universe of 280,000 well-formed bounded submissions, the specified deterministic reconstruction kernel returns exactly the bytes `[0,1,3]` for every submission. Fourteen inputs contain valid distance certificates; all 279,986 others invoke task-only solving. The maximum pairwise total variation between receiver-visible **content** rows is therefore zero. This holds for any choice of encoder/decoder within that universe and adds no payload information to any receiver side information, because the output is constant conditional on the trusted task.

Repeated calls to this stateless content kernel yield the same constant transcript. This is not a guarantee for unspecified interactive state, secret-dependent task/query selection or physical execution. When the deliberately expanded view exposes comment length and fallback status, maximum pairwise TV is one; the content theorem does not cover that diagnostic channel.

The finite analysis supports a restricted mechanism: unique verified intermediate information can be reused while a nonunique sender-selected witness is replaced. It does not establish a new removal algorithm, useful performance savings, a reusable compact-program sanitizer, general steganography prevention or physical noninterference. Exact finite enumeration is evidence about this model, not a mechanical proof of the deployment stack.

## Artifacts and closure

- [Final proposal](proposal.md): bounded construction, matrix, strong baseline, cost caveats, keys/history and iO comparator.
- [Kernel](kernel_analysis.py) and [existing finite-analysis output](kernel-analysis.json): unchanged after round two.
- [Source/read-depth ledger](sources.md) and [first-round response](revision-1.md).

The original rich-artifact objective, net efficiency and novelty remain open gates. Further work should start with a specific useful capability or consequential counterexample and its contribution claim, rather than scaling this control example into a stronger headline.
