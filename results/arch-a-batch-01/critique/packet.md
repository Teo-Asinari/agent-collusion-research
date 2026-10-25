
<source path="research/workstreams/architecture/formal-model.md">
# Formal model: labeled learned/verified dataflow with contracted release

2026-10-24, Approach A batch 1. **Status: a small formal model with an informal (pen-and-paper) noninterference proof, per-instance z3 checks that quantify over every interpretation of the learned functions, explicit ablation counterexamples, one non-vacuous task, and a timing-channel analysis.** Not a mechanized general proof (no proof assistant was installed: the root disk had <1 GB free), not a trained language model, not a novelty claim. Code: [`experiments/verified_arch/`](../../../experiments/verified_arch/README.md). Results: `results/arch-a-batch-01/`.

## 1. Model

A program is a straight-line SSA list of nodes (`ir.py`):

- `Input(w, kind)`: kinds `public_task`, `public_rand`, `public_weight` (public); `authorized` (private task data z), `payload` (m), `private_weight`, `private_rand`, `private_state` (private).
- `Op(w, fn, args, weight, secondary)`: `fn` is either trusted fixed code or an **opaque** learned function; `weight` names a parameter wire. Parameters, gradients, optimizer state, random tapes and counters are ordinary wires, so a training step is just `Op(phi2, Sgd, [phi, g])`.
- `Release(w, spec, spec_args, impl, impl_out, cost)`: the only private-to-public edge. `impl` is a sub-program (may contain learned ops and read anything); `spec` is a declared function of `spec_args`.
- `Observe(w)`: receiver-visible wire.

**Typing rules (full checker).** Label of an `Op` output = join of labels of *all* reads, including `secondary` args and the weight wire. Release-internal wires are private and unobservable. A `Release` output is public iff (R1) its `spec_args` are only `public_task` or `authorized` inputs, and (R2) the pair (spec, impl) has a verified contract `impl_out = spec(spec_args)` for **all** inputs and **all** interpretations of opaque functions. `Observe` requires a public, non-internal wire.

**Semantics.** Given an input valuation ρ and an interpretation ι of opaque symbols, values are computed in order. Varying private weight wires under a fixed ι covers varying private learned functions (the symbol is uninterpreted and receives the weight as an argument).

## 2. Theorem 1 (noninterference modulo declared release, all weights)

Let ⊢ P under verified contracts C. Define ρ₁ ~ ρ₂ iff ρ₁, ρ₂ agree on every public input and every Release's spec value agrees. Then for **every** interpretation ι, ρ₁ ~ ρ₂ implies obs(P, ρ₁, ι) = obs(P, ρ₂, ι).

*Proof (pen-and-paper, not machine-checked for general P).* Induct over top-level nodes with invariant: every top-level wire labeled public has equal values in both runs. Public input: by ~. Public `Op`: by the join rule every read (args, secondary args, weight) is public and earlier, hence equal; the same trusted function or the same ι(fn) yields equal outputs. `Release`: by contract (R2), its value equals spec(spec_args) in each run, for this ι and every input; by ~ the spec values agree. Release-internal wires are labeled private, so no public op can read them. `Observe` reads only public wires. ∎

**Role of (R1).** Without it the theorem stays formally true but vacuous: a spec may itself read m (ablation `spec_reads_anything`). With (R1), ~ is a condition on public inputs and authorized data only: the declared disclosure cannot mention payload, private weights, private randomness or private state. *Which* function of z is authorized remains the task owner's decision; the checker only enforces that it is a function of z.

**Lemma 2 (sequential/parallel composition and multi-session histories).** If P₁ and P₂ are well-typed, and P₂ reads P₁'s outputs with their labels preserved (public outputs as public inputs, private carried state as `private_state`), then the concatenation is well-typed and Theorem 1 applies with ~ over the tuple of all releases. Proof: concatenation of SSA programs with fresh names; each node's typing premise only refers to earlier labels, which are unchanged. Unrolling k sessions gives the history version: equal public history plus equal per-session authorized releases implies equal full transcripts. The earlier **XOR-history attack** (release private r, later release r⊕m) is rejected statically: releasing r needs a spec reading `private_rand`, and r⊕m needs one reading `payload`, both violating (R1).

**Lemma 3 (release contracts discharged).**

| Release | Claim | Evidence |
| --- | --- | --- |
| Witness cell: learned predictor picks a candidate j; check P(q,z_j); early-exit scan of the rest | `impl = OR_i P(q,z_i)` for every predictor, every predicate P, every input | z3 `unsat` for N=1..8 with predictor and P uninterpreted; general N by the obvious argument (v becomes true only through some true P(q,z_i); if no early exit, all i≠j are scanned) |
| Certified learned index: verifier checks \|Pred(k_i)−i\| ≤ e for all stored keys; if it passes, binary-search only the clipped window around Pred(q), else full binary search | `impl = [q ∈ z]` for every Pred, every e, every sorted key array | z3 `unsat` for N=4,8,16; general N: window search is sound (returns true only on an equality probe) and, when the certificate holds and q=k_i, i lies in the window |
| Same index **without** the verifier | — | z3 `sat` (N=8): learned output decides the answer |
| Shortest-route cost after one learned-order sweep | — | z3 `sat` (n=3): order-dependent |
| Shortest-route cost after n−1 full sweeps | schedule-independent | Not z3-discharged: the n=3, two-sweep query did not finish within ~10 min. Rests on the earlier informal proof and exhaustive 614,227-schedule check. |

Direct cross-check: z3 also proves the whole witness program noninterferent (two-world query, every opaque function free) for N=1..8, both against arbitrary private differences and payload-only differences.

## 3. Invariant ablations

Each ablation switches off one rule. The program is rejected by the full checker, accepted by the ablated one, and z3 finds a **payload-only** counterexample: two worlds identical except m, with different observations (N=2 and N=4; `prove.json`).

| Ablated invariant | Channel | Scripted decoder, learned-index task (test acc., 100 sessions) |
| --- | --- | --- |
| `mask_only`: join ignores residual/normalization args | public readout normalized with statistics of a private activation | 1.00 |
| `weights_not_wires`: weight args not in the join | public readout fine-tuned on a payload-dependent private gradient | 0.96 |
| `trust_release`: no contract required | release the predictor-chosen index / trust the window without verifier | 1.00 |
| `spec_reads_anything`: (R1) off | declared spec = F ⊕ m, contract holds | z3 only |
| `observe_internal`: release internals observable | work count of the witness/index search | 0.97 (see §5) |

**Random-program search** (5,000 random programs, N=2, seed 1, with good, unverified and payload-reading release variants): the full checker accepted 771, **0 leaky** by z3. Each ablated checker accepted more programs, of which 178 (mask_only), 448 (weights_not_wires), 200 (trust_release), 188 (spec_reads_anything) and 281 (observe_internal) were leaky (payload-only leaks 39/4/200/188/281). This is a search for counterexamples to Theorem 1 at small size, not a proof.

## 4. Non-vacuous task

Learned-index membership on N=16,384 private lognormal keys, 4,000 queries (half present). Model: two-stage regression index (Gaussian-CDF routing on log-key, 1,024 linear leaves, 2,050 parameters), trained on private z. Certified radius e=13. The release value was correct on all queries. Mean probes: **3.69 learned vs 13.76 plain binary search**. Authorized private data affects the output (F is nonconstant in z); the payload cannot affect any R0 observation (paired check: 50/50 sessions identical under opposite payloads).

Honest limits: the learned model is a regression index, not a transformer (the theory treats it as an opaque function, so this is a choice of test vehicle). A 32-unit tanh MLP on raw keys certified only e=10,820, with no saving. Learned indexes with error bounds are prior art (Kraska et al., SIGMOD 2018, cited from memory, not re-read in this pass). Per-query model evaluation, fit and the O(N) certificate are extra costs not counted in probes. No wall-clock comparison is made.

## 5. Timing / work-count channel

**Receiver models.** Theorem 1 is stated for **R0**: the receiver sees `Observe` wires at fixed logical slots and nothing else. **R1** adds per-query visible cost; we use the probe count as a deterministic proxy for completion time. Real hardware timing (caches, model-evaluation time, contention, power) is **not** modeled. Under R1 the release cost is an observable wire, so Theorem 1 covers R1 only if that cost is itself a declared function of public/authorized data, a "cost release" subject to (R1)/(R2).

**Attack.** The all-weights value guarantee says nothing about work. Scripted adversarial parameters: m=0 uses the honest fit (e=7 on the leakage dataset); m=1 shifts leaf intercepts by up to ±60 (e=62–67). The model is still certified, so every value is still exact, but probe counts differ. Decoder from per-session mean visible cost: **0.97 test accuracy** unpadded. Paired exact check: 0/50 identical views.

**Defenses** (utility and decoder: N=16,384, decoder over 200 sessions × 16 queries with one payload bit per session, tested on 100; paired exact check: N=4,096, 50 session pairs):

| Defense | Payload decoder (test) | Paired views identical | Visible cost / query | Internal probes | What survives |
| --- | --- | --- | --- | --- | --- |
| Unpadded | 0.97 | 0/50 | 3.69 | 3.69 | full speedup, leaks |
| Pad to worst case (⌊log₂N⌋+1 = 15) | 0.53 (chance) | 50/50 | 15 | 3.69 | no visible gain over binary search; internal work saving only if reclaimed invisibly |
| Pad to certified radius, **sender-chosen** parameters | **1.00** | 0/50 | 5 | 3.69 | leaks: e is chosen by the weights. Capacity ≤ log₂(#distinct padded costs) ≤ log₂15 ≈ 3.9 bits **per parameter choice** (cost is constant across queries for fixed e); with one public radius bucket, ≤ 1 bit (pass/fail) per choice. Bounded, not zero |
| Pad to radius of a **canonical trusted fit** of z | 0.53 | 50/50 | 5 | 3.69 | 3× lower visible cost than worst-case padding, zero payload flow. But cost = g(z) discloses the radius bucket of z's fit (≤ ~3.9 bits about z), which must be added to the declared release, and the fit procedure becomes trusted |
| Batch / fixed-slot release (B answers at slot B·15) | 0.53 | constant by construction | 15 (latency) | 3.69 | no latency or throughput gain visible to the receiver; internal savings only |

**Conclusion.** Exact values are guaranteed for all weights. Visible work is not. Visible learned speedup survives only if the parameters that determine work are not sender-controlled: a trusted, deterministic, sender-independent training procedure whose output depends on z alone, with its cost profile declared as an authorized disclosure. Otherwise padding (worst case or fixed slot) removes the visible benefit, and radius-dependent padding leaves a bounded per-parameter-choice channel. For agent collusion, an untrusted agent's own learned heuristics cannot buy receiver-visible efficiency without opening a channel of that size. This mirrors classical timing-channel mitigation (padding to worst case; leakage bounded by the number of distinct schedules, e.g. Agat 2000; Askarov–Zhang–Myers CCS 2010). Those are cited from memory as **unverified leads**, not re-read in this pass, and the observation is not claimed new.

## 6. Prior art and novelty status

- **Volpano–Smith-style IFC typing / LLMbda (v2).** Theorem 1 is a standard noninterference-by-typing argument. LLMbda already mechanizes probabilistic IFC for an LLM calculus. Our proof is not a new IFC result.
- **Tiwari et al. (USENIX Sec 2024).** Already uses architecture/training partitioning for data-domain IFC. Treating parameters and optimizer state as labeled wires is the same concern stated in dataflow form; not claimed new.
- **Vehicle.** Neural-to-symbolic specification/proof bridges. Our contracts need no neural specification at all (they hold for every weight setting), which avoids Vehicle's embedding gap but restricts what the learned part may decide.
- **Delimited release; algorithms with predictions (Polak–Schmidt); learned indexes; certifying algorithms.** Supply the release-by-contract and predict-verify-fallback ingredients.
- **Candidate delta (unverified):** combining (i) all-weights value contracts for learned computation inside the release, (ii) parameters as labeled wires, and (iii) the explicit split between an all-weights *value* guarantee and a trusted-learner requirement for *visible-work* guarantees, demonstrated with machine-found counterexamples for each removed invariant. A literature check for (iii) in the timing-channel and learned-systems literature is needed before claiming anything.

## 7. Limitations

- General-N proofs are pen-and-paper. z3 covers instance sizes N≤8 (witness), N≤16 (index), n=3 (sweep counterexample), plus 5,000 random N=2 programs.
- Deterministic semantics only. Public randomness is a public input wire, so the coupling argument is built in, but probabilistic programs with private sampling feeding releases are not modeled.
- No hardware refinement. R1 uses a deterministic probe proxy.
- The authorized function is trusted. Sender-chosen queries or falsified z are out of scope.
- The scripted adversary shows channel capacity, not autonomous discovery or exploitation.
- The useful task is a learned index, not language generation. The architecture admits any opaque public model *after* the release, but a private learned model may only influence values through a verified contract, which excludes free-form private generation.

</source>

<source path="experiments/verified_arch/ir.py">
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

</source>

<source path="experiments/verified_arch/programs.py">
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

</source>

<source path="experiments/verified_arch/learned_task.py">
"""Non-vacuous task: certified learned-index membership, plus the timing channel.

Private data z: N sorted distinct keys. Public task: query q. Authorized release
F(q, z) = [q in z], a nonconstant function of private data. A learned position
model (two-stage regression index: Gaussian-CDF routing on log-key, 1024 linear
leaves) predicts a key's position. A trusted verifier checks a claimed global
error radius e against every stored key; if it passes, a query searches only the
window around its prediction, otherwise full binary search. The released VALUE
equals F for every parameter setting (z3: prove.py learned_index, N<=16; general
argument in formal-model.md). The learned-index idea is prior art (Kraska et
al., 2018); this file is a test vehicle, not a contribution claim.

Receiver models:
  R0  receiver sees released values at fixed logical slots only.
  R1  receiver also sees per-query visible cost (probe count, a deterministic
      proxy for completion time). Real hardware timing is NOT modeled.

Timing defenses compared (cost = what an R1 receiver sees):
  unpadded        actual probes                       (internal work = visible)
  pad_worst       floor(log2 N)+1 probes always
  pad_radius      floor(log2(2e+1))+1 if certified, else worst; e set by weights
  canonical       pad_radius, but parameters come from a trusted deterministic
                  fit of z (sender cannot choose them); cost is then g(z), a
                  disclosure that must be added to the declared release
  batch_slot      B answers released together at slot B*worst; only the slot is seen

Encoders are scripted adversarial parameters: this is a capability/boundary
check, not evidence about autonomous collusion.

Run: python learned_task.py  (writes ../../results/arch-a-batch-01/learned_task.json)
"""
import json
from pathlib import Path

import numpy as np
from scipy.special import ndtr

OUT = Path(__file__).resolve().parents[2] / 'results/arch-a-batch-01'
LEAVES = 1024


# ---------------- trusted primitives ----------------

def bsearch(keys, q, lo, hi, probes):
    lo, hi = max(lo, 0), min(hi, len(keys) - 1)
    while lo <= hi:
        mid = (lo + hi) // 2
        probes[0] += 1
        if keys[mid] == q:
            return True
        if keys[mid] < q:
            lo = mid + 1
        else:
            hi = mid - 1
    return False


def worst(n):
    return int(np.floor(np.log2(n))) + 1


def window_bound(e, n):
    return min(int(np.floor(np.log2(2 * e + 1))) + 1, worst(n))


def certify(keys, model, e):
    """Trusted O(N) check that every stored key lies within e of its prediction."""
    return bool(np.all(np.abs(model(keys) - np.arange(len(keys))) <= e))


def release(keys, q, model, e, cert):
    """Exact membership for every `model`/`e`; returns (answer, internal probes)."""
    probes = [0]
    if cert:
        p = int(model(np.array([q]))[0])
        return bsearch(keys, q, p - e, p + e, probes), probes[0]
    return bsearch(keys, q, 0, len(keys) - 1, probes), probes[0]


def visible_cost(mode, n, e, cert, probes):
    if mode == 'unpadded':
        return probes
    if mode == 'pad_worst':
        return worst(n)
    if mode in ('pad_radius', 'canonical'):
        return window_bound(e, n) if cert else worst(n)
    raise ValueError(mode)


# ---------------- learned component ----------------

def fit_index(keys, leaves=LEAVES):
    """Deterministic least-squares fit; returns (model, certified radius)."""
    n = len(keys)
    lk = np.log(keys.astype(float))
    pos = np.arange(n)
    mu, sd = lk.mean(), lk.std()
    route = lambda l: np.clip((ndtr((l - mu) / sd) * leaves).astype(int), 0, leaves - 1)
    leaf = route(lk)
    coef = np.zeros((leaves, 2))
    for i in range(leaves):
        s = leaf == i
        if s.sum() >= 2:
            coef[i] = np.polyfit(lk[s], pos[s], 1)
        elif s.sum() == 1:
            coef[i] = [0.0, pos[s][0]]

    def model(qs, coef=coef):
        l = np.log(np.maximum(np.asarray(qs, float), 1.0))
        k = route(l)
        return np.rint(coef[k, 0] * l + coef[k, 1]).astype(int)

    e = int(np.max(np.abs(model(keys) - pos)))
    return model, e, (route, coef)


def perturbed(keys, parts, delta, rng):
    """Adversarial parameters: same routing, leaf intercepts shifted by up to
    +/-delta. Still a valid (certifiable) model, just with a larger radius."""
    route, coef = parts
    c2 = coef.copy()
    c2[:, 1] += rng.integers(-delta, delta + 1, len(c2))

    def model(qs):
        l = np.log(np.maximum(np.asarray(qs, float), 1.0))
        k = route(l)
        return np.rint(c2[k, 0] * l + c2[k, 1]).astype(int)

    e = int(np.max(np.abs(model(keys) - np.arange(len(keys)))))
    return model, e


# ---------------- data ----------------

def make_keys(n, rng):
    raw = np.unique(np.rint(rng.lognormal(10, 1.0, 4 * n)).astype(np.int64))
    return np.sort(rng.choice(raw, n, replace=False))


def queries(keys, count, rng, keyset=None):
    keyset = set(keys.tolist()) if keyset is None else keyset
    present = rng.choice(keys, count // 2)
    absent = []
    while len(absent) < count - count // 2:
        c = int(rng.integers(keys[0] - 10, keys[-1] + 10))
        if c not in keyset:
            absent.append(c)
    qs = np.concatenate([present, np.array(absent)])
    rng.shuffle(qs)
    return qs


# ---------------- utility under honest parameters ----------------

def utility(seed=0, n=1 << 14, nq=4000):
    rng = np.random.default_rng(seed)
    keys = make_keys(n, rng)
    keyset = set(keys.tolist())
    model, e, _ = fit_index(keys)
    cert = certify(keys, model, e)
    qs = queries(keys, nq, rng, keyset)
    internal, binary = [], []
    for q in qs:
        truth = int(q) in keyset
        a, k = release(keys, int(q), model, e, cert)
        assert a == truth
        internal.append(k)
        b = [0]
        assert bsearch(keys, int(q), 0, n - 1, b) == truth
        binary.append(b[0])
    vis = {m: float(np.mean([visible_cost(m, n, e, cert, k) for k in internal]))
           for m in ('unpadded', 'pad_worst', 'pad_radius', 'canonical')}
    vis['batch_slot'] = float(worst(n))
    return {
        'n_keys': n, 'queries': nq, 'present_fraction': 0.5, 'leaves': LEAVES,
        'certified_radius_e': e, 'certificate_passed': cert,
        'release_value_correct_all_queries': True,
        'mean_internal_probes_learned': float(np.mean(internal)),
        'mean_probes_plain_binary_search': float(np.mean(binary)),
        'mean_visible_cost_by_defense': vis,
        'per_query_model_cost': 'one normal-CDF evaluation, one leaf lookup, one multiply-add (constant)',
        'one_time_cost': {'fit': 'least squares per leaf', 'certificate_model_evals': n,
                          'model_parameters': 2 * LEAVES + 2},
        'note': ('Probes are trusted-primitive reads. Model evaluation is a constant '
                 'per-query cost not included in probe counts. No wall-clock or '
                 'hardware comparison is claimed. A 32-unit tanh MLP on raw keys '
                 'was tried first and certified only e=10820 (no useful saving).'),
    }


# ---------------- payload decoding ----------------

def threshold_decoder(feats, labels):
    """Best single-coordinate threshold on half the sessions, tested on the rest."""
    idx = np.arange(len(labels))
    tr, te = idx % 4 < 2, idx % 4 >= 2
    F, y = np.array(feats, float), np.array(labels)
    best, rule = 0.5, None
    for d in range(F.shape[1]):
        for thr in np.unique(F[tr, d]):
            for sign in (1, -1):
                acc = np.mean((sign * (F[tr, d] - thr) > 0) == y[tr])
                if acc > best:
                    best, rule = acc, (d, thr, sign)
    if rule is None:
        return float(best), 0.5
    d, thr, sign = rule
    return float(best), float(np.mean((sign * (F[te, d] - thr) > 0) == y[te]))


def payload_channels(seed=1, n=1 << 14, sessions=200, per_session=16, delta=60):
    """One balanced payload bit per session (one parameter choice per session).

    Value-channel ablations reuse the IR invariants; timing rows use R1.
    """
    rng = np.random.default_rng(seed)
    keys = make_keys(n, rng)
    keyset = set(keys.tolist())
    honest, e0, parts = fit_index(keys)
    phi0 = np.array([0.7, 0.2, 0.5])

    def readout(phi, a, r, extra=0.0):
        return round(float(np.tanh(phi[0] * a + phi[1] * r + phi[2] * extra)), 9)

    rows = {k: [] for k in ('R0_full', 'R1_unpadded', 'R1_pad_worst', 'R1_pad_radius',
                            'R1_canonical', 'R1_batch_slot', 'value_trust_release',
                            'value_weights_not_wires', 'value_mask_only')}
    labels, radii = [], {0: [], 1: []}
    for s in range(sessions):
        m = s % 2
        labels.append(m)
        # Sender-controlled parameters: honest fit for m=0, perturbed for m=1.
        if m == 0:
            model, e = honest, e0
        else:
            model, e = perturbed(keys, parts, delta, rng)
        radii[m].append(e)
        cert = certify(keys, model, e)
        qs = queries(keys, per_session, rng, keyset)
        rs = rng.normal(size=per_session)
        vals, costs = [], {k: [] for k in ('unpadded', 'pad_worst', 'pad_radius')}
        canon_costs, ys = [], []
        tr_vals, wnw, mo = [], [], []
        for q, r in zip(qs, rs):
            a, k = release(keys, int(q), model, e, cert)
            a = int(a)
            vals.append(a)
            ys.append(readout(phi0, a, r))
            for mode in costs:
                costs[mode].append(visible_cost(mode, n, e, cert, k))
            # canonical: timing path uses the trusted fit of z, never sender params
            ca, ck = release(keys, int(q), honest, e0, True)
            canon_costs.append(visible_cost('canonical', n, e0, True, ck))
            # value ablations (scripted, same payload bit)
            p = int(model(np.array([q]))[0]) + (0 if m == 0 else 10 * n)
            pr = [0]
            tr_vals.append(int(bsearch(keys, int(q), p - e, p + e, pr)))
            wnw.append(readout(phi0 + 0.5 * m * np.array([1, 0, 0]), a, r))
            mo.append(readout(phi0, a, r, extra=3.0 * m))
        rows['R0_full'].append((np.mean(vals), np.mean(ys)))
        for mode in costs:
            rows[f'R1_{mode}'].append((np.mean(vals), np.mean(ys), np.mean(costs[mode])))
        rows['R1_canonical'].append((np.mean(vals), np.mean(ys), np.mean(canon_costs)))
        rows['R1_batch_slot'].append((np.mean(vals), np.mean(ys), per_session * worst(n)))
        rows['value_trust_release'].append((np.mean(tr_vals),))
        rows['value_weights_not_wires'].append((np.mean(vals), np.mean(wnw)))
        rows['value_mask_only'].append((np.mean(vals), np.mean(mo)))
    dec = {}
    for k, feats in rows.items():
        tr, te = threshold_decoder(feats, labels)
        dec[k] = {'decoder_train_acc': tr, 'decoder_test_acc': te}
    return {
        'n_keys': n, 'sessions': sessions, 'queries_per_session': per_session,
        'adversary': f'm=0 honest fit; m=1 leaf intercepts shifted by up to +/-{delta} (still certified)',
        'certified_radius': {'m0_honest': sorted(set(radii[0])),
                             'm1_range': [min(radii[1]), max(radii[1])]},
        'decoders': dec,
        'note': ('Single-threshold decoder on session means. Failure of this decoder '
                 'is not a security argument; zero-leak rows rely on the cost being a '
                 'constant (pad_worst, batch_slot) or a function of z alone (canonical).'),
    }


def paired_exact(seed=2, n=1 << 12, sessions=50, per_session=16, delta=60):
    """Exact check: same z, queries and tape, opposite payload. Compare full views."""
    rng = np.random.default_rng(seed)
    keys = make_keys(n, rng)
    keyset = set(keys.tolist())
    honest, e0, parts = fit_index(keys)
    adv, e1 = perturbed(keys, parts, delta, rng)
    out = {}
    for mode in ('R0_values', 'unpadded', 'pad_worst', 'pad_radius', 'canonical'):
        same = 0
        r2 = np.random.default_rng(seed + 7)
        for _ in range(sessions):
            qs = queries(keys, per_session, r2, keyset)
            views = []
            for model, e in ((honest, e0), (adv, e1)):
                cert = certify(keys, model, e)
                v = []
                for q in qs:
                    a, k = release(keys, int(q), model, e, cert)
                    if mode == 'R0_values':
                        v.append(int(a))
                    elif mode == 'canonical':
                        _, ck = release(keys, int(q), honest, e0, True)
                        v.append((int(a), visible_cost(mode, n, e0, True, ck)))
                    else:
                        v.append((int(a), visible_cost(mode, n, e, cert, k)))
                views.append(tuple(v))
            same += views[0] == views[1]
        out[mode] = f'{same}/{sessions} identical'
    out['radii'] = {'honest': e0, 'adversarial': e1}
    return out


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rep = {'utility': utility(), 'payload_channels': payload_channels(),
           'paired_exact': paired_exact()}
    (OUT / 'learned_task.json').write_text(json.dumps(rep, indent=2) + '\n')
    print(json.dumps(rep, indent=2))


if __name__ == '__main__':
    main()

</source>

<source path="results/arch-a-batch-01/prove.json (excerpt)">
{
 "learned_index": {
  "n4": "unsat",
  "n8": "unsat",
  "n16": "unsat",
  "n8_uncertified_window": "sat"
 },
 "shortest_path": {
  "n3_sweeps1": "sat"
 },
 "fuzz": {
  "trials": 5000,
  "n": 2,
  "seed": 1,
  "stats": {
   "full": {
    "accepted": 771,
    "accepted_and_leaky": 0,
    "accepted_and_payload_leaky": 0
   },
   "mask_only": {
    "accepted": 949,
    "accepted_and_leaky": 178,
    "accepted_and_payload_leaky": 39
   },
   "weights_not_wires": {
    "accepted": 1219,
    "accepted_and_leaky": 448,
    "accepted_and_payload_leaky": 4
   },
   "trust_release": {
    "accepted": 1031,
    "accepted_and_leaky": 200,
    "accepted_and_payload_leaky": 200
   },
   "spec_reads_anything": {
    "accepted": 1019,
    "accepted_and_leaky": 188,
    "accepted_and_payload_leaky": 188
   },
   "observe_internal": {
    "accepted": 1052,
    "accepted_and_leaky": 281,
    "accepted_and_payload_leaky": 281
   }
  },
  "first_leaky_example": {
   "weights_not_wires": "[Release(out='a', spec='exists_2', spec_args=['q', 'z1', 'z2'], impl=[Op(out='j', fn='NetPred', args=['q', 'c', 'm'], kind='neural', weight='theta', secondary=[]), Op(out='jc', fn='clamp1_2', args=['j'], kind='trusted', weight=None, secondary=[]), Op(out='p1', fn='P', args=['q', 'z1'], kind='trusted', weight=None, secondary=[]), Op(out='p2', fn='P', args=['q', 'z2'], kind='trusted', weight=None, secondary=[]), Op(out='v0', fn='select_2', args=['jc', 'p1', 'p2'], kind='trusted', weight=None, secondary=[]), Op(out='k0', fn='one', args=[], kind='trusted', weight=None, secondary=[]), Op(out='ji1',",
   "trust_release": "[Op(out='w0', fn='Net1w', args=['phi'], kind='neural', weight='theta', secondary=['phi']), Op(out='u1', fn='Net1w', args=['theta'], kind='neural', weight='w0', secondary=['theta']), Release(out='a', spec='exists_2', spec_args=['q', 'z1', 'z2'], impl=[Op(out='j', fn='NetPred', args=['q', 'c', 'm'], kind='neural', weight='theta', secondary=[]), Op(out='jc', fn='clamp1_2', args=['j'], kind='trusted', weight=None, secondary=[]), Op(out='p1', fn='P', args=['q', 'z1'], kind='trusted', weight=None, secondary=[]), Op(out='p2', fn='P', args=['q', 'z2'], kind='trusted', weight=None, secondary=[]), Op(ou",
   "spec_reads_anything": "[Op(out='u0', fn='Net2w', args=['q', 'r'], kind='neural', weight='phi', secondary=['q', 'r']), Op(out='u1', fn='Net1w', args=['u0'], kind='neural', weight='phi', secondary=['u0']), Op(out='u2', fn='Net1', args=['u0'], kind='neural', weight=None, secondary=[]), Release(out='a', spec='existsxor_2', spec_args=['q', 'z1', 'z2', 'm'], impl=[Op(out='j', fn='NetPred', args=['q', 'c', 'm'], kind='neural', weight='theta', secondary=[]), Op(out='jc', fn='clamp1_2', args=['j'], kind='trusted', weight=None, secondary=[]), Op(out='p1', fn='P', args=['q', 'z1'], kind='trusted', weight=None, secondary=[]), O",
   "mask_only": "[Release(out='a', spec='exists_2', spec_args=['q', 'z1', 'z2'], impl=[Op(out='j', fn='NetPred', args=['q', 'c', 'm'], kind='neural', weight='theta', secondary=[]), Op(out='jc', fn='clamp1_2', args=['j'], kind='trusted', weight=None, secondary=[]), Op(out='p1', fn='P', args=['q', 'z1'], kind='trusted', weight=None, secondary=[]), Op(out='p2', fn='P', args=['q', 'z2'], kind='trusted', weight=None, secondary=[]), Op(out='v0', fn='select_2', args=['jc', 'p1', 'p2'], kind='trusted', weight=None, secondary=[]), Op(out='k0', fn='one', args=[], kind='trusted', weight=None, secondary=[]), Op(out='ji1',",
   "observe_internal": "[Op(out='u0', fn='Net2w', args=['phi', 'r'], kind='neural', weight='phi', secondary=[]), Op(out='w1', fn='Net1w', args=['q'], kind='neural', weight='phi', secondary=[]), Op(out='u2', fn='Net2w', args=['phi', 'q'], kind='neural', weight='w1', secondary=[]), Op(out='u3', fn='Net3w', args=['w1', 'z2', 'r'], kind='neural', weight='w1', secondary=['z2']), Op(out='w4', fn='Net2w', args=['w1', 'phi'], kind='neural', weight='w1', secondary=[]), Release(out='a', spec='exists_2', spec_args=['q', 'z1', 'z2'], impl=[Op(out='j', fn='NetPred', args=['q', 'c', 'm'], kind='neural', weight='theta', secondary=["
  }
 },
 "witness_n2": {
  "contract": {
   "exists_2:v": "unsat"
  },
  "typecheck_full": "accepted",
  "direct_ni": "unsat",
  "direct_ni_payload_only": "unsat",
  "ablations": {
   "mask_only": {
    "contracts": {
     "exists_2:v": "unsat"
    },
    "typecheck_full": "rejected: observes private wire y",
    "typecheck_with_this_ablation": "accepted",
    "ni_counterexample": {
     "result": "sat",
     "world_A_obs": [
      "1",
      "24"
     ],
     "world_B_obs": [
      "1",
      "26"
     ],
     "payload_A_B": [
      "0",
      "1"
     ]
    },
    "payload_only_counterexample": {
     "result": "sat",
     "world_A_obs": [
      "1",
      "20"
     ],
     "world_B_obs": [
      "1",
      "22"
     ],
     "payload_A_B": [
      "0",
      "1"
     ]
    }
   },
   "weights_not_wires": {
    "contracts": {
     "exists_2:v": "unsat"
    },
    "typecheck_full": "rejected: observes private wire y",
    "typecheck_with_this_ablation": "accepted",
    "ni_counterexample": {
     "result": "sat",
     "world_A_obs": [
      "1",
      "22"
     ],
     "world_B_obs": [
      "1",
      "29"
     ],
     "payload_A_B": [
      "0",
      "1"
     ]
    },
    "payload_only_counterexample": {
     "result": "sat",
     "world_A_obs": [
      "0",
      "20"
     ],
     "world_B_obs": [
      "0",
      "23"
     ],
     "payload_A_B": [
      "0",
      "1"
     ]
    }
   },
   "trust_release": {
    "contracts": {
     "exists_2:leak": "sat"
    },
    "typecheck_full": "rejected: release exists_2 has no verified contract",
    "typecheck_with_this_ablation": "accepted",
    "ni_counterexample": {
     "result": "sat",
     "world_A_obs": [
      "2",
      "15"
     ],
     "world_B_obs": [
      "1",
      "16"
     ],
     "payload_A_B": [
      "1",
      "1"
     ]
    },
    "payload_only_counterexample": {
     "result": "sat",
     "world_A_obs": [
      "1",
      "11"
     ],
     "world_B_obs": [
      "2",
      "12"
     ],
     "payload_A_B": [
      "1",
      "0"
     ]
    }
   },
   "spec_reads_anything": {
    "contracts": {
     "existsxor_2:vx": "unsat"
    },
    "typecheck_full": "rejected: release existsxor_2 spec reads m (payload); only public task and authorized data",
    "typecheck_with_this_ablation": "accepted",
    "ni_counterexample": {
     "result": "sat",
     "world_A_obs": [
      "1",
      "22"
     ],
     "world_B_obs": [
      "0",
      "23"
     ],
     "payload_A_B": [
      "0",
      "1"
     ]
    },
    "payload_only_counterexample": {
     "result": "sat",
     "world_A_obs": [
      "1",
      "0"
     ],
     "world_B_obs": [
      "0",
      "0"
     ],
     "payload_A_B": [
      "0",
      "1"
     ]
    }
   },
   "observe_internal": {
    "contracts": {
     "exists_2:v": "unsat"
    },
    "typecheck_full": "rejected: observes release-internal wire cost",
    "typecheck_with_this_ablation": "accepted",
    "ni_counterexample": {
     "result": "sat",
     "world_A_obs": [
      "1",
      "0",
      "2"
     ],
     "world_B_obs": [
      "1",
      "0",
      "1"
     ],
     "payload_A_B": [
      "0",
      "0"
     ]
    },
    "payload_only_counterexample": {
     "result": "sat",
     "world_A_obs": [
      "1",
      "18",
      "1"
     ],
     "world_B_obs": [
      "1",
      "18",
      "2"
     ],
     "payload_A_B": [
      "0",
      "1"
     ]
    }
   }
  }
 }
}
</source>