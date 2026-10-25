"""Experimental two-stream attention. No deployment or novelty guarantee.

Public computation never reads private tensors. Private losses cannot update
public computation through this forward graph. Public parameters must also be
excluded from private optimizers and private-dependent training decisions.
"""
import math

import torch
from torch import nn


class Attention(nn.Module):
    def __init__(self, width):
        super().__init__()
        self.q = nn.Linear(width, width)
        self.k = nn.Linear(width, width)
        self.v = nn.Linear(width, width)
        self.o = nn.Linear(width, width)

    def forward(self, queries, context):
        scores = self.q(queries) @ self.k(context).transpose(-1, -2)
        weights = torch.softmax(scores / math.sqrt(queries.shape[-1]), dim=-1)
        return self.o(weights @ self.v(context))


class SplitAttentionBlock(nn.Module):
    """Single-head, noncausal seed block; tensor shape [batch, tokens, width]."""
    def __init__(self, width):
        super().__init__()
        self.public_attention = Attention(width)
        self.private_attention = Attention(width)
        self.public_norm = nn.LayerNorm(width)
        self.private_norm = nn.LayerNorm(width)
        self.public_ff = nn.Sequential(nn.Linear(width, 2 * width), nn.GELU(),
                                       nn.Linear(2 * width, width))
        self.private_ff = nn.Sequential(nn.Linear(width, 2 * width), nn.GELU(),
                                        nn.Linear(2 * width, width))

    def forward(self, public, private):
        p = public + self.public_attention(public, public)
        p = p + self.public_ff(self.public_norm(p))
        # Private branch has its own projections, normalization and parameters.
        # This detachment also prevents private-loss backpropagation into p.
        context = torch.cat([p.detach(), private], dim=1)
        h = private + self.private_attention(private, context)
        h = h + self.private_ff(self.private_norm(h))
        return p, h


def release_candidate(public_candidates, private_scores):
    """One fixed-size finite choice, per batch; release no scores/hidden states.

Requires trusted candidate construction and exactly 2**k candidates. Variable
candidate count, status, timing and the number of releases are outside this API.
"""
    count = public_candidates.shape[1]
    if count < 1 or count & (count - 1):
        raise ValueError('candidate count must be a positive power of two')
    if private_scores.shape != public_candidates.shape[:2]:
        raise ValueError('one score is required per candidate')
    chosen = private_scores.argmax(dim=1)
    return public_candidates[torch.arange(len(chosen), device=chosen.device), chosen]
