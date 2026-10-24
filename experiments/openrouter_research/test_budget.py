"""Local accounting checks. Never makes network calls or reads credentials."""
from decimal import Decimal
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location('batch', Path(__file__).with_name('run_batch.py'))
BATCH = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BATCH)


class BudgetChecks(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.path = Path(self.directory.name) / 'ledger.json'
        self.budget = BATCH.Budget(self.path)

    def tearDown(self):
        self.directory.cleanup()

    def test_in_flight_reservations_count_toward_cap(self):
        self.budget.reserve('a', Decimal('3'))
        with self.assertRaises(RuntimeError):
            self.budget.reserve('b', Decimal('2.01'))
        self.assertNotIn('b', json.loads(self.path.read_text())['calls'])

    def test_actual_charge_replaces_reservation(self):
        self.budget.reserve('a', Decimal('3'))
        self.budget.finish('a', '0.25', True, {})
        self.budget.reserve('b', Decimal('4.5'))

    def test_unknown_cost_halts_subsequent_requests_and_survives_reload(self):
        self.budget.reserve('a', Decimal('1'))
        self.budget.finish('a', None, False, {})
        restored = BATCH.Budget(self.path)
        with self.assertRaises(RuntimeError):
            restored.reserve('b', Decimal('0.1'))
        self.assertEqual(restored.state['calls']['a']['reserved_usd'], '1')

    def test_prevents_duplicate_and_thirteenth_request(self):
        self.budget.reserve('a', Decimal('0.01'))
        with self.assertRaises(RuntimeError):
            self.budget.reserve('a', Decimal('0.01'))
        for index in range(11):
            self.budget.reserve(str(index), Decimal('0.01'))
        with self.assertRaises(RuntimeError):
            self.budget.reserve('thirteenth', Decimal('0.01'))

    def test_over_reservation_cost_halts_even_below_total_cap(self):
        self.budget.reserve('a', Decimal('0.1'))
        self.budget.finish('a', '0.2', True, {})
        with self.assertRaises(RuntimeError):
            self.budget.reserve('b', Decimal('0.01'))

    def test_worst_case_twelve_requests_fit_authorized_budget(self):
        messages = [{'content': 'x' * BATCH.MAX_PROMPT_BYTES}]
        prices = [{'pricing': {'prompt': '0.000003', 'completion': '0.000015'}},
                  {'pricing': {'prompt': '0.000002', 'completion': '0.000012'}}]
        total = sum(BATCH.reserve_bound(messages, m) * 6 for m in prices)
        self.assertLessEqual(total, BATCH.CAP)
        with self.assertRaises(ValueError):
            BATCH.reserve_bound([{'content': 'x' * (BATCH.MAX_PROMPT_BYTES + 1)}], prices[0])


if __name__ == '__main__':
    unittest.main()
