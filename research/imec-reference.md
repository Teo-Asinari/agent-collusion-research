# Inspection and minimal execution of the iMEC reference

2026-10-24. Source: [author repository](https://github.com/schroederdewitt/perfectly-secure-steganography/tree/cc36ae0b585fae4c7fcf65f7ee4db43aac2edd28), pinned commit `cc36ae0b585fae4c7fcf65f7ee4db43aac2edd28`. Upstream source downloaded externally to `/tmp/imec-reference`; no upstream implementation was vendored. No top-level LICENSE was present in the inspected tree, so licensing needs clarification before code incorporation.

## Concrete code exists

- [`src/imec.py`](https://github.com/schroederdewitt/perfectly-secure-steganography/blob/cc36ae0b585fae4c7fcf65f7ee4db43aac2edd28/src/imec.py): `IMECEncoder.encode`, `IMECDecoder.decode`, and mask/unmask functions.
- [`src/main.py`](https://github.com/schroederdewitt/perfectly-secure-steganography/blob/cc36ae0b585fae4c7fcf65f7ee4db43aac2edd28/src/main.py): experiment harness masks bits, encodes to a carrier, decodes using original token IDs/context and known block information, then unmasks/reconstructs the message.
- [`src/mec.py`](https://github.com/schroederdewitt/perfectly-secure-steganography/blob/cc36ae0b585fae4c7fcf65f7ee4db43aac2edd28/src/mec.py): numerically stabilized greedy Kocaoglu-style coupling, plus marginal/KL and entropy-gap diagnostics. It is not an exact optimal solver for every input.
- [`README`](https://github.com/schroederdewitt/perfectly-secure-steganography/blob/cc36ae0b585fae4c7fcf65f7ee4db43aac2edd28/README.md): GPT-2 iMEC run at block size 10; Python 3.8-era dependencies and WandB instructions. It warns runtime differs from the optimized implementation used in the paper. Default language-model wrapper requests `gpt2-large`. The bottom-of-file standalone snippet in `imec.py` is stale relative to current function names/return values; use the actual class API/harness.

Thus it would be wrong to suggest there is no concrete reference implementation. Existence of code and successful decoding still do not certify exact throughput optimality or all implementation-level security assumptions.

## Executed check

Using our [inspection runner](../experiments/reference_imec_check.py), executed the original selected iMEC classes, coupling functions, entropy helpers and DRBG/masking code without source changes. AST selection avoids unrelated model/image imports and the stale standalone entry point. Our adapter supplies a fixed four-symbol cover distribution `[1/2, 1/4, 1/8, 1/8]`. No GPT-2, model download, network, WandB login or provider inference was used.

Observed exact round trip with block size 4, encoder seed 42, fixed public test key/nonce/context:

```text
Input:      Hi
Cover:      elm elm ash fir oak oak oak fir oak oak
Recovered:  Hi
Payload:    16 bits
Carrier:    10 symbols
```

This is a concrete execution of upstream iMEC logic on our finite carrier. It is not a reproduction of GPT-2 experiments, a distributed-agent experiment, an optimality proof, a security validation, or evidence that this fixed test-key fixture is secure. The decoder is given original token identifiers, known payload chunk count and the same context/cover mechanism.

Environment observed: NumPy 2.0.2; PyTorch 2.8.0+cu128, CPU tensors; Python 3.9.12. No dependency installation occurred. Reproduce after obtaining the pinned source:

```bash
python experiments/reference_imec_check.py --source /tmp/imec-reference/src
```

The runner reports upstream file SHA-256 digests with its result. These were:

```text
imec.py 2323df0ae22efde6d498bbff8bb7960c8c5dfcd7d107d351f89e93b2b44cabac
mec.py  c1a71571bef39d2e8e3c740e14b373f274aa49ccc0b57ec287c1da8129c26dc7
utils.py 27d36fd1489ea540662318babf76266a44669453f27b23b15064f7b748947577
```
