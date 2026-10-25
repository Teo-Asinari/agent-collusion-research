"""Candidate algebraic neuron, not established novelty or a secure float backend.

Q_c(U,V,x) = square(U sum_j c_j (VU)^j Vx).
Over exact arithmetic this depends on U,V only through M=UV. Float arithmetic
does not inherit that guarantee. Coefficients must not carry protected payloads.
"""
import argparse
from fractions import Fraction
import hashlib
from itertools import product
import json
from pathlib import Path
import platform

import torch
from torch import nn


class QuotientPolynomial(nn.Module):
    """Differentiable numerical prototype; fixed scalar coefficient parameters.

    U: [d,r], V: [r,d], x: [d,b]. Activation is applied after contraction.
    This module does not enforce exact arithmetic, trusted coefficients, input
    authenticity, public shapes, resource isolation or optimizer confinement.
    """
    def __init__(self, degree=1):
        super().__init__()
        if degree < 0:
            raise ValueError('degree must be nonnegative')
        self.coefficients = nn.Parameter(torch.ones(degree + 1, dtype=torch.float64))

    def forward(self, u, v, x):
        z = v @ x
        latent_operator = v @ u
        accumulated = self.coefficients[0] * z
        for coefficient in self.coefficients[1:]:
            z = latent_operator @ z
            accumulated = accumulated + coefficient * z
        return (u @ accumulated).square()


def mv(matrix, vector, modulus):
    return tuple(sum(a * b for a, b in zip(row, vector)) % modulus for row in matrix)


def exact_rank_one(u, v, x, coefficients, modulus=3):
    # U is a column and V a row; VU is a scalar. Fixed public shapes.
    z = sum(a * b for a, b in zip(v, x)) % modulus
    s = sum(a * b for a, b in zip(v, u)) % modulus
    accumulated = 0
    for coefficient in coefficients:
        accumulated = (accumulated + coefficient * z) % modulus
        z = s * z % modulus
    return tuple((a * accumulated) ** 2 % modulus for a in u)


def check():
    field_vectors = list(product(range(3), repeat=2))
    fibers, products_seen = {}, set()
    count = 0
    for u, v in product(field_vectors, repeat=2):
        m = tuple(tuple(a * b % 3 for b in v) for a in u)
        products_seen.add(m)
        for x, coefficients in product(field_vectors, repeat=2):
            result = exact_rank_one(u, v, x, coefficients)
            mx = mv(m, x, 3)
            mmx = mv(m, mx, 3)
            reference = tuple((coefficients[0] * a + coefficients[1] * b) ** 2 % 3
                              for a, b in zip(mx, mmx))
            assert result == reference
            key = (m, x, coefficients)
            assert key not in fibers or fibers[key] == result
            fibers[key] = result
            count += 1
    # A scalar GL(1,F3) basis change keeps UV=1 but hidden squaring leaks it.
    unsafe = [(u * (v * 1) ** 2) % 3 for u, v in [(1, 1), (2, 2)]]
    assert unsafe == [1, 2]
    safe = [exact_rank_one((u,), (v,), (1,), (1,)) for u, v in [(1, 1), (2, 2)]]
    assert safe == [(1,), (1,)]
    # Protected coefficient changes are outside the same-coefficient theorem.
    coefficient_leak = [exact_rank_one((1,), (1,), (1,), (c,))[0] for c in [0, 1]]
    assert coefficient_leak == [0, 1]
    model = QuotientPolynomial(degree=0)
    stable_u = torch.tensor([[1., 0., 0.]], dtype=torch.float64)
    unstable_u = torch.tensor([[float(2**54), 1., -float(2**54)]], dtype=torch.float64)
    v = torch.ones(3, 1, dtype=torch.float64)
    x = torch.ones(1, 1, dtype=torch.float64)
    # All input numbers are exactly representable; the ideal UV product is 1.
    assert sum(Fraction(a) for a in unstable_u[0].tolist()) == 1
    float_outputs = [model(u, v, x).item() for u in [stable_u, unstable_u]]
    assert float_outputs == [1., 0.], 'Backend changed: inspect numerical counterexample'
    # A well-conditioned shear orbit: derivative along its basis choice vanishes.
    shear = torch.tensor(0.5, dtype=torch.float64, requires_grad=True)
    one, zero = shear.new_tensor(1.), shear.new_tensor(0.)
    g = torch.stack([torch.stack([one, shear]), torch.stack([zero, one])])
    inverse = torch.stack([torch.stack([one, -shear]), torch.stack([zero, one])])
    u2 = torch.tensor([[1., 2.], [0., 1.]], dtype=torch.float64)
    v2 = torch.tensor([[1., 0.], [1., 1.]], dtype=torch.float64)
    x2 = torch.tensor([[1.], [2.]], dtype=torch.float64)
    model2 = QuotientPolynomial(degree=1)
    y = model2(u2 @ g, inverse @ v2, x2)
    assert torch.equal(y, model2(u2, v2, x2))
    y.sum().backward()
    assert shear.grad.item() == 0.
    assert model2.coefficients.grad.abs().sum().item() > 0.
    # Naive training of the factors can turn a basis choice into different M.
    # Loss is (uv-target)^2/2, target=0, eta=1/10, before any outer square.
    def update_product(u, v):
        residual = u * v
        return (u - Fraction(1, 10) * residual * v) * (v - Fraction(1, 10) * residual * u)
    updated = [update_product(Fraction(u), Fraction(v))
               for u, v in [(1, 1), (2, Fraction(1, 2))]]
    assert updated == [Fraction(81, 100), Fraction(117, 200)]
    return {
        'status': 'exploratory algebra and counterexample checks complete',
        'exact_field': 'F_3', 'dimension': 2, 'factor_width': 1,
        'coefficient_count': 2, 'factor_pairs': 81,
        'exact_rows_checked': count, 'distinct_authorized_products': len(products_seen),
        'distinct_product_query_coefficient_keys': len(fibers),
        'exact_product_equivalence_mismatches': 0,
        'unsafe_hidden_square_outputs_same_product': unsafe,
        'safe_outputs_same_product': [list(a) for a in safe],
        'protected_coefficient_outputs_same_product': coefficient_leak,
        'same_exact_product_float64_outputs': float_outputs,
        'shear_direction_derivative': shear.grad.item(),
        'learnable_coefficients_have_nonzero_gradient': True,
        'factor_sgd_updated_products_same_initial_product': [str(a) for a in updated],
        'python': platform.python_version(), 'torch': str(torch.__version__),
        'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'model_api_cost_usd': 0, 'cloud_cost_usd': 0,
        'limits': ['Finite enumeration is not a general mechanized proof.',
                   'Ordinary float64 is explicitly falsified as an exact backend.',
                   'No training, efficiency, full-model security or novelty established.']
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError(args.output)
    report = check()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x') as handle:
        handle.write(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
