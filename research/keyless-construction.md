# Keyless construction: assumptions and implications

**Later-source update:** this note concerns Vaikuntanathan–Zamir specifically. [The expanded review](stego-prior-art.md) adds Codetta's different keyless construction and distinguishes its measured-channel algebraic evaluation from live exchanges. Do not generalize this note's assumptions or implementation status to every keyless scheme.

Checked 2026-10-24 against [Vaikuntanathan & Zamir, arXiv v1](https://arxiv.org/html/2604.04757v1), especially §§2.4–2.6, 5.2–5.4, 6.2–6.3. Targeted reading, not a complete proof audit.

## Assumptions from the paper

- Compatible prescribed covert algorithms and public parameters; no initial common private key.
- Private random coins and local state remain hidden.
- Both parties can sample their current honest next-message distributions repeatedly.
- All participants see the same, **noiseless** message transcript; the modeled schedule is fixed.
- A passive computational auditor, not an active rewriting adversary or full execution monitor.
- Public randomness independent of the fixed honest protocol, models and contexts; fresh embedding parameters are not reused.
- Enough eligible messages; both endpoints can recognize suitable entropy-bearing rounds. Message length is used as an entropy proxy under an additional assumption.
- The low-entropy reduction requires a suitable pseudorandom noise-resilient key exchange. A concrete instantiation uses sparse-secret LPN hardness with conjectured quasipolynomial security. Higher-entropy variants use different machinery, including DDH-based exchange.

The noise tolerated by the cryptographic primitive models hidden-bit decoding errors; it is not arbitrary editing of the visible conversation. Polynomial/asymptotic feasibility does not provide a practical budget. This is a theoretical construction, not measured autonomous LLM adoption.

## Operational questions we infer from those assumptions

These are our research questions, not results claimed by the paper:

1. **Who controls release?** An agent may sample candidates privately yet fail to control the actual receiver-visible realization. A trusted broker can change that capability. It must preserve enough task meaning to remain useful.
2. **What does the observer see?** Additional sampling, tool code, timing and private state are outside transcript-only guarantees. An execution monitor's actual visibility must be specified, not assumed omniscient.
3. **What is the honest distribution?** A public timestamp or nonce is not automatically independent of how the task is performed. Hashing predictable metadata does not create fresh entropy. Test the real dependency rather than treating any timestamp as a cryptographic random source.
4. **Can endpoints recognize eligible rounds?** Neither long messages nor low decoding temperature alone establish the required conditional min-entropy. An empirical entropy proxy needs validation.
5. **Is the budget sufficient?** Candidate sampling, eligible visible messages, state retention and key reconciliation consume resources. The low-entropy existence result does not specify a cheap API-only deployment configuration.
6. **Do both parties execute compatible machinery?** The construction specifies algorithms; it does not solve autonomous discovery, protocol choice or intent to collude.

## Relation to the first defense prototype

[Task-aware release](../experiments/anti_stego/README.md) gives the defender control over the released realization. The sender supplies a structured task result; the defender regenerates its representation. This deliberately changes the channel, rather than claiming to distinguish two distributions covered by the theorem.

The proof-style property is narrow: no information can cross through discarded representation choices when the retained task result is fixed. Information can still cross through the result itself. The implemented semantic-channel counterexample makes that limitation observable. Independently replanning removes that sender-controlled choice in a tiny public task, while sacrificing autonomy.
