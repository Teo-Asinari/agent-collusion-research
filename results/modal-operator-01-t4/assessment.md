# First usable Modal operation-training result

2026-10-25. Exploratory feasibility check. One usable checkpoint and metrics file
were recovered after three earlier launch/transport/queue attempts. All four apps
are stopped with zero tasks in `app-status.json`. No further run is authorized.

## What was actually trained

A 137,696-parameter, two-block, width-64 split-attention model was trained from
scratch. Public inputs are eight distinct keys with 16-valued entries and a query
key. The target is its paired value. Each public token embeds a key and value;
the final token embeds the query. One private token embeds an independent random
bit. The bit contains no legitimate task information.

Each block uses distinct public/private affine attention projections, softmax,
residual connections, per-token LayerNorm and Linear–GELU–Linear layers. Public
attention sees public state only. Private attention sees protected state and
detached public state. Private-loss gradients cannot update public embeddings or
the public path through this forward graph. These are conventional algebraic
operations with constrained connectivity, not a newly established mathematical
primitive or a general language architecture.

Training jointly optimizes two 16-class cross-entropies (public and private
heads). AdamW, lr 0.001, weight decay 0.01, batch 128, 1,000 steps, fixed seeds:
128,000 generated training examples, not necessarily all distinct. Gates are
evaluated afterward: public logits supply top-2^k candidate labels; the private
head ranks those candidates. Gates were not jointly trained. The earlier
word-denoising proposer/chooser was not retrained by this job.

## Result

Tesla T4, torch 2.8.0+cu128, CUDA 12.8. Training plus evaluation inside `run()`
took **9.1296 seconds**; this excludes container startup and result transfer.

| Evaluation on 1,024 fresh synthetic instances | Accuracy |
| --- | --- |
| Public head | 100% |
| Unrestricted private head | 100% |
| Gate k=0,1,2,4 | 100% each |
| Exact symbolic lookup | 100% |

Public logits were bitwise equal when the nuisance bit was flipped. The checkpoint
loads on local CPU, has 137,696 finite parameter values, and reproduces 100%
public accuracy on the same seeded evaluation. Source hashes match the submitted
files. See `verification.json`, `metrics.json`, `model.pt` and `call.json`.

**Interpretation:** the structural seed can be trained and transported from CUDA
to CPU. This task supplies no evidence of a useful private branch or bounded-choice
advantage: the public branch and a trivial symbolic lookup already solve it.
The private bit is irrelevant, tests are fresh draws rather than a provably disjoint
task universe, and only one seed was trained. No large-model, language capability,
novelty, autonomous collusion, adaptive attacker or physical-security conclusion
follows. The separate Lean support-count theorem is not an implementation proof.

## Attempts and operational deviations

1. `modal-operator-01`: launcher assumed its local path depth. Remote import at
   `/root/modal_train.py` raised IndexError. App was explicitly stopped to end
   repeated platform startup replacement. Zero training steps observed.
2. `modal-operator-01-relaunch`: corrected import; L4 trained all 1,000 steps.
   Return deserialization failed locally because a TorchVersion metric required
   importing torch in the isolated client. Logs were recovered, but the cleaned-up
   result was unavailable; no usable checkpoint or evaluation metrics retained.
3. `modal-operator-01-final`: dependency-free JSON/bytes return was preflight-tested.
   An L4 scheduler snapshot showed backlog 1 and zero runners. The queue later
   began running while we were stopping the app; logs arriving during the stop
   showed step 1,000. No result was received. The snapshot was accurate when taken
   but did not establish that the job remained queued until cancellation.
4. `modal-operator-01-t4`: changed only GPU choice and result handling, within the
   original reservation. T4 trained successfully; checkpoint and metrics saved.
   `spawn()` records the call ID; `get(timeout=600)` now bounds the whole wait,
   whereas the original function timeout did not bound the queue wait.

These were manual corrections and one cheaper-GPU fallback, not four independent
research replications or evidence about between-seed uncertainty. The usable run
does not erase the failures. Credentials remain outside the repo (0600).

## Cost

The owner approved **one $1 reservation including setup**. The original L4
600-second requested-resource estimate was $0.154248. T4 uses the previously
checked rate $0.000164/s, so its corresponding estimate is
600*(0.000164+2*0.0000131+4*0.00000222) = $0.119448.
Both are estimates, not measured bills. Queue, initialization, failed starts,
manual attempts, build, egress and CPU/memory metering must be accounted for in
the provider bill. **Actual total Modal cost is currently unknown**; no claim that
the invoice is under $1 is made. No new model API inference spend occurred.
