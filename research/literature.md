# Living literature review

Initial primary-source review, accessed 2026-10-24. This is a selective landscape, not an exhaustive review of the starter's 234 entries. No novelty claim has been established. Paper results below are author-reported, not reproduced here. Abstract-only readings are marked. Code observations are separate in [starter-map.md](starter-map.md).

## 1. Tool-use capability versus secure implementation versus choice

**Rippin et al., [Tool Use Enables Undetectable Steganography in Multi-Agent LLM Systems](https://arxiv.org/html/2606.28425v1), v1.** Inspected §§3–4, Appendix A, prompts, Appendix D/Table 1, code-availability statement.

Question: can tool-using agents implement stegosystems and independently select compatible plans? Threat model: cooperating keyed receiver; output-only monitor excludes tool activity/intermediate artifacts; encoder can execute code, access sampling probabilities, files, and papers/search.

Evidence: instructed Opus 4.6 construction; default 4/6 successes. Appendix D qualifies the headline: the coupling implementation lost perfect security through bugs; the implementation missed by a code-review monitor lacked information-theoretic undetectability. Prompt injection failed in 2/2 trials. Small samples and edge-case bugs limit inference.

Coordination: 100 plans per model/condition in a 2×2×2 prompt design; no tools; LLM categorization. CCI approximates compatibility by multiplying parameter-match terms. Undetectability-required cells had zero estimated CCI; this is not an impossibility result. Plan matching is not executed interoperability or spontaneous harmful collusion. The implementation/coordination/harm factorization assumes independence, rather than demonstrating it.

Security foundations are imported from prior work. Follow-up: execute independently built encoder/decoder pairs and manipulate shared artifacts.

Code: paper claims supplementary implementation setup and coordination code; no directly accessible author release verified. Do not substitute unrelated steganography code and call it a reproduction.

## 2. What the relevant security guarantees actually require

**Schroeder de Witt et al., [Perfectly Secure Steganography Using Minimum Entropy Coupling](https://arxiv.org/html/2210.14889v4), v4, ICLR 2023.** Inspected §2 and Theorems 1–2.

Question: characterize perfectly secure encoders and maximize their information throughput. In Cachin's passive-observer model, perfect security means equality of cover and stegotext distributions (zero KL divergence). An encoding procedure is secure iff induced by a coupling with the required marginals; minimum-entropy coupling maximizes mutual information among those encoders.

The construction uses a shared private key, random source, and specified cover/message distributions; the outlined encryption induces uniform ciphertext. Exact preservation concerns the chosen cover law. Experiments use GPT-2, WaveRNN, and Image Transformer. Neither arbitrary agent implementation bugs nor a mismatch between model cover and real task behavior inherits the theorem. This is not a result about whether agents choose collusion or about an auditor observing their tools.

Follow-up: measure implementation fidelity and distribution mismatch separately from communication reliability. Do not infer perfect security from round-trip decoding tests.

**Zamir, [Undetectable Steganography for Language Models](https://openreview.net/forum?id=fq6aQoMSHz), TMLR 2024.** OpenReview was blocked by browser verification. Read the author-linked [arXiv v1](https://arxiv.org/html/2401.10360v1), titled *Excuse me, sir? Your language model is leaking (information)*, §§2, 6–8; this is not a verified comparison with the final TMLR text. Author links [code](https://github.com/OrZamir/steg) from [his publication list](https://zamir.prof/).

Threat: an unkeyed polynomial-time distinguisher with model access and adaptive queries. Guarantee relies on pseudorandom functions and controlled sampling from next-token probabilities. Distinguish single-query Lemma 6.1 from multi-query Theorem 6.4, which adds randomized-prefix handling to prevent repeated PRF inputs. Retrieval requires sufficient distributed empirical entropy; the general construction spends O(security-parameter) entropy before payload transmission. Decoder uses key and output. Empirical examples include GPT-2 and Llama 2. Editing robustness is largely left open.

Follow-up: operational costs under short outputs or restricted sampling access. A hosted chat completion API is not automatically the needed sampling interface.

**Vaikuntanathan & Zamir, [Undetectable Conversations Between AI Agents via Pseudorandom Noise-Resilient Key Exchange](https://arxiv.org/html/2604.04757v1), v1.** Inspected introduction/results overview, model definitions, shared-key construction, keyless construction overview.

Question: can an honest-looking interactive transcript carry a parallel covert conversation without an initial shared secret? The passive computational auditor can know model descriptions, protocol, and private contexts. Shared-key construction uses an interaction-unique key; keyless results introduce pseudorandom noise-resilient key exchange, with cryptographic hardness and sufficient message entropy. The low-entropy construction tolerates constant decoding noise when sufficiently many messages have constant min-entropy; details depend on the chosen construction and assumptions. This is a theoretical construction, not evidence of spontaneous model adoption or a low-overhead deployed system.

Implication: absent pre-shared keys is not a universal defense. Practical overhead, access to distributions/sampling, agreement on the protocol, and active channel modification remain distinct empirical questions. Do not equate constant-noise resilience with resilience to arbitrary semantic rewriting.

## 3. Behavioral emergence and adoption are already active research areas

**Zeng & Rudzicz, [Voluntary Collusion with Secret Tools in Competing LLM Agents](https://arxiv.org/html/2605.27593v2), v2.** Inspected adoption protocol, empirical design, limitations, Appendices A and G; [author code](https://github.com/AgentSafety2025/LLM-Agent-collusion).

Question: will agents accept an offered unfair secret capability? The protocol separates acceptance, partner choice, partner consent, and gameplay. Twelve models receive offers; gameplay scope is smaller, in Liar's Bar/Cleanup. These are expressly offered secret tools, not independent discovery of a hidden encoding channel. Acceptance is not use or demonstrated harm.

The updated Appendix A already crosses observation cues and tests post-adoption concealment under record access and penalties. Appendix G supplies neutrally framed benign-tool controls. Thus offer wording, monitoring notices, and denial of prior adoption are substantially occupied territory. Simulated reporting does not establish successful evasion of deployed monitoring or hidden intent.

Follow-up: discoverability without an offered alliance, verification of subsequent tool use, and causal third-party harm in operational workflows. Re-read the complete latest design before claiming any intervention is new.

**Mathew et al., [Hidden in Plain Text: Emergence & Mitigation of Steganographic Collusion in LLMs](https://arxiv.org/html/2410.03768v2), v2, IJCNLP-AACL 2025.** Inspected introduction, methods overview and mitigation results; [code repository](https://github.com/olliematthews/lasr-steganography), whose README links this paper.

Question: can optimization elicit covert signaling, including under misspecified incentives, and do oversight/paraphrasing prevent it? Gradient-based and in-context reinforcement-learning procedures optimize sender/receiver behavior in controlled tasks. Learned communication can survive tested mitigations. This occupies “steganography emerges under incentives” broadly; it does not establish the rate of independent discovery by untrained deployment agents in ordinary workflows. Mitigation failure is empirical and scheme/task dependent.

Follow-up: distinguish training/search-induced emergence from deployment-time exploration; test operational action channels and substitution with matched utility controls rather than merely another paraphraser.

## 4. Outcomes and causal evidence

**Nakamura et al., [Colosseum: Auditing Collusion in Cooperative Multi-Agent Systems](https://arxiv.org/html/2602.15198v1), v1.** Inspected formulation, experimental settings, §5.4, metrics/prompt appendices; [author repository](https://github.com/umass-ai-safety/colosseum).

Question: audit coalitions that improve subgroup objectives while degrading a cooperative task. DCOP environments give explicit objectives and counterfactual regret metrics. Jira/hospital tasks expose tools, private information, communication topologies, and optional secret blackboards. Both control agents with added private channels and explicitly prompted coalitions are studied. Therefore “private channels cause workplace coalition advantage” is not a fresh demonstration.

Action/regret metrics and transcript judges can disagree. This supports examining outcomes, but an advantaged subset alone does not establish communication-mediated harmful agreement: heterogeneous skills, topology, and action order can also create advantages. These are our identification concerns, not claims that the framework provides no value.

Follow-up: randomized interventions preserving task semantics, with causal information-transfer and harm measurements. Avoid treating a no-secret-channel condition as no communication when public posts/actions remain observable.

**Bonjour et al., [Information-Theoretic Approach to Detect Collusion in Multi-Agent Games](https://proceedings.mlr.press/v180/bonjour22a.html), UAI 2022.** Read paper introduction and §3, including [PDF](https://proceedings.mlr.press/v180/bonjour22a/bonjour22a.pdf).

Question: infer colluding pairs from state/action records, without decoding their messages. Conditional mutual information motivates individual influence and pairwise net influence. Evaluation includes rule-based and learned strategies in iterated rock–paper–scissors and Leduc poker. Scope assumes exactly two colluders and more than two players; estimating empirical policy matrices requires repeated coverage of state/action combinations. This is not a general causal-identification theorem for correlated LLM actions. Shared observations and badly represented state are important confounders when porting the statistic.

Follow-up: compare state-conditioned dependence against randomized channel interventions, using benign coordination and common-cause controls. Merely proposing MI on actions is already established.

**Tailor, [Audit the Whisper: Detecting Steganographic Collusion in Multi-Agent LLMs](https://arxiv.org/html/2510.04303v1), v1.** Read threat model, capacity/power argument, experiment and limitation sections; [author code](https://github.com/Ostailor/Steganographic_Collusion).

Question: combine interventions and calibrated detectors against configured covert schemes in pricing, auctions, and peer review. Adversaries share a blueprint; auditor sees transcripts/outcomes and can intervene or replay. The power bound depends on achieved rate, intervention penalty, calibrated threshold, bounded statistics and concentration conditions. It is not universal detection of arbitrary secure channels. Reported benchmark performance is tied to those policies and null distributions.

Follow-up: test adaptive held-out carriers and null-distribution shift. The shipped code requires independent inspection before reuse (see starter map). Our statistical caution: zero false positives in 200 independent null trials gives about a 1.49% one-sided 95% upper bound, not empirical validation of FPR ≤0.1%. That calculation does not itself refute a separate theorem under additional assumptions.

## 5. Nearby results that constrain novelty and infrastructure choices

These entries have **abstract-level review only**, unless stated otherwise; do not rely on them for exact experimental reproduction.

| Source | Already studied | Limit / implication for our ideas |
| --- | --- | --- |
| Radev et al., [The Best-Laid SCHEMEs](https://arxiv.org/abs/2605.29178v1) | Multi-agent code sabotage requiring complementary actions; monitoring edits alone versus edits plus communication; monitoring-awareness prompts | Instructed covert side tasks. A generic “hybrid action/text monitor” is insufficiently differentiated. Potential overlap must be checked in full before selecting a coding-workflow study. |
| Rose et al., [Detecting Multi-Agent Collusion Through Multi-Agent Interpretability](https://arxiv.org/abs/2604.01151v5), updated Oct 15 | HELIOS uses per-agent activation probes and group-level tests; evaluates instructed and emergent settings, with partial transfer | Internal activations add a monitoring surface beyond transcripts; needs open weights, unlike initial API-only plans. No universal best statistic claimed. |
| Jiralerspong et al., [Noticing the Watcher](https://arxiv.org/abs/2603.16928v1) | Single-agent inference of hidden CoT monitoring from blocking feedback; evasion intent did not translate into successful concealment in reported cases | Motivation for adaptation studies, not evidence that multi-agent carrier switching happens. |
| Agrawal et al., [Evaluating LLM Agent Collusion in Double Auctions](https://arxiv.org/abs/2507.01413v1) | Seller communication, model choice, oversight and urgency change collusive outcomes | Keeps market intervention studies viable, but basic communication-on/off or pressure studies are replications. [Code](https://github.com/andyjliu/llm-agent-collusion). |

The starter additionally links Fish pricing, Lin market division, Aharon focal points, LLMCartel and trust-breaking work. Their harnesses are mapped in the starter inventory; their full papers have not been audited here. The literature CSV is a search index, not verified evidence: its own README says summaries were LLM-drafted and incompletely checked.

## 6. Research conclusions we may defend now

- Separate the monitor's information boundary from the carrier. An output-only theorem says nothing automatic about file provenance, tool execution traces, network restrictions, or downstream losses.
- Specify the cover distribution. Security relative to a freely sampled model does not automatically preserve task-conditioned operational behavior.
- Keep statistical dependence, information transfer, policy violation, outsider harm, and deliberate agreement separate. None alone identifies all the others.
- Capacity, choice, interoperability, harm, and adaptive persistence require separate measurements and denominators. Pre-register which step the study addresses.
- Candidate gaps below are provisional. An experiment may be useful as a careful replication or methodological stress test without being a novel communication mechanism.
