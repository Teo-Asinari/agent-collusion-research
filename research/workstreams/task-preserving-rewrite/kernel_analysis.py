"""Exact finite content-channel analysis, not a timing-secure implementation."""
from collections import Counter
from itertools import product
import json

VERTICES = range(4)
EDGES = ((0, 1, 1), (0, 2, 1), (1, 3, 1), (2, 3, 1), (0, 3, 4))
WEIGHTS = {(u, v): w for u, v, w in EDGES}
ADJACENCY = tuple(tuple((v, w) for a, v, w in EDGES if a == u) for u in VERTICES)
COMMENTS = tuple(c for n in range(3) for c in product((0, 1), repeat=n))


def canonical_path(dist):
    pred = {}
    for u, v, w in EDGES:
        if dist[v] == dist[u] + w:
            pred[v] = min(u, pred.get(v, u))
    path = [3]
    for _ in range(3):
        if path[-1] == 0:
            break
        path.append(pred[path[-1]])
    if path[-1] != 0:
        raise ValueError('nondecreasing or incomplete predecessor chain')
    return tuple(reversed(path))


def independently_solve():
    # Deterministic array-based Dijkstra: no input certificate or comment read.
    dist = [0, 99, 99, 99]
    done = set()
    for _ in VERTICES:
        u = min((v for v in VERTICES if v not in done), key=lambda v: (dist[v], v))
        done.add(u)
        for v, w in ADJACENCY[u]:
            dist[v] = min(dist[v], dist[u] + w)
    return tuple(dist)


def valid_certificate(dist, parents):
    # All listed constraints evaluated; no certificate-dependent early return.
    checks = [dist[0] == 0]
    checks.extend(dist[v] <= dist[u] + w for u, v, w in EDGES)
    for v, u in enumerate(parents, start=1):
        w = WEIGHTS.get((u, v), 0)
        checks.append((u, v) in WEIGHTS)
        checks.append(dist[v] == dist[u] + w)
    return sum(checks) == len(checks)


def rewrite(dist, parents, comment):
    good = valid_certificate(dist, parents)
    chosen = dist if good else independently_solve()
    released = json.dumps(canonical_path(chosen), separators=(',', ':')).encode('ascii')
    # This deliberately exposed diagnostic view demonstrates the timing caveat.
    diagnostic = (len(comment), not good)
    return released, diagnostic, good


def main():
    content_rows = Counter()
    diagnostic_rows = Counter()
    valid_labels = set()
    valid_count = 0
    total = 0
    for dist in product(range(5), repeat=4):
        for parents in product(VERTICES, repeat=3):
            for comment in COMMENTS:
                release, diag, good = rewrite(dist, parents, comment)
                content_rows[release] += 1
                diagnostic_rows[(release, diag)] += 1
                total += 1
                valid_count += good
                if good:
                    valid_labels.add(dist)
    assert total == 280000
    assert valid_count == 14
    assert valid_labels == {(0, 1, 1, 2)}
    assert content_rows == {b'[0,1,3]': total}
    report = {
        'scope': 'All 280000 bounded record inputs; fixed public graph; content only.',
        'input_count': total,
        'valid_count': valid_count,
        'invalid_count': total-valid_count,
        'unique_accepted_distances': sorted(valid_labels),
        'content_distribution_rows': [{'output': p.decode('ascii'), 'row_count': n, 'probability': 1}
                                      for p, n in sorted(content_rows.items())],
        'max_pairwise_content_TV': 0,
        'diagnostic_outcomes': [
            {'path': p.decode('ascii'), 'comment_length': d[0], 'fallback': d[1], 'row_count': n}
            for (p, d), n in sorted(diagnostic_rows.items())],
        'max_pairwise_TV_with_diagnostics': 1,
        'randomness': 'none',
        'independent_solving_on_valid_input': False,
        'efficiency_advantage_over_strong_symbolic_baseline': 'not established',
        'limitations': ['Not a mechanized proof or a secure running service.',
                       'Observed status/work/duration can reveal fallback and input length.',
                       'No conclusion about arbitrary malformed bytes or physical side channels.'],
    }
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
