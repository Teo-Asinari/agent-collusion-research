## Adversarial Review: Arch.Agents

---

### Finding 1 — Pre-shared key modeled as `publicWeight` (SEVERE)

**Location:** `κo` definition; `orch_payload_ni` hypothesis `h : ∀ a, a ∈ [0,1,2,6] → ρ1 a = ρ2 a`; channel table row "Colluding / adversarial LLM."

**Problem.** Wire 2 is typed `publicWeight` and appears in the hypothesis requiring `ρ1 2 = ρ2 2`. The channel table says pre-shared keys are "receiver side information (`publicWeight` wires)." But a pre-shared key is by definition shared between *sender* and *receiver*; the two compared worlds in `payload_nia` fix the key to be equal. This means the proof assumes both worlds see the same key, which correctly captures that the key is not payload-dependent. However, the claim "receiver side information including pre-shared keys" in the channel table implies that a key the receiver holds but the sender does not is modeled — yet in `orch`, both `LLM_S` and `LLM_R` receive wire 2 as an argument. So the model gives the sender the key too. Under a colluding-agent threat model where both agents have the key, the key is a common side channel that can be used to construct a codebook, e.g., HMAC(key, position) as a steganographic symbol map. The theorem says observations are equal across payload-worlds *given* the key is fixed and equal — which is trivially true regardless of steganography, because the codebook is also fixed. The theorem does **not** say the channel capacity is zero; it says two fixed worlds give the same output. A steganographic scheme can embed m into outputs that are a deterministic function of (key, m, public inputs), and this is consistent with `obs ι p ρ1 = obs ι p ρ2` whenever ρ1 and ρ2 agree on public inputs and the key — *because the key is in both worlds and both agents exploit it identically*. The proof closes only against payload variation, not against key-mediated encoding. The channel table claim "Closed. State versions are wires…" does not address this.

**Counterexample.** Let ι be: `LLM_S [q, m, tape, mem, z, key] = HMAC(key, m)`, `LLM_R` observes 11 (which is closed by WTa, so the receiver must use the release). But wire 11 feeds `write_file` (wire 12), which is then not observed. The key issue is subtler: if the key feeds into a *public op* that the receiver observes (wire 15 reads wire 2), the receiver can decode HMAC(key, m) from the slot or tool output if the sender influences those. The verify-or-recompute release prevents tool output manipulation, but wire 15 (`LLM_R [14, 13, 2, 1]`) is a public op whose output depends on the key and on the verified tool result — the receiver reads both the fixed tool result and the key, and can apply any policy. Yet wire 15's label is public only because its inputs 14, 13 are public and 2, 1 are public. This is sound for the theorem but does not mean the receiver cannot decode a pre-agreed encoding from the *structure* of the outputs.

**Repair.** The honest-limits section should explicitly state: the theorem closes payload variation at fixed public inputs and key, but does not bound steganographic capacity across the key itself. A separate argument is needed that the key is independent of the sender's payload distribution, i.e., key establishment is out of scope.

---

### Finding 2 — Release spec reads public *computed* wires: `WTa` relaxation is sound but its scope claim is overstated (MODERATE)

**Location:** `WTa.release` condition `Γ a = some .pub ∨ κ a = some .authorized`; `wt_to_wta`; channel table row "Tool choice."

**Observation.** The relaxation is logically sound: if wire `a` is labeled `.pub` in the current context (proved by the label propagation invariant), then it cannot depend on private data, so reading it in a spec is safe. `wt_to_wta` correctly shows every WT-accepted program is WTa-accepted.

**Problem.** The table says the tool-choice channel is "Closed in the model." Wire 10 (`LLM_R [0,2,1]`) is labeled public (its inputs are all public). The release at wire 14 reads wire 10 as a spec arg. So the receiver's adaptively chosen query is verifiably public and can feed the release spec. But the sender's LLM call (wire 11) reads wire 10, and the sender's *response* (wire 11) is private. The orchestrator calls `write_file [11]` producing wire 12, which is private and not observed. The tool release ignores wire 11 (reads only 10 and 6). So the sender cannot influence the tool output — but this is only because the tool contract is F(query, z), where z is authorized and query is public. The sender's output is discarded unless it matches. This is the verify-or-recompute pattern and is honest about it in the honest-limits section.

**However**, the table row says "Dispatch is an op labeled by what it reads; an observed tool choice made from private data is rejected." This is correct for `chanTool`. But it conflates two things: (a) which *tool* is called and (b) what *arguments* are passed. The model has no way to constrain which tool is called adaptively if the orchestrator is an op reading private data — and in `orch` the orchestrator doesn't dispatch tools, it just runs a fixed sequence. Real orchestrations with LLM-chosen tool selection are not modeled.

---

### Finding 3 — `toolImpl` contract: the verify-or-recompute branch is a no-op for leakage, but the sender influences *timing* of the branch (MODERATE)

**Location:** `toolImpl`, `toolImpl_contract`.

The contract is `impl ι ρ = spec (specArgs.map ρ)` for all ι, ρ. This is proved. The implementation always returns `F(ρ 10)(ρ 6)` regardless of the candidate. So the tool output wire (14) carries no payload information. **But** the branch `if cand = F(ρ 10)(ρ 6)` is taken or not depending on whether `LLM_S_answer` matches. This branch condition is observable as timing (fast path vs. recompute path). The honest-limits section says "Physical timing (CPU, cache, network) is not modeled" — this is honest. But the branch is part of the *modeled* semantics and its observability as a boolean is not addressed. If the orchestrator records whether the candidate matched (e.g., in a log), that is a 1-bit channel from sender to whoever reads the log. This is not closed and not mentioned.

**Repair.** Note in honest limits that the verify-or-recompute implementation leaks 1 bit (match/no-match) through any log or observable that captures the branch taken, analogous to CaMeL's exception channel (§7).

---

### Finding 4 — `obs_factors` distributional claim: correct but the stated corollary is weaker than implied (MODERATE)

**Location:** `obs_factors` theorem statement and markdown claim "the receiver view is independent of the payload."

The theorem says `obs ι p ρ = obs ι p (proj κ ρ)` — the view equals the view computed from the zeroed-out private projection. This is a **deterministic** factorization. The distributional claim follows only if `(public, authorized)` is independent of payload in the joint distribution. The markdown states this correctly as a conditional: "for any input distribution in which (public inputs, authorized data) is independent of the payload." This is fine. But the channel table says the private-tape channel is "Closed. Private tapes are private inputs… `obs_factors`: the view depends only on public and authorized inputs, so it is payload-independent under any input distribution where those are independent of m." The condition "public inputs independent of m" may fail when the sender chooses its tape *after* seeing m (adaptive sender), or when the authorized data z is correlated with m. The model fixes z as authorized and ρ as an arbitrary function — so these cases are correctly excluded. No overstatement here, but the independence assumption is doing real work and should be flagged more prominently.

---

### Finding 5 — Channel table: missing channels (MODERATE)

**Location:** Table in §2.

The following channels are present in the CaMeL §7 discussion or standard covert-channel literature but absent from the table:

- **Abort/termination channel**: whether the orchestration halts or loops is not a wire in the model. CaMeL §7 explicitly mentions the exception (halt-or-not) channel as leaking 1 bit. The model's `run` always terminates (fixed program list); this rules out termination channels by construction but is not stated.
- **Output length / cardinality of `obs`**: the number of observe nodes is fixed at compile time. Real LLM outputs have variable length; that channel is not modeled and not mentioned.
- **Error messages**: CaMeL §7 discusses errors as a channel. Not in the table.
- **Number of tool calls**: mentioned in FIDES §4.4 as an implicit flow. The table says FIDES leaves this open; it should note the model also leaves it open (the model has a fixed number of ops).
- **Order of observations**: `obs` returns a list; if observations have timestamps, order encodes information. Not addressed.

The honest-limits section mentions timing but not the others. The table should add a row or note acknowledging these.

---

### Finding 6 — CaMeL/FIDES table claims: minor inaccuracy (MINOR)

**Location:** Table row "Timing / scheduling," CaMeL column: "**Open** (§7 timing example)."

This is accurate per the quoted §7. The FIDES column says "Not addressed in the sections read" — this is appropriately scoped. No unfair characterization found. The CaMeL exception-channel mitigation in STRICT mode is noted accurately. The FIDES explicit-secrecy limitation quote is accurate. No misrepresentation.

---

### Finding 7 — Honest limits: one item understated (MINOR)

**Location:** §4 "Utility" paragraph.

The text says "values can be guaranteed for all policies, but useful LLM contributions are limited to checkable certificates." This is accurate. But it does not note that the sender's LLM call (wire 11) is **entirely wasted** from the information-theoretic standpoint of the receiver's view — its output is discarded unless it matches the trusted tool. The sender adds no computational value; it can only save a recompute. This makes the "lift" relative to CaMeL/FIDES (which allow LLM-influenced outputs) even larger than stated.

---

## Summary

| # | Severity | Topic |
|---|----------|-------|
| 1 | **Severe** | Pre-shared key in both agents' inputs; theorem does not bound key-mediated steganography |
| 2 | Moderate | WTa tool-choice claim conflates tool identity with tool arguments; real adaptive dispatch unmodeled |
| 3 | Moderate | Verify-or-recompute match/no-match branch leaks 1 bit through any observable log; unmentioned |
| 4 | Moderate | `obs_factors` independence assumption is load-bearing; needs more prominence |
| 5 | Moderate | Table missing: abort, output length, error message, tool-call count, observation order channels |
| 6 | Minor | CaMeL/FIDES table claims accurate |
| 7 | Minor | Utility paragraph understates sender's zero informational contribution |

**Verdict: faithful-with-caveats.**

The Lean proofs are semantically sound for what they state. The primary gap is that the pre-shared-key setup (Finding 1) means the theorem closes payload variation at *fixed key*, which is consistent with a steganographic scheme using that key as a codebook — the intended adversarial scenario. This is not a proof error but a modeling scope limitation that is not clearly flagged. Findings 3 and 5 identify channels that the model implicitly excludes by construction without acknowledging it. The honest-limits section is largely accurate but incomplete on these points.
