"""Fast checks: typing decisions, concrete interpreter, contracts and timing defenses.

Run: <z3 venv python> -m pytest -q test_verified_arch.py   (or python test_verified_arch.py)
"""
import random
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import ir  # noqa: E402
import programs as pg  # noqa: E402
import learned_task as lt  # noqa: E402

try:
    import prove
except ImportError:  # z3 not installed: skip solver-backed checks
    prove = None


def contracts_for(program):
    return {ir.contract_key(x) for x in program if isinstance(x, ir.Release)}


def test_full_accepted_and_each_ablation_rejected():
    n = 3
    full = pg.full(n)
    ir.check(full, contracts_for(full))
    for name in ir.ABLATIONS:
        ab = pg.ablation(name, n)
        trusted = set() if name == 'trust_release' else contracts_for(ab)
        try:
            ir.check(ab, trusted)
            raise AssertionError(f'{name} accepted by full checker')
        except ir.TypeError_:
            pass
        ir.check(ab, trusted, frozenset([name]))


def test_concrete_witness_equals_exists_for_any_predictor():
    n, rng = 5, random.Random(0)
    fns = pg.py_trusted(n)
    for _ in range(300):
        zs = [rng.randint(0, 3) for _ in range(n)]
        q = rng.randint(0, 3)
        env = {'q': q, 'r': 0, 'phi': 0, 'c': rng.randint(-9, 9),
               'm': rng.randint(0, 1), 'theta': rng.randint(-9, 9)}
        env.update({f'z{i+1}': z for i, z in enumerate(zs)})
        pick = rng.randint(-3, 9)
        fns.update({'P': lambda q, z: int(q == z),
                    'NetPred': lambda th, q, c, m: pick,
                    'NetGrad': lambda th, *a: 0, 'Sgd': lambda a, b: a,
                    'NetPub': lambda ph, q, a, r: 10 * a})
        val, obs = ir.run(pg.full(n), env, fns)
        assert obs[0] == int(q in zs)
        assert 1 <= val['cost'] <= n


def test_certified_index_exact_under_adversarial_parameters():
    rng = np.random.default_rng(3)
    keys = lt.make_keys(2048, rng)
    keyset = set(keys.tolist())
    model, e, parts = lt.fit_index(keys)
    adv, e2 = lt.perturbed(keys, parts, 40, rng)
    garbage = lambda qs: rng.integers(-10**6, 10**6, len(np.atleast_1d(qs)))
    for mdl, rad in ((model, e), (adv, e2), (garbage, 3)):
        cert = lt.certify(keys, mdl, rad)
        for q in lt.queries(keys, 200, rng, keyset):
            a, _ = lt.release(keys, int(q), mdl, rad, cert)
            assert a == (int(q) in keyset)


def test_padding_defenses_constant_cost():
    n = 4096
    assert lt.visible_cost('pad_worst', n, 999, True, 1) == lt.worst(n)
    assert lt.visible_cost('pad_radius', n, 7, True, 1) != lt.visible_cost('pad_radius', n, 64, True, 1)


def test_z3_contracts_and_counterexamples():
    if prove is None:
        return
    assert prove.learned_index_contract(8) == 'unsat'
    assert prove.learned_index_contract(8, certified=False) == 'sat'
    prog = pg.full(3)
    assert prove.prove_contract(prog, 'a') == 'unsat'
    assert prove.ni_query(prog, 3, payload_only=True)['result'] == 'unsat'
    assert prove.ni_query(pg.ablation('observe_internal', 3), 3, payload_only=True)['result'] == 'sat'


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_'):
            fn()
            print('ok', name)
