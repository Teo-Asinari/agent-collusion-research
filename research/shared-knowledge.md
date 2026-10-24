# Does steganography require common private knowledge?

Primary-source check, 2026-10-24. **No universal requirement for a pre-shared secret exists.** Public-key and covert-key-exchange constructions already provide counterexamples. This is a targeted classification, not an exhaustive survey of all steganography. The findings do not select an experiment.

## Distinctions

- **Shared public protocol:** compatible encoding/decoding rules, interfaces, models or parameters. These need not be concealed from an auditor.
- **Pre-shared secret:** private key material or another hidden resource already known to both endpoints before communication starts.
- **Individual private information:** a receiver's private key or each party's independent random choices. This is not common private knowledge at initialization.
- **Acquired common information:** a secret or convention established during interaction or joint training. Its origin and observer access matter.
- **Empirical decoder advantage:** a receiver succeeds more often than the tested monitor. This need not satisfy a formal security definition against an equally informed adversary.

Do not equate recovering payload bits with detecting that a payload was intentionally sent. A public decoder can also map ordinary outputs to arbitrary bits. Conversely, concealing intentional transmission does not automatically keep recovered bits confidential. Specify the adversary, payload distribution and security experiment.

## Source checks

### Minimum-entropy coupling — pre-shared key in the specified construction

[Schroeder de Witt et al., v4, §2.1](https://arxiv.org/html/2210.14889v4): the key is explicitly shared over a secure channel before the steganographic process. Cover distribution is known to sender, receiver and adversary. The outlined encryption makes ciphertext uniform regardless of plaintext distribution. The coupling characterization concerns distribution-preserving encoding; it does not itself solve key establishment. Review: §2.1 and methodological outline. No experiment reproduced.

### Zamir — short shared cryptographic key

[Zamir, arXiv v1, §2.4 and §6](https://arxiv.org/html/2401.10360v1): Setup generates a key used by encoder and receiver; security is against an unkeyed computational observer. PRF-based constructions do not require a newly provisioned one-time-pad bit for each payload bit. Repeated-query safety still requires the specified prefix/state handling. This differs from the pedagogical toy example. Review: definitions and scheme/security sections. Final TMLR version remains unverified because OpenReview access was blocked.

### Public-key steganography — no pre-shared secret

[von Ahn & Hopper, EUROCRYPT 2004, author-hosted paper](https://www.cs.cmu.edu/~hopper/public_key_steganography.pdf): SG produces a public/private key pair; the encoder uses the recipient's public key and a channel-sampling oracle, while decoding uses the recipient's private key. The sender does not possess that private key. The paper also constructs steganographic key exchange. Guarantees are computational and assumption-dependent. A usable public-key setup and compatible algorithms are required, not a common secret. Review: abstract, §4 definitions and §6.1 construction. No LLM-agent implementation assessed.

### Covert conversation/key exchange — independent secrets initially

[Vaikuntanathan & Zamir, v1, §2.6 and §5](https://arxiv.org/html/2604.04757v1): the model explicitly permits independent private information for Alice and Bob. Its keyless construction establishes a shared key through the honest-looking interaction, then supports covert conversation. Assumptions include compatible prescribed algorithms, private randomness, cryptographic hardness and suitable message entropy/sampling. It does not demonstrate autonomous protocol discovery by LLM agents. Review: definitions and construction overviews; no full proof audit or implementation reproduction.

### Learned LLM protocols — training can supply coordination

[Mathew et al., v2, §3.3 and Appendix A.2](https://arxiv.org/html/2410.03768v2): sender/receiver behavior is optimized through GBRL or ICRL. Centralized ICRL distributes strategies to both; decentralized ICRL has separate learners, with the receiver inferring a strategy from sender outputs/examples and feedback shaping subsequent iterations. A cryptographic key is not the universal coordination mechanism. These setups supply training/feedback and restricted observer access; they do not establish independent first-contact deployment coordination or universal undetectability. Review: methods and centralized/decentralized algorithms.

### Early LLM collusion evaluations — heterogeneous assumptions

[Motwani et al., v5, Appendices F–G and insider-trading case](https://arxiv.org/html/2402.07510v5): studies include protocol-choice prompts, shared passages or encoding instructions withheld from the overseer, and a case where a receiver can decode without the encoder's supplied codebook. Therefore it is inaccurate to describe all evaluations as one shared-key setup. Some explicitly grant private common information; others rely on inferable conventions or monitor limitations. These demonstrations do not establish cryptographic security against an equally informed observer. Review: targeted appendix/case sections, not full paper audit.

### Seed-recovery channel — shared implementation knowledge, not a secret seed beforehand

[Steganography Without Modification: Hidden Communication via LLM Seeds, v1, §3.1](https://arxiv.org/html/2606.09135v1): the payload is placed in the seed; the receiver recovers it by search. Assumptions include deterministic known sampling, model/probability access, known parameters, exact outputs, and a tractable seed space. Prompt-sharing can be relaxed in a tested setting. The paper assumes uniform payloads. The recoverable seed is the transmitted information, not a pre-shared key. Author-reported empirical recovery is not our reproduction.

**Our caution:** uniformly random seed selection and arbitrary message-controlled seed selection need not have the same distribution. The paper's broad “no distribution change” language should not be generalized beyond its assumptions; equal-access observers can attempt the same seed recovery. Review: communication model, empirical overview and security discussion; no code audit. [Author-linked code](https://github.com/UzL-ITS/Hidden-Communication-via-LLM-Seeds).

## Implications for our brainstorm

The question “can steganography work without a pre-shared secret?” is already answered affirmatively. “Can it work without *any* shared private knowledge at any point?” is different: public-key systems need not give sender and receiver the same private key, while covert key exchange creates shared private information during the exchange.

The assumption worth auditing is the **origin of receiver advantage**: supplied key, receiver-only key, acquired session key, trained strategy, private examples, public convention, asymmetric model access, or a weak monitor. For each experiment record the exact observer access to these resources.

The practical formation question remains open at a narrower level: can independently deployed agents choose and execute compatible constructions with the permitted resources, and what traces arise during that attempt? Neither public protocols nor a common base model automatically constitute a secret. Matching an algorithm name also does not establish interoperable keys or parameters.

Our earlier “courtship” proposal must not assume setup is necessarily detectable: covert-key-exchange theory can cover the setup transcript. Investigate implementation/behavioral failures under explicit constraints rather than announcing an impossibility result.
