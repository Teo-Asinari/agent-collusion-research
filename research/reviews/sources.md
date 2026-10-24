# Independent adversarial-review source ledger

2026-10-24. Targeted primary-source review. No full proof/code audit, source reproduction, inference or training. Links are external; no third-party texts vendored. This ledger records review depth rather than implying all downloaded text was read.

| Primary source | Inspected | Use/qualification |
| --- | --- | --- |
| [Tiwari et al., USENIX Security 2024](https://www.usenix.org/system/files/usenixsecurity24-tiwari.pdf) | Abstract, §§2.3,3.1–3.2 | Training-domain isolation and access-aware neural architecture; not general malicious-agent stego prevention. |
| [LLMbda, arXiv 2602.20064v2](https://arxiv.org/html/2602.20064v2) | §4.2, Lemma 4.2 and theorem framing | Total-program specialization is existing prior art; Lean not inspected/executed. |
| [Pandey et al., arXiv 2610.25032v1](https://arxiv.org/html/2610.25032v1) | Abstract, §V-C Eq.35/Prop.V.3, key discussion, §VI-D and appendix proof-framing passages | Distinguish balanced-attribute/independent-key average bounds from a per-task/per-key interactive specification. Full derivation and code not audited. |
| [Roger–Greenblatt, arXiv 2310.18512v2](https://arxiv.org/html/2310.18512v2) | §§5.3,7.2 | Reusing useful insights versus answering afresh and generation limits already explicit. |
| [Kahng et al., DAC 1998](https://www.cs.ucla.edu/~miodrag/papers/Kahng_DAC_98.pdf) | §4 tampering discussion | Re-solving and local/global attacks precede the proposal; no universal hardness theorem inferred. |
| [SrcMarker, arXiv 2309.00860v2](https://arxiv.org/html/2309.00860v2) | §IV-E adaptive de-watermarking | Adaptive removal and executable utility already tested, with bounded tests and particular attacks. |
| [Polak–Schmidt, arXiv 2607.00857v1](https://arxiv.org/abs/2607.00857) | Primary abstract only | Prediction-assisted APSP with optimality certification/error recovery; adjacent algorithms-with-predictions comparator, not a security result. |
| [Jain–Lin–Sahai, arXiv 2008.09317v1](https://arxiv.org/pdf/2008.09317) | Abstract/introduction and §2 definition framing; indexed ePrint definition additionally located | Conditional iO for equivalent equal-size circuits is a direct computational-indistinguishability comparator. Construction proof not reviewed. ePrint 2020/1003 PDF returned 403; arXiv PDF accessible. |
| [Neural-Guided Deductive Search, arXiv 1804.01186v2](https://arxiv.org/abs/1804.01186v2) | Primary abstract | Learned guidance of deductive synthesis is prior art, not newly established anti-stego. |
| [Sabelfeld–Myers, Delimited Information Release, 2004](https://research.chalmers.se/en/publication/2026) | Author institutional abstract only | Controlled disclosure is an existing information-flow target. |
| [egg, arXiv 2004.03082v3](https://arxiv.org/abs/2004.03082) | Primary abstract | Equivalent-expression representation/search; no canonical-output or secrecy guarantee inferred. |

STOKE author PDF https://theory.stanford.edu/~aiken/publications/papers/asplos13.pdf failed with timeout/status errors in this pass. Watermark random-walk and Hand and Brain observations are inherited from the workspace's explicit source ledgers, not newly completed full-text reviews here. Obfuscation-impossibility search results were discovery leads only and are not used to infer impossibility of the proposed sanitizer.

Representative searches: learning-augmented shortest paths with certification; exact equivalent-program canonicalization; iO same-size circuit definition; exact titles from the two author ledgers. New source additions are theoretical comparators, not proof that a practical follow-up is novel or impossible.

## Round-two addition

[McConnell, Mehlhorn, Näher & Schweitzer, Certifying Algorithms, author preprint](https://people.mpi-inf.mpg.de/~mehlhorn/ftp/master-final.pdf), abstract and §2.4 read on 2026-10-24. The positive-weight shortest-distance certificate and proof conditions directly precede the rewrite repair. The 94-page survey was not fully read; no proof or implementation audit is claimed. A guessed `CertifyingAlgorithms.pdf` URL timed out; the author's `master-final.pdf` source was accessible. Architecture round-two checking reused the source set above and audited its revised transition argument without new paper claims.
