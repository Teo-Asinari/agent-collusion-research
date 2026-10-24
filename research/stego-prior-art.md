# Secure steganography: assumptions, implementations and active defenses

Review date: 2026-10-24. This completes a **bounded comparative review**, not an exhaustive survey or certification of proofs. No new model experiment was run. Scope: the four requested families, their relevant predecessors, asymmetric/keyless constructions, and defenses or robustness results that change our proposed experiments.

Primary PDFs and small artifacts were inspected outside the repository in `/tmp/stego-deep-review`. [The source ledger](../references/stego-review-sources.json) records retrieved-file hashes and access failures. Upstream source is not vendored. Author-reported experiments below have not been reproduced here.

## Findings that change the brainstorm

1. **Passive undetectability and resilience to an active intervention are different guarantees.** A protocol can satisfy the former and fail the latter. Active wardens are already part of classical theory; intervention does not automatically defeat every construction.
2. **Reproducing the sender's model is not universal.** Zamir's receiver uses tokenization, a key and scores; Codetta uses a shared auxiliary model; BAM has a model-agnostic receiver. A defense based only on sender/receiver model mismatch misses these families.
3. **There are concrete implementation gaps.** The inspected SparSamp experimental decoder accepts encoder-side interval data as a numerical workaround. This is stronger setup than an isolated receiver. It is not evidence of a new attack or a refutation of the ideal theorem.
4. **Editing and resynchronization are already researched.** Alkaid and sentence-space resynchronization are necessary adversarial comparisons for an erasure proposal, although their guarantees differ substantially.
5. **Cost needs two denominators:** visible carrier tokens and private generation/computation. A short visible exchange can require extensive candidate sampling. Setup cost, payload cost, repair cost and task utility should be measured separately.

## Comparison of dependencies

Each cell describes the inspected construction, not every possible variant of its family. “Not guaranteed” does not mean empirically impossible.

| Family | Receiver dependency | Security / optimality being discussed | Active alteration |
| --- | --- | --- | --- |
| iMEC | Matched probability calculations, key and evolving posterior | Ideal distribution matching; MEC characterizes an information-throughput objective; practical coupling is approximate | No general editing guarantee in our inspected reference |
| Zamir | Key, tokenizer, scoring/ECC rules; no receiver model inference | Computational undetectability; entropy-conditioned retrieval rate | Restart/substring adaptation discussed; broad editing robustness left open in inspected v1 |
| SparSamp | Model/context, random stream and arithmetic state | Computational security argument and efficient embedding | Token ambiguity treated separately; arbitrary edits not covered |
| Shimmer | Model/prompt, key/random stream, interval state | Computational security; information collection and rate bounds | Correctness concerns an unaltered encoded token string |
| Wang–Moulin | Shared randomized code/key and channel model | Perfect block-distribution matching; asymptotic capacity under distortion constraints | Explicit compound memoryless attack channel |
| Codetta | Keyed phase: public auxiliary model and transcript; keyless phase: prescribed exchange | Computational covertness, extraction correctness and measured payload rate | Its ECC handles embedding noise, not edited transcripts |
| BAM | Key, tokenizer, identical observed prefix and feedback rules | Cryptographic covertness and empirical reliability | Transcript rewriting explicitly outside security setting |
| Alkaid | Model/history, seed, reconstructed codebook and alignment | Ideal distribution equality under message-distribution conditions; PRG instantiation computational | Minimum-distance correction; bounded edits / specified random edit channel |

## Requested core sources

### Zamir: model-free decoding is already present

[arXiv v1, §§2.4, 5–8](https://arxiv.org/html/2401.10360v1); [author code](https://github.com/OrZamir/steg/tree/c099f157550135e528ee799d686d6b480bdff335).

The sender chooses tokens using keyed pseudorandom scores; the receiver accumulates scores and decodes a dynamic error-correcting stream without evaluating the LLM. Retrieval requires sufficient realized entropy with additional regularity conditions. Computational undetectability does not mean exact finite-output capacity optimality. The evaluation uses GPT-2, 100 runs per response length, and the simpler single-query algorithms. Broad edit robustness is left open; substring/restart adaptation is discussed.

**Code inspection:** `generate.py:8–24` explicitly limits the demo to single-query algorithms and warns that its PRF is insecure. `utils.py:7–10` implements it through Python `random`; `generate.py:156–177` confirms model-free extraction. Thus the demonstration is not a hardened multi-query implementation. OpenReview access to the published TMLR version was blocked; this review must not silently substitute v1 for that version.

### SparSamp: practical synchronization is a real dependency

[USENIX Security 2025, §§3.4–3.6, 4.6–4.8](https://www.usenix.org/system/files/usenixsecurity25-wang-yaofei.pdf); [initial artifact](https://zenodo.org/records/14736967); [v4 artifact](https://zenodo.org/records/15025436).

Sparse candidates encode a shrinking range of possible payloads using matched pseudorandom offsets. Both sides need compatible model/context/state. The security argument assumes a secure random generator; arithmetic and surface-text token ambiguity require separate attention. The paper already discusses BackCheck and SynPool for tokenization ambiguity. Tests against particular steganalyzers do not certify universal undetectability.

**Code inspection:** v1 and v4 Basic Test use Python `random`. More consequentially, v4 `Experiments/src/sparsamp.py:102–133` takes `enSE_list`, recomputes intervals, and replaces discrepancies with encoder values. `get_statistics.py:94–102` supplies that list. Basic Test has no such argument. This documents an assisted experimental path, not an observed isolated-decoder failure rate. A reproduction must report both paths separately and replace demo randomness before evaluating cryptographic security.

### Shimmer: residual entropy is reused, but “optimal” needs qualification

[USENIX Security 2025, §§3–6](https://www.usenix.org/system/files/usenixsecurity25-bai-minhao.pdf); [retrieved artifact record 15636547](https://zenodo.org/records/15636547).

Shimmer retains information left over in an interval after emitting bits, reducing waste across tokens; its refinement mitigates interval splitting. Security uses a secure PRG and finite-grid approximation arguments. Rate analysis accounts for splitting and residual information: it is not an assertion that every finite output reaches Shannon capacity. Correctness assumes matching model/prompt and unaltered encoded tokens. Evaluations compare rate, speed and text quality, not an active task-preserving warden.

**Code inspection:** `shimmer.py` loads a hard-coded local model path at import. Encoding and decoding reseed Python `random` with `seed + str(token_cnt)`; this is not a cryptographic PRG. The source provides a research implementation, not independent verification of the theorem's cryptographic assumptions. The paper-linked API record resolved to 15636547; exact source hashes are preserved.

### Wang–Moulin: active resistance predates LLM steganography

[2007 arXiv v3, §§III–VII and Theorem 1](https://arxiv.org/pdf/cs/0702161v3).

An encoder modifies an i.i.d. finite-alphabet cover under a distortion budget; the warden may apply an unknown discrete memoryless channel under another budget. The receiver has the key but not the original cover. Perfect security equates full cover/stegotext block distributions. Shared randomized permutations help enforce it; their key entropy grows with block length. The paper characterizes asymptotic capacity and achievable error exponents, including the passive special case.

This already addresses reliable hidden communication under constrained interference. Its main attack model is not arbitrary insertion/deletion, adaptive semantic rewriting or preservation of software-task correctness. We inspected definitions, the capacity statement and key/passive sections, not all converse/achievability proofs. Translating a task's utility into its distortion function is substantive work, not an automatic application.

## Newer results that constrain our proposals

### Codetta: asymmetry and keyless setup, with substantial qualifications

[arXiv 2609.28900v2, §§3, 6.1, 7, 9](https://arxiv.org/html/2609.28900v2).

Different private sender models/contexts are allowed. A public draft model estimates the channel; coupling plus adaptive ECC enables keyed delivery. Keyless setup uses MLWE-based machinery and candidate-block pools. Security assumes a passive computational auditor, fresh session identifiers and matching public transcript. Sender-state evolution must not directly depend on the hidden payload beyond token selection.

Crucially, §7.1's 100,000 key-exchange trials **algebraically replay** measured displacement distributions; they are not 100,000 live end-to-end exchanges. Bounds are conditional on that measurement model. Approximately 80k published tokens exclude private sampling: §7.4 mentions 13,316 candidates per published block in its comparison. §9 explicitly proposes perturbation and verifiable sampling, and leaves defense evaluation open. No author implementation was verified in this pass. Do not claim autonomous protocol discovery or live setup reproduction.

### BAM: feedback can replace receiver knowledge of model probabilities

[Feedback Coding Enables Inference-Time Covert Agentic Communication, arXiv v1, §§3, 5, 7 and Appendix A](https://arxiv.org/abs/2609.24994v1); [author demonstration](https://github.com/infotheorylab/Covert_Chess).

BAM combines posterior matching with decode/confirm feedback. The sender controls inference-time sampling; the receiver knows tokenization and protocol secrets, not the sender's probability distribution. Both see the same token prefix. Cryptographic security and measured reliability are distinct; the reported near-zero error for small payloads is an empirical result. An “active API adversary” may choose inputs, but rewriting the delivered transcript is expressly excluded. The demonstration README also acknowledges decoding errors and does not simulate every multi-agent scenario. Source implementation/proofs were not audited here.

### Alkaid: edits do not automatically erase secure steganography

[arXiv 2603.06169v1, §§II–V, Theorems 1–3 and Appendix A](https://arxiv.org/html/2603.06169v1).

Alkaid samples a codebook, groups nearby codewords and uses minimum-distance decoding. The receiver regenerates codebooks using the shared model/history/seed and repairs alignment. Separation supports correction of fewer than half the relevant minimum distance; its probability bound uses a specified independent random-edit channel. Perfect-security analysis assumes message probabilities proportional to group sizes; the PRG implementation claim is computational. These conditions require scrutiny before asserting arbitrary chosen-message or multi-session security. Experiments report resilience to random edits with candidate-sampling overhead. This is a necessary robust baseline; it is not guaranteed to survive arbitrary semantic rewriting. No code execution or full proof audit was done.

### Finite-precision detection: our proposed gap is already partly studied

[Cao, Wang & Hu, ACL Findings 2026, §§3–5 and Limitations](https://aclanthology.org/2026.findings-acl.1013/).

Low-Probability Vanishing targets tail loss from finite-precision interval coding. The detector reconstructs sampling statistics using a matched model, tokenizer and policy. Main detection experiments concern AC and Meteor, with other schemes included in broader comparisons. Precision and sample length matter; a teacher-forced pass adds audit cost. The limitations explicitly reject transfer to arbitrary mismatched systems or a universal detector. Thus “finite precision can expose theoretically secure text” is already occupied territory. A stronger follow-up must establish a different leakage mechanism, a more realistic auditor, or a prevention result with measured utility. This does not invalidate an exact-arithmetic theorem.

### ANStega: another capacity/efficiency construction with explicit fragility

[NDSS 2026, §§VI–VIII](https://www.ndss-symposium.org/wp-content/uploads/2026-f605-paper.pdf); [artifact](https://zenodo.org/records/17943483).

ANS-based state updates and cryptographic masking pursue near-entropy embedding with small coding overhead. Constant-time coding updates must not be confused with constant-time LLM inference. The limitations explicitly require exact reception, strict model/sampling synchronization and seed setup, and acknowledge cross-hardware numerical issues. These make it relevant to a practical-barriers comparison, not evidence of a universal weakness. The artifact archive and Apache-2.0 metadata were retrieved, but its implementation was not inspected or run in this pass.

## Earlier foundations and defenses

- [Hopper–Langford–von Ahn, 2002](https://eprint.iacr.org/2002/137.pdf): computational steganography from cryptographic assumptions and channel access. Discovery-level check in this pass; exact entropy/channel conditions need a separate proof-level reading.
- [Dedić et al., author page / full paper](https://www.cs.bu.edu/~reyzin/bbstego.html): black-box sampling lower bounds exponential in embedding rate, with matching constructions and a high-entropy stateless variant. The lower bound concerns a specified sampling-access model, not all model-aware encoders. Author abstract checked; full proof not reviewed.
- [Backes–Cachin](https://eprint.iacr.org/2003/231.pdf): public-key security under adaptive chosen-covertext attacks. This security notion must not be equated with guaranteed delivery after arbitrary rewriting. Discovery-level check only.
- [Christ–Gunn–Zamir, COLT 2024, §§3–5](https://proceedings.mlr.press/v247/christ24a.html): keyed watermarking, entropy-conditioned substring detection and a removal theorem for prefix-specifiable models. A watermark detector is not a general payload decoder. The removal oracle/interface assumptions are material.
- [Liao et al., USENIX Security 2025, §§2, 5](https://www.usenix.org/system/files/conference/usenixsecurity25/sec25cycle1-prepub-856-liao.pdf): a shared-distribution framework separating uniform-channel encoding from distribution recombination. Optimal capacity/complexity results are qualified by that framework; it is not an asymmetric or general edit-resilient construction. Only targeted sections read; artifact not inspected.
- [Roger–Greenblatt, v2, §§5–7](https://arxiv.org/abs/2310.18512v2): paraphrasing/standardization already evaluated as defenses. They explicitly discuss hard-to-replace semantic choices and code understanding. Their bounded tasks/encoders cannot establish universal erasure.
- [Sentence embedding / global resynchronization, 2609.04970, §§3–4](https://arxiv.org/abs/2609.04970): requires a common corpus, embedding model, key and coding identifiers. Semantic-space symbols and LT coding limit bit-slippage. Its empirical resistance to steganalysis is not a proof of exact distribution matching. Threat/setup and evaluation overview inspected; not a full proof audit.
- [Conceptual Steganography, 2605.26537, §4.9 and Limitations](https://arxiv.org/abs/2605.26537): instructed reasoning-behavior codebooks survive ordinary paraphrasing; a strategy-aware paraphraser impairs the tested channel. Coverage of this targeted defense is limited to one strategy/dataset and three models. This directly occupies “semantic choices survive paraphrasing”; it does not prove theoretical undetectability.

## What remains unverified

No full cryptographic proof audit, fresh model reproduction, cross-hardware failure measurements or adaptive defense experiment was performed. Most checks are targeted readings of definitions, mechanisms, evaluation and limitations. Retrieval of a full PDF is not evidence of reading every page. The survey and curated bibliography were discovery aids, not substitutes for primary evidence. Published Zamir/TMLR text was inaccessible; additional robust watermarking, pseudorandom codes, ARS, Pulsar and Discop deserve further targeted review before claiming novelty in their neighborhoods.

The review establishes concrete prior-art constraints. It does **not** establish that a particular anti-steganographic proposal is novel. See [revised candidates](practical-barrier-candidates.md) for falsifiable directions that remain worth comparing.
