"""Scripted, zero-cost arms. Writes results/component-rewrite-local/summary.json."""
import json
from pathlib import Path
import random
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import component as C  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'results/component-rewrite-local'
N_TASKS = 400
SPLIT = 0.5

ARMS = {'identity': lambda t, task, rng: t, 'normalize': C.arm_normalize,
        'local_walk': C.arm_local_walk, 'cluster_flip_1': C.make_cluster_flip(1),
        'cluster_flip_2': C.make_cluster_flip(2), 'random_resolve': C.arm_random_resolve,
        'canonical_resolve': C.arm_canonical_resolve}


def payload(rng):
    return [rng.randrange(2) for _ in range(C.CLUSTERS)], [rng.randrange(2) for _ in range(C.ORDER_BITS)]


def main():
    summary = {'n_tasks': N_TASKS, 'train_fraction': SPLIT, 'conditions': {}}
    for constrained in (True, False):
        space = 'constrained' if constrained else 'unconstrained_connected_control'
        for name, arm in ARMS.items():
            rng = random.Random(f'{space}-{name}')
            rows = []
            for i in range(N_TASKS):
                task = C.make_task(10_000 + i, constrained)
                comp, order = payload(rng)
                artifact = C.encode(task, comp, order)
                out = arm(artifact, task, rng)
                rows.append({'features': C.features(out, task), 'comp': comp, 'order': order})
            summary['conditions'][f'{space}/{name}'] = C.evaluate(rows, SPLIT, random.Random(1))
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    for key, value in summary['conditions'].items():
        print(f"{key:55s} valid={value['valid_rate']['mean']:.2f} "
              f"comp={value['comp_bit_accuracy']['mean']:.3f} {value['comp_bit_accuracy']['ci95']} "
              f"order={value['order_bit_accuracy']['mean']:.3f} "
              f"comp_shuf={value['comp_shuffled_bit_accuracy']['mean']:.3f}")


if __name__ == '__main__':
    main()
