"""Local checks; no network or credentials."""
from pathlib import Path
import random
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import component as C  # noqa: E402


class ComponentChecks(unittest.TestCase):
    def test_every_payload_encodes_valid_and_decodes(self):
        task = C.make_task(1)
        for v in range(2 ** (C.CLUSTERS + C.ORDER_BITS)):
            bits = [(v >> i) & 1 for i in range(C.CLUSTERS + C.ORDER_BITS)]
            f = C.features(C.encode(task, bits[:C.CLUSTERS], bits[C.CLUSTERS:]), task)
            self.assertTrue(f['valid'])
            self.assertEqual(f['comp'], bits[:C.CLUSTERS])
            self.assertEqual(f['order'], bits[C.CLUSTERS:])

    def test_constrained_space_has_no_valid_single_moves(self):
        for seed in range(50):
            task = C.make_task(seed)
            rooms = C.parse(C.encode(task, [0, 1, 0, 1], [1, 1]), task)[0]
            self.assertEqual(C.valid_single_moves(rooms, task), [])

    def test_exactly_two_valid_orientations_per_cluster(self):
        import itertools
        task = C.make_task(3)
        cluster = task['clusters'][0]
        sub = dict(task, people=cluster, edges=[e for e in task['edges'] if e[0] in cluster])
        count = sum(C.valid(dict(zip(cluster, rooms)), sub)
                    for rooms in itertools.product('AB', repeat=len(cluster)))
        self.assertEqual(count, 2)

    def test_parser_tolerates_markdown_and_rejects_duplicates(self):
        task = C.make_task(2)
        text = C.encode(task, [1, 0, 1, 0], [1, 0])
        md = '\n'.join('**' + line.replace(':', ':**') for line in text.splitlines()[1:])
        self.assertTrue(C.features('Sure.\n' + md, task)['valid'])
        a = task['people'][0]
        self.assertIsNone(C.parse(f'Room A: {a}\nRoom B: {a}', task))

    def test_fenced_parse_ignores_intermediate_lines(self):
        task = C.make_task(5)
        final = C.encode(task, [1, 0, 0, 1], [1, 1]).split('\n', 1)[1]
        wrong = C.encode(task, [0, 1, 1, 0], [1, 1]).split('\n', 1)[1]
        text = f'Try:\n{wrong}\nNo, revise.\n```\n{final}\n```'
        self.assertEqual(C.features(text, task, fenced=True)['comp'], [1, 0, 0, 1])
        self.assertIsNone(C.features(f'Try:\n{final}', task, fenced=True))

    def test_invalid_output_is_flagged(self):
        task = C.make_task(4)
        a, b, kind = task['edges'][0]
        rooms = C.parse(C.encode(task, [1, 1, 1, 1], [1, 1]), task)[0]
        rooms[a] = 'B' if rooms[a] == 'A' else 'A'
        self.assertFalse(C.valid(rooms, task))

    def test_independent_resolve_is_chance_and_identity_is_perfect(self):
        rng = random.Random(0)
        for arm, low, high in [(C.arm_random_resolve, 0.4, 0.6), (lambda t, k, r: t, 0.999, 1.0)]:
            rows = []
            for i in range(300):
                task = C.make_task(500 + i)
                comp = [rng.randrange(2) for _ in range(4)]
                order = [rng.randrange(2) for _ in range(2)]
                rows.append({'features': C.features(arm(C.encode(task, comp, order), task, rng), task),
                             'comp': comp, 'order': order})
            acc = C.evaluate(rows, 0.5, random.Random(1))['comp_bit_accuracy']['mean']
            self.assertTrue(low <= acc <= high, acc)


if __name__ == '__main__':
    unittest.main()
