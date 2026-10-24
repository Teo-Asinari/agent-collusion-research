# Small source-feasibility checks

## 2026-10-24 — permutation-null invariant

Purpose: determine whether the supplied permutation detector is a sound candidate baseline before selecting a research question. No model inference or experiment was run.

Source: [official starter permutation detector](https://github.com/poseidon-research/collusion_hackathon/blob/e6fb1308dae9cf97ae42aec1c5f7889d9e2291e8/steganographic-collusion/auditor/detectors/permutation.py), pinned commit `e6fb1308dae9cf97ae42aec1c5f7889d9e2291e8`.

The detector computes `mean(distance(vector, centroid))` and compares it to a shuffled ordering of the same vectors. Reordering preserves the centroid and multiset of distances. Therefore it cannot supply the intended permutation null, apart from floating-point variation.

Reproduce after obtaining the pinned source externally; point `SOURCE` to that file. This loads only the two arithmetic function definitions, not upstream imports, clients, or model code:

```python
import ast
import itertools
import math
from pathlib import Path

SOURCE = Path('/tmp/collusion-starter-inspect/steganographic-collusion/auditor/detectors/permutation.py')
tree = ast.parse(SOURCE.read_text())
functions = [node for node in tree.body
             if isinstance(node, ast.FunctionDef)
             and node.name in {'_euclidean_distance', '_alignment_score'}]
namespace = {'math': math, 'Sequence': list}
exec(compile(ast.Module(body=functions, type_ignores=[]), str(SOURCE), 'exec'), namespace)
vectors = [[0., 0.], [1., 3.], [4., 7.], [9., 2.]]
scores = [namespace['_alignment_score'](list(p))
          for p in itertools.permutations(vectors)]
print(min(scores), max(scores), max(scores) - min(scores))
```

Observed: `4.182767761636298 4.182767761636298 0.0` across all 24 permutations. This confirms the local invariant only. It does not reproduce the paper's aggregate results or test other detectors. Original arithmetic definitions remain external; this is our inspection recipe, not vendored source.
