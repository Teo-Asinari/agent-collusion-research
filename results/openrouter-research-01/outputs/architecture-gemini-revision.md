### Objection Disposition

*   **Objection 1 (F depends on protected θ) & Objection 2 (Capability vs. noninterference contradiction):** **Accepted.** The previous proposal claimed the neural model could prove properties the fallback solver could not. This makes the released bit $v$ dependent on the private neural weights $\theta$ and payload $m$, violating the core architectural requirement that the authorized release $F(x)$ be a fixed predicate independent of protected state. The capability claim is explicitly withdrawn.
*   **Objection 3 (Verification cost assumption):** **Accepted.** Checking non-linear inductive invariants requires SMT queries, which do not offer the categorical verification-vs-solving cost asymmetry seen in shortest-path certificates.
*   **Objection 4 (No new architectural mechanism):** **Accepted.** The proposal merely instantiated the existing abstract machine in a new domain.
*   **Objection 5 (Oracle ≠ learnable test):** **Accepted.**

### Surviving Construction: None

**No compelling design survives.** The attempt to find a useful capability for the closed abstract retrieval machine has failed. I am explicitly withdrawing the Neural Invariant Generation proposal. 

The verified context and the adversarial critique jointly demonstrate that the current architectural constraints foreclose both potential avenues for neural utility: capability and efficiency.

### The Exact Unsolved Technical Bottleneck

The bottleneck is a structural contradiction between the **strict noninterference requirement** (implemented via fixed-slot padding and total exact fallback) and the **requirements for neural utility** (which demand either expanded capability or reduced public latency).

**1. The Capability Bottleneck (Proof Sketch):**
*   *Assumption:* The architecture requires releasing only $F(x)$, where $F$ is a fixed, trusted predicate independent of private state $(\theta, m)$.
*   *Assumption:* A neural predictor provides a "capability advantage" if it causes the system to output $v=1$ (success) for an input $x$ where the deterministic fallback solver would output $v=0$ (failure/timeout).
*   *Implication:* If the neural predictor provides a capability advantage for $x$, the released bit $v$ depends on whether the neural predictor succeeds. The predictor's success depends on its private weights $\theta$ and hidden payload $m$. Therefore, $v$ depends on $(\theta, m)$.
*   *Conclusion:* A system cannot simultaneously possess a capability advantage and satisfy the noninterference requirement. The fallback must be a complete decision procedure for $F(x)$, rendering the neural model's capability redundant.

**2. The Efficiency Bottleneck (Observation):**
*   *Definition:* Public latency efficiency requires the total public ticks $T(x)$ to be strictly less than the worst-case fallback ticks $K_F$.
*   *Assumption:* To prevent timing channels (as specified in the verified context), the architecture pads execution to fixed abstract slots regardless of early private completion. Total time is $T(x) = B + K_V + K_F$.
*   *Conclusion:* The padding paradox ensures that public latency is strictly worse than or equal to the baseline fallback solver. 
*   *Conjecture:* While *private* compute cycles might be saved (if the fallback phase idles rather than computes), these savings cannot be translated into public throughput or latency without creating a timing channel that leaks the private neural success rate (and thus $m$).

### Closest-Predecessor Delta

The closest predecessor remains the exact retrieval abstract machine from the verified context (Revision 1). The delta achieved in this iteration is negative: we have formally mapped the boundaries of the architecture and proved that substituting a generative task (invariant synthesis) for a retrieval task (record matching) does not bypass the fundamental padding and completeness limitations. 

### Smallest Decisive Next Check

Do not write code, train models, or search for new application domains (like theorem proving or scheduling). The bottleneck is theoretical. 

The next decisive check must answer this specific mechanism-design question:
**Can we construct a public readout transition $G$ that safely amortizes private early-completion savings into public throughput without violating the conditional-history invariant?**

*   *Verification step:* Formulate a mathematical definition of an amortized queueing system where tasks arrive publicly, are processed privately with variable neural acceleration, and depart publicly. 
*   *Success criteria:* Prove that the public departure schedule (the transcript of readout slots) is conditionally independent of the private payload $m$, while still demonstrating a lower average latency than a system without neural acceleration.
*   *Failure criteria:* If queuing theory dictates that any work-conserving scheduler exposing variable completion times inherently leaks the variance (and thus the payload), the architectural approach to anti-steganography via exact F-release is fundamentally incompatible with cost-saving neural acceleration. At that point, the architecture research direction should be abandoned in favor of statistical or task-preserving rewrite approaches.
