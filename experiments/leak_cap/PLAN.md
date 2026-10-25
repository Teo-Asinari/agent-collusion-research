# First Modal operation-training run

Prepared 2026-10-24; usable training result completed 2026-10-25 on T4 after L4
startup/transport/queue problems. See [execution assessment](../../results/modal-operator-01-t4/assessment.md).
This is an exploratory CUDA trainability/portability check, not a full study.

Owner approved the proposed $1 reservation in the next conversation turn.
Authentication succeeded. All four attempted apps are now stopped. The reservation
covered this run and corrective setup; it is not an account-level cap. Actual
invoice cost remains unknown. The original L4 execution contract below is preserved
as the plan, with the T4 fallback and other deviations recorded in the assessment.

## Research and execution contract

Question: can the explicit split-attention block learn exact public associative
recall while maintaining public-logit invariance to a protected nuisance bit?
This does not test useful authorized dependence on private task information.

- Synthetic task: eight distinct keys with values in 0..15, plus a public query.
  Output the value paired with that key. The exact task-only lookup baseline is
  included and must score 100%. Data and seeds are generated locally in the job.
- Two split-attention blocks, width 64, 137,696 parameters. Public/private heads
  optimize cross entropy with private gradients detached from public states.
- One training seed (20261024), 1,000 steps, batch 128. Test: 1,024 freshly sampled
  instances; not a disjoint exhaustively held-out task universe. No confirmatory
  significance claims. Test public-only, unrestricted private-head and finite
  candidate gates with k in {0,1,2,4}. Public candidates are top-2^k labels.
- Payload-flipped public-logit equality is a structural regression check, not
  evidence of physical isolation. Scripted gate correctness is covered by tests.
- Strong symbolic solving is already cheap. Learning is not claimed to improve
  this task's efficiency; the task discriminates working training from dead wiring.
- One L4, requested CPU=2 and memory=4 GiB, one container, zero retries, no
  warm pool; 480-second training stop and 600-second function timeout. No
  parallel maps, provider requests or persistent volume. Return checkpoint and
  metrics locally. Image includes only the two explicitly named Python sources;
  no .env, account token, repository clone, word corpus or previous logs mounted.
- GPU purpose: validate the CUDA training path of the new matrix operations
  before considering larger models, not an established speedup over CPU.

## Cost and approval

Verified [Modal pricing](https://modal.com/pricing), accessed 2026-10-24:
L4 $0.000222/s, CPU $0.0000131/core/s, RAM $0.00000222/GiB/s.
At requested resources, 600 seconds costs approximately
600*(0.000222 + 2*0.0000131 + 4*0.00000222) = **$0.154248**.
This is an execution-resource estimate, not a guaranteed billing cap: image build,
startup, metering differences and egress are additional. Reserve **$1** for this
single invocation and its setup. No assumption about available credits is made.
No account-level dollar cap is configured by this code. Modal's timeout is per
attempt and excludes scheduling: [timeout docs](https://modal.com/docs/guide/timeouts).
No retries are configured. Actual invoice cost remains unknown until inspected;
do not relabel the estimate as actual cost. Prior worker's $15–17 scale-up proposal
is separate and is not being launched.

Owner approved this estimate and authenticated Modal before launch.
This follows the preserved worker instruction to present a Modal estimate before
using it, recorded in `research/decisions.md` under the leak-cap correction.
Client 1.2.6 is installed in `/tmp/agent-collusion-modal-venv`. Authentication is
stored only in `/tmp/agent-collusion-modal.toml` (0600), outside the repo. Never
paste tokens in chat. For the existing local session use `MODAL_CONFIG_PATH` as
shown below; a new environment needs local authentication.

```bash
MODAL_CONFIG_PATH=/tmp/agent-collusion-modal.toml \
  /tmp/agent-collusion-modal-venv/bin/python -m modal run \
  experiments/leak_cap/modal_train.py --approve-estimated-cost \
  --output results/modal-operator-01
```

The launcher records attempted execution and errors without token values, refuses
to overwrite result directories and returns a checkpoint and metrics on success.
Before launch, record the Git commit and confirm no secrets enter the image.

## Completed local preparation

20 CPU training steps completed in about 0.46 seconds. Public logit equality under
payload flips held; symbolic oracle scored 100%. Public accuracy was 22.56% and
private-head accuracy 16.99%; these are smoke results, not converged comparisons.
Metrics and the checkpoint are in `results/operator-training-local-smoke/`.
Modal launcher CLI help parses with SDK 1.2.6. Subsequent remote execution and
failures are recorded in the assessment linked above; this authorization is spent.
