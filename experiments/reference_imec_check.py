"""Check selected upstream iMEC classes on our finite medium, not GPT-2.

Obtain upstream commit cc36ae0b585fae4c7fcf65f7ee4db43aac2edd28 externally.
No upstream code is vendored. Requires numpy, torch and bitarray.
The mask key is a public test fixture, not a secret or a security assertion.
"""
import argparse
import ast
import hashlib
import hmac
import json
import time
from collections import defaultdict
from copy import deepcopy
from pathlib import Path
import bitarray
import numpy as np
import torch as th

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--source', type=Path, default=Path('/tmp/imec-reference/src'))
args=parser.parse_args()
root=args.source
ns={'np':np,'th':th,'time':time,'bitarray':bitarray,'deepcopy':deepcopy,
    'defaultdict':defaultdict,'hashlib':hashlib,'hmac':hmac,
    'ActionLabelException':RuntimeError}

def load_selected(filename,names):
    tree=ast.parse((root/filename).read_text())
    nodes=[n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name in names]
    assert {n.name for n in nodes}==set(names)
    exec(compile(ast.Module(body=nodes,type_ignores=[]),str(root/filename),'exec'),ns)

load_selected('utils.py',['kl2','entropy2','DRBG'])
load_selected('mec.py',['greatest_lower_bound','mec_kocaoglu_np','minimum_entropy_coupling'])
load_selected('imec.py',['IMECEncoder','IMECDecoder','apply_random_mask','remove_random_mask'])

class DiscreteMedium:
    def reset(self,context=None):
        self.output=[]
        return self.step(None)
    def step(self,action):
        if action is not None:self.output.append(int(action))
        self.action_labels=th.tensor([0,1,2,3])
        p=np.array([.5,.25,.125,.125],dtype=np.longdouble)
        h=float(ns['entropy2'](p))
        return p,{'medium_entropy_raw':h,'medium_entropy':h}
    def get_output(self,clean_up=False):return list(self.output)
    def humanify(self,output):return ' '.join(['oak','elm','ash','fir'][i] for i in output)

message=bitarray.bitarray();message.frombytes(b'Hi')
mask={'input_key':b'public-test-fixture-only','sample_seed_prefix':b'demo','input_nonce':b'nonce'}
medium=DiscreteMedium()
with np.errstate(divide='ignore',invalid='ignore'):
    masked=ns['apply_random_mask'](message,**mask)
    encoder=ns['IMECEncoder'](medium=medium,block_size=4,seed=42,clean_up_output=False)
    text,tokens,stats=encoder.encode(private_message_bit=masked,context='fixed-public-context')
    decoder=ns['IMECDecoder'](medium=medium,block_size=4,n_chunks=4,clean_up_output=False)
    recovered,_=decoder.decode(public_message_token=tokens,context='fixed-public-context')
    recovered=ns['remove_random_mask'](recovered,**mask)[:len(message)]
assert recovered==message
print(json.dumps({'upstream_commit':'cc36ae0b585fae4c7fcf65f7ee4db43aac2edd28',
 'scope':'Original selected numerical functions and iMEC classes; our four-symbol medium adapter; no GPT-2 or full upstream CLI',
 'plaintext':'Hi','cover_symbols':text,'recovered':recovered.tobytes().decode(),
 'payload_bits':len(message),'symbols':len(tokens),'exact_match':recovered==message,
 'numpy':np.__version__,'torch':th.__version__,
 'source_sha256':{n:hashlib.sha256((root/n).read_bytes()).hexdigest() for n in ['imec.py','mec.py','utils.py']}},indent=2))
