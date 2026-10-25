# Stopped L4 attempt

2026-10-25. App `ap-cDWq1SyKrnNGLwkL89S25O` initially had one queued input and
zero runners (saved scheduler snapshot). After a prolonged wait it was stopped
to switch to T4. Training started in the interval between the snapshot and stop;
logs delivered while stopping included step 1,000. No checkpoint or evaluation
metrics were received. `failure.json` records the resulting RemoteError.

Do not count this as zero training or as a usable replication. Actual billed cost
is unknown. See the complete assessment in `../modal-operator-01-t4/assessment.md`.
