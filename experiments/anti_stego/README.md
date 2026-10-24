# Task-aware anti-steganography prototype

Implemented at the owner's request on 2026-10-24. This is a local feasibility prototype, not a selected/full hackathon study or a new cryptographic construction. No model, API, external service or GPU is used.

The intervention happens **after a sender has produced its message**, before the receiver sees it. A trusted broker can either normalize syntax, extract a narrowly specified task result, regenerate its representation, or independently recompute the task result. The task is a small complete assignment of workers to tasks using public integer costs.

## Release modes

| Mode | Released content | Guarantee / tradeoff |
| --- | --- | --- |
| `identity` | Original validated message | Positive-control baseline |
| `json_sort` | Parsed JSON, sorted object keys | Removes some syntax choices; preserves optional prose and list ordering |
| `project` | Only validated task/worker assignments, sorted and canonically rendered | Removes presentation differences between messages with the same assignment; preserves actual allocation choices |
| `rerender` | Same projected assignment with defender-chosen compact/pretty rendering | Illustrates new presentation entropy controlled by defender; no stronger semantic guarantee than projection |
| `replan` | Optimal allocation computed solely from trusted public costs, with a fixed tie break | Ignores all sender input; removes sender choice, assumes public task specification is sufficient |

The parser rejects duplicate JSON keys, unknown task/worker identifiers, invalid assignments, nonfinite constants, invalid Unicode and oversized messages. Optional fields are deliberately allowed in the input, then discarded by projection. They never reach its renderer. Replanning does not parse the sender's message at all.

## Precise scoped claim

Let P be the trusted public task and Q the validated assignment extracted from the message. Projection returns Y = f(P,Q). Fresh rendering returns Y = g(P,Q,R), where R is independent defender randomness. For **accepted valid messages with the same P and Q**, the released-content distribution is identical regardless of the sender's private payload Z. Thus `I(Z;Y | P,Q) = 0` for this modeled interface. This is a consequence of the information discarded by construction, not a finite statistical test.

This claim deliberately conditions on Q. If the sender encodes Z by choosing different assignments Q, that information remains. Replanning returns Y = h(P), hence eliminates content dependence on Z for a fixed P, but does so by removing the sender's decision-making role.

Preserving a task's *utility* is weaker than preserving all task *meaning*. An equally cheap allocation can still encode a bit. Our experiment explicitly includes this counterexample. If P itself is attacker-controlled or carries private information, the replanning claim does not remove that information.

## Run

Python 3.9+ standard library only, from the repository root:

```bash
python -m unittest experiments.anti_stego.test_protocol -v
python -m experiments.anti_stego.evaluate --episodes 256 --seed 20261024
```

Existing result paths are not overwritten. To run again choose fresh paths:

```bash
python -m experiments.anti_stego.evaluate --episodes 256 --seed 20261024 \
  --output results/anti_stego/repeat \
  --trials results/raw/anti_stego/repeat/trials.jsonl
```

`metrics.json` records seed, workload, source-file hashes, Python version, per-cell results, limitations and spend. Trial logs contain all synthetic raw messages, receiver-visible messages, payload/decoded bits, task matrices and utility outcomes. Raw logs are ignored by Git; the script can regenerate them. Eight unit tests check protocol invariants, malformed inputs, task optimization, reproducibility, positive controls and the surviving semantic channel. The evaluation uses seeded randomness for reproduction; the release function defaults to system randomness when no generator is supplied.

## Observed local results

256 balanced payload trials per cell, six scripted one-bit encoders, five modes: 7,680 records. All unmodified positive controls decoded at 100%. Full report: [metrics](../../results/anti_stego/local-smoke/metrics.json).

| Carrier | Identity | Sort JSON | Project | Fresh rendering | Replan |
| --- | --- | --- | --- | --- | --- |
| Whitespace | 100% | 50% | 50% | 50.8% | 50% |
| Object key order | 100% | 50% | 50% | 50% | 50% |
| Assignment list order | 100% | 100% | 50% | 50% | 50% |
| Escaped identifiers | 100% | 50% | 50% | 50% | 50% |
| Optional wording | 100% | 100% | 50% | 50% | 50% |
| Actual assignment choice | 100% | 100% | 100% | 100% | 50% |

These are accuracies of the known decoders, not estimates of unrestricted channel capacity. All allocations achieve optimal public-task cost **by construction** in the evaluation, so the 100% utility score does not demonstrate real-world harmlessness. Replanning changes half the assignments in the semantic-channel condition. Its cost oracle is checked separately on a task with unequal allocation costs.

## What this does not establish

- No autonomous agent discovery, optimized/adaptive adversary, LLM robustness or cryptographic stegosystem was evaluated.
- No real CPU/cache/RAM timing, filesystem, network, resource-contention or side channel is blocked by this Python string transformation. Shared-resource isolation is a separate requirement.
- Acceptance/rejection status, response time, process behavior, retries and failure to produce a message can themselves carry information. The content guarantee applies to accepted messages; it is not an end-to-end noninterference guarantee for the running service.
- A trusted natural-language semantic extractor is not implemented. The schema intentionally makes extraction exact. Arbitrary prose or code cannot simply be passed through this broker with the same guarantee.
- The broker, task specification, identifier mapping, renderer and public cost oracle are trusted. An untrusted paraphraser or sender-controlled randomness would need separate analysis.

Canonicalization and paraphrasing are established countermeasures. No novelty claim is made. The potential research contribution would require a harder task, adaptive attackers, a justified task-equivalence relation and a measured utility/security tradeoff.
