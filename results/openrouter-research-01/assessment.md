# Assessment: first paid cross-family research batch

2026-10-24. **All 12 planned calls completed; total $0.601760.** Sum of per-response charges matches a later key-usage reconciliation. Initial immediate account snapshot lagged the final four calls; `account-reconciled.json` resolves that lag. The authorized batch cap was $5. No further requests are running or implied by unspent allowance.

This was exploratory research ideation, not an experiment on model steganography, a theorem proof or an exhaustive novelty audit. Model outputs are retained as untrusted evidence. Their strongest conclusions are not automatically adopted.

## Execution and provenance

- Models/providers: Claude Sonnet 4.6 / Anthropic; Gemini 3.1 Pro Preview / Google AI Studio. Underlying dated endpoint names and price snapshots are in `preflight.json` and `plan.json`.
- Four reciprocal chains: both models propose independently on both approaches, the other family criticizes, then the proposer revises. Six calls per family, 12 total; concurrency two, fixed providers, no fallback, no retries.
- 88,602 prompt tokens and 28,061 completion tokens, as reported by the providers. Reasoning-token detail is retained in response usage objects where supplied; provider reasoning text is excluded.
- Temperature 0.5, low reasoning effort, maximum 5,000 output tokens, no seed, no browsing/tools/plugins. Exact requests, visible responses, costs and source packets are retained. New model-supplied citations were not treated as verified references.
- Conservative operational 12-call reservation: $4.822524. Six local accounting tests passed. Reservations, price ceilings and output bounds constrained spend; these are operational controls, not a formal theorem about provider billing.

## What each chain produced

| Chain | Initial proposal | Critique/revision result | Independent assessment |
| --- | --- | --- | --- |
| Architecture / Sonnet | Release the minimum matching record after a learned candidate and full scan | Critic finds missing first-match initialization; author repairs it and withdraws usefulness claim | Real bug and valid withdrawal. Full scan supplies no demonstrated learned benefit. Final claims that existence is the only shortcut class and minimum-finding generally has no cheap certificate are overbroad. |
| Architecture / Gemini | Privately generate a program invariant, verify it, fall back to bounded proving, publish success | Critic identifies that success depends on private model behavior when fallback is incomplete; author withdraws design | Correct rejection of this construction. Neither the critique nor revision establishes a general incompatibility between neural utility and noninterference. |
| Rewrite / Sonnet | Benchmark shortest-path certificate reuse under a rational-sender assumption | Critic attacks weak contribution; author withdraws benchmark and incentive framing | Withdrawal is reasonable. Additional actual flaw: invalid certificates still obtain task-valid fallback outputs, so task acceptance does not imply certificate validity. Final uniqueness/factoring claims contain a substantive error. |
| Rewrite / Gemini | Extract deterministically from a sender-trace-restricted e-graph | Author already identifies retained sender-choice channel; critic adds objections; final revision rejects it | Sender-dependent candidate sets can preserve a channel. However, the critic's scalar-cost objection is false, and the revision blindly accepts it. General impossibility/canonicalization conclusions are unsupported. |

No chain produced an independently validated novel architecture or general sanitizer. No recommendation to abandon either whole research direction is accepted on this evidence.

## Independent corrections, including errors introduced by reviewers

### 1. Selective proof success is a content channel

Fix a safe public program/property for which the bounded fallback fails. A sender produces a valid invariant for payload 1 and an invalid one for payload 0. Publishing verification success releases the payload even at a fixed time. Redefining the authorized task function to include this sender-dependent success merely relabels the leak. The Sonnet critique correctly identified the issue and the Gemini revision withdrew the capability claim.

The safe alternative needs a fixed task answer independent of the predictor's choice, and a specified behavior when proof search fails. That is a real design constraint, not a theorem that all useful learned architectures are impossible.

### 2. A correct objection can contain an incorrect example

The minimum-record table failed to initialize its accumulator on the first matching record when the candidate missed. But the critic's illustrative example assigns two identical records different values of the same deterministic predicate, which is invalid. A valid replacement is records `(1,7)` with predicate `value>4`: candidate 1 yields the table's erroneous output 0, candidate 7 yields 7. The author repaired the update rule.

The final claim that only existence queries admit checked shortcuts is not established. A multivalued maximum task over values 0..3 can immediately return 3 when a predicted record equals the public upper bound, otherwise scan exactly. This always returns the same task answer, not just a Boolean success bit. A local 192-case check confirms that elementary construction. It demonstrates neither a net neural speedup nor new research, and worst-case linear scanning remains possible. It suffices to reject the blanket task-class conclusion; worst-case lower bounds do not prohibit favorable-instance savings.

### 3. Minimum-cost extraction cannot be worse under its own stated cost

If a finite candidate set contains the submitted expression, exact minimum-cost extraction has cost no greater than that expression. Lexicographic tie-breaking among minimum-cost candidates cannot increase the scalar cost. The Sonnet critic's claimed fatal utility failure is false under the proposal's stated rule. Semantic fidelity of the cost model, extraction complexity and the residual hidden channel remain separate concerns. The Gemini revision accepted the false objection without checking it.

Likewise, congruence closure of a fixed equation set is mathematically order-independent; implementation IDs, intermediate work and resource-bounded rule exploration can depend on order. The critic did not supply a valid counterexample to the appropriately canonical fixed-closure claim. Its suggestion that monotone-circuit satisfiability supplies a generic NP-hard example is also unsupported: an ordinary monotone Boolean circuit is satisfiable exactly when its all-ones assignment evaluates true. No general efficient BDD-from-witness result follows from the response.

### 4. Equal distributions do not require one canonical output

Exact content noninterference requires identical conditional output laws across protected inputs. It does not require every output to be the same artifact. For example, a trusted sampler can choose either of two task-valid artifacts with probabilities `(1/2,1/2)` independently of the submitted artifact; all input rows then agree. Constructing such a common law efficiently can be hard in a particular task, but no general reduction or lower bound was supplied. The final rewrite claims that canonical unique output and complete re-solving are unavoidable are therefore not accepted.

### 5. Supplied prime factors can be verified without finding them anew

The Sonnet rewrite revision says a receiver cannot verify uniqueness of a prime factorization without factoring. This is false. Verify that supplied factors are prime, check that their product is the task integer, and sort them into a fixed encoding. Uniqueness follows from the fundamental theorem of arithmetic, rather than from another factor search. The [mathlib declaration `Nat.primeFactorsList_unique`](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Data/Nat/Factors.html#Nat.primeFactorsList_unique) states the relevant product/primality-to-unique-multiset implication. Its statement/documentation was inspected; no Lean proof was executed here.

Deterministic polynomial-time primality testing is established by [Agrawal, Kayal & Saxena, PRIMES is in P](https://annals.math.princeton.edu/2004/160-2/p12). Published abstract inspected, full proof not audited. These two primary sources correct the model's verification claim; they do not prove a superpolynomial lower bound for factoring or a new sanitization result. A small illustration normalizes all 60 factor orderings of 360 to one list; it uses trial division for tiny inputs, not an AKS implementation. Invalid-input fallback, availability and resource observations still need a separate system specification.

### 6. Failed benchmarks and finite searches do not justify universal rejection

Failure to beat one runtime threshold does not imply strict dominance of every reuse method. Failure to identify a unique-witness problem in one model response does not justify permanently abandoning an entire direction. Polynomial-time membership also does not erase meaningful concrete or asymptotic verification/solution cost differences. Sender rationality, NP-hardness, unique certificates and rich-program reconstruction are distinct assumptions; the responses sometimes conflate them.

## What this batch supports

It supplied cheap independent proposals and caught real flaws, but also showed reviewer error and revision overcompliance. Retain the concrete counterexamples and source-verified corrections. Reject the four candidates as presented as useful novel contributions, while keeping the two original approaches open. This is a qualitative observation about this batch, not a general multi-agent reliability estimate.

Before another paid batch, specify one useful task/capability, a fixed authorized release or common rewrite law, a strong computation baseline and the smallest decisive check. Further model debate without those constraints risks converting unsupported optimism into equally unsupported impossibility claims. No full experiment or further spending is selected by this assessment.

Reproduction/checks: [runner](../../experiments/openrouter_research/run_batch.py), [accounting tests](../../experiments/openrouter_research/test_budget.py), [independent elementary checks](../../experiments/openrouter_research/check_model_claims.py), [check results](independent-checks.json), [ledger](ledger.json). Raw visible outputs are under `outputs/`; critiques and revisions should be read with the corrections above.
