# Prior art: physical confinement and constrained interaction

2026-10-24. Owner asked whether physical environments could prevent steganography and requested prior art in both directions. This review covers (1) hardware/OS isolation, including physically embodied robots as a separate subcase, and (2) mediated protocols that retain a specified useful task. Targeted reading, not a complete proof audit or system reproduction. No project selected or experiment run.

## Assessment

Both directions have established, concrete results. **A controlled substrate can remove modeled channels; a constrained protocol can remove extra communication introduced by implementing a task.** Neither establishes that arbitrary interacting agents in an unrestricted physical world cannot signal. The useful question is which information flows and observations are allowed, which substrate/interface enforces that boundary, and what remains outside the guarantee.

Three distinct objectives must remain separate:

1. No communication between isolated agents.
2. No extra communication beyond the prescribed task's inputs, outputs and permitted interactions.
3. No harmful coordinated behavior.

The second permits legitimate information flow. Neither the first nor second rules out all previously agreed strategies or malicious actions. A system can also bound leakage without making it zero.

## Direction 1: physical/hardware/OS environments

### Deterministic compute environments

[Aviram et al., Determinating Timing Channels in Compute Clouds, 2010](https://arxiv.org/abs/1003.5303), primary abstract and design/conclusion overview.

Provider-enforced determinism prevents internal execution timing from changing a computation's results. The stated exceptions include explicit timing inputs and total computation duration. This addresses a class of timing channels without enumerating encoders; it is not universal content-channel prevention. The provider must enforce the environment, not merely ask application code to behave deterministically. A fixed random seed in an agent harness does not supply that guarantee. The proposed application boundary and permitted I/O are part of the claim.

[Wu & Ford, Deterland, 2015](https://dedis.cs.yale.edu/cloud/papers/trios15-deterland.pdf), abstract, §§2–3 and mitigation overview.

A prototype hypervisor gives guest code a deterministic view of time and paces I/O. It aims to eliminate internal timing channels within a mitigation domain while rate-limiting external timing leakage, with tunable performance cost. Running legacy OSes/applications is an implementation contribution. External timing bounds are not zero leakage, and neither the hypervisor nor pacing removes message-content choices. This is strong prior art for a timing-blind agent execution substrate; merely implementing fixed ticks is not new.

### Time protection and hardware-software contracts

[Ge et al., Time Protection: The Missing OS Abstraction, EuroSys 2019](https://yuval.yarom.org/pdfs/GeYCH19.pdf), threat scenarios, mechanisms, evaluation and hardware-contract discussion.

seL4-based protection partitions concurrently shared state and flushes time-shared microarchitectural state; it also addresses kernel sharing, interrupts and variable flush latency. The confinement scenario requires single-domain execution across cores or single-core execution to avoid unpartitioned interconnect channels. Simultaneous multithreading has restrictions. Thus the result must not be summarized as arbitrary co-resident malicious VMs being unable to communicate. Experiments demonstrate specified channel mitigation under these assumptions; functional OS correctness alone does not establish timing noninterference.

[Sison et al., FM 2023](https://trustworthy.systems/publications/papers/Sison_BMKH_23.abstract) formalizes observer-relative nonleakage and proves a generic OS model. Abstract inspected, proofs not audited. The [current author project page](https://trustworthy.systems/projects/timeprotection/) distinguishes implemented mechanisms, hardware support and ongoing complete-system verification. A generic model proof is not certification of every commodity CPU or inference deployment.

### Air gaps and automatic channel discovery

[Guri et al., BitWhisper, 2015](https://arxiv.org/abs/1503.07919v1): adjacent compromised computers signal through heat and thermal sensors; the reported bandwidth is small but nonzero. Abstract/setup overview inspected, no reproduction. This establishes that disconnecting a network does not itself eliminate all physical communication. It does not establish that arbitrary LLM agents autonomously discover or can access such a channel.

[Orenes-Vera et al., AutoCC, MICRO 2023](https://cris.unibo.it/retrieve/0dcfd3b5-3b55-432d-a48f-e33ef5a197dc/AutoCC.pdf) uses formal property verification at RTL to find state persisting across context switches and produce encoding/recovery traces. Primary abstract inspected. It finds known and unknown channels in the evaluated hardware designs; its scope is the formal model, not all physical emissions. “Use automated agents to discover unforeseen hardware channels” therefore needs comparison with existing automated discovery, not just manual attacks.

## Physical embodiment: robots do not automatically close channels

[Chang, Lin & Echizen, Cyber-Physical Steganography in Robotic Motion Control](https://globals.ieice.org/en_transactions/information/10.1587/transinf.2025MUP0001/_f), problem/method and experimental setup.

Environmental stimuli affect a robot's actions while it performs manipulation tasks; a receiver decodes from motion. Evidence is a simulated proof of concept, not a guarantee for every real robot or autonomous colluder. Model integrity and small motion changes are constraints, not proof of distributional undetectability. Local PDF retrieval failed; publisher text and PDF passages were readable with the web tool.

[Chang, Amir, Flageat & Prorok, Remotely Detectable Keyed Communication through Motion, arXiv 2609.08920v1](https://arxiv.org/html/2609.08920v1), problem setting, real-robot results and Appendices A.14–A.15.

Encodes messages through temporally structured action noise; reports simulation and real-robot decoding. Task preservation is task-specific, with measurable costs in some environments. Noise and band-stop removal are already evaluated. A.15 expressly does not claim prohibitive removal cost and leaves structured adaptive cancellation and some other attacks unevaluated. Preserving a marginal action distribution does not by itself preserve every closed-loop outcome or prove an undetectable trajectory. This is direct prior art against both “physical motion cannot carry useful hidden messages” and “first test filtering of motion channels.”

### Related but different: trusted actuator controllers

[NASA, A Formal Verification Framework for Runtime Assurance, 2024](https://ntrs.nasa.gov/citations/20230017350) formalizes a Simplex-style trusted controller/monitor around an untrusted controller. Primary abstract/introduction inspected. Such work shows how to enforce a specified physical safety property, not covert-channel noninterference. Multiple safe trajectories may still encode information. A safety shield cannot be advertised as an anti-steganographic shield without a separate information-flow property and observer model.

## Direction 2: preserve a task while constraining communication

### Physically enabled collusion-free protocols

[Lepinski, Micali & shelat, Collusion-Free Protocols, STOC 2005](https://shelat.khoury.northeastern.edu/dl/CollusionFreeSTOC.pdf), ideal/real explanation, Theorems 1–4 and physical-channel remark.

For finite partial-information games with publicly observable actions, the construction uses idealized physical envelopes plus trapdoor permutations. Setup and later protocol execution play different roles. It aims to avoid extra coordination enabled by the implementation relative to the ideal game. The paper explicitly excludes other physical signaling—timing, gestures and similar avenues must be closed separately. Ideal hiding/binding envelopes and absence of extra channels are assumptions, not a demonstrated sealed room. This is direct physical-assumption prior art, and does not prove that real-world confinement is easy or that game-intrinsic signaling vanishes.

### Digital mediation instead of ideal physical envelopes

[Alwen, shelat & Visconti, CRYPTO 2008](https://crypto.ethz.ch/publications/files/AlShVi08.pdf), introduction, mediator model and security discussion.

All communication passes through a mediator that filters/rerandomizes protocol messages. This is protocol-specific, not arbitrary prose paraphrasing. An honest mediator supplies collusion-freeness; dishonest-mediator security is separately defined, with setup/broadcast-honesty qualifications in the inspected version. The authors explicitly discuss timing, marks and even temperature as problems for implementing envelope-based channels. Thus a trusted communication broker removing extra entropy is already an established approach.

[Alwen et al., Collusion-Free Multiparty Computation in the Mediated Model, CRYPTO 2009](https://crypto.ethz.ch/publications/files/AKLPSV09.pdf), §§1.1–1.2 and model overview.

Extends the setting to general multiparty functionalities. A mediator participates in secure computations, distributes independent commitments and substitutes defaults on invalid/aborted steps. Its definition permits a single bit indicating that some abort occurred, while hiding who/when; the preceding model permits more abort leakage. Setup alternatives have different assumptions. This is a conditional protocol result, not absolute zero information flow. “General functionality” also does not make a cheap drop-in wrapper for unrestricted LLM conversations. Definitions/construction overview inspected; full simulation proofs not audited.

### Other relevant protocol constraints already reviewed

The [semantic-erasure review](semantic-erasure.md) records steganography-free zero knowledge with honest preprocessing, computationally unique proof transcripts and reverse firewalls. Those are additional positive results for precisely designed protocols, not universal filters for arbitrary agent output. They must be included before claiming novelty for pre-creation prevention, fixed randomness or trusted rerandomization.

## Comparison of the two directions

| Approach | What it controls | What remains to address |
| --- | --- | --- |
| Dedicated/partitioned execution | Shared memory, resource state and selected observations | Physical emissions, external services, permitted outputs |
| Deterministic timing substrate | Internal timing observations; external timing may be bounded | Explicit inputs, output content and total duration/mitigation exceptions |
| Restricted robot actuation | Motions reachable under a controller | Task-valid trajectory choices and environmental observations |
| Collusion-free mediated protocol | Extra communication beyond an ideal functionality | Honest mediator/setup, abort exceptions, bypass channels and task-intrinsic signals |
| Generic safety controller | Specified physical safety constraints | Information hidden among safe actions |

These are complementary. A mathematically sound mediator can be bypassed through a shared cache. Perfect cache isolation still permits signaling through a free-form report. Neither individual result proves their composition secure; the complete receiver-visible view must be modeled.

## What a defensible follow-up would have to add

**Isolation candidate.** Evaluate a bounded agent execution interface with and without timing/state isolation. Hypothesis: a specified known-good resource channel loses decoding power under the intervention while legitimate task success persists. Controls: a functioning encoder/decoder, allowed explicit-channel control, disconnected control, and matched task workload. Include timeout/retry/status observations. A null with a failed positive control says nothing about isolation. Hardware validation requires controllable local resources; hosted model APIs do not expose or certify the provider's hardware isolation. A harness simulation can test an interface, not prove commodity-hardware security. Novelty beyond deterministic VMs/time protection/AutoCC is currently unverified.

**Mediation candidate.** Define one useful ideal task and all authorized outputs; compare a transparent relay with a trusted broker whose releases depend only on authorized task information and independent randomness. Hypothesis: extra randomized private payload transfer decreases under mediation without general task impairment. Controls: honest agents, instructed colluders, retained semantic-choice encoder, explicit legitimate information, and abort/retry signaling. Measure surviving payload/partial information and utility, not only a fixed decoder's errors. The informative negative is a task-valid choice that still conveys payload. The existing assignment prototype already illustrates this limitation; repeating it is not new. A full cryptographic MPC implementation is too large as routine sprint infrastructure.

**Embodied candidate.** A physical simulator can compare known motion encoders with task-preserving actuator mediation and measure utility/recovery. Neither a new motion channel nor additive noise/notch filtering is novel on the sources above. A specific stronger cancellation method might be an extension, but the paper's future-work list is not proof that no one has done it. Real robots would add calibration and hardware costs without automatically strengthening the scientific question.

For all three, begin with a precise novelty delta and working baseline. No compute/inference budget, task family, hardware platform or full study has been selected. Fresh local feasibility work is possible later; this note launches none.

## Conclusion for the owner's proposal

The useful form of the idea is an **enforced observation-and-interaction boundary with a stated leakage guarantee**. Physical separation can help implement it; physical embodiment alone can increase signaling opportunities. Prior art supports prevention and bounded-leakage results under explicit assumptions, while undermining a broad novelty claim for “physically isolate agents” or “put a trusted mediator between them.”

[Source ledger](../references/isolation-prior-art-sources.json) records versions, hashes, inspected scope and retrieval limitations. No third-party source is vendored and no deployment or experiment was performed.
