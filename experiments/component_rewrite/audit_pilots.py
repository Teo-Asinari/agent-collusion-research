"""Read-only audit of existing pilot records. No requests or result overwrites.

This reproduces direct-decoder, valid-output statistics as a post-hoc audit,
separating attempted, unattempted, failed and held-out observations. It does not
recreate the fitted receiver's preregistered primary analysis.
"""
import argparse
from collections import defaultdict
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import random

from experiments.component_rewrite import component as C


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit(directory):
    units = {u['index']: u for u in json.loads((directory / 'units.json').read_text())}
    records = [json.loads(line) for line in (directory / 'records.jsonl').read_text().splitlines()]
    seen = set()
    by = defaultdict(list)
    for record in records:
        key = (record['label'], record['arm'], record['index'])
        if key in seen:
            raise ValueError(f'Duplicate job observation: {key}')
        seen.add(key)
        by[key[:2]].append(record)
    output = {}
    for (label, arm), rows in sorted(by.items()):
        subsets = {}
        for split in ['all', 'train', 'test']:
            planned = [u for u in units.values() if split == 'all' or u['split'] == split]
            selected = [r for r in rows if split == 'all' or units[r['index']]['split'] == split]
            accuracies, stopped_accuracies = [], []
            valid_count = duplicate_rosters = 0
            for r in selected:
                unit = units[r['index']]
                f = C.features(r.get('content'), unit['task'], directory.name.endswith('02'))
                if not f or not f['valid']:
                    continue
                valid_count += 1
                score = sum(a == b for a, b in zip(f['comp'], unit['comp'])) / C.CLUSTERS
                accuracies.append(score)
                if r.get('finish_reason') == 'stop':
                    stopped_accuracies.append(score)
                text = C.last_fenced(r.get('content')) if directory.name.endswith('02') else r.get('content')
                _, lists = C.parse(text, unit['task'])
                roster = lists['A'] + lists['B']
                duplicate_rosters += len(roster) != len(set(roster))
            subsets[split] = {
                'planned_tasks': len(planned), 'attempted_tasks': len(selected),
                'unattempted_tasks': len(planned) - len(selected),
                'error_records': sum(bool(r.get('error')) for r in selected),
                'truncated_records': sum(r.get('finish_reason') == 'length' for r in selected),
                'valid_under_existing_checker': valid_count,
                'duplicate_rosters_accepted_by_existing_checker': duplicate_rosters,
                'valid_fraction_of_attempted': valid_count / len(selected) if selected else None,
                'direct_accuracy_among_valid': C.bootstrap(accuracies, random.Random(1)),
                'direct_accuracy_among_valid_stop': C.bootstrap(stopped_accuracies, random.Random(1)),
                'recorded_cost_usd': str(sum((Decimal(str(r['cost_usd'])) for r in selected
                                             if r.get('cost_usd') is not None), Decimal(0))),
                'records_missing_cost': sum(r.get('cost_usd') is None for r in selected)
            }
        output[f'{label}/{arm}'] = subsets
    return {
        'analysis': 'Post-hoc audit, direct known decoder, validity selection reported explicitly',
        'input_hashes': {name: digest(directory / name) for name in ['records.jsonl', 'units.json']},
        'records': len(records), 'groups': output
    }


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    if args.output.exists():
        raise FileExistsError(args.output)
    root = Path(__file__).resolve().parents[2]
    reports = {name: audit(root / 'results' / name)
               for name in ['component-rewrite-pilot-01', 'component-rewrite-pilot-02']}
    report = {'source_sha256': digest(Path(__file__)), 'new_api_calls': 0, 'new_api_cost_usd': 0,
              'reports': reports}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x') as handle:
        handle.write(json.dumps(report, indent=2) + '\n')
    for name, r in reports.items():
        print(name, 'records:', r['records'])
        for key, group in r['groups'].items():
            row = group['all']
            print(key, 'attempted', row['attempted_tasks'], 'valid', row['valid_under_existing_checker'],
                  'valid_acc', row['direct_accuracy_among_valid'],
                  'test_attempted', group['test']['attempted_tasks'])
