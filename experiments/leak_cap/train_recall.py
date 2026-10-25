"""Exploratory operation-level training; synthetic public associative recall.

No external corpus or API. Private input is independent nuisance/payload, not
information required by the task. This tests trainability, not private-data utility.
"""
import argparse
import hashlib
import json
import time
from pathlib import Path

import torch
from torch import nn
from torch.nn import functional as F

from experiments.leak_cap.operators import SplitAttentionBlock, release_candidate


def batch(n, generator, device):
    keys = torch.rand(n, 16, generator=generator).argsort(dim=1)[:, :8]
    values = torch.randint(16, (n, 8), generator=generator)
    index = torch.randint(8, (n,), generator=generator)
    query = keys[torch.arange(n), index]
    target = values[torch.arange(n), index]
    payload = torch.randint(2, (n,), generator=generator)
    return [t.to(device) for t in (keys, values, query, target, payload)]


class RecallModel(nn.Module):
    def __init__(self, width=64, depth=2):
        super().__init__()
        self.key = nn.Embedding(16, width)
        self.value = nn.Embedding(17, width)
        self.payload = nn.Embedding(2, width)
        self.blocks = nn.ModuleList([SplitAttentionBlock(width) for _ in range(depth)])
        self.public_head = nn.Linear(width, 16)
        self.private_head = nn.Linear(width, 16)

    def forward(self, keys, values, query, payload):
        k = torch.cat([keys, query[:, None]], dim=1)
        v = torch.cat([values, torch.full_like(query[:, None], 16)], dim=1)
        p = self.key(k) + self.value(v)
        h = self.payload(payload)[:, None, :]
        for block in self.blocks:
            p, h = block(p, h)
        return self.public_head(p[:, -1]), self.private_head(h[:, 0])


def run(steps=1000, seed=20261024, device='cpu', seconds=480):
    if not 1 <= steps <= 2000 or not 1 <= seconds <= 480:
        raise ValueError('Exploratory run limits: 1..2000 steps, 1..480 seconds')
    torch.manual_seed(seed)
    if device == 'cpu':
        torch.set_num_threads(4)
    model = RecallModel().to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)
    generator = torch.Generator().manual_seed(seed + 1)
    start = time.monotonic()
    losses = []
    completed = 0
    for step in range(steps):
        if time.monotonic() - start > seconds:
            break
        keys, values, query, target, payload = batch(128, generator, device)
        public, private = model(keys, values, query, payload)
        loss = F.cross_entropy(public, target) + F.cross_entropy(private, target)
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        optimizer.step()
        completed = step + 1
        if step % 100 == 0 or step == steps - 1:
            losses.append({'step': step + 1, 'loss': loss.item()})
            print(json.dumps(losses[-1]), flush=True)
    model.eval()
    correct = {k: 0 for k in [0, 1, 2, 4]}
    public_correct = private_correct = oracle_correct = 0
    invariance = True
    with torch.no_grad():
        tests = torch.Generator().manual_seed(seed + 2)
        for _ in range(8):
            keys, values, query, target, payload = batch(128, tests, device)
            public, private = model(keys, values, query, payload)
            other, _ = model(keys, values, query, 1 - payload)
            invariance &= torch.equal(public, other)
            public_correct += (public.argmax(1) == target).sum().item()
            private_correct += (private.argmax(1) == target).sum().item()
            # Strong exact task-only solver, with no learned component.
            oracle = values.gather(1, (keys == query[:, None]).long().argmax(1)[:, None])[:, 0]
            oracle_correct += (oracle == target).sum().item()
            for k in correct:
                candidates = public.topk(2 ** k, dim=1).indices
                scores = private.gather(1, candidates)
                result = release_candidate(candidates[:, :, None], scores)[:, 0]
                correct[k] += (result == target).sum().item()
    elapsed = time.monotonic() - start
    result = {
        'status': 'complete' if completed == steps else 'time_limited',
        'analysis': 'Exploratory trainability check; not confirmatory or a novelty claim',
        'task': '8-item, 16-key/value synthetic associative recall; exact task-only oracle',
        'private_input': 'independent random bit; no private task information',
        'seed': seed, 'train_seed': seed + 1, 'test_seed': seed + 2,
        'requested_steps': steps, 'completed_steps': completed,
        'batch_size': 128, 'test_examples': 1024, 'seconds': elapsed,
        'width': 64, 'depth': 2, 'parameters': sum(p.numel() for p in model.parameters()),
        'optimizer': 'AdamW', 'lr': 1e-3, 'weight_decay': 0.01,
        'device': device, 'torch': str(torch.__version__),
        'cuda_version': torch.version.cuda,
        'cudnn_version': torch.backends.cudnn.version(),
        'cuda_matmul_allow_tf32': torch.backends.cuda.matmul.allow_tf32,
        'deterministic_algorithms': torch.are_deterministic_algorithms_enabled(),
        'gpu': torch.cuda.get_device_name() if device == 'cuda' else None,
        'public_only_accuracy': public_correct / 1024,
        'unrestricted_private_head_accuracy': private_correct / 1024,
        'symbolic_oracle_accuracy': oracle_correct / 1024,
        'gated_accuracy': {str(k): v / 1024 for k, v in correct.items()},
        'public_logits_equal_under_payload_flip': bool(invariance),
        'losses': losses,
        'source_sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in (Path(__file__), Path(__file__).with_name('operators.py'))},
        'limits': ['Single training seed; fresh synthetic tests may repeat training tasks.',
                   'Not compute-matched to a separate conventional transformer baseline.',
                   'Finite gate bound is abstract content-only; no physical side-channel proof.',
                   'No end-to-end checkpoint reproducibility across hardware is asserted.'],
    }
    return result, {k: v.cpu() for k, v in model.state_dict().items()}


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--steps', type=int, default=1000)
    p.add_argument('--seconds', type=int, default=480)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    metrics, state = run(args.steps, seconds=args.seconds)
    (args.output / 'metrics.json').write_text(json.dumps(metrics, indent=2) + '\n')
    torch.save(state, args.output / 'model.pt')
