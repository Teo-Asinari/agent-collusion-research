"""Recover a completed result without another training invocation.

Uses installed SDK execution logs to locate calls in an explicitly named app.
Result deserialization needs PyTorch because the original torch.__version__ was
a TorchVersion instance. No credentials or training data are printed.
Recovery is only possible while Modal retains the function output. A failed
local deserialization can occur after cleanup, in which case the output is lost.
"""
import argparse
import asyncio
import hashlib
import json
from pathlib import Path
import sys


async def locate(app_id, output):
    from modal.client import _Client
    from modal_proto import api_pb2
    client = await _Client.from_env()
    calls = set()
    logs = []
    request = api_pb2.AppGetLogsRequest(app_id=app_id, timeout=5)
    async for batch in client.stub.AppGetLogs.unary_stream(request):
        for item in batch.items:
            if item.function_call_id:
                calls.add(item.function_call_id)
            if item.data:
                logs.append({'timestamp': item.timestamp, 'data': item.data,
                             'function_call_id': item.function_call_id})
        if batch.app_done:
            break
    (output / 'remote-logs.json').write_text(json.dumps(logs, indent=2) + '\n')
    return sorted(calls)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--app-id', required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--torch-site-packages', type=Path)
    args = parser.parse_args()
    if args.torch_site_packages:
        sys.path.append(str(args.torch_site_packages))
    import modal
    import torch
    calls = asyncio.run(locate(args.app_id, args.output))
    if len(calls) != 1:
        raise RuntimeError(f'Expected one training call, found {len(calls)}')
    call_id = calls[0]
    try:
        metrics, checkpoint = modal.FunctionCall.from_id(call_id).get(timeout=30)
    except Exception as error:
        (args.output / 'recovery-failure.json').write_text(json.dumps({
            'status': 'recovery_failed', 'app_id': args.app_id,
            'function_call_id': call_id, 'error_type': type(error).__name__,
            'new_training_invocations': 0
        }, indent=2) + '\n')
        raise
    # Normalize SDK/framework scalar types to standard JSON primitives.
    metrics['torch'] = str(metrics['torch'])
    for name in ['metrics.json', 'model.pt', 'recovery.json']:
        if (args.output / name).exists():
            raise FileExistsError(args.output / name)
    (args.output / 'metrics.json').write_text(json.dumps(metrics, indent=2) + '\n')
    (args.output / 'model.pt').write_bytes(checkpoint)
    record = {
        'status': 'recovered_completed_training', 'app_id': args.app_id,
        'function_call_id': call_id, 'new_training_invocations': 0,
        'checkpoint_sha256': hashlib.sha256(checkpoint).hexdigest(),
        'torch_for_local_deserialization': str(torch.__version__),
        'actual_cost_usd': None,
    }
    (args.output / 'recovery.json').write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps(record, indent=2))


if __name__ == '__main__':
    main()
