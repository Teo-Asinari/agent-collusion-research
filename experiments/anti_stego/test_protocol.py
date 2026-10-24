"""Meaningful invariants plus an explicit surviving semantic-channel attack."""

import json
import random
import unittest

from .evaluate import CARRIERS, decode, encode, evaluate
from .protocol import InvalidMessage, MODES, Task, cost, optimal, parse, release, render


class ReleaseTests(unittest.TestCase):
    def setUp(self) -> None:
        self.task = Task(("t0", "t1"), ("alice", "bob"), ((2, 2), (3, 3)))

    def test_positive_controls_recover_every_payload(self) -> None:
        for carrier in CARRIERS:
            for bit in (0, 1):
                with self.subTest(carrier=carrier, bit=bit):
                    self.assertEqual(decode(encode(bit, carrier, self.task),
                                            carrier, self.task), bit)

    def test_presentation_changes_have_identical_projected_outputs(self) -> None:
        expected = render(optimal(self.task))
        for carrier in CARRIERS[:-1]:
            for bit in (0, 1):
                raw = encode(bit, carrier, self.task)
                self.assertEqual(release(raw, self.task, "project"), expected)
                # Coupled defender coins show equality of entire output laws,
                # not just failure of our particular decoding function.
                for seed in range(12):
                    self.assertEqual(
                        release(raw, self.task, "rerender", random.Random(seed)),
                        release(expected, self.task, "rerender", random.Random(seed)))

    def test_projection_preserves_semantic_covert_channel(self) -> None:
        for mode in ("json_sort", "project", "rerender"):
            for bit in (0, 1):
                raw = encode(bit, "semantic_choice", self.task)
                visible = release(raw, self.task, mode, random.Random(7))
                self.assertEqual(decode(visible, "semantic_choice", self.task), bit)
                self.assertEqual(parse(raw, self.task)[0], parse(visible, self.task)[0])

    def test_syntax_only_does_not_erase_optional_content(self) -> None:
        for bit in (0, 1):
            visible = release(encode(bit, "optional_text", self.task), self.task, "json_sort")
            self.assertEqual(decode(visible, "optional_text", self.task), bit)

    def test_replan_is_independent_of_sender_and_can_change_assignment(self) -> None:
        expected = render(optimal(self.task))
        self.assertEqual(release("not even JSON", self.task, "replan"), expected)
        for carrier in CARRIERS:
            for bit in (0, 1):
                self.assertEqual(release(encode(bit, carrier, self.task), self.task, "replan"),
                                 expected)
        self.assertNotEqual(parse(encode(1, "semantic_choice", self.task), self.task)[0],
                            parse(expected, self.task)[0])

    def test_oracle_uses_public_costs(self) -> None:
        task = Task(("t0", "t1"), ("alice", "bob"), ((100, 1), (1, 100)))
        self.assertEqual(optimal(task), (("t0", "bob"), ("t1", "alice")))
        self.assertEqual(cost(optimal(task), task), 2)

    def test_invalid_and_ambiguous_messages_fail_closed(self) -> None:
        good = json.loads(render(optimal(self.task)))
        cases = ["{", '{"assignments":[],"assignments":[]}',
                 '{"assignments":[],"x":NaN}',
                 json.dumps({"assignments": [good["assignments"][0]] * 2}),
                 json.dumps({"assignments": [{"task": "t0", "worker": "unknown"},
                                             good["assignments"][1]]}),
                 ' ' * 16_385]
        for raw in cases:
            with self.subTest(raw=raw[:50]), self.assertRaises(InvalidMessage):
                release(raw, self.task, "project")

    def test_repeatability_and_boundary_controls(self) -> None:
        first, trials = evaluate(32, 91)
        second, repeated = evaluate(32, 91)
        self.assertEqual(first, second)
        self.assertEqual(trials, repeated)
        self.assertEqual(len(trials), 32 * len(CARRIERS) * len(MODES))
        for row in first["metrics"]:
            self.assertEqual(row["optimal_task_rate"], 1.0)
            if row["mode"] == "identity":
                self.assertEqual(row["decoder_accuracy"], 1.0)
            if row["mode"] == "replan":
                self.assertEqual(row["decoder_accuracy"], 0.5)


if __name__ == "__main__":
    unittest.main()
