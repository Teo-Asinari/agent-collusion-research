# Novelty audit: solution choice, computational erasure and active defenses

2026-10-24. Requested explicitly by the owner to check whether our evolving direction actually covers new ground. **Verdict: novelty of the current proposal is not established. Several broad claims should be withdrawn as potential contributions.** This audit materially downgrades the recommendation to build a generic SAT/solution-choice erasure experiment as if its central idea were new.

## Search and evidence standard

Expanded beyond LLM-steganography vocabulary into hardware/IP watermarking, optimization-intensive watermarking, software semantics/abstract interpretation, cryptographic program watermarking, code-watermark removal and AI control. Used backward/related-work trails and targeted searches for recent agentic defenses. [Source/access ledger and representative queries](../references/novelty-audit-sources.json).

Full PDFs were retrieved where possible, but only targeted methods, assumptions, attacks, results and limitations were inspected. An inaccessible full text is not a completed review. Primary indexed PDF passages are explicitly distinguished from downloaded/full-text inspection. Third-party summaries were discovery aids only; one secondary title/arXiv association was rejected after the primary identifier resolved to an unrelated paper. No model experiments, model downloads, dependencies or spending.

## The closest newly found predecessors

### 1. Kahng et al., DAC 1998: our proposed mechanism is already recognizable

[Watermarking Techniques for Intellectual Property Protection](https://www.cs.ucla.edu/~miodrag/papers/Kahng_DAC_98.pdf), motivating 3SAT example, §3.1 and §4 tampering discussion.

Embed a signature by imposing additional constraints on a design/optimization problem with many acceptable solutions. They explicitly discuss difficult solution generation, local-search barriers, design symmetries, quality preservation, and removal by solving again from scratch. Downstream design stages can increase the cost of replacement. These are design principles/arguments, not a blanket proof that every sanitizer must re-solve an NP-hard problem. Nevertheless, they directly anticipate the central mechanism and cost intuition of our candidate. The 2001 journal follow-up was located, but both attempted full downloads timed out; do not label it fully reviewed.

### 2. Hand and Brain: the closest agentic-defense overlap

[Krzyzanowski et al., primary OpenReview PDF](https://openreview.net/pdf?id=P7fHU7ZNFQ), indexed introduction, Table 3, §5, Appendix A.5–A.6 and D.1–D.2.

Indexed primary passages describe signals in solution strategies, a synthetic math graph/codebook and trained code/perspective/writing organisms. A weaker model supplies prefixes at decision anchors. This directly overlaps our proposed semantic-choice, graph and pre-creation defense framing. The math substrate is synthetic; trained-organism results use particular decoders. §5 flags adaptation and codebook/anchor limitations; Appendix A.6 already adjusts a codebook post hoc. Do not claim that any adaptive analysis is absent.

**Access limit:** direct PDF, attachment, API attachment and forum access were blocked. These findings rely on indexed primary passages, not complete proof/code review. Claimed release was not verified. This is sufficient to reject a broad first-demonstration claim, insufficient to certify a particular extension is new.

### 3. SrcMarker: removal, functionality and defender capability are measured together

[Yang et al., Towards Code Watermarking with Dual-Channel Transformations, arXiv v2](https://arxiv.org/html/2309.00860v2), §II, §IV-D–E and discussion.

Embeds bitstrings through identifiers and AST transformations. It evaluates random and adaptive de-watermarking, including execution-based checks on MBXP. In the inspected adaptive experiment, removing more watermark information also severely damages test performance. Its discussion explicitly relates a sufficiently capable rewriting model to independently generating useful code. Thus even an LLM/code-specific removal-cost versus utility study has close predecessors. The weak generative remover and bounded tests do not establish universal hardness or exact semantic equivalence. A new study needs stronger task-valid attacks or a distinct causal/mechanistic result, not simply another utility plot.

### 4. Semantics-based software watermarking: invariants and observer ability are already formalized

[Dalla Preda & Pasqua, published 2017 article](https://doi.org/10.1016/j.entcs.2017.02.005); [extended author manuscript](https://iris.univr.it/bitstream/11562/1002042/1/main.pdf), §3.2.

Uses abstract interpretation to model signature properties, observers and program transformations. The extended framework explicitly separates resilience, secrecy, transparency and preservation of observable behavior. This is a direct mathematical predecessor to reasoning about task-visible equivalence classes and features preserved by an attacker. Results are relative to formal abstractions and allowed transformations; they are not cryptographic lower bounds against arbitrary computation. Published abstract and targeted extended-manuscript passages were accessible through the web tool; direct PDF download was forbidden. No full proof audit.

### 5. Cryptographic capabilities: formal unremovability can be stronger than local-rewrite resistance

[Cohen, Holmgren, Nishimaki, Vaikuntanathan & Wichs, Watermarking Cryptographic Capabilities](https://people.csail.mit.edu/holmgren/papers/watermarking.pdf), introduction, §1.1 and theorem statements.

Studies function-preserving program watermarks under arbitrary adversarial modification, including message embedding. Positive constructions rely on strong cryptographic assumptions and approximate-correctness definitions; some families instead admit canonicalization/learning attacks and cannot be watermarked under their definitions. This already addresses a rigorous version of useful computation inseparable from a recoverable mark. Ownership detection and covert distribution matching remain different goals. The paper's message-embedding and mark-presence variants also have different approximation thresholds; they must not be merged into one stronger guarantee. Full PDF retrieved; definitions/results overview inspected, proofs not certified.

## Additional checks that narrow possible claims

- [SEW, arXiv 2609.39414v1](https://arxiv.org/abs/2609.39414v1): structural-context-dependent style watermarking, targeted flipping and LLM rewriting, with functional-performance evaluation. Appendix discussion explicitly calls rewriting robustness partial. Method/evaluation and late-appendix limitations inspected. A code-normalization study must compare against current structural schemes; formatting is a weak baseline.
- [PlaceMark, arXiv 2610.21031v1](https://arxiv.org/abs/2610.21031v1): a payload can live in repository module placement; import updates preserve intended functionality. Text transformations leave this carrier intact, while relocation and identity changes are tested separately. Primary abstract checked and PDF retrieved, not a full code/runtime audit. Reformatting source does not close workflow/repository channels.
- [DeCoMa, ISSTA 2025](https://wssun.github.io/papers/2025-ISSTA-DeCoMa.pdf), abstract and §5.3.3: evaluates detection/purification of training-dataset watermarks and compares LLM rewriting cost. Its main purification deletes selected samples; it is not a task-output sanitizer preserving each artifact. CodeBLEU quality does not establish executable equivalence. This is an adjacent cost/utility predecessor, not a direct substitute for our threat model.
- [AI Control, arXiv v5](https://arxiv.org/abs/2312.06942v5): trusted editing, deferral and output signaling already combine weaker defenders with stronger untrusted code generation. The objective is preventing backdoors, not proving covert-channel closure. Abstract and targeted protocol passages inspected; no new reproduction.
- [Rank-Token Mapping Steganography in LLM Chatbots, 2026](https://www.mdpi.com/2079-9292/15/18/4251): already reports HumanEval functional-code evaluation. Primary abstract/introduction/§4.3 checked. Merely adding a code benchmark or execution metric is not a contribution.
- Prior [semantic-erasure review](semantic-erasure.md): Roger–Greenblatt's replacement-capability discussion, semantic-unit channels, conceptual steganography, quality-preserving random walks, slow mixing and constrained cryptographic prevention also remain controlling precedents.

## Claim-by-claim verdict

| Proposed contribution | Closest overlap | Current verdict |
| --- | --- | --- |
| Hide information in which valid solution is selected | Constraint-based design watermarking; semantic-unit systems | Established mechanism |
| Erasure may require expensive regeneration or re-solving | Kahng §4; Roger–Greenblatt §7.2; SrcMarker adaptive-removal discussion | Established intuition and bounded empirical precedent |
| Encode through SAT/constraint solutions and test local versus global removal | Kahng's 3SAT example and design-attack discussion | Broad toy design insufficiently distinct |
| Use solution-space barriers to explain robust signals | Kahng §3.1; watermark-removal mixing literature | Broad explanation already present |
| Use semantic invariants/equivalence and observer capabilities | Abstract-interpretation software watermarking | Established formal direction |
| Intervene in agent decisions rather than just paraphrase | Hand and Brain | Direct agentic-defense overlap |
| Measure code correctness while suppressing an embedded message | SrcMarker; newer code watermarking | Metrics/application alone insufficient |
| Establish unremovability under arbitrary efficient replacement | Cryptographic program watermarking | Existing formal results under restricted families/assumptions |
| Adapt sender/decoder after intervention | Hand and Brain discusses adaptation and already has a post-hoc codebook adjustment | Extension candidate, not verified gap |

## What would actually be a new contribution?

We need a **specific result beyond a named closest predecessor**, not a combination of familiar vocabulary. Three possible forms remain, each currently unverified:

1. **A counterexample to a concrete defense under its deployment assumptions.** For example, demonstrate residual payload transfer after the advertised intervention using a held-out attacker-owned decoder, while preserving the legitimate task. First establish which decoder/adaptation settings are already evaluated; the inaccessible Hand and Brain material is a material review gap. A decoder's error rate can be reversed or corrected, so failure of its frozen head is not by itself channel closure. This is a standard concern, not a new theorem.
2. **A replacement-cost measurement that changes a concrete operational conclusion.** Include strong local and global transformations, independent task re-solving and exact task-validity checks, all under equal resource budgets. The result must identify a previously unmeasured boundary, not repeat that weak rewriters damage code. Constraint-based watermarking and SrcMarker need explicit comparison.
3. **A narrowly stated theorem for a precisely defined task/interface.** Specify honest-task utility, sender control, receiver knowledge and all allowed defender computation. Demonstrating invariance under our chosen edits is insufficient. Existing program-watermarking results mean this cannot be advertised as the first computational barrier to erasure. No such new theorem is currently established in this workspace.

Before selecting any of these, the minimum novelty argument is a table comparing our exact claim, threat model, intervention, adaptation and measurement with the closest sources. A paper's future-work suggestion is not evidence that nobody subsequently did it. Negative keyword searches are not proof of absence.

## Updated recommendation

**Do not treat the current generic solution-selection/erasure-cost proposal as a novel hackathon project.** It remains a useful organizing lens, but new work must now be an explicit extension, counterexample, replication with a consequential correction, or more sharply specified result. The strongest immediate scientific baseline is an existing agentic defense, not a newly invented weak paraphraser. No full experiment or project selection is authorized by this audit.

Search limits: targeted open-web/author/primary searches through 2026-10-24, not an exhaustive citation-index search. Multiple full-text access failures are recorded. The absence of a verified follow-up here does not establish novelty. No unrelated AI-generated secondary record was accepted as a primary result.
