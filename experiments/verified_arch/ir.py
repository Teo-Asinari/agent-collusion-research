"""Labeled dataflow IR for a learned/verified cell: model, type checker, interpreter.

Research artifact, not a secure runtime. Programs are straight-line SSA graphs.
Weights, optimizer state, random tapes and counters are ordinary wires, so
training-time and inference-time dependencies obey one rule. Neural functions
are opaque: the checker never inspects them, and the z3 module quantifies over
all of them. A Release node is the only private-to-public edge; it is admitted
only with a separately verified contract that its implementation equals a
declared spec reading authorized private data, never payload or private weights.

Ablation flags each switch off exactly one invariant, so counterexamples can
show that the invariant is load-bearing.
"""
from dataclasses import dataclass, field

PUB, PRIV = 'pub', 'priv'

# Input kinds and their labels. 'authorized' is private task data z that the
# release spec F may read; 'payload' is the sender's m; both are private.
INPUT_LABEL = {
    'public_task': PUB, 'public_rand': PUB, 'public_weight': PUB,
    'authorized': PRIV, 'payload': PRIV, 'private_weight': PRIV,
    'private_rand': PRIV, 'private_state': PRIV,
}
SPEC_READABLE = {'public_task', 'authorized'}


@dataclass
class Input:
    out: str
    kind: str


@dataclass
class Op:
    """out = fn(args). kind 'neural' is opaque/learned; 'trusted' is fixed code.

    `secondary` marks args an attention mask would not see (residual adds,
    normalization statistics, gradients into a weight update). The full checker
    treats them like any other arg; the mask_only ablation ignores them.
    `weight` names a parameter wire for neural ops.
    """
    out: str
    fn: str
    args: list
    kind: str = 'trusted'
    weight: str = None
    secondary: list = field(default_factory=list)


@dataclass
class Release:
    """out (public) = impl(...), claimed equal to spec(spec_args).

    impl is a sub-program over any wires, ending in wire impl_out. Its internal
    wires stay private; `cost` names an internal work-count wire, if any.
    """
    out: str
    spec: str
    spec_args: list
    impl: list
    impl_out: str
    cost: str = None


@dataclass
class Observe:
    """Receiver-visible wire."""
    wire: str


class TypeError_(Exception):
    pass


def contract_key(release):
    """A contract certifies one (spec, implementation) pair, not a spec name."""
    return (release.spec, tuple(release.spec_args), release.impl_out, repr(release.impl))


ABLATIONS = ('mask_only', 'weights_not_wires', 'trust_release',
             'spec_reads_anything', 'observe_internal')


def check(program, contracts=frozenset(), ablate=frozenset(), kinds=None):
    """Return wire labels; raise TypeError_ on a violation.

    contracts: contract_key values whose impl == spec has been verified.
    kinds: map wire -> input kind (filled in here).
    """
    bad = set(ablate) - set(ABLATIONS)
    if bad:
        raise ValueError(f'unknown ablation {bad}')
    label, kinds = {}, {} if kinds is None else kinds
    internal = set()

    def join(ws):
        return PRIV if any(label[w] == PRIV for w in ws) else PUB

    def define(w, lab):
        if w in label:
            raise TypeError_(f'wire {w} defined twice (SSA)')
        label[w] = lab

    def visit(node, inside_release=False):
        if isinstance(node, Input):
            define(node.out, INPUT_LABEL[node.kind])
            kinds[node.out] = node.kind
        elif isinstance(node, Op):
            reads = list(node.args)
            if 'mask_only' in ablate:
                reads = [a for a in reads if a not in node.secondary]
            if node.weight and 'weights_not_wires' not in ablate:
                reads.append(node.weight)
            for a in node.args + ([node.weight] if node.weight else []):
                if a not in label:
                    raise TypeError_(f'{node.out} reads undefined {a}')
            if not set(node.secondary) <= set(node.args):
                # secondary only annotates real args; it has no other semantics
                raise TypeError_(f'{node.out}: secondary must be a subset of args')
            define(node.out, PRIV if inside_release else join(reads))
            if inside_release:
                internal.add(node.out)
        elif isinstance(node, Release):
            if 'spec_reads_anything' not in ablate:
                for a in node.spec_args:
                    if kinds.get(a) not in SPEC_READABLE:
                        raise TypeError_(
                            f'release {node.spec} spec reads {a} '
                            f'({kinds.get(a)}); only public task and authorized data')
            if contract_key(node) not in contracts and 'trust_release' not in ablate:
                raise TypeError_(f'release {node.spec} has no verified contract')
            defined = {sub.out for sub in node.impl if isinstance(sub, Op)}
            if node.impl_out not in defined or (node.cost and node.cost not in defined):
                raise TypeError_(f'release {node.spec}: impl_out/cost must be defined inside impl')
            for sub in node.impl:
                visit(sub, inside_release=True)
            if node.cost:
                internal.add(node.cost)
            define(node.out, PUB)
        elif isinstance(node, Observe):
            if node.wire in internal and 'observe_internal' not in ablate:
                raise TypeError_(f'observes release-internal wire {node.wire}')
            if label[node.wire] != PUB and not (
                    node.wire in internal and 'observe_internal' in ablate):
                raise TypeError_(f'observes private wire {node.wire}')
        else:
            raise TypeError_(f'unknown node {node!r}')

    for node in program:
        visit(node)
    return label


def run(program, env, fns):
    """Concrete interpreter. env: input values; fns: name -> python callable.

    Neural ops receive the weight value as first argument when present.
    Returns (all wire values, observation tuple).
    """
    val = dict(env)
    obs = []

    def step(node):
        if isinstance(node, Input):
            if node.out not in val:
                raise KeyError(f'missing input {node.out}')
        elif isinstance(node, Op):
            args = [val[a] for a in node.args]
            if node.weight:
                args = [val[node.weight]] + args
            val[node.out] = fns[node.fn](*args)
        elif isinstance(node, Release):
            for sub in node.impl:
                step(sub)
            val[node.out] = val[node.impl_out]
        elif isinstance(node, Observe):
            obs.append(val[node.wire])

    for node in program:
        step(node)
    return val, tuple(obs)
