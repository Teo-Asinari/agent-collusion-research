"""One bounded Modal L4 training invocation; no secrets or datasets mounted."""
from pathlib import Path

import modal

ROOT = Path(__file__).resolve().parents[2]
app = modal.App('agent-collusion-operator-feasibility')
image = (modal.Image.debian_slim(python_version='3.11')
         .pip_install('torch==2.8.0')
         .add_local_file(ROOT / 'experiments/leak_cap/operators.py', '/root/experiments/leak_cap/operators.py')
         .add_local_file(ROOT / 'experiments/leak_cap/train_recall.py', '/root/experiments/leak_cap/train_recall.py'))


@app.function(image=image, gpu='L4', cpu=2, memory=4096, timeout=600,
              retries=0, max_containers=1, min_containers=0,
              scaledown_window=2)
def train():
    import io
    import torch
    from experiments.leak_cap.train_recall import run
    metrics, state = run(steps=1000, device='cuda', seconds=480)
    buffer = io.BytesIO()
    torch.save(state, buffer)
    return metrics, buffer.getvalue()


@app.local_entrypoint()
def main(output: str = 'results/modal-operator-01', approve_estimated_cost: bool = False):
    import json
    import hashlib
    import subprocess
    from datetime import datetime, timezone
    if not approve_estimated_cost:
        raise ValueError('Review PLAN.md and supply --approve-estimated-cost before launch')
    target = Path(output)
    target.mkdir(parents=True, exist_ok=False)
    (target / 'launch.json').write_text(json.dumps({
        'status': 'launching', 'gpu': 'L4', 'timeout_seconds': 600,
        'training_seconds': 480, 'retries': 0, 'max_containers': 1,
        'estimated_execution_ceiling_usd': 0.16,
        'approved_reservation_usd': 1,
        'started_utc': datetime.now(timezone.utc).isoformat(),
        'git_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
        'working_tree_status': subprocess.check_output(['git', 'status', '--short'], cwd=ROOT, text=True),
        'modal_client_version': modal.__version__,
        'modal_app_id': app.app_id,
        'launcher_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'billing_note': 'Build/startup/egress not included; actual invoice cost not known.'
    }, indent=2) + '\n')
    try:
        metrics, checkpoint = train.remote()
    except Exception as error:
        (target / 'failure.json').write_text(json.dumps({
            'error_type': type(error).__name__, 'status': 'failed',
            'actual_cost_usd': None, 'automatic_retry': False
        }, indent=2) + '\n')
        raise
    (target / 'metrics.json').write_text(json.dumps(metrics, indent=2) + '\n')
    (target / 'model.pt').write_bytes(checkpoint)
