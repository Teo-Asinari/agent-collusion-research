"""Exact finite-field identification and learned bilinear hidden maps.

Exploratory structured-family check; see PLAN.md for frozen scope and controls.
No APIs, floating-point fitting, external datasets or gradient optimization.
"""
import argparse
import hashlib
import itertools
import json
import os
from pathlib import Path
import platform
import random
import subprocess
import tempfile
import time

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def training_points(d):
    points = [tuple([0]*d)]
    for i in range(d):
        for value in (1, 2):
            x = [0]*d
            x[i] = value
            points.append(tuple(x))
    for i in range(d):
        for j in range(i+1, d):
            x = [0]*d
            x[i] = x[j] = 1
            points.append(tuple(x))
    return points


def factor(matrix):
    """Q=UV over F3; pivot columns learn U, elimination learns V.

    This is a rank factorization, not a real-field eigendecomposition.
    Returns lists of learned hidden row vectors u_j and v_j.
    """
    d = len(matrix)
    reduced = [[v % 3 for v in row] for row in matrix]
    pivots = []
    for col in range(d):
        row = next((i for i in range(len(pivots), d) if reduced[i][col]), None)
        if row is None:
            continue
        k = len(pivots)
        reduced[k], reduced[row] = reduced[row], reduced[k]
        inv = pow(reduced[k][col], -1, 3)
        reduced[k] = [(v*inv) % 3 for v in reduced[k]]
        for i in range(d):
            if i != k:
                scale = reduced[i][col]
                reduced[i] = [(a-scale*b) % 3 for a, b in zip(reduced[i], reduced[k])]
        pivots.append(col)
    rank = len(pivots)
    if rank == 0:
        return [], []
    u = [[matrix[i][j] % 3 for j in pivots] for i in range(d)]
    augmented = [row[:] + [v % 3 for v in target] for row, target in zip(u, matrix)]
    for col in range(rank):
        row = next(i for i in range(col, d) if augmented[i][col])
        augmented[col], augmented[row] = augmented[row], augmented[col]
        inv = pow(augmented[col][col], -1, 3)
        augmented[col] = [(v*inv) % 3 for v in augmented[col]]
        for i in range(d):
            if i != col:
                scale = augmented[i][col]
                augmented[i] = [(a-scale*b) % 3 for a, b in zip(augmented[i], augmented[col])]
    return [list(column) for column in zip(*u)], [row[rank:] for row in augmented[:rank]]


def fit(inputs, labels):
    """Learner sees only labeled identification queries, never teacher weights."""
    if not inputs or len(inputs) != len(labels):
        raise ValueError('Empty/mismatched training observations')
    d = len(inputs[0])
    table = {}
    for x, y in zip(inputs, labels):
        if len(x) != d:
            raise ValueError('Inconsistent input dimension')
        key = tuple(int(v) % 3 for v in x)
        if key in table:
            raise ValueError('Duplicate semantic observation')
        table[key] = int(y) % 3
    if set(table) != set(training_points(d)):
        raise ValueError('Requires the declared identification queries')
    c = table[tuple([0]*d)]
    linear, diagonal = [], []
    for i in range(d):
        plus, minus = [0]*d, [0]*d
        plus[i], minus[i] = 1, 2
        a, b = table[tuple(plus)], table[tuple(minus)]
        linear.append((2*(a-b)) % 3)
        diagonal.append((2*(a+b-2*c)) % 3)
    matrix = [[0]*d for _ in range(d)]
    for i in range(d):
        matrix[i][i] = diagonal[i]
        for j in range(i+1, d):
            x = [0]*d
            x[i] = x[j] = 1
            cross = (table[tuple(x)]-c-linear[i]-linear[j]-diagonal[i]-diagonal[j]) % 3
            matrix[i][j] = matrix[j][i] = (2*cross) % 3
    u, v = factor(matrix)
    return {'constant':c, 'linear':linear, 'matrix':matrix, 'u':u, 'v':v}


def parameters(model):
    return [model['constant']] + model['linear'] + sum(model['u'], []) + sum(model['v'], [])


def predict(params, d, rank, inputs, modulus=9):
    x = np.asarray(inputs, dtype=np.int64)
    p = np.asarray(params, dtype=np.int64)
    out = p[0] + x @ p[1:1+d]
    if rank:
        u = p[1+d:1+d+rank*d].reshape(rank, d)
        v = p[1+d+rank*d:].reshape(rank, d)
        out = out + (((x @ u.T) % modulus) * ((x @ v.T) % modulus)).sum(axis=1)
    return out % modulus


def target(model, inputs):
    x = np.asarray(inputs, dtype=np.int64)
    return (model['constant'] + x @ np.asarray(model['linear'])
            + ((x @ np.asarray(model['matrix'])) * x).sum(axis=1)) % 3


def teacher(d, rank, seed):
    rng = random.Random(seed)
    w = np.array([[int(i == j) if j < rank else rng.randrange(3)
                   for j in range(d)] for i in range(rank)], dtype=np.int64)
    diagonal = np.array([rng.choice([1, 2]) for _ in range(rank)])
    q = ((w.T * diagonal) @ w) % 3
    return {'constant':rng.randrange(3), 'linear':[rng.randrange(3) for _ in range(d)],
            'matrix':q.tolist()}


def score(predictions, labels):
    correct = int(np.sum(predictions == labels))
    return {'correct':correct, 'total':len(labels), 'accuracy':correct/len(labels)}


def affine_erm(train_x, train_y):
    """Exhaustive ERM baseline ONLY, not the bilinear learner."""
    d = len(train_x[0])
    candidates = np.array(list(itertools.product(range(3), repeat=d+1)), dtype=np.int64)
    outputs = (candidates[:, :1] + candidates[:, 1:] @ np.array(train_x).T) % 3
    correct = np.sum(outputs == np.asarray(train_y)[None, :], axis=1)
    index = int(np.argmax(correct))
    return candidates[index], int(correct[index]), len(candidates)


def verify_lean(output, tasks):
    lines = ['import Bilinear', 'set_option maxRecDepth 200000',
             'set_option maxHeartbeats 0', 'namespace LearnedBilinear']
    for task in tasks:
        if task['dimension'] != 4:
            continue
        ident = task['id']
        t, model = task['teacher'], task['learned']
        lines += [f'def parameters_{ident} : List Nat := {parameters(model)}',
                  f'theorem correct_{ident} : ∀ a b c d : Fin 3,',
                  f'  Bilinear.predict 4 {len(model["u"])} 3 parameters_{ident} [a.val,b.val,c.val,d.val] =',
                  f'  Bilinear.target 4 3 {t["constant"]} {t["linear"]} {sum(t["matrix"], [])} [a.val,b.val,c.val,d.val] := by decide',
                  f'#print axioms correct_{ident}']
    lines.append('end LearnedBilinear')
    certificate = output/'Learned.lean'
    certificate.write_text('\n'.join(lines)+'\n')
    logs = []
    lean = os.environ.get('LEAN_BIN', '/home/tasinari/.elan/bin/lean')
    version = subprocess.run([lean, '--version'], capture_output=True, text=True, check=True)
    with tempfile.TemporaryDirectory(prefix='bilinear-lean-') as directory:
        env = dict(os.environ, LEAN_PATH=directory)
        commands = [
            [lean, '-o', str(Path(directory)/'Residue.olean'), str(ROOT/'experiments/residue_network/Residue.lean')],
            [lean, '-o', str(Path(directory)/'Bilinear.olean'), str(HERE/'Bilinear.lean')],
            [lean, str(certificate)]]
        for command in commands:
            print('Checking Lean:', Path(command[-1]).name, flush=True)
            start = time.perf_counter()
            result = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, text=True, timeout=180)
            logs.append({'command':command, 'exit_code':result.returncode,
                         'elapsed_seconds':time.perf_counter()-start,
                         'stdout':result.stdout, 'stderr':result.stderr})
            (output/'lean.json').write_text(json.dumps({'version':version.stdout.strip(), 'checks':logs}, indent=2)+'\n')
            if result.returncode:
                raise RuntimeError('Lean rejected certificate: see lean.json')
    return {'successful_commands':len(logs), 'certified_models':12,
            'inputs_per_certified_model':81, 'version':version.stdout.strip(),
            'certificate_sha256':digest(certificate)}


def run(output):
    output.mkdir(parents=True, exist_ok=False)
    sources = [Path(__file__), HERE/'Bilinear.lean', HERE/'PLAN.md',
               ROOT/'experiments/residue_network/Residue.lean']
    config = {'dimensions':[4,6,8], 'ranks':'1,2,d', 'seeds':list(range(20261025,20261029)),
              'attack_cases_per_task':128, 'training_attacks_per_task':32,
              'source_hashes':{str(p.relative_to(ROOT)):digest(p) for p in sources},
              'python':platform.python_version(), 'numpy':np.__version__,
              'model_api_calls':0, 'cloud_jobs':0, 'estimated_external_cost_usd':0}
    (output/'config.json').write_text(json.dumps(config, indent=2)+'\n')
    (output/'PLAN.md').write_text((HERE/'PLAN.md').read_text())
    tasks, negatives = [], []
    for d in config['dimensions']:
        train_x = training_points(d)
        all_x = list(itertools.product(range(3), repeat=d))
        seen = set(train_x)
        test_x = [x for x in all_x if x not in seen]
        for requested_rank in (1,2,d):
            for seed in config['seeds']:
                task_id = len(tasks)
                t = teacher(d, requested_rank, seed)
                train_y = target(t, train_x).tolist()
                start = time.perf_counter()
                learned = fit(train_x, train_y)
                fit_seconds = time.perf_counter()-start
                assert learned['constant'] == t['constant'] and learned['linear'] == t['linear']
                assert learned['matrix'] == t['matrix']
                rank = len(learned['u'])
                assert rank == requested_rank
                assert np.array_equal((np.array(learned['u']).T @ np.array(learned['v'])) % 3,
                                      np.array(t['matrix']))
                params = parameters(learned)
                labels = target(t, test_x)
                predictions = predict(params, d, rank, test_x) % 3
                assert np.array_equal(predictions, labels)
                assert np.array_equal(predict(params, d, rank, train_x) % 3, train_y)
                assert np.array_equal(predict(params, d, rank, test_x, 3), predictions)
                affine, train_correct, candidates = affine_erm(train_x, train_y)
                affine_predictions = (affine[0] + np.array(test_x) @ affine[1:]) % 3
                rng = random.Random(seed + d*1000 + requested_rank*100000)
                for _ in range(config['attack_cases_per_task']):
                    index = rng.randrange(len(all_x))
                    x = all_x[index]
                    lifted_x = [[v+3*rng.randrange(3) for v in x]]
                    lifted_p = [v+3*rng.randrange(3) for v in params]
                    assert int(predict(lifted_p, d, rank, lifted_x)[0] % 3) == int(target(t, [x])[0])
                for _ in range(config['training_attacks_per_task']):
                    lifted_x = [[v+3*rng.randrange(3) for v in x] for x in train_x]
                    lifted_y = [v+3*rng.randrange(3) for v in train_y]
                    assert fit(lifted_x, lifted_y) == learned
                raw = []
                for trit in range(3):
                    attack = params[:]
                    attack[0] += 3*trit
                    raw.append(int(predict(attack, d, rank, [all_x[0]])[0]))
                assert len(set(raw)) == 3 and len({v % 3 for v in raw}) == 1
                tasks.append({'id':task_id, 'dimension':d, 'seed':seed,
                    'teacher_rank':requested_rank, 'learned_hidden_units':rank,
                    'learned_parameters':len(params), 'fit_seconds':fit_seconds,
                    'teacher':t, 'learned':learned,
                    'training_inputs':train_x, 'training_labels':train_y,
                    'training_count':len(train_x), 'test_count':len(test_x),
                    'held_out':score(predictions, labels),
                    'direct_quadratic_held_out':score(target(learned, test_x), labels),
                    'affine_erm':{'parameters':affine.tolist(), 'training_correct':train_correct,
                                  'candidates':candidates, 'held_out':score(affine_predictions, labels)},
                    'lookup_default_zero_held_out':score(np.zeros(len(test_x), dtype=int), labels),
                    'sampled_forward_attacks':128, 'sampled_training_attacks':32,
                    'raw_bias_positive_control':raw})
                print(f'd={d} rank={rank} seed={seed}: {len(test_x)}/{len(test_x)} held-out; fit={fit_seconds:.6f}s', flush=True)
        cubic_y = [int(x[0]*x[1]*x[2] % 3) for x in train_x]
        model = fit(train_x, cubic_y)
        cubic_test = np.array([x[0]*x[1]*x[2] % 3 for x in test_x])
        neg = score(predict(parameters(model), d, len(model['u']), test_x) % 3, cubic_test)
        assert neg['correct'] < neg['total']
        negatives.append({'dimension':d, 'target':'x0*x1*x2 mod 3', 'held_out':neg})
    metrics = {'status':'numerical checks passed; Lean pending', 'tasks':tasks,
               'negative_controls':negatives, 'task_count':len(tasks),
               'held_out_correct':sum(t['held_out']['correct'] for t in tasks),
               'held_out_total':sum(t['test_count'] for t in tasks),
               'limits':'Designed noiseless quadratic identification; no iid or arbitrary-task claim.'}
    (output/'metrics.json').write_text(json.dumps(metrics, indent=2)+'\n')
    proofs = verify_lean(output, tasks)
    metrics['status'] = 'numerical checks and Lean certificates passed'
    metrics['lean'] = proofs
    (output/'metrics.json').write_text(json.dumps(metrics, indent=2)+'\n')
    print(json.dumps({k:v for k,v in metrics.items() if k not in ['tasks']}, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=ROOT/'results/bilinear-network-01')
    run(parser.parse_args().output)
