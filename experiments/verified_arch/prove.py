"""z3 checks quantified over every interpretation of the opaque (learned) functions.

Opaque functions are z3 uninterpreted functions, and all inputs are free, so an
`unsat` result covers every weight setting and every predictor/readout function,
for the stated finite instance size. This is not a proof for all N; the general
statement is the pen-and-paper induction in formal-model.md.

Run: python prove.py  (writes ../../results/arch-a-batch-01/prove.json)
"""
import json
import random
import sys
import time
from pathlib import Path

import z3

sys.path.insert(0, str(Path(__file__).parent))
from ir import Input, Op, Release, Observe, INPUT_LABEL, PUB, check, contract_key, TypeError_, ABLATIONS  # noqa: E402
import programs as pg  # noqa: E402

OUT = Path(__file__).resolve().parents[2] / 'results/arch-a-batch-01'
I = z3.IntSort()


class Sym:
    def __init__(self):
        self.funcs = {}
        self.Puf = z3.Function('Puf', I, I, I)

    def uf(self, name, arity):
        key = (name, arity)
        if key not in self.funcs:
            self.funcs[key] = z3.Function(name, *([I] * arity), I)
        return self.funcs[key]

    def b(self, x):
        return z3.If(x, 1, 0)

    def trusted(self, fn, args):
        if fn.startswith('clamp1_'):
            n = int(fn.split('_')[1])
            (j,) = args
            return z3.If(j < 1, 1, z3.If(j > n, n, j))
        if fn.startswith('select_'):
            j, *p = args
            e = p[-1]
            for i in range(len(p) - 1, 0, -1):
                e = z3.If(j == i, p[i - 1], e)
            return e
        if fn.startswith('neq_'):
            return self.b(args[0] != int(fn.split('_')[1]))
        if fn.startswith('exists_'):
            q, *zs = args
            return self.b(z3.Or([self.Puf(q, z) != 0 for z in zs]))
        if fn.startswith('existsxor_'):
            q, *rest = args
            zs, m = rest[:-1], rest[-1]
            e = self.b(z3.Or([self.Puf(q, z) != 0 for z in zs]))
            return z3.If(e == m, 0, 1)
        table = {
            'P': lambda q, z: self.b(self.Puf(q, z) != 0),
            'one': lambda: z3.IntVal(1), 'id': lambda x: x,
            'not': lambda x: 1 - x, 'and': lambda x, y: x * y,
            'or': lambda x, y: z3.If(x + y > 0, 1, 0),
            'xor': lambda x, y: z3.If(x == y, 0, 1),
            'add': lambda x, y: x + y,
        }
        if fn in table:
            return table[fn](*args)
        return None

    def apply(self, node, val):
        args = [val[a] for a in node.args]
        if node.weight:
            args = [val[node.weight]] + args
        t = None if node.kind == 'neural' else self.trusted(node.fn, args)
        if t is None:
            t = self.uf(node.fn, len(args))(*args)
        return t

    def execute(self, program, tag, domain):
        """Symbolically run one world; returns (values, observations)."""
        val, obs = {}, []

        def step(node):
            if isinstance(node, Input):
                val[node.out] = z3.Int(f'{tag}_{node.out}')
                if node.kind == 'payload':
                    domain.append(z3.Or(val[node.out] == 0, val[node.out] == 1))
            elif isinstance(node, Op):
                val[node.out] = self.apply(node, val)
            elif isinstance(node, Release):
                for sub in node.impl:
                    step(sub)
                val[node.out] = val[node.impl_out]
                val[('spec', node.out)] = self.trusted(node.spec, [val[a] for a in node.spec_args])
            elif isinstance(node, Observe):
                obs.append(val[node.wire])

        for node in program:
            step(node)
        return val, obs


def prove_contract(program, release_out):
    """Valid(impl_out == spec) over all functions and inputs, for one world."""
    s, dom = z3.Solver(), []
    val, _ = Sym().execute(program, 'w', dom)
    s.add(dom)
    s.add(val[release_out] != val[('spec', release_out)])
    r = s.check()
    return str(r)  # 'unsat' means the contract holds universally


def ni_query(program, n, payload_only=False):
    """Search for two worlds with equal public inputs and equal authorized F but
    different observations. unsat = noninterference for this instance.
    payload_only: additionally fix every input except the payload m, so a sat
    result is a pure payload channel rather than leakage of other private state."""
    sym, dom = Sym(), []
    v1, o1 = sym.execute(program, 'A', dom)
    v2, o2 = sym.execute(program, 'B', dom)
    s = z3.Solver()
    s.add(dom)
    for node in program:
        if isinstance(node, Input) and (INPUT_LABEL[node.kind] == PUB or (
                payload_only and node.kind != 'payload')):
            s.add(v1[node.out] == v2[node.out])
    args = pg.spec_args(n)
    s.add(sym.trusted(f'exists_{n}', [v1[a] for a in args])
          == sym.trusted(f'exists_{n}', [v2[a] for a in args]))
    s.add(z3.Or([x != y for x, y in zip(o1, o2)]))
    r = s.check()
    out = {'result': str(r)}
    if r == z3.sat:
        mdl = s.model()
        out['world_A_obs'] = [str(mdl.eval(x, model_completion=True)) for x in o1]
        out['world_B_obs'] = [str(mdl.eval(x, model_completion=True)) for x in o2]
        out['payload_A_B'] = [str(mdl.eval(v1['m'], model_completion=True)),
                              str(mdl.eval(v2['m'], model_completion=True))]
    return out


def isolated(program, release):
    """Proof context for one release: every wire it reads from outside its impl
    becomes a free input (original Input kept where it is one). A contract proved
    here holds for any values those wires take in any program, which is what
    makes keying contracts by (spec, args, impl) sound across programs."""
    inner = {sub.out for sub in release.impl if isinstance(sub, Op)}
    reads = set(release.spec_args)
    for sub in release.impl:
        reads |= set(sub.args) | ({sub.weight} if sub.weight else set())
    reads -= inner
    by_name = {x.out: x for x in program if isinstance(x, Input)}
    return [by_name.get(w, Input(w, 'private_state')) for w in sorted(reads)] + [release]


def verified_contracts(program):
    keys, report = set(), {}
    for node in program:
        if isinstance(node, Release):
            r = prove_contract(isolated(program, node), node.out)
            report[node.spec + ':' + node.impl_out] = r
            if r == 'unsat':
                keys.add(contract_key(node))
    return keys, report


def typecheck(program, contracts, ablate=()):
    try:
        check(program, contracts, frozenset(ablate))
        return 'accepted'
    except TypeError_ as e:
        return f'rejected: {e}'


# ---- random program fuzzing: is every accepted program noninterferent? ----

def release_variant(n, kind):
    if kind == 'good':
        return Release('a', f'exists_{n}', pg.spec_args(n), pg.witness_impl(n), 'v', cost='cost')
    if kind == 'unverified':  # releases the predictor-chosen index
        return Release('a', f'exists_{n}', pg.spec_args(n),
                       pg.witness_impl(n) + [Op('leak', 'id', ['jc'])], 'leak')
    if kind == 'spec_reads_m':
        return Release('a', f'existsxor_{n}', pg.spec_args(n) + ['m'],
                       pg.witness_impl(n) + [Op('vx', 'xor', ['v', 'm'])], 'vx')
    raise ValueError(kind)


def random_program(rng, n, n_ops):
    """Random DAG over the standard inputs plus one release (good or bad variant).
    Args are biased toward public wires so that a useful fraction typechecks."""
    prog = pg.inputs(n)
    pub = ['q', 'r', 'phi']
    priv = [x.out for x in prog if x.out not in pub]
    weights = ['phi', 'theta']
    kind = rng.choices(['good', 'unverified', 'spec_reads_m'], [0.6, 0.2, 0.2])[0]
    rel = release_variant(n, kind)
    pos = rng.randrange(n_ops + 1)
    made = []
    for k in range(n_ops + 1):
        if k == pos:
            prog.append(rel)
            pub.append('a')
            made.append('a')
        if k == n_ops:
            break
        args = []
        for _ in range(rng.randint(1, 3)):
            pool = pub if (rng.random() < 0.8 or not priv) else priv
            args.append(rng.choice(pool))
        args = list(dict.fromkeys(args))
        w = rng.choice(weights + [None, None])
        sec = [x for x in args if rng.random() < 0.3]
        name = f'u{k}'
        if rng.random() < 0.15:
            name = f'w{k}'
            weights.append(name)
        prog.append(Op(name, f'Net{len(args)}' + ('w' if w else ''), args,
                       kind='neural', weight=w, secondary=sec))
        # Track the label the FULL checker would assign, for generation bias only.
        reads = args + ([w] if w else [])
        (priv if any(x in priv for x in reads) else pub).append(name)
        made.append(name)
    if rng.random() < 0.25:
        prog.append(Observe('cost') if kind == 'good' else Observe('jc'))
    for x in rng.sample(made, min(2, len(made))):
        prog.append(Observe(x))
    return prog


def fuzz(trials, n, seed):
    rng = random.Random(seed)
    contracts = set()
    for kind in ('good', 'unverified', 'spec_reads_m'):
        rel = release_variant(n, kind)
        if prove_contract(isolated(pg.inputs(n), rel), 'a') == 'unsat':
            contracts.add(contract_key(rel))
    stats = {mode: {'accepted': 0, 'accepted_and_leaky': 0, 'accepted_and_payload_leaky': 0}
             for mode in ('full',) + ABLATIONS}
    examples = {}
    cache = {}
    for t in range(trials):
        prog = random_program(rng, n, rng.randint(2, 6))
        for mode in stats:
            abl = () if mode == 'full' else (mode,)
            if typecheck(prog, contracts, abl) != 'accepted':
                continue
            stats[mode]['accepted'] += 1
            if t not in cache:
                cache[t] = (ni_query(prog, n)['result'] == 'sat',
                            ni_query(prog, n, payload_only=True)['result'] == 'sat')
            leak, pleak = cache[t]
            stats[mode]['accepted_and_leaky'] += leak
            stats[mode]['accepted_and_payload_leaky'] += pleak
            if leak:
                examples.setdefault(mode, repr(prog[len(pg.inputs(n)):])[:600])
    return stats, examples


# ---- direct release contracts outside the IR ----

def shortest_path_contract(n, sweeps):
    """Arbitrary per-sweep edge permutations (any neural schedule after a total
    decoder) on a complete directed n-graph with arbitrary nonnegative integer
    weights and presence bits. Compare d[t] after `sweeps` sweeps with the
    minimum over simple paths. unsat = schedule-independent exact release."""
    verts = range(n)
    edges = [(u, v) for u in verts for v in verts if u != v]
    INF = None
    w = {e: z3.Int(f'w_{e[0]}_{e[1]}') for e in edges}
    pres = {e: z3.Bool(f'p_{e[0]}_{e[1]}') for e in edges}
    s = z3.Solver()
    s.add([w[e] >= 0 for e in edges])
    big = z3.Int('BIG')  # infinity stand-in strictly above any simple-path cost
    s.add(big > z3.Sum([w[e] for e in edges]))
    d = [z3.IntVal(0)] + [big] * (n - 1)
    for sw in range(sweeps):
        pos = {e: z3.Int(f'pos{sw}_{e[0]}_{e[1]}') for e in edges}
        s.add(z3.Distinct(list(pos.values())))
        s.add([z3.And(pos[e] >= 0, pos[e] < len(edges)) for e in edges])
        for k in range(len(edges)):
            new = list(d)
            for (u, v) in edges:
                cand = z3.If(z3.And(pos[(u, v)] == k, pres[(u, v)], d[u] + w[(u, v)] < d[v]),
                             d[u] + w[(u, v)], d[v])
                new[v] = z3.If(pos[(u, v)] == k, cand, new[v])
            d = new
    # true distance by simple-path enumeration
    from itertools import permutations
    results = []
    for t in range(1, n):
        costs = []
        mids = [x for x in verts if x not in (0, t)]
        for r in range(len(mids) + 1):
            for path in permutations(mids, r):
                seq = (0,) + path + (t,)
                es = list(zip(seq, seq[1:]))
                costs.append((z3.And([pres[e] for e in es]), z3.Sum([w[e] for e in es])))
        true = big
        for ok, c in costs:
            true = z3.If(z3.And(ok, c < true), c, true)
        results.append(d[t] != true)
    s.add(z3.Or(results))
    return str(s.check())


def learned_index_contract(n, certified=True):
    """Learned position model Pred (uninterpreted: any weights) and claimed error
    radius e (arbitrary). A trusted verifier checks |Pred(k_i) - i| <= e for every
    stored key; if it passes, answer membership by bounded binary search of the
    clipped window around Pred(q) only, else by full binary search. Release is
    membership. Same algorithm as learned_task.release(). certified=False trusts
    the window without the verifier (ablation)."""
    keys = [z3.Int(f'k{i}') for i in range(n)]
    q, e = z3.Ints('q e')
    pred = z3.Function('Pred', I, I)
    s = z3.Solver()
    s.add([keys[i] < keys[i + 1] for i in range(n - 1)])

    def bsearch(lo, hi):
        found = z3.BoolVal(False)
        for _ in range(n.bit_length() + 1):
            live = lo <= hi
            mid = (lo + hi) / 2
            key = keys[-1]
            for i in range(n - 1, -1, -1):
                key = z3.If(mid == i, keys[i], key)
            hit = z3.And(live, key == q)
            found = z3.Or(found, hit)
            lo2 = z3.If(z3.And(live, key < q), mid + 1, lo)
            hi2 = z3.If(z3.And(live, key > q), mid - 1, hi)
            lo, hi = lo2, z3.If(hit, lo2 - 1, hi2)
        return found

    def clip(x):
        return z3.If(x < 0, 0, z3.If(x > n - 1, n - 1, x))

    cert = z3.And([z3.And(pred(keys[i]) - i <= e, i - pred(keys[i]) <= e) for i in range(n)])
    window = z3.And(pred(q) - e <= n - 1, pred(q) + e >= 0,
                    bsearch(clip(pred(q) - e), clip(pred(q) + e)))
    full = bsearch(z3.IntVal(0), z3.IntVal(n - 1))
    out = z3.If(cert, window, full) if certified else window
    s.add(out != z3.Or([k == q for k in keys]))
    return str(s.check())


def section_witness():
    out = {}
    for n in range(1, 9):
        prog = pg.full(n)
        contracts, creport = verified_contracts(prog)
        entry = {'contract': creport, 'typecheck_full': typecheck(prog, contracts),
                 'direct_ni': ni_query(prog, n)['result'],
                 'direct_ni_payload_only': ni_query(prog, n, payload_only=True)['result']}
        if n in (2, 4):
            entry['ablations'] = {}
            for name in ABLATIONS:
                ab = pg.ablation(name, n)
                ac, acr = verified_contracts(ab)
                entry['ablations'][name] = {
                    'contracts': acr,
                    'typecheck_full': typecheck(ab, ac),
                    'typecheck_with_this_ablation': typecheck(ab, ac, (name,)),
                    'ni_counterexample': ni_query(ab, n),
                    'payload_only_counterexample': ni_query(ab, n, payload_only=True)}
        out[n] = entry
    return out


def section_shortest_path():
    # Only the one-sweep counterexample: z3 did not finish the n=3, two-sweep
    # validity query within ~10 minutes (linear integer arithmetic over free
    # permutations). The full-sweep claim rests on the informal proof plus the
    # earlier exhaustive check in research/workstreams/architecture/.
    return {'n3_sweeps1': shortest_path_contract(3, 1)}


def section_learned_index():
    out = {f'n{n}': learned_index_contract(n) for n in (4, 8, 16)}
    out['n8_uncertified_window'] = learned_index_contract(8, certified=False)
    return out


def section_fuzz(trials=5000):
    stats, ex = fuzz(trials=trials, n=2, seed=1)
    return {'trials': trials, 'n': 2, 'seed': 1, 'stats': stats, 'first_leaky_example': ex}


SECTIONS = {'witness': section_witness, 'shortest_path': section_shortest_path,
            'learned_index': section_learned_index, 'fuzz': section_fuzz}


def main(names):
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / 'prove.json'
    rep = json.loads(path.read_text()) if path.exists() else {}
    rep['z3_version'] = z3.get_version_string()
    rep['meaning'] = ("contract/NI 'unsat' = holds for every interpretation of opaque "
                      "functions (all weights) at that instance size; 'sat' = counterexample exists")
    rep.setdefault('seconds', {})
    for name in names:
        t0 = time.time()
        rep[name] = SECTIONS[name]()
        rep['seconds'][name] = round(time.time() - t0, 1)
        path.write_text(json.dumps(rep, indent=2) + '\n')
        print(name, rep['seconds'][name], 's', flush=True)


if __name__ == '__main__':
    main(sys.argv[1:] or list(SECTIONS))
