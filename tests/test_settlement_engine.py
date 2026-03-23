import unittest
from src.settlement_engine import calculate_settlement

class TestSettlementEngine(unittest.TestCase):

    def test_settlement_only_valid_transactions(self):
        txns = [
            {"merchant_id": "M1", "transaction_amount": "100", "transaction_status": "VALID"},
            {"merchant_id": "M1", "transaction_amount": "50", "transaction_status": "SUSPICIOUS"}
        ]
        result = calculate_settlement(txns)
        self.assertEqual(result["M1"]["amount"], 100)

    def test_settlement_amount_calculation(self):
        txns = [
            {"merchant_id": "M1", "transaction_amount": "100", "transaction_status": "VALID"},
            {"merchant_id": "M1", "transaction_amount": "200", "transaction_status": "VALID"}
        ]
        result = calculate_settlement(txns)
        self.assertEqual(result["M1"]["amount"], 300)

    def test_no_valid_transactions(self):
        txns = [
            {"merchant_id": "M1", "transaction_amount": "100", "transaction_status": "SUSPICIOUS"}
        ]
        result = calculate_settlement(txns)
        self.assertEqual(result["M1"]["amount"], 0)