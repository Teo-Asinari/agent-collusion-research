# Local rewrites can preserve a hidden component label

**Status:** exploratory conceptual result, not a selected study or novelty claim. Added 2026-10-24 to connect task-preserving reconstruction with the owner's interest in topology and complexity.

## The construction

Fix a task `x`. Let `V_x` be its task-valid artifacts, and choose an explicit set of allowed elementary rewrites. These define an undirected graph `G_x`: artifacts are vertices and a legal one-step rewrite is an edge. A sanitizer restricted to these moves must return an artifact in the connected component of its input.

If two sender inputs `y_0,y_1` lie in distinct components, then no sequence of allowed rewrites can map one to the other. More generally, any output supported only on artifacts reachable from its input preserves the component label. If the receiver can distinguish the components, that label remains a perfect payload channel even though every intermediate and final artifact passes the task-validity check. In topological language, the invariant is the connected-component class (the simplest, zero-dimensional part of the space); no knot invariant or continuous topology is needed for this statement.

Tiny example: task-valid assignments satisfy `x != y`. The two valid strings `01` and `10` form separate components when an elementary rewrite may flip only one bit and every intermediate state must remain valid. A rewrite walk that starts at `01` cannot output `10`; the choice remains decodable. This is a pedagogical counterexample, not evidence about LLMs or a useful benchmark.

The conclusion depends entirely on the move set. If the defender may discard the input and solve the task afresh, it can jump components. If it may make a multi-edit jump, components can merge. If the receiver cannot identify the component, component preservation alone does not establish a usable channel. If artifacts are only required to be approximately valid, the graph must include the permitted invalid intermediates and the conclusion can change.

## Why this might help the research

It gives a precise way to ask whether a proposed “small edit,” local paraphrase, or incremental repair can remove sender choice while preserving validity. It also explains why a rewrite can succeed at normalization within a region yet retain a coarse choice between regions. A meaningful study would need to measure the cost of *cross-component* reconstruction against a strong task-only solver and test whether component identity is observable to an adaptive receiver.

The candidate question is: **When do task-valid artifact spaces have receiver-distinguishable components under a realistic defender edit budget, and what extra compute is required to erase component information while retaining task utility?** This is narrower than arbitrary steganography prevention and is not yet shown to matter for any realistic agent workflow.

Potential design, only if retained after more review:

1. Choose a task family with an exact validity checker and many valid artifacts.
2. Define a defender edit grammar before seeing payloads; include one-edit, bounded-edit, and task-only resynthesis arms.
3. Encode a balanced payload by selecting between artifacts/components, then compare identity, local rewrite, global canonicalization, and independent reconstruction.
4. Measure task validity/quality, component-label recovery by a receiver trained after the rewrite, defender work, and visible failure/timing/status.
5. Include cases with connected spaces as negative controls and cases where the rewrite grammar connects components as an intervention check.

This would test a boundary of local sanitization; it would not show that arbitrary steganography is impossible to remove.

## Prior-art warning and novelty status

Combinatorial solution reconfiguration already models feasible solutions as vertices and legal local changes as edges, and studies reachability, connectedness and hardness. [Ito et al., *On the Complexity of Reconfiguration Problems*](https://www.math.uwaterloo.ca/~harvey/Publications/Reconfiguration/Reconfiguration.pdf) explicitly defines a search problem, feasible solutions and a polynomially testable adjacency relation. [Cardinal et al., *Reconfiguration of Satisfying Assignments and Subset Sums: Easy to Find, Hard to Connect*](https://arxiv.org/abs/1805.04055) proves PSPACE-completeness for particular reconfiguration problems. These are direct mathematical precedents for the graph model and its reachability difficulty.

There is also adjacent software-watermarking prior art that uses program-graph structure to encode an identifier and studies semantics-preserving graph edits against it: [Collberg et al., *More on Graph Theoretic Software Watermarks: Implementation, Analysis, and Attacks*](https://doi.org/10.1016/j.infsof.2008.09.016). This is not the same claim as a task-valid solution-space component invariant, but it means “topology can carry a watermark and survive some semantics-preserving transformations” is plainly not a new observation.

The anti-steganography application overlaps solution-choice watermarking and reconstruction/re-solving, already covered in [the source ledger](sources.md) and [novelty audit](../../novelty-audit.md). The elementary component-preservation lemma is not a novelty claim. The graph-watermarking literature is an additional warning that topology itself is an established carrier. The possible gap is empirical and deployment-specific: whether realistic task-preserving rewrite grammars leave a receiver-decodable component label, and the measured price of leaving that grammar to remove it. That gap is unverified, and broad claims about all sanitizers would be false because task-only reconstruction can leave the starting component.

Primary-source reading: Ito et al. PDF, abstract and §§1–2; Cardinal et al. arXiv primary, abstract and introduction/definitions/results; Collberg et al. journal abstract. These confirm the reconfiguration setup/complexity results and adjacent use of program-graph structure for watermarking. No code or proofs reproduced. No new experiment, dependency, model call or compute spend was used for this note.
