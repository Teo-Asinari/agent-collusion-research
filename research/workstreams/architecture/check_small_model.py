"""Finite sanity check, not a theorem proof or a trained neural model.

Exhaust all unweighted directed graphs on three named vertices and every pair
of full edge-order sweeps. The learned scheduler is abstracted as arbitrary
permutations. Also detect order-sensitive states after only one sweep.
"""

import json
from itertools import permutations, product


def relax(state, order):
    result = state[:]
    for u, v in order:
        result[v] = min(result[v], result[u] + 1)
    return result


def run():
    all_edges = [(u, v) for u in range(3) for v in range(3) if u != v]
    schedules = 0
    order_sensitive = 0
    example = None
    for bits in product([0, 1], repeat=6):
        edges = [edge for edge, present in zip(all_edges, bits) if present]
        orders = list(permutations(edges))
        expected = [0, 99, 99]
        for _ in range(2):
            previous = expected[:]
            for u, v in edges:
                expected[v] = min(expected[v], previous[u] + 1)
        first_states = {tuple(relax([0, 99, 99], order)) for order in orders}
        if len(first_states) > 1:
            order_sensitive += 1
            if example is None:
                example = edges
        for first_order in orders:
            first_state = relax([0, 99, 99], first_order)
            for second_order in orders:
                assert relax(first_state, second_order) == expected
                schedules += 1
    return {
        "scope": "All 64 directed three-vertex graphs, unit edges, source 0",
        "two_sweep_schedules": schedules,
        "two_sweep_mismatches": 0,
        "graphs_with_order_dependent_one_sweep_state": order_sensitive,
        "first_counterexample_edges": example,
        "limitations": [
            "Not a mechanized general proof",
            "No trained model, floats, resource isolation or physical timing",
            "Results cover only the finite graph family declared above",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
