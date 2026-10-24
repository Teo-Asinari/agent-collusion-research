"""Analyze results/component-rewrite-pilot-01/records.jsonl per the preregistration."""
from collections import defaultdict
from decimal import Decimal
import json
from pathlib import Path
import random
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import component as C  # noqa: E402

OUT = Path(__file__).resolve().parents[2] / 'results/component-rewrite-pilot-01'


def main():
    units = {u['index']: u for u in json.loads((OUT / 'units.json').read_text())}
    by = defaultdict(dict)
    for line in (OUT / 'records.jsonl').read_text().splitlines():
        r = json.loads(line)
        by[(r['label'], r['arm'])][r['index']] = r
    summary = {}
    for (label, arm), recs in sorted(by.items()):
        rows, anchored, flips, costs, latency, tokens = [], 0, [], [], [], []
        for i in sorted(units):
            u, r = units[i], recs.get(i)
            feats = C.features(r['content'], u['task']) if r else None
            rows.append({'features': feats, 'comp': u['comp'], 'order': u['order']})
            if r and r.get('cost_usd') is not None:
                costs.append(Decimal(str(r['cost_usd'])))
                latency.append(r['elapsed_seconds'])
                tokens.append(r['completion_tokens'] or 0)
            if feats and feats['valid'] and arm != 'instructed_sender':
                same = sum(a == b for a, b in zip(feats['comp'], u['comp']))
                anchored += same == C.CLUSTERS
                flips.append(C.CLUSTERS - same)
        result = C.evaluate(rows, 0.5, random.Random(f'{label}-{arm}'))
        valid_n = len(flips)
        result.update({
            'calls_with_record': len(recs),
            'unchanged_assignment_rate_among_valid': round(anchored / valid_n, 4) if valid_n else None,
            'mean_cluster_flips_among_valid': round(sum(flips) / valid_n, 4) if valid_n else None,
            'cost_usd_total': str(sum(costs)), 'cost_usd_per_call': str(sum(costs) / len(costs)) if costs else None,
            'mean_latency_s': round(sum(latency) / len(latency), 3) if latency else None,
            'mean_completion_tokens': round(sum(tokens) / len(tokens), 1) if tokens else None})
        summary[f'{label}/{arm}'] = result
    (OUT / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(f"{'condition':32s} valid  comp_acc [95% CI]        exact  order  shuf   unchanged flips $/call")
    for key, s in summary.items():
        c = s['comp_bit_accuracy']
        print(f"{key:32s} {s['valid_rate']['mean']:.2f}  {c['mean']:.3f} {str(c['ci95']):18s} "
              f"{s['comp_exact']['mean']:.2f}   {s['order_bit_accuracy']['mean']:.2f}   "
              f"{s['comp_shuffled_bit_accuracy']['mean']:.2f}   {s['unchanged_assignment_rate_among_valid']}  "
              f"{s['mean_cluster_flips_among_valid']}  {s['cost_usd_per_call']}")


if __name__ == '__main__':
    main()
