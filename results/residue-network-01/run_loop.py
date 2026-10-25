"""Finite neural architecture loop. Exact CPU integer arithmetic, no APIs.

Nine learned parameters: two affine/square hidden units and affine readout.
Semantic values are remainders modulo 3; internal words are modulo 9.
"""
import argparse
import hashlib
from itertools import product
import json
from pathlib import Path
import platform
import random
import time

import torch

PAIRS = list(product(range(2), repeat=2))
TASKS = list(product(range(2), repeat=4))
INITIAL_SEEDS = [20261025, 20261026, 20261027, 20261028]


def network(weights, inputs, modulus=9):
    """Batched models [N,9], examples [B,2]; output [N,B]."""
    a = (weights[:, 0, None] * inputs[None, :, 0]
         + weights[:, 1, None] * inputs[None, :, 1] + weights[:, 2, None]) % modulus
    b = (weights[:, 3, None] * inputs[None, :, 0]
         + weights[:, 4, None] * inputs[None, :, 1] + weights[:, 5, None]) % modulus
    a, b = a.square() % modulus, b.square() % modulus
    return (weights[:, 6, None] * a + weights[:, 7, None] * b
            + weights[:, 8, None]) % modulus


def python_network(weights, inputs, modulus=9):
    values = []
    for x, y in inputs:
        a = (weights[0]*x + weights[1]*y + weights[2]) % modulus
        b = (weights[3]*x + weights[4]*y + weights[5]) % modulus
        values.append((weights[6]*(a*a % modulus) + weights[7]*(b*b % modulus)
                       + weights[8]) % modulus)
    return values


def gradient(weights, inputs, labels):
    g = [0]*9
    for (x, y), label in zip(inputs, labels):
        a = (weights[0]*x + weights[1]*y + weights[2]) % 9
        b = (weights[3]*x + weights[4]*y + weights[5]) % 9
        ha, hb = a*a % 9, b*b % 9
        error = (weights[6]*ha + weights[7]*hb + weights[8] - label) % 9
        da, db = error*weights[6]*2*a % 9, error*weights[7]*2*b % 9
        terms = [da*x, da*y, da, db*x, db*y, db, error*ha, error*hb, error]
        g = [(u+v) % 9 for u, v in zip(g, terms)]
    return g


def try_gradient(labels, seed, rate, trace, task):
    rng = random.Random(seed)
    weights = [rng.randrange(3) for _ in range(9)]
    # One paired protected training execution; semantic data and parameters agree.
    shadow_w = [v + 3*rng.randrange(3) for v in weights]
    shadow_x = [[v+3*rng.randrange(3) for v in pair] for pair in PAIRS]
    shadow_y = [v+3*rng.randrange(3) for v in labels]
    seen = set()
    for step in range(65):
        semantic = tuple(v % 3 for v in weights)
        predictions = [v % 3 for v in python_network(weights, PAIRS)]
        assert semantic == tuple(v % 3 for v in shadow_w)
        assert predictions == [v % 3 for v in python_network(shadow_w, shadow_x)]
        fit = predictions == list(labels)
        repeated = semantic in seen
        trace.append({'task':task, 'seed':seed, 'rate':rate, 'step':step,
                      'weights':weights, 'shadow_weights':shadow_w,
                      'predictions':predictions, 'fit':fit, 'repeated_state':repeated})
        if fit or repeated or step == 64:
            return {'fit':fit, 'stop':'fit' if fit else 'cycle' if repeated else 'step_limit',
                    'steps':step, 'weights':list(weights)}
        seen.add(semantic)
        g, h = gradient(weights, PAIRS, labels), gradient(shadow_w, shadow_x, shadow_y)
        weights = [(w-rate*d) % 9 for w,d in zip(weights,g)]
        shadow_w = [(w-(rate+3)*d) % 9 for w,d in zip(shadow_w,h)]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(output):
    output.mkdir(parents=True, exist_ok=False)
    torch.set_num_threads(1)
    start = time.monotonic()
    config = {'tasks':TASKS,'inputs':PAIRS,'modulus':9,'observation_modulus':3,
              'initial_seeds':INITIAL_SEEDS,'gradient_rates':[1,2], 'gradient_limit':64,
              'joint_training_cases_per_task':256,'joint_seed':20261025,
              'parameters':9,'hidden_units':2,'hidden_activation':'square',
              'training':'formal modular gradient, then finite weight search if needed',
              'cost_usd_api':0,'cost_usd_cloud':0,
              'plan_sha256':sha(Path('research/workstreams/architecture/residue-network/plan.md')),
              'source_sha256':sha(Path(__file__)), 'python':platform.python_version(),
              'torch':str(torch.__version__), 'device':'cpu','threads':1}
    (output/'config.json').write_text(json.dumps(config,indent=2)+'\n')
    inputs = torch.tensor(PAIRS,dtype=torch.int64)
    candidates = torch.tensor(list(product(range(3),repeat=9)),dtype=torch.int64)
    predictions = network(candidates, inputs, 3)
    # Stronger checks on expressivity and overparameterization, not new capacity claims.
    affine = torch.tensor(list(product(range(3),repeat=3)),dtype=torch.int64)
    affine_pred = (affine[:,0,None]*inputs[None,:,0] + affine[:,1,None]*inputs[None,:,1]
                   + affine[:,2,None]) % 3
    one_unit = torch.tensor(list(product(range(3),repeat=5)),dtype=torch.int64)
    h = (one_unit[:,0,None]*inputs[None,:,0] + one_unit[:,1,None]*inputs[None,:,1]
         + one_unit[:,2,None]) % 3
    one_pred = (one_unit[:,3,None]*(h.square()%3) + one_unit[:,4,None]) % 3
    weight_lifts = torch.tensor(list(product(range(3),repeat=9)),dtype=torch.int64)*3
    input_lifts, targets = [], []
    for index, pair in enumerate(PAIRS):
        for lift in product(range(3),repeat=2):
            input_lifts.append([a+3*b for a,b in zip(pair,lift)])
            targets.append(index)
    lifted_inputs = torch.tensor(input_lifts,dtype=torch.int64)
    trace, summaries = [], []
    training_inputs = torch.tensor(PAIRS,dtype=torch.int64).reshape(1,4,2)
    all_input_lifts = torch.tensor(list(product(range(3),repeat=8)),dtype=torch.int64).reshape(-1,4,2)
    assert torch.equal((training_inputs+3*all_input_lifts)%3,
                       training_inputs.expand(len(all_input_lifts),-1,-1))
    rng = random.Random(20261025)
    with (output/'training-stress.jsonl').open('x') as joint_log:
        for task, labels in enumerate(TASKS):
            target = torch.tensor(labels,dtype=torch.int64)
            results = []
            for seed,rate in product(INITIAL_SEEDS,[1,2]):
                result = try_gradient(labels,seed,rate,trace,task)
                results.append({'seed':seed,'rate':rate,**result})
            consistent = torch.all(predictions == target,dim=1).nonzero().flatten()
            if not len(consistent):
                raise RuntimeError(f'Architecture cannot fit task {task}; preserve artifacts and revise')
            # The deterministic finite-search learner always returns this first match.
            selected_index = int(consistent[0])
            selected = candidates[selected_index]
            expected = target[torch.tensor(targets,dtype=torch.int64)]
            all_words = selected[None,:] + weight_lifts
            outputs = network(all_words,lifted_inputs,9)
            mismatches = int(((outputs%3) != expected[None,:]).sum())
            if mismatches:
                raise RuntimeError(f'Protected forward mismatch in task {task}')
            # Training-data reduction is the actual learner's allowed observation.
            # All 81 label lifts select exactly the same candidate; no new search needed.
            for label_lift in product(range(3),repeat=4):
                received = [v+3*m for v,m in zip(labels,label_lift)]
                assert tuple(v%3 for v in received) == labels
            for case in range(256):
                x_received = [[v+3*rng.randrange(3) for v in pair] for pair in PAIRS]
                y_received = [v+3*rng.randrange(3) for v in labels]
                assert [[v%3 for v in row] for row in x_received] == [list(p) for p in PAIRS]
                assert [v%3 for v in y_received] == list(labels)
                joint_log.write(json.dumps({'task':task,'case':case,'inputs':x_received,
                                            'labels':y_received,'selected_index':selected_index})+'\n')
            affine_best = int((affine_pred == target).sum(dim=1).max())
            one_count = int(torch.all(one_pred == target,dim=1).sum())
            item = {'task':task,'truth_table':labels,'weights':selected.tolist(),
                    'consistent_networks':len(consistent), 'selected_index':selected_index,
                    'formal_gradient_attempts':results,
                    'gradient_any_fit':any(r['fit'] for r in results),
                    'finite_search_fit':True,'correct_inputs':4,
                    'affine_best_correct':affine_best,'one_hidden_unit_solutions':one_count,
                    'weight_lifts':len(all_words),'lifted_inputs':len(lifted_inputs),
                    'forward_cases':outputs.numel(),'forward_mismatches':mismatches,
                    'output_sha256':hashlib.sha256(bytes((outputs%3).flatten().tolist())).hexdigest(),
                    'training_label_lifts_checked':81,'training_input_lifts_checked':len(all_input_lifts),
                    'joint_training_cases':256}
            summaries.append(item)
            print(f'task {task:02d}: fit=4/4; gradient={item["gradient_any_fit"]}; '
                  f'protected cases={item["forward_cases"]}; mismatches={mismatches}',flush=True)
    raw_positive = [(m,python_network([0,0,0,0,0,0,0,0,3*m],[(0,0)])[0])
                    for m in range(3)]
    assert [v//3 for _,v in raw_positive] == list(range(3))
    assert [v%3 for _,v in raw_positive] == [0,0,0]
    unsafe_pairs = [(a,b) for a,b in product(range(9),repeat=2)
                    if a%3==b%3 and (a//3)%3!=(b//3)%3]
    assert unsafe_pairs
    with (output/'gradient-traces.jsonl').open('x') as f:
        for item in trace:
            f.write(json.dumps(item)+'\n')
    report = {'status':'finite architecture loop complete','tasks':summaries,
              'formal_gradient_tasks_fitted':sum(t['gradient_any_fit'] for t in summaries),
              'finite_search_tasks_fitted':len(summaries),
              'affine_tasks_perfect':sum(t['affine_best_correct']==4 for t in summaries),
              'one_hidden_unit_tasks_representable':sum(t['one_hidden_unit_solutions']>0 for t in summaries),
              'forward_cases':sum(t['forward_cases'] for t in summaries),
              'forward_mismatches':sum(t['forward_mismatches'] for t in summaries),
              'training_label_lift_checks':16*81,'training_input_lift_checks':16*len(all_input_lifts),
              'joint_training_checks':16*256,'raw_positive_control':raw_positive,
              'unsafe_high_digit_counterexample':unsafe_pairs[0],
              'seconds':time.monotonic()-start,
              'limits':['Finite truth tables are training data, not held-out generalization.',
                        'Exact finite search is exponential in the number of learned weights.',
                        'Security conditions on permitted semantic remainders; only canonical content observed.',
                        'No hardware timing/implementation refinement or novelty established.']}
    (output/'metrics.json').write_text(json.dumps(report,indent=2)+'\n')
    certificates(output,summaries)
    return report


def certificates(output, tasks):
    lines=['import Residue','namespace Learned','set_option maxRecDepth 10000',
           'set_option maxHeartbeats 2000000']
    for t in tasks:
        i=t['task']
        lines.append(f'def weights_{i} : List Nat := {t["weights"]}')
        lines.append(f'def labels_{i} : List Nat := {list(t["truth_table"])}')
        lines.append(f'theorem task_{i}_correct : ∀ a b : Bool,\n'
                     f'  Residue.eval 3 (Residue.env2 weights_{i} a b) Residue.network2 =\n'
                     f'  (labels_{i}[a.toNat * 2 + b.toNat]?).getD 0 := by decide')
    lines.append('#print axioms task_6_correct\nend Learned')
    (output/'Learned.lean').write_text('\n'.join(lines)+'\n')


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args()
    result=run(args.output)
    print(json.dumps({k:v for k,v in result.items() if k!='tasks'},indent=2))
