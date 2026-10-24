# Open questions

Research question **unselected**. See [literature.md](literature.md) for evidence and [ideas.md](ideas.md) for proposed designs.

## Definitions to settle before selection

| Construct | Operational evidence we would want | Insufficient on its own |
| --- | --- | --- |
| Channel capacity | Randomized payload recovery above a declared baseline | Two agents make similar decisions |
| Discovery | First use of an available affordance without an alliance offer or encoding instruction | Acceptance after being explicitly offered a secret tool |
| Chosen exploitation | Observable use after an opportunity to abstain | Describing a scheme or claiming willingness |
| Harmful coordination | Joint advantage plus measured outsider/nominal-objective loss, with unilateral and benign controls | A high-reward pair, a price increase, or a judge's suspicion |
| Communication-mediated effect | Randomized valid intervention changes dependence on sender-private information | Unconditional action correlation |
| Adaptation | Recovery of the relevant behavior after a restriction, relative to continued and fresh-instance controls | Changing wording or saying “I will hide it” |

The unit of independence should normally be a fresh task/agent-team episode. Turns within an episode and branches from one checkpoint are correlated observations. Pairwise comparisons of the same small pool of plans are not independent runs.

## Questions left open by this first review

1. How much of apparent willingness comes from an explicit offer, authority framing, or visible reward instructions? Is neutral tool discovery followed by exploitation, not just tool selection?
2. Does deleting one carrier reduce total harmful coordination, or merely move the signal to ordering, identifiers, shared state, or resource choices?
3. Can randomized, task-preserving channel interventions reveal forbidden private-information use while avoiding false accusations from benign coordination?
4. Do independently authored protocol implementations actually interoperate? How much do public artifacts help, and are those artifacts simultaneously available to the auditor?
5. Under which intervention does the legitimate task stay solvable? If utility falls, can harm reduction be attributed to channel restriction rather than general impairment?
6. Which observations does the proposed monitor truly have: final messages, actions, intermediate files, prompts, private state, network access, or weights? What can it modify?
7. Are incentives literal environmental rewards, prompt descriptions of rewards, or an optimization/training signal? These are different interventions.
8. Can unilateral cheating achieve the same result? If so, success is not evidence of a coordination requirement.

## Carriers: established classes versus candidate applications

Storage and timing covert channels are longstanding concepts; actions as signaling and learned text steganography are also established. The initial source trail includes [Lampson's confinement problem](https://doi.org/10.1145/362375.362389), the tool-use paper, Colosseum and market-division work. Lampson's full paper was not reviewed here; this is a provenance pointer, not a new novelty claim.

| Affordance | Potential signal | Defensible research question rather than “new channel” claim |
| --- | --- | --- |
| Tool arguments and equivalent action choices | Selecting one valid representation among alternatives | Does canonicalization remove private-information transfer while preserving the task? |
| Task ordering, delegation, assignment | A permutation or choice of recipient | Do agents switch to ordering when prose is normalized? |
| Shared files, filenames, edits, tests | Persistent state or redundant edits | Can permitted provenance-preserving workflows constrain cross-run signaling? |
| Resource reservations or cache state | Occupancy or response differences | Is the behavior communication or a direct environmental effect? |
| Timing, retries, failure status | Delay or presence/absence of an event | Can controlled timing separate intentional signaling from provider latency? |
| Public artifacts and documentation | Common protocol defaults and conventions | Do artifacts improve real interoperability, and can an auditor exploit the same artifact? |

Timing and cache studies carry high confounding risk during a short sprint. A workflow-specific measurement or intervention can contribute even when the channel class is old.

## Current practical-barrier questions

The owner's later focus is active prevention and practical limits of secure constructions. The [expanded review](stego-prior-art.md) and [revised candidates](practical-barrier-candidates.md) add:

1. Does exact payload recovery persist when the receiver is isolated from encoder-side numerical data? Separate runtime drift from tokenization ambiguity.
2. Which utility-preserving interventions suppress delivery after codebook repair, resynchronization or semantic encoding? Measure surviving information, not only exact-message failure.
3. How much private sampling, setup and repair computation is required per delivered bit? Distinguish algebraic simulation from live end-to-end generation.
4. If the defender controls final sampling, can agents communicate through input/context choice or selective retries instead?

## Earlier focused discussion prompt

Which uncertainty should the next study resolve: **why agents choose a channel**, **whether restrictions merely relocate coordination**, or **how to establish causal evidence of harmful coordination**? These are scientific priorities, not implementation commitments. Protocol interoperability is a fourth option if theoretical-to-practical translation is the main interest.
