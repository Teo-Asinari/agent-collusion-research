"""Independent scalar audit of saved fits, provenance and checked certificates.

No fitting, NumPy, API calls or repeated Lean compilation. Lean results are the
recorded completed compiler commands, bound to current hashed source/artifacts.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit(folder, output):
    if output.exists():
        raise FileExistsError(output)
    config = json.loads((folder/'config.json').read_text())
    metrics = json.loads((folder/'metrics.json').read_text())
    logs = json.loads((folder/'lean.json').read_text())
    for name, expected in config['source_hashes'].items():
        assert sha(ROOT/name) == expected, name
    assert sha(folder/'PLAN.md') == config['source_hashes']['experiments/bilinear_network/PLAN.md']
    cert = (folder/'Learned.lean').read_text()
    assert sha(folder/'Learned.lean') == metrics['lean']['certificate_sha256']
    assert 'sorry' not in cert and 'native_decide' not in cert and 'axiom ' not in cert
    assert len(logs['checks']) == 3 and all(c['exit_code'] == 0 for c in logs['checks'])
    assert metrics['status'] == 'numerical checks and Lean certificates passed'
    assert len(metrics['tasks']) == 36
    checked = heldout = certified = 0
    for task in metrics['tasks']:
        d = task['dimension']
        m, t = task['learned'], task['teacher']
        train = {tuple(x): y for x, y in zip(task['training_inputs'], task['training_labels'])}
        assert len(train) == 1+2*d+d*(d-1)//2 == task['training_count']
        assert len(m['u']) == len(m['v']) == task['teacher_rank']
        assert all(len(row) == d for row in m['u']+m['v'])
        for i in range(d):
            for j in range(d):
                assert sum(u[i]*v[j] for u,v in zip(m['u'],m['v'])) % 3 == t['matrix'][i][j]
        test_correct = 0
        for x in itertools.product(range(3), repeat=d):
            hidden = sum(sum(a*b for a,b in zip(u,x))*sum(a*b for a,b in zip(v,x))
                         for u,v in zip(m['u'],m['v']))
            observed = (m['constant']+sum(a*b for a,b in zip(m['linear'],x))+hidden) % 3
            reference = (t['constant']+sum(t['linear'][i]*x[i] for i in range(d))+
                         sum(t['matrix'][i][j]*x[i]*x[j] for i in range(d) for j in range(d))) % 3
            assert observed == reference
            checked += 1
            if x in train:
                assert train[x] == reference
            else:
                test_correct += 1
                heldout += 1
        assert test_correct == task['held_out']['correct'] == task['test_count']
        if d == 4:
            ident = task['id']
            p = [m['constant']]+m['linear']+sum(m['u'],[])+sum(m['v'],[])
            assert f'def parameters_{ident} : List Nat := {p}' in cert
            assert f'Bilinear.predict 4 {len(m["u"])} 3 parameters_{ident}' in cert
            assert f'Bilinear.target 4 3 {t["constant"]} {t["linear"]} {sum(t["matrix"], [])}' in cert
            assert f"'LearnedBilinear.correct_{ident}' depends on axioms: [propext]" in logs['checks'][2]['stdout']
            certified += 1
    assert heldout == metrics['held_out_correct'] == metrics['held_out_total'] == 87396
    assert certified == 12
    result = {'status':'independent scalar and artifact checks passed',
              'full_domain_cases':checked, 'held_out_cases':heldout,
              'certificates_matched_to_saved_models':certified,
              'metrics_sha256':sha(folder/'metrics.json'),
              'certificate_sha256':sha(folder/'Learned.lean'),
              'verifier_sha256':sha(Path(__file__)),
              'lean_checks':'Recorded successful commands; not re-executed by this audit.',
              'model_api_calls':0, 'cloud_jobs':0}
    output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--results',type=Path,default=ROOT/'results/bilinear-network-01')
    parser.add_argument('--output',type=Path,default=ROOT/'results/bilinear-network-01/verification.json')
    args = parser.parse_args()
    audit(args.results,args.output)
