"""POST-HOC analysis (not preregistered): restrict to valid, untruncated outputs.

Motivated by finding, after the run, that the 600-token limit truncated most
resolve/tc_sanitize outputs. Uses the direct decoder (anchor-in-A per cluster),
which needs no fitting; small-n subsets make fitted decoders unstable.
"""
from collections import defaultdict
import json
from pathlib import Path
import random
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import component as C  # noqa: E402

OUT = Path(__file__).resolve().parents[2] / 'results/component-rewrite-pilot-01'
units = {u['index']: u for u in json.loads((OUT / 'units.json').read_text())}
groups = defaultdict(lambda: defaultdict(list))
for line in (OUT / 'records.jsonl').read_text().splitlines():
    r = json.loads(line)
    u = units[r['index']]
    f = C.features(r['content'], u['task'])
    if not f or not f['valid']:
        continue
    hit = sum(a == b for a, b in zip(f['comp'], u['comp'])) / C.CLUSTERS
    key = (r['label'], r['arm'])
    groups[key]['valid'].append(hit)
    if r.get('finish_reason') == 'stop':
        groups[key]['valid_and_stop'].append(hit)
summary = {}
for key, subsets in sorted(groups.items()):
    summary['/'.join(key)] = {name: C.bootstrap(v, random.Random(1)) for name, v in subsets.items()}
    row = summary['/'.join(key)]
    print(f"{'/'.join(key):30s} " + '  '.join(
        f"{n}: n={s['n_tasks']} acc={s['mean']:.3f} {s['ci95']}" for n, s in row.items()))
(OUT / 'posthoc-valid-only.json').write_text(json.dumps(summary, indent=2) + '\n')
