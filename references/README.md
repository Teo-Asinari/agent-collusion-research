# References

Primary URLs, paper versions and review scope are recorded in [the literature review](../research/literature.md). Starter source paths, code observations and license limitations are recorded in [the pinned inventory](../research/starter-map.md).

Expanded follow-up: [secure-steganography review](../research/stego-prior-art.md) and [machine-readable source ledger](stego-review-sources.json). The ledger records 16 paper retrieval attempts (one blocked), artifact hashes, inspected code locations and explicit reading limits. Retrieval does not imply full review.

Substantive-choice follow-up: [semantic erasure review](../research/semantic-erasure.md) and [its source ledger](semantic-erasure-sources.json) record direct conceptual predecessors, task-quality-preserving removal, mixing obstacles, cryptographic counterexamples and the pinned semantic-unit manuscript/code inspection. Abstract-only sources are explicitly marked.

Access date: 2026-10-24. Sources inspected directly include:

| Source | Version / provenance | Review depth |
| --- | --- | --- |
| [Official sprint](https://apartresearch.com/sprints/ai-collusion-research-sprint-2026-10-23-to-2026-10-25) | Live page accessed Oct 24 | Tracks, detailed research questions, resources and submission deadline |
| [Starter repository](https://github.com/poseidon-research/collusion_hackathon/tree/e6fb1308dae9cf97ae42aec1c5f7889d9e2291e8) | Commit e6fb1308dae9cf97ae42aec1c5f7889d9e2291e8 | Root README, literature guide/CSV, project READMEs and selected code/configs |
| [Rippin tool-use paper](https://arxiv.org/html/2606.28425v1) | v1 | Methods, theory framing, experiments, limitations, prompts and Appendix D |
| [Minimum entropy coupling](https://arxiv.org/html/2210.14889v4) | v4 | Threat model, definitions, Theorems 1–2; [author-linked code](https://github.com/schroederdewitt/perfectly-secure-steganography) identified, not audited |
| [Zamir steganography](https://arxiv.org/html/2401.10360v1) | arXiv v1 under earlier title | Definitions, security/retrieval results, evaluation/limitations; final OpenReview text inaccessible |
| [OrZamir/steg](https://github.com/OrZamir/steg/tree/c099f157550135e528ee799d686d6b480bdff335) | Pinned author-linked reference | Follow-up static source inspection: single-query/insecure-PRF caveats and model-free decoder; README prohibits commercial use; no separate LICENSE in inspected tree |
| [Covert conversation/key exchange](https://arxiv.org/html/2604.04757v1) | v1 | Results overview, model, construction overviews; not a complete proof audit |
| [Voluntary secret tools](https://arxiv.org/html/2605.27593v2) | v2 | Protocol, empirical design, limitations and observation/benign-control appendices |
| [Hidden in Plain Text](https://arxiv.org/html/2410.03768v2) | v2 | Methods/mitigation overview; [code README](https://github.com/olliematthews/lasr-steganography) associates repository with paper; code not audited |
| [Colosseum](https://arxiv.org/html/2602.15198v1) | v1 | Formulation, experimental settings, emergent/prompted contrasts and metric/prompt appendices |
| [Bonjour](https://proceedings.mlr.press/v180/bonjour22a.html) | UAI 2022 published paper | Introduction and §3 in PDF |
| [Audit the Whisper](https://arxiv.org/html/2510.04303v1) | v1 | Threat model, power argument, experiment and limitation sections; selected bundled detector code inspected |
| [HELIOS](https://arxiv.org/abs/2604.01151v5), [SCHEME](https://arxiv.org/abs/2605.29178v1), [Noticing the Watcher](https://arxiv.org/abs/2603.16928v1), [Double auctions](https://arxiv.org/abs/2507.01413v1) | Versions linked | Abstract-level paper review; auction runner additionally inspected in starter |

No paper PDFs, upstream source trees, credentials, or raw source archives are committed here. Temporary source copies are disposable and are not a durable dependency. Primary links plus pinned versions make the inspection recoverable.

Tool-use paper code availability remains unresolved: its checklist claims supplementary setup/code, but no accessible author-owned release was verified. A GitHub repository title search returned no results; that is not proof no release exists. Use the paper's supplied prompts for methodological context; do not describe the foundational Zamir or focal-points repositories as the tool-use paper's released experiment code.
