# Substantive choices as channels: prior art and limits of erasure

**Subsequent novelty correction:** [the expanded audit](novelty-audit.md) found direct constraint-based/SAT watermarking predecessors and a closer agentic-defense paper, Hand and Brain. The candidate below is retained as exploration, but its broad mechanism and erasure-cost intuition are insufficiently novel. Do not start a full study on the assumption that they are new.

2026-10-24. Follow-up requested by the owner after questioning the focus on token-sampling codecs. Scope: signaling through examples, reasoning, citations, programs and solutions; the computational cost of replacing those contributions; and counterexamples where a protocol can sanitize outputs efficiently. This is targeted primary-source research, not an exhaustive survey or proof audit. No new experiment selected or run.

## Main assessment

The broad intuition already has direct predecessors. **“The defender may understand an output but be unable to generate a different useful one” is explicitly discussed by Roger–Greenblatt.** Semantic channels and task-preserving random-walk removal are also established. A stronger contribution would characterize a particular replacement-cost gap under a defined task, adversary and resource budget. We did not establish a general lower bound that erasing a useful agent contribution requires recomputing it.

Two preservation requirements must be separated:

- **Preserve the submitted content:** keep its claims, references, example, solution and intended meaning while changing expression.
- **Preserve performance on the original task:** permit a different example, citation selection, solution or plan if it still meets the task specification.

A signal attached to the selected content can survive the first requirement by construction. That alone says little about the second. Conversely, replacing content may destroy legitimate specificity or utility; the task contract must settle what changes are allowed.

## Direct predecessors

### Roger & Greenblatt, 2023: the replacement-capability problem is explicit

[Preventing Language Models From Hiding Their Reasoning, v2, §7.2](https://arxiv.org/abs/2310.18512v2).

They distinguish failures of generation from failures of understanding. A weaker trusted paraphraser may recognize a hidden choice yet lack the capability to replace an example or generate another prime; rearranging function calls may require understanding a codebase. They suggest standardization and canonical choices as partial mitigations. These are conceptual limitations in a paper with bounded mitigation experiments, not a proven computational lower bound. Prime generation itself should not be treated as a universally hard task: standardized algorithms can often replace that particular choice cheaply. The user's proposed intuition is directly anticipated here; novelty cannot rest on restating it.

Inspected: full relevant §7.2 discussion and surrounding evaluation limitations from the earlier retrieved PDF.

### Jin, Jurayj & Walden: semantic units in QA, stories and literature reviews

[Author repository and manuscript source, pinned at 6264b4a](https://github.com/ChihshengJ/robust-steganography/tree/6264b4ac1f3d2ceff47a5b51ef7b09a3c9726d85).

The public manuscript selects discussion subtopics, plot details or references according to a secret-key mapping, then uses an LLM to produce prose. The receiver reconstructs the alternatives and identifies which appeared. Its cited-content channel survives ordinary paraphrasing because those attacks preserve the chosen content. The literature-review implementation uses keyed HMAC labels and ordering; the README's older SHA-256 description is not the precise current implementation.

The manuscript reports recovery on 30 texts per task/payload size, with only one baseline and tuned prompts. This is empirical robustness under specified transformations, not demonstrated perfect distribution matching or spontaneous agent discovery. It explicitly excludes attacks that change meaning. Independently replacing citations while preserving task quality is outside that evaluation. The public repository includes manuscript variants; independent venue/publication status was not confirmed.

Inspected: README, `src-realm-2026-cam` abstract/setup/results/limitations and selected `litreview.py` functions; source only, no execution.

### Conceptual Steganography, 2026: reasoning behavior carries the signal

[Zhou & May, §4.9 and Limitations](https://arxiv.org/abs/2605.26537).

An instructed codebook maps reasoning behaviors to payload bits. Content-preserving paraphrasing can retain these behaviors. A defense told which behavior to remove substantially reduces recovery in the tested setting, but leaves a residual channel. This already occupies “signal through reasoning choices rather than surface words.” The targeted defense's coverage is narrow; there is no universal undetectability guarantee or measured lower bound on replacement computation. See the [earlier review](stego-prior-art.md) for scope.

### Perry et al., 2025: formal robustness depends on the allowed transformation

[Robust Steganography from Large Language Models, v1, §§4–7 and Appendix B.3](https://arxiv.org/html/2504.08977v1).

The semantic construction rejection-samples text until an embedding hash matches a payload chunk. Strong robustness constrains paraphrases by embedding distance and assumes hash stability; cost depends on sampling entropy and hash balance. Evaluation includes small payloads and explicit sampling-cost limits. The formal hash/entropy assumptions require scrutiny rather than treating the result as universal semantic security. In particular, Appendix B.3's balancing argument alone does not show that conditioning on a fixed payload leaves the cover law unchanged; payload/key averaging and the security game matter. This is an issue to resolve, not a completed proof refutation. It neither establishes nor tests task-equivalent replacement beyond preserving the source semantics.

## The most relevant theoretical/empirical debate

### Watermarks in the Sand, ICML 2024

[Zhang et al., §§1.1, 4 and Theorem 2](https://proceedings.mlr.press/v235/zhang24o.html).

The remover may produce any comparably good response to the original prompt; it need not preserve the original answer's meaning. A quality oracle checks candidates and a perturbation oracle produces edits. The guarantee depends on quality-preserving transitions and mixing of the high-quality-output graph; running time scales with mixing time. The work already formalizes the task-preserving search idea suggested in our earlier topology notes. It does not assert that every task admits cheap transitions or fast mixing. Its primary target is watermark detection; translating a guarantee to payload erasure requires stating the output-independence or communication-security goal explicitly.

### Sandcastles in the Storm, ACL 2025

[Harel-Canada et al., §§3–5, Limitations](https://aclanthology.org/2025.acl-long.1436/).

This empirical follow-up tests slow mixing, imperfect quality judgments and practical attack success. It discusses disconnected high-quality “islands”: moving between good answers using local edits can pass through bad intermediates. Such barriers may disappear with larger rewrites or relaxed intermediate-quality requirements. Reported lineage attribution uses best-of-two judgments with model escalation; it is not a clean single-call classifier accuracy or formal total-variation estimate. Recognizable origin also does not by itself prove a particular watermark or payload remains recoverable. The study is strong prior art on practical erasure obstacles, not an unconditional lower bound or proof of permanent unremovability.

## Related mathematical and cryptographic work

### Solution reconfiguration: valid alternatives need not be locally accessible

[Gopalan, Kolaitis, Maneva & Papadimitriou, arXiv v2 / SIAM J. Computing](https://arxiv.org/abs/cs/0609072v2).

Study a graph of satisfying Boolean assignments with edges for single-variable changes. Their dichotomies include PSPACE-complete connectivity questions and exponentially large component diameter. This illustrates the gap between checking a supplied solution and navigating among solutions. It is adjacent complexity theory, not a steganography result. Worst-case reachability hardness does not establish average-case sanitizer hardness, prohibit global resampling, or show that finding any different solution is hard. Review depth: primary abstract only; theorem reductions not inspected.

### Source-code transformations have a long history

[Hulette & Solis, WIIS 2011](https://www.johnsolis.com/publications/stego-wiis11.pdf).

They propose encoding through term-rewriting transformations of programs and discuss semantic preservation and invertibility. This is an exploratory proposal, explicitly leaving implementation/theory development to future work. Its claims about fundamental limitations should not be imported as proved impossibility results. It establishes prior conceptual coverage of source-code choice as a carrier; a contemporary contribution must go beyond identifiers or arbitrary equivalent rewrites. Review depth: abstract, transformation overview and concluding limitations/future work.

### Reverse firewalls: replacement need not reconstruct the secret work

[Mironov & Stephens-Davidowitz, EUROCRYPT 2015](https://eprint.iacr.org/2014/758); [Ganesh, Magri & Venturi, ICALP 2020](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ICALP.2020.55).

These design intermediaries that modify cryptographic traffic while preserving specified functionality/security and blocking exfiltration. Protocol-specific rerandomization can provide a route to sanitization without learning the hidden witness or solving the original task. This is a counterweight to a universal “must redo the work” claim. Such results depend on protocol structure, interfaces and the exact leakage model; they are not generic prose sanitizers. The original framework also requires care about which party observes leakage and how firewall security is defined. Review depth: primary abstracts and targeted search passages; original full-paper download was blocked. No theorem-level review claimed.

### Steganography-free proofs: pre-creation prevention already exists in restricted models

[Abdolmaleki et al., TCC 2022, §1 definition/construction overview and §7 impossibility statement](https://eprint.iacr.org/2022/1263).

An honest preprocessing phase fixes later degrees of freedom; an observer detects nonconforming execution. At least one party must be honest during preprocessing. Computationally unique accepted transcripts constrain signaling; the definition addresses unique-witness languages with an extension discussed for multiple witnesses. Two constructions use different assumptions and execution/reuse conditions. Fully malicious preprocessing faces a stated impossibility under their additional properties except for languages in BPP. These are formal protocol results, not ready LLM defenses. They suggest replacing a rich artifact with a constrained verifiable assertion when the task permits it; doing so may discard the explanation or executable program the user needed.

[Quach, Tyner & Wichs, Unique NIZKs and Steganography Detection, EUROCRYPT 2025](https://eprint.iacr.org/2025/1898) further studies computationally unique proofs with prover setup and unique-witness qualifications. The advertised monitoring application requires its protocol machinery; it does not contradict transcript-only impossibility for arbitrary existing outputs. Review depth: primary abstract only; PDF access failed.

Earlier lineage: [Lepinski's 2006 MIT thesis](https://dspace.mit.edu/entities/publication/e3efeaef-ab06-4226-95e5-fc8813714bda) directly connects covert protocol traffic and collusion prevention. Only the repository abstract was inspected here; its game/protocol results need separate reading before operational use.

## A sharper candidate: replacement cost across useful solution classes

**Question.** Under equal legitimate-task success, does removing sender-selected substantive choices cost substantially more than rewriting syntax, and which structural properties predict that gap?

**Possible controlled setting.** Use small constraint/planning tasks with an exact validity oracle and several acceptable solutions. Sender encodes via solution selection; receiver reads a declared semantic property. Compare format normalization, valid local rewrites, larger coordinated rewrites and solving afresh. Include a task with cheap global rerandomization as a negative control. Use easy and hard task families, measuring actual difficulty rather than labeling every SAT instance hard.

**Falsifiable hypothesis.** At matched solver budget and task validity, local transformations retain more sender-payload dependence in clustered solution spaces than in easily rerandomizable ones; global replacement may remove the difference. Signal visibility, component structure and restricted transformations must be independently checked. This can fail, and a cheap global sanitizer would be a valuable counterexample.

**Positive controls / confounders.** Require a functioning encoder/decoder before sanitization and independent payload assignments. Do not give the defender the payload. Check performance against the original task specification, not embedding similarity. Measure exact recovery, partial information and whole-channel closure across repeated outputs. Ensure the signal is genuinely optional task content rather than an obligatory private fact. A fixed decoder's failure is weaker than output independence; disconnected local-edit components do not defeat a global solver.

**Feasibility and inference.** A small scripted feasibility check can test the mechanism with no model calls; connecting it to real useful agent work is the harder scientific step. Benchmark construction, several independent instances per difficulty level and end-to-end decoder validation are required. No defensible total cost/power estimate exists before choosing a family and solver limits. No experiment is launched by this note.

**Informative negative results.** Fresh solving may be cheap, local rewrites may already cross the relevant signal classes, or a structured release may satisfy the task while eliminating the signal. Any of these narrows the premise. A toy worst-case obstruction is insufficient evidence of a real deployment barrier.

## What is established versus still open for us

**Established prior art:** semantic-choice channels; capability limitations of paraphrasers; quality-preserving random-walk removal; practical mixing/oracle problems; constrained cryptographic prevention.

**Not established by this review:** a novel general anti-steganography protocol; a generic lower bound equating erasure with recomputation; reliable semantic noninterference for unconstrained agents; novelty of the proposed task/complexity comparison. The useful next discussion is about a concrete task and adversary boundary, not whether semantic steganography exists.

Source hashes and detailed access/review limits: [ledger](../references/semantic-erasure-sources.json). PDFs and upstream source remain external; no API keys, model calls, dependencies or GPU allocation were involved.
