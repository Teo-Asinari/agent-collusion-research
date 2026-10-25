import unittest
import torch
from experiments.leak_cap.operators import SplitAttentionBlock, release_candidate


class OperatorChecks(unittest.TestCase):
    def test_private_perturbation_across_composed_blocks(self):
        torch.manual_seed(11)
        blocks = [SplitAttentionBlock(8) for _ in range(3)]
        public = torch.randn(2, 3, 8)
        p1, p2 = public.clone(), public.clone()
        h1, h2 = torch.randn(2, 4, 8), torch.randn(2, 4, 8) * 100
        for block in blocks:
            p1, h1 = block(p1, h1)
            p2, h2 = block(p2, h2)
        self.assertTrue(torch.equal(p1, p2))
        self.assertFalse(torch.equal(h1, h2))

    def test_private_loss_has_no_public_parameter_gradient(self):
        block = SplitAttentionBlock(8)
        _, h = block(torch.randn(2, 3, 8), torch.randn(2, 4, 8))
        h.square().sum().backward()
        for name, parameter in block.named_parameters():
            if name.startswith('public_'):
                self.assertIsNone(parameter.grad, name)
            else:
                self.assertIsNotNone(parameter.grad, name)

    def test_cross_stream_normalization_is_a_counterexample(self):
        public = torch.tensor([1., 2.])
        a = torch.nn.functional.layer_norm(torch.cat([public, torch.zeros(2)]), (4,))[:2]
        b = torch.nn.functional.layer_norm(torch.cat([public, torch.ones(2) * 10]), (4,))[:2]
        self.assertFalse(torch.equal(a, b))

    def test_gate_restricts_arbitrary_selections_to_public_candidates(self):
        candidates = torch.tensor([[[10.], [20.], [30.], [40.]]])
        observed = set()
        for index in range(4):
            scores = torch.zeros(1, 4)
            scores[0, index] = 100
            observed.add(release_candidate(candidates, scores).item())
        self.assertEqual(observed, {10., 20., 30., 40.})


if __name__ == '__main__':
    unittest.main()
