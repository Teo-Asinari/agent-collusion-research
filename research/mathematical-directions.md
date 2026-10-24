# Mathematical connections for active anti-steganography

**Prior-art update:** [Watermarks in the Sand and Sandcastles in the Storm](semantic-erasure.md) already formalize/test task-quality-preserving walks and practical mixing obstacles. Our transformation-graph proposal below is therefore a restatement/application of existing research, not a new connection. The same review adds solution-reconfiguration complexity as an adjacent, carefully qualified direction.

2026-10-24. Owner asked whether knot theory, topology and complexity can clarify prevention/erasure. These are conceptual tools and candidate questions, not novelty claims or a selected full experiment.

## Equivalence classes and constrained release

Choose an explicit task semantics U(x), rather than an informal similarity score. Define x ~ y iff U(x) = U(y). This is an equivalence relation, and the quotient groups all representations with the same allowed meaning.

A trusted release function of the form N(x) = g(U(x), R), with defender randomness independent of the payload and input, eliminates dependence on the input representation once U is fixed. This is what the current structured prototype illustrates. It does not remove a payload encoded in U itself. The substantive question is how much task semantics can be coarsened or independently resolved while retaining useful agent authority.

This is naturally an algebra/semantics connection; calling every quotient a topological construction would add terminology without a result. For arbitrary prose, an exact trustworthy U is not supplied by saying “preserve meaning.”

## Transformation graphs, surviving invariants and mixing

Proposed model: nodes are valid realizations of the same permitted task result; edges are allowed local rewrites. An attacker can encode information in features preserved by all the rewrites. Distinct connected components are an immediate obstacle to a rewrite-only sanitizer that must stay on those edges.

Knot theory suggests looking for invariants under allowed transformations, but no knot encoding or useful knot invariant has been established for this setting. A literal knot representation could introduce an artificial problem. The useful question is which observable invariants survive our actual transformations and whether a receiver can read them.

A more concrete candidate uses Markov chains: repeatedly apply randomized task-valid rewrites. On a finite irreducible aperiodic chain, sufficiently long walks approach a stationary law independent of the initial node. Investigate the finite-time mixing/security versus legitimate-utility/latency tradeoff, and deliberately test disconnected components and slowly mixing regions. Connectivity alone does not make a short walk erase information. This proposal is an application of standard Markov-chain reasoning, not an established new anti-steganography theorem.

## Information-flow security and topology of executions

[Goguen & Meseguer, Security Policies and Security Models (1982)](https://www.cs.purdue.edu/homes/ninghui/readings/AccessControl/goguen_meseguer_82.pdf) provides the noninterference foundation: forbidden activity must not affect what another observer can see. Review scope: introduction and policy framing. We would adapt this to allowed task information and explicitly modeled observations, including timing when relevant.

[Clarkson & Schneider, Hyperproperties (2010)](https://www.cs.cornell.edu/fbs/publications/Hyperproperties.pdf) treats security policies over sets of executions, including information flow. It supplies a genuine topological connection via characterizations of safety/liveness hyperproperties (§6), and discusses probabilistic noninterference (§7.2.4). Review scope: introduction and targeted sections. This motivates comparing executions that differ only in private payloads, rather than deciding whether a single transcript “looks suspicious.” The classification itself is not an implemented defense or proof of a deployed service.

## Complexity: distinguish optimal efficiency from security

[Compton et al., Minimum-Entropy Coupling Approximation Guarantees Beyond the Majorization Barrier (AISTATS 2023)](https://arxiv.org/abs/2302.11838) studies approximating the NP-hard coupling optimization and provides bounds for greedy coupling. Review scope: abstract; do not infer detailed algorithm behavior beyond this without reading proofs.

Importantly for our ideas, making exact throughput optimization difficult does not automatically prevent distribution-preserving communication. An attacker may accept an inefficient channel. The reference steganography repository itself uses an efficient approximate coupling procedure; see the inspection note. A complexity-based defense needs an actual asymmetry: legitimate task completion remains feasible while the forbidden signaling operation becomes costly under specified resources. “This optimization is NP-hard” alone is not that argument.

## Questions worth comparing

1. Can task-aware rewrite graphs remove signals an ordinary paraphraser leaves as invariants?
2. Does the erasure budget needed for independent outputs scale differently from the budget needed merely to defeat a fixed decoder?
3. Can we construct a practical noninterference argument for one released observation surface, then identify its failure under added timing/resource observations?
4. When does canonicalization become more expensive than trusted recomputation, and what agent capabilities does recomputation remove?

These connections suggest experiments; they do not establish that knot theory is necessary or that a novel protocol has already been discovered.
