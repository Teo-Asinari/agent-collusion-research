# Multi-agent lift and comparison with CaMeL and FIDES

2026-10-24, Approach A batch 3. Lean: `experiments/verified_arch/lean/Arch.lean`, namespace `Arch.Agents` (core Lean 4.35.0, no `sorry`, axiom `propext` only). This is a model of orchestration dataflow, not an implemented agent runtime. Novelty is not claimed.

## 1. What the two systems are and guarantee (primary sources)

Both PDFs were read on 2026-10-24 (text extracted locally). Only the sections named here were read; neither paper was audited in full.

**CaMeL**: Debenedetti, Shumailov, Fan, Hayes, Carlini, Fabian, Kern, Shi, Terzis, Tramèr. *Defeating Prompt Injections by Design*, [arXiv 2503.18813v2](https://arxiv.org/abs/2503.18813) (24 Jun 2025). Code: github.com/google-research/camel-prompt-injection (not inspected).
- §3 threat model: "The primary goal of CaMeL is to stop prompt injection attacks coming from untrusted data sources." A privileged LLM writes a program from the **trusted** user query; a quarantined LLM processes untrusted data without tool access. Capabilities on values gate tool calls. §8 extends this to rogue users and tools.
- §4: security is a game (PI-SEC) against an adversary who controls injected data. The abstract reports 77% of AgentDojo tasks "with provable security" (84% undefended). We found no mechanized proof.
- §7, "Side Channels Can Be a Problem", says CaMeL "is vulnerable to side-channel attacks." It gives three examples: an indirect dependency via loop count to an external resource (stopped by STRICT mode); a one-bit **exception** channel in which the quarantined LLM conditionally raises an error and the halt is observable (mitigated in STRICT mode by making later statements depend on Q-LLM inputs); and a **timing** channel (`time.sleep(private_variable)`, Fig. 16) that strips the private annotation.

**FIDES**: Costa, Köpf, Kolluri, Paverd, Russinovich, Salem, Tople, Wutschitz, Zanella-Béguelin (Microsoft). *Securing AI Agents with Information-Flow Control*, [arXiv 2505.23643v2](https://arxiv.org/abs/2505.23643) (3 Sep 2025). Code: github.com/microsoft/fides (not inspected).
- §2.1 threat model: "We assume that the agent's configuration is trusted, including the system message, tool descriptions, and **LLMs used by the agent**." The adversary controls tool-returned content (indirect prompt injection).
- §4.4 and Proposition 1: with policies P-T/P-F, the planner (Algorithm 5) "guarantees non-interference for the integrity of tool calls and data, and **explicit secrecy** for the confidentiality of data." Explicit secrecy "does not prevent implicit flows due to data-dependent control flow. An adversary that is able to see the sequence of tool calls may still be able to infer limited information" (§4.4). On egress policy (§4.3): it "does not attempt to hide whether data has been sent (which can itself reveal information)." The per-tool non-interference statement is not formalized ("We forgo a formalization of this statement, which is straightforward"). We did not find a mechanized proof.

## 2. Collusion channels: who closes what

Our threat model differs from both. Here the **LLM agents themselves are the adversary**: a sender holding payload m and a receiver may run any pre-agreed policy and share keys. In Lean every LLM and tool symbol is interpreted by an arbitrary `ι`, and pre-shared keys are receiver side information (`publicWeight` wires).

| Channel | CaMeL (sections read) | FIDES (sections read) | Our `WTa` rules (Lean) |
| --- | --- | --- | --- |
| Colluding / adversarial LLM | Outside the threat model: the P-LLM is trusted and the adversary is injected data | Outside: the LLMs are trusted configuration | **In scope.** Theorems quantify over every `ι` |
| Shared state (files, memory, tool results) | Capabilities track provenance and readers of values; tool-call policies gate flows | Labels propagate; explicit flows to lower readers blocked | **Closed.** State versions are wires; a write's label is the join of its inputs; the receiver may only read public wires (`chanFile` rejected) |
| Tool choice / control flow | Control flow fixed by the P-LLM from the trusted query. The Q-LLM still has an exception channel that leaks 1 bit (§7), mitigated in STRICT mode | **Open by design**: explicit secrecy allows implicit flows; the sequence of tool calls can leak | **Closed in the model.** Dispatch is an op labeled by what it reads; an observed tool choice made from private data is rejected (`chanTool`) |
| Timing / scheduling | **Open** (§7 timing example) | Not addressed in the sections read | **Closed for modeled timing.** A slot or completion time is a wire: an op output carries its dependencies' label (`chanTime` rejected), or it is a cost release whose spec reads only public data. Physical timing (CPU, cache, network) is **not modeled** |
| Private sampling randomness | Not treated as a channel in the sections read | Not treated (LLM is trusted) | **Closed.** Private tapes are private inputs, and no release spec may read them (`chanRand` rejected). `obs_factors`: the view depends only on public and authorized inputs, so it is payload-independent under any input distribution where those are independent of m. Only public randomness, equal across compared worlds, may feed releases |
| Adaptive receiver queries | No adversarial receiver | No adversarial receiver | **Modeled.** The receiver's LLM calls are public ops; release specs may read public computed wires, such as the adaptively chosen query (`orch`, wire 10→14) |
| Payload via authorized release itself | — | — | **Not closed** if the owner authorizes a function that the sender can influence, e.g. a sender-chosen query. Authorization is trusted |

## 3. What is proved in Lean (batch 3)

- `WTa`: the single-agent rules, plus one change: a release spec may read wires that are public in the current context or `authorized` inputs. `wt_to_wta` shows that every single-agent-accepted program is still accepted.
- `payload_nia`: for every `ι` (every LLM, tool and file-system semantics, colluding or not), two worlds agreeing on public inputs and authorized data give identical receiver views, whatever the sender's payload, private tape, private memory and private weights.
- `obs_factors`: the view is a function of the public/authorized projection of the inputs. This is the distributional reading for sampling.
- `orch`, `orch_wt`, `orch_payload_ni`: a concrete orchestration with a receiver LLM choosing a query adaptively, a sender LLM, a shared-file write, a slot-schedule cost release, a verified tool output (verify-or-recompute), and a receiver LLM reading tool result and schedule. Lean proves it well-typed and payload-noninterferent.
- Channel witnesses: shared file, tool choice, completion time and private-tape release each leak concretely under a summing interpretation, and each is rejected by `WTa`.

## 4. Honest limits

- **Utility.** Every receiver-visible value derived from private data must pass through a release with a proved contract. In `orch` the sender's candidate is accepted only if it equals the trusted tool's answer, so the sender adds no information and at most saves work. This is the batch-1 lesson again: values can be guaranteed for all policies, but useful LLM contributions are limited to checkable certificates. In practice this is far more restrictive than CaMeL or FIDES, which permit LLM-influenced outputs and accept implicit flows (FIDES) or side channels (CaMeL) for utility. Their AgentDojo utility results have no counterpart here.
- **Integrity / prompt injection** is not modeled. CaMeL and FIDES address it; we do not.
- **Timing** is covered only to the extent it is a modeled wire. The batch-1 analysis showed that real visible cost needs padding or a trusted learner.
- Deterministic semantics given tapes. The probabilistic statement is the factorization argument, not a measure-theoretic theorem in Lean.
- The Lean model is a hand abstraction of orchestration. No orchestrator implementation is verified against it.
