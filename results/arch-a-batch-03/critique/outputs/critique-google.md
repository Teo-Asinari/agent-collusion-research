Here is an adversarial review of the `Arch.Agents` Lean formalization and the comparison document, focusing on the meaning and implications of the modeling choices.

### 1. Meaning of `payload_nia` and Colluding Agents
**Finding 1.1: "Verify-or-recompute" assumes perfectly silent orchestrator interventions.**
*   **Severity:** High.
*   **Location:** `toolImpl F` in `Arch.lean` and Section 3 of the MD.
*   **Analysis:** The contract `toolImpl` checks if the sender's candidate equals `F(q, z)`. If it does not, it silently outputs `F(q, z)`. The proof of `orch_payload_ni` relies on the fact that the output is *exactly* `F(q, z)` in both branches, meaning the sender's choice of whether to provide the correct answer or intentionally fail is mathematically erased. 
*   **Counterexample:** In any real orchestrator, a verification failure triggers a fallback that consumes extra compute time and generates an orchestrator log (e.g., `DEBUG: Sender candidate rejected, recomputing`). If the receiver agent has access to metadata, execution logs, or physical timing, the sender can perfectly transmit 1 bit of payload per tool call by choosing whether to fail the check. 
*   **Repair:** Add a boolean `status` wire to `toolImpl` that records whether the candidate was accepted. If this status wire is labeled public and observed by the receiver, `WTa` will correctly reject the program (because the status depends on the payload-tainted candidate). The current model hides this channel by hardcoding the erasure.

**Finding 1.2: Keys as public wires is standard but requires strict independence.**
*   **Severity:** Low.
*   **Location:** `orch` wire 2 (`publicWeight`).
*   **Analysis:** Treating the pre-shared key as a public wire is mathematically sound and standard in steganography (the key is independent of the message). The model correctly proves that *if* the key is identical across worlds (`hpubin`), the view is identical. 

### 2. Soundness of `WTa` and `wt_to_wta`
**Finding 2.1: The `WTa` relaxation is information-theoretically sound.**
*   **Severity:** None (Validation).
*   **Location:** `WTa.release` rule.
*   **Analysis:** Allowing a release spec to read wires where `Γ a = some .pub` is sound. By the definition of the typing rules, a wire is only labeled `.pub` if it was computed entirely from other `.pub` wires. By induction, its value is identical across the two worlds (`ρ1 a = ρ2 a`). Therefore, feeding it into a deterministic release spec will yield the exact same result in both worlds, preserving noninterference. `wt_to_wta` correctly verifies that this is a strict generalization of the single-agent rules.

### 3. `obs_factors` and the Distributional Claim
**Finding 3.1: Factorization correctly implies the distributional claim, but assumes perfect sampling.**
*   **Severity:** Medium.
*   **Location:** `obs_factors` and Section 4 (Honest limits).
*   **Analysis:** The theorem proves $V = f(X_{pub}, X_{auth})$. From standard probability, if the tuple $(X_{pub}, X_{auth})$ is statistically independent of the payload $M$, then $V$ is independent of $M$. This correctly justifies the distributional claim. 
*   **Caveat:** This assumes the sender's private tape (`privateRand`) is perfectly isolated and does not bias the public tape or authorized data. If the LLM runtime uses a shared PRNG state for both agents, the sender's consumption of randomness advances the PRNG, altering the receiver's future "public" randomness. 
*   **Repair:** Explicitly state in the honest limits that the distributional claim assumes the underlying runtime provides cryptographically isolated randomness tapes per agent.

### 4. Channel Table vs. CaMeL/FIDES
**Finding 4.1: Unfair comparison regarding Exceptions/Aborts.**
*   **Severity:** High.
*   **Location:** Section 2 Table (Tool choice / control flow) & Section 1 (CaMeL summary).
*   **Analysis:** The document quotes CaMeL acknowledging a "one-bit exception channel" where a quarantined LLM conditionally raises an error to halt execution. In the comparison table, your model claims Control Flow is "Closed in the model." This is misleading. Your model closes *modeled* control flow (tool dispatch), but it completely ignores exceptions. The Lean semantics (`run`) evaluate a fixed `List Node` to completion; there is no `abort`, `throw`, or `halt` instruction. 
*   **Counterexample:** If the sender LLM outputs a malformed JSON that crashes the JSON parser before the receiver runs, the receiver observes the absence of execution (or the user observes the crash). The Lean model cannot express this.
*   **Repair:** Add a row for "Exceptions / Aborts / Termination". Mark CaMeL as "Mitigated (STRICT mode)", FIDES as "Not addressed", and your model as "Not modeled (total execution semantics)".

**Finding 4.2: Missing channel: Output Length / Resource Exhaustion.**
*   **Severity:** Medium.
*   **Location:** Section 2 Table.
*   **Analysis:** The model abstracts all data as `Val` (Int). Real LLMs output variable-length strings. A sender can encode payload in the *length* of its output (e.g., padding with spaces), which might exhaust context windows or cause truncation for the receiver.
*   **Repair:** Add a row for "Message Length / Truncation". Mark it as "Not modeled (abstracted to fixed-size `Val`)".

### 5. Honest Limits
**Finding 5.1: The limits are mostly accurate but miss the orchestrator-log assumption.**
*   **Severity:** Medium.
*   **Location:** Section 4.
*   **Analysis:** The statement "useful LLM contributions are limited to checkable certificates" is an excellent and honest summary of the batch-3 findings. However, the limits section fails to mention that checking these certificates must be done *silently and in constant time* (or with padded time) relative to the receiver's view. 
*   **Repair:** Add a bullet to Section 4: "Silent Verification: The verify-or-recompute pattern assumes the orchestrator does not expose verification failures to the receiver via logs, metadata, or unpadded timing."

### Conclusion

**Verdict: Faithful with caveats.**

The Lean proofs are mathematically sound, and the core claim—that you can force payload noninterference against colluding agents by restricting them to checkable certificates and strict dataflow—is verified by the model. The `WTa` relaxation is correct, and the factorization theorem supports the distributional claim.

However, the translation from the math to the physical reality of orchestration contains blind spots. The model achieves "closed" channels partly by defining away the mechanisms that cause them (exceptions, orchestrator logs, variable-length outputs). The comparison table is slightly unfair to CaMeL by penalizing it for an exception channel that your model simply lacks the syntax to express. Fixing the table and adding the "silent verification" assumption to the honest limits will make the research document entirely rigorous.
