"""Check artifact provenance and Lean certificates; no training or API calls."""
import ast
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'results/residue-verification-01'
LEAN=Path('/home/tasinari/.elan/bin/lean')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(output=OUT):
    output.mkdir(parents=True,exist_ok=False)
    artifact_checks=[]
    for number in [1,2,3]:
        folder=ROOT/f'results/residue-network-0{number}'
        metrics=json.loads((folder/'metrics.json').read_text())
        config=json.loads((folder/'config.json').read_text())
        source=folder/'run_loop.py' if number==1 else ROOT/'experiments/residue_network/run_loop.py'
        assert sha(source)==config['source_sha256']
        assert len(metrics['tasks'])==16 and metrics['finite_search_tasks_fitted']==16
        assert metrics['forward_mismatches']==0
        expected=16*36*3**config['parameters']
        assert metrics['forward_cases']==expected
        cert=(folder/'Learned.lean').read_text()
        assert 'sorry' not in cert and 'axiom ' not in cert
        for task in metrics['tasks']:
            i=task['task']
            w=re.search(rf'def weights_{i} : List Nat := (\[[^\n]+\])',cert)
            y=re.search(rf'def labels_{i} : List Nat := (\[[^\n]+\])',cert)
            assert ast.literal_eval(w[1])==task['weights']
            assert ast.literal_eval(y[1])==list(task['truth_table'])
        shadow_rows=0
        for line in (folder/'gradient-traces.jsonl').read_text().splitlines():
            row=json.loads(line)
            assert [x%3 for x in row['weights']]==[x%3 for x in row['shadow_weights']]
            shadow_rows+=1
        artifact_checks.append({'run':folder.name,'source_hash_matches':True,
            'certificate_weights_match':True,'forward_cases':expected,
            'protected_gradient_states_checked':shadow_rows,
            'metrics_sha256':sha(folder/'metrics.json'),
            'certificate_sha256':sha(folder/'Learned.lean')})
    proof_source=ROOT/'experiments/residue_network/Residue.lean'
    assert 'sorry' not in proof_source.read_text() and 'axiom ' not in proof_source.read_text()
    commands=[]
    with tempfile.TemporaryDirectory(prefix='residue-proof-') as directory:
        env=dict(os.environ,LEAN_PATH=directory)
        for args in [
            [str(LEAN),'-o',str(Path(directory)/'Residue.olean'),str(proof_source)],
            *[[str(LEAN),str(ROOT/f'results/residue-network-0{i}/Learned.lean')] for i in [1,2,3]]]:
            result=subprocess.run(args,cwd=ROOT,env=env,capture_output=True,text=True,timeout=60)
            commands.append({'command':args,'exit_code':result.returncode,
                             'stdout':result.stdout,'stderr':result.stderr})
            if result.returncode:
                (output/'failure.json').write_text(json.dumps(commands,indent=2)+'\n')
                raise RuntimeError('Lean rejected a proof; see failure.json')
    report={'status':'all artifact and proof checks passed',
            'proof_source_sha256':sha(proof_source),'artifact_checks':artifact_checks,
            'lean_commands':commands,'model_api_calls':0,'cloud_jobs':0,
            'limits':'Abstract algebra and finite model certificates, not Python/hardware refinement.'}
    (output/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'status':report['status'],'runs':len(artifact_checks),
                      'lean_checks':len(commands)},indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,default=OUT)
    args=parser.parse_args()
    main(args.output)
