# Synchronization, numerical determinism and optimality

2026-10-24. Owner questioned whether a receiver can reproduce model probabilities given nondeterministic LLM outputs, expressed interest in breaking synchronization, and asked whether iMEC is the only theoretically optimal scheme. No additional experiment was run for this question.

## What must be reproduced?

An ideal fixed autoregressive model maps an exact token prefix to a next-token probability vector. A separate sampling procedure selects a token. Different samples from the same vector do not imply different vectors. The iMEC receiver recomputes the vector and coupling/posterior updates for the sender's observed tokens; it does not independently sample a continuation and hope it matches.

Actual inference can also have numerical nondeterminism. [PyTorch's reproducibility documentation](https://docs.pytorch.org/docs/2.14/notes/randomness.html) explicitly does not guarantee complete reproducibility across releases/platforms or CPU/GPU even with identical seeds. Review: reproducibility notes. Bitwise agreement across arbitrary hosted endpoints is not established by model-name equality or temperature zero.

The inspected reference harness is a local known-model/token-ID setting. Real deployments must match weights, tokenization and exact token history, prompts/templates, sampling transformations, numerical implementation, block/framing conventions, key material and nonce handling as required by the selected scheme. Some differences can be tolerated; failure thresholds need measurement rather than assertion. Idempotence (`f(f(x)) = f(x)`) is a different mathematical property from repeated-call reproducibility.

## iMEC's theorem versus its implementation

[Schroeder de Witt et al., §4 and §5.1](https://arxiv.org/html/2210.14889v4) explicitly use approximate MEC subroutines within iMEC. The coupling theorem identifies the information-efficient optimum in its model, but the practical iterative/greedy implementation is not thereby proven globally optimal for every input. Distribution preservation, payload recovery and throughput optimization are separate properties. Finite-length/numerical behavior must be assessed separately.

## Other schemes relevant to evaluating a defense

| Source | What it contributes | What must not be conflated |
| --- | --- | --- |
| [Zamir, arXiv v1, §2.4 and §6–8](https://arxiv.org/html/2401.10360v1) | Computationally undetectable keyed sampling; linear-order payload retrieval under entropy assumptions; discusses substring/restart adaptation and leaves broad editing robustness open | Not the same exact information-theoretic throughput objective as MEC; not general editing immunity |
| [SparSamp, USENIX Security 2025, §3.4](https://www.usenix.org/system/files/usenixsecurity25-wang-yaofei.pdf) | Sparse sampling with distribution-preserving security claims and empirical efficiency; explicitly shares model, context and PRNG seed | Security and fast embedding do not establish exact global rate optimality or synchronization robustness |
| [Shimmer, USENIX Security 2025](https://www.usenix.org/system/files/usenixsecurity25-bai-minhao.pdf) | Entropy-collecting construction; discusses asymptotic optimality of utilized information and finite residual loss | “Asymptotically optimal” needs its stated setting; not synonymous with every finite output reaching capacity |
| [Wang & Moulin, 2007, v3](https://arxiv.org/abs/cs/0702161) | Earlier perfectly secure steganographic capacity/code-construction work under an i.i.d. cover setting | Different channel/attack assumptions; not a ready LLM implementation |
| [Vaikuntanathan & Zamir, v1](https://arxiv.org/html/2604.04757v1) | Interactive covert conversation and key establishment; shared-key entropy rate up to constant factors, separate keyless construction | Receiver need not know the sender's private next-message distribution in the keyless construction; a model-probability mismatch intervention is not automatically universal |

Review depth for new sources: SparSamp abstract/method overview/shared settings; Shimmer abstract and targeted optimality passage; Wang–Moulin abstract. No full proof audit or code reproduction for these alternatives.

## Candidate synchronization study

Separate interventions on (a) delivered tokens or framing, (b) receiver model/probability calculations, and (c) shared state/key/nonce alignment. Hold sender behavior fixed initially to establish mechanisms, then allow repair/adaptation as a distinct evaluation.

Measure exact payload recovery, bit error rate, synchronization recovery time, rejection/abort rates, communication cost and legitimate task utility. One altered token can affect both the posterior and subsequent context; its effect is a hypothesis to test, not an automatic permanent failure. Use error-correction, chunking or restart/repetition variants as stronger adversarial controls where available.

A positive result would establish disruption for a specified scheme and observation interface. It would not defeat distributional security theorems, or channels that bypass the transformed surface. Controlled model drift is a possible resource restriction; changing all production model instances might be impractical and expensive. A sender could choose a shared auxiliary model instead if allowed, so the experimental boundary matters.
