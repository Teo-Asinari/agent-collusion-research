"""Concrete IR programs: the witness cell, its public readout, and one-invariant ablations.

Values are integers; booleans are 0/1. `P` is the fixed trusted task predicate;
names starting with `Net` or listed in OPAQUE are learned/opaque functions.
"""
from ir import Input, Op, Release, Observe

OPAQUE = {'NetPred', 'NetPub', 'NetGrad', 'NetH', 'Norm', 'Sgd'}


def witness_impl(n, pred_args=('q', 'c', 'm'), out='v', cost='cost'):
    """Predictor-first existential check with early-exit fallback scan."""
    impl = [Op('j', 'NetPred', list(pred_args), kind='neural', weight='theta'),
            Op('jc', f'clamp1_{n}', ['j'])]
    impl += [Op(f'p{i}', 'P', ['q', f'z{i}']) for i in range(1, n + 1)]
    impl += [Op('v0', f'select_{n}', ['jc'] + [f'p{i}' for i in range(1, n + 1)]),
             Op('k0', 'one', [])]
    for i in range(1, n + 1):
        impl += [Op(f'ji{i}', f'neq_{i}', ['jc']),
                 Op(f'nv{i}', 'not', [f'v{i-1}']),
                 Op(f'ev{i}', 'and', [f'nv{i}', f'ji{i}']),
                 Op(f'hit{i}', 'and', [f'ev{i}', f'p{i}']),
                 Op(f'v{i}', 'or', [f'v{i-1}', f'hit{i}']),
                 Op(f'k{i}', 'add', [f'k{i-1}', f'ev{i}'])]
    impl += [Op(out, 'id', [f'v{n}']), Op(cost, 'id', [f'k{n}'])]
    return impl


def inputs(n):
    nodes = [Input('q', 'public_task'), Input('r', 'public_rand'),
             Input('phi', 'public_weight'), Input('c', 'private_state'),
             Input('m', 'payload'), Input('theta', 'private_weight')]
    nodes += [Input(f'z{i}', 'authorized') for i in range(1, n + 1)]
    return nodes


def spec_args(n):
    return ['q'] + [f'z{i}' for i in range(1, n + 1)]


def full(n):
    """Accepted architecture: private witness cell, exact release, public readout.

    Private training of theta is allowed and stays private.
    """
    return inputs(n) + [
        Op('g', 'NetGrad', ['c', 'm'] + [f'z{i}' for i in range(1, n + 1)],
           kind='neural', weight='theta'),
        Op('theta2', 'Sgd', ['theta', 'g']),
        Release('a', f'exists_{n}', spec_args(n), witness_impl(n), 'v', cost='cost'),
        Op('y', 'NetPub', ['q', 'a', 'r'], kind='neural', weight='phi'),
        Observe('a'), Observe('y')]


def ablation(name, n):
    """Program rejected by the full checker; accepted when `name` is ablated."""
    base = inputs(n)
    rel = Release('a', f'exists_{n}', spec_args(n), witness_impl(n), 'v', cost='cost')
    if name == 'mask_only':
        # Public token normalized with statistics that include a private activation.
        return base + [rel,
                       Op('h', 'NetH', ['c', 'm'], kind='neural', weight='theta'),
                       Op('y', 'NetPub', ['q', 'a', 'r', 'h'], kind='neural',
                          weight='phi', secondary=['h']),
                       Observe('a'), Observe('y')]
    if name == 'weights_not_wires':
        # Shared public readout fine-tuned on a private, payload-dependent gradient.
        return base + [rel,
                       Op('g', 'NetGrad', ['c', 'm'], kind='neural', weight='theta'),
                       Op('phi2', 'Sgd', ['phi', 'g']),
                       Op('y', 'NetPub', ['q', 'a', 'r'], kind='neural', weight='phi2'),
                       Observe('a'), Observe('y')]
    if name == 'trust_release':
        # Claims the exists spec but releases the predictor-chosen index.
        bad = witness_impl(n) + [Op('leak', 'id', ['jc'])]
        return base + [Release('a', f'exists_{n}', spec_args(n), bad, 'leak'),
                       Op('y', 'NetPub', ['q', 'a', 'r'], kind='neural', weight='phi'),
                       Observe('a'), Observe('y')]
    if name == 'spec_reads_anything':
        # Contract holds for a declared spec that itself reads the payload.
        impl = witness_impl(n) + [Op('vx', 'xor', ['v', 'm'])]
        return base + [Release('a', f'existsxor_{n}', spec_args(n) + ['m'], impl, 'vx'),
                       Op('y', 'NetPub', ['q', 'a', 'r'], kind='neural', weight='phi'),
                       Observe('a'), Observe('y')]
    if name == 'observe_internal':
        # Correct release, but the receiver sees its internal work count.
        return base + [rel,
                       Op('y', 'NetPub', ['q', 'a', 'r'], kind='neural', weight='phi'),
                       Observe('a'), Observe('y'), Observe('cost')]
    raise ValueError(name)


def py_trusted(n):
    """Python semantics for trusted (non-opaque) functions used above."""
    fns = {
        f'clamp1_{n}': lambda j: min(max(int(j), 1), n),
        f'select_{n}': lambda j, *p: p[j - 1],
        'one': lambda: 1, 'id': lambda x: x,
        'not': lambda x: 1 - x, 'and': lambda x, y: x & y,
        'or': lambda x, y: x | y, 'xor': lambda x, y: x ^ y,
        'add': lambda x, y: x + y,
    }
    for i in range(1, n + 1):
        fns[f'neq_{i}'] = (lambda i: lambda j: int(j != i))(i)
    return fns
