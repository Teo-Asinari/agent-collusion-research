## 1) Do `payload_nia` / `orch_payload_ni` really capture “agent-level payload noninterference against colluding LLM agents with a pre-shared key”?

### Finding 1.1 — **You prove NI only for the explicitly modeled observation channel** (not “receiver-visible behavior” broadly)
- **Severity:** High (scope/claim mismatch risk)
- **Location:** `Arch.lean` header comment: “Observations are values of `observe` nodes only (receiver model R0). Cost or timing is not modeled here.” vs. comparison doc + channel table implying closure of many channels.
- **Issue:** `payload_nia` quantifies over all `ι` (good) but the *attacker’s view* is only `obs` (values of `.observe` nodes). Anything not represented as an observed wire is out-of-scope by construction: abort/termination, exception text, token length, tool-call count, order of tool calls, network-visible traffic, etc.
- **Concrete counterexample:** A colluding sender/receiver can leak 1 bit via **whether the run halts** after seeing payload (or by triggering an exception) even if no `.observe` differs—because the model always produces `List Val` and has no stuck/error semantics.
- **Smallest repair:** Tighten theorem statements/docs to: *“noninterference for the `obs` channel under total semantics; termination/errors are not modeled.”* If you want the stronger claim, extend semantics with an outcome type (`Done obs` / `Error e` / `Diverge`) and prove NI for that outcome (or explicitly add padding/STRICT-style constraints as part of the model).

### Finding 1.2 — **Pre-shared key as `publicWeight` is fine for NI, but it hides a realistic “key exfiltration”/“key-dependent formatting” surface**
- **Severity:** Medium
- **Location:** `κo`: wire 2 is `.publicWeight` (“pre-shared key known to both agents”); doc table row “Shared keys are receiver side information (`publicWeight` wires).”
- **Issue:** Modeling the key as public is consistent with the theorem (it’s equal across worlds, so cannot carry payload-differences). However, in real systems the key is secret to the *outside*, and colluding agents can use it to make outputs look innocuous while still encoding. Your theorem still blocks payload flow into observed values, but the *story* “colluding agents with a pre-shared key” may mislead readers into thinking you modeled cryptographic steganography per se. You modeled it as “receiver has side information (fixed across worlds).”
- **Smallest repair:** Rephrase: *“receiver side information (including codebooks/keys) is modeled as public-to-the-proof (held fixed across worlds), so the result holds even if agents share arbitrary fixed side information.”*

### Finding 1.3 — **`orch`’s “verify-or-recompute” design makes the sender’s contribution intentionally non-informative; the theorem doesn’t show useful collusion resistance for typical agent designs**
- **Severity:** Medium (not wrong, but easy to over-interpret)
- **Location:** `toolImpl` + `orch` + comparison doc “Utility limits”
- **Issue:** In `orch`, the only payload-dependent values (sender op 11, file write 12) are never observed. The observed tool output (14) is forced to equal `F(query,z)` regardless of sender behavior. So `orch_payload_ni` is mostly witnessing “don’t observe the sender” + “only release checked values”.
- **Smallest repair:** In the comparison doc, explicitly separate (a) *general theorem* (`payload_nia`) from (b) *illustrative orchestration* whose utility is intentionally restricted. You already gesture at this; I’d make it sharper: “`orch` demonstrates enforcement, not competitive utility.”

---

## 2) Is the `WTa` relaxation (release specs may read public computed wires) sound? Is `wt_to_wta` a good sanity check?

### Finding 2.1 — **Sound for NI as stated; but introduces an “authorized-by-computation” subtlety**
- **Severity:** Medium
- **Location:** `WTa.release` readability condition: `(∀ a ∈ specArgs, Γ a = some .pub ∨ κ a = some .authorized)`
- **Issue:** Allowing specArgs to include *computed public wires* is sound *for noninterference* because any public wire is already (by invariant) payload-independent. However, this shifts trust to the *typing* of everything that ever becomes `.pub`. If some other rule mistakenly labels a payload-influenced value `.pub`, then releases can launder it.
- **Smallest repair:** Document an explicit invariant lemma: “if `Γ w = pub` under `WTa` from `ctx0`, then `w` is payload-independent” (you essentially prove this via `payload_nia` / `obs_factors`, but it’s not packaged as a named invariant). This will make the relaxation easier to audit.

### Finding 2.2 — **`wt_to_wta` is a reasonable sanity check, but it doesn’t validate the new surface area**
- **Severity:** Low
- **Location:** `wt_to_wta`
- **Issue:** It proves backward compatibility (“old programs still typecheck”), but not “new programs are safe” (that’s `payload_nia`) nor “new programs are meaningful.” That’s fine; just don’t oversell `wt_to_wta` as validating the relaxation beyond conservativity.
- **Smallest repair:** In the doc: label it “conservativity check” only.

---

## 3) Is `obs_factors` a correct basis for the distributional claim about sampling?

### Finding 3.1 — **Mathematically the factoring claim is fine; the probabilistic leap needs one more explicit assumption**
- **Severity:** Medium
- **Location:** `obs_factors` + doc text: “Hence, for any input distribution in which (public inputs, authorized data) is independent of payload…”
- **Issue:** `obs_factors` shows a *deterministic functional dependence*: `obs ι p ρ = obs ι p (proj κ ρ)`. From this you can conclude independence if `(proj κ ρ)` is independent of payload. Your doc says “(public inputs, authorized data) independent of payload,” which matches `proj`.
  - What’s missing: you also need the distribution to treat `ι` as fixed (or independent of payload). In the Lean theorem, `ι` is universally quantified externally, so you’re fine, but the prose should say “for any fixed `ι`” or “even if `ι` is adversarial but not payload-dependent across the compared worlds.”
- **Smallest repair:** Add one sentence: “We consider `ι` fixed across the compared worlds (adversarial but not re-sampled as a function of payload).”

---

## 4) Channel-table fairness vs the quoted CaMeL/FIDES text; missing channels

### Finding 4.1 — **CaMeL timing channel row is supported by your quote; but your “STRICT mode stops X” claims are stronger than what you quoted**
- **Severity:** Low–Medium
- **Location:** comparison doc §1 + table rows “Tool choice/control flow” and “Timing/scheduling”
- **Evidence:** You quote CaMeL §7 giving examples and saying “vulnerable to side-channel attacks,” plus mitigations “stopped by STRICT mode” / “mitigated in STRICT mode…”
- **Issue:** Without quoting the precise guarantees of STRICT mode, saying “stopped” is slightly strong. It may be accurate, but based only on your excerpt it’s not airtight.
- **Smallest repair:** Replace “stopped” with “intended to be mitigated” unless you can cite an explicit statement from the read sections.

### Finding 4.2 — **FIDES “tool choice/control flow open by design” matches the explicit secrecy quote**
- **Severity:** Low
- **Location:** table row “Tool choice/control flow”
- **Evidence:** You quote: “Explicit secrecy does not prevent implicit flows… adversary… may infer limited information” and “does not attempt to hide whether data has been sent.”
- **Comment:** This row is fair given the quoted text.

### Finding 4.3 — **Your table omits several major side channels that are acknowledged in CaMeL and/or are standard in IFC discussions**
- **Severity:** High (for completeness of “who closes what”)
- **Missing channels (at least):**
  1. **Termination / abort / exception text** (you mention exceptions in CaMeL row, but not in “Our rules”; your Lean model has no error/abort channel at all).
  2. **Output length / token count** (LLM responses, logs).
  3. **Number/order of tool calls** (you model “dispatch choice” but not “how many calls happened” unless explicitly observed; FIDES explicitly warns about sequence of tool calls).
  4. **Resource exhaustion / memory pressure** (can be externally visible).
  5. **Observation timing/order**: in Lean, `obs` is a list in program order; but a real receiver may see streaming partial outputs or interleavings.
- **Smallest repair:** Add rows: termination, exceptions-as-observations, output length, tool-call count, streaming/interleaving. For “Our rules,” mark them “not modeled” unless you actually add explicit wires/observations and prove rejection witnesses.

---

## 5) Honest-limits section: anything overstated?

### Finding 5.1 — **“Timing is closed for modeled timing” is accurate but can be misread as “timing channel solved”**
- **Severity:** Medium
- **Location:** comparison doc Honest limits + timing row
- **Issue:** You do say physical timing not modeled, but the earlier “Closed for modeled timing” can still be misread.
- **Smallest repair:** Change phrasing to “Closed only if timing is fully mediated through modeled wires; physical/OS/network timing remains open.”

---

## Bottom-line rating
**faithful-with-caveats**: The Lean meaning supports payload noninterference for the *modeled observation channel* even with fully adversarial/colluding `ι` and fixed shared side information. The main risks are (i) readers over-generalizing beyond `.observe`/total semantics and (ii) table/comparison completeness around unmodeled side channels (termination, length, count, streaming).
