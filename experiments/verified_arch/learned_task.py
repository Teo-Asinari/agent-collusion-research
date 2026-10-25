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
try:
    from scipy.special import ndtr  # used for the recorded results
except ImportError:  # test-only fallback; may differ from scipy in the last bits
    import math
    _erf = np.vectorize(math.erf)

    def ndtr(x):
        return 0.5 * (1 + _erf(np.asarray(x) / math.sqrt(2)))

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
