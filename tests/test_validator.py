import unittest
from src.validator import validate_transaction

class TestValidator(unittest.TestCase):

    def test_invalid_merchant_rejected(self):
        txn = {
            "merchant_id": "M999",
            "transaction_amount": "100",
            "transaction_time": "2024-05-01T10:00"
        }
        merchants = {}
        valid, _ = validate_transaction(txn, merchants)
        self.assertFalse(valid)

    def test_blocked_merchant_rejected(self):
        txn = {
            "merchant_id": "M1",
            "transaction_amount": "100",
            "transaction_time": "2024-05-01T10:00"
        }
        merchants = {"M1": {"status": "BLOCKED"}}
        valid, _ = validate_transaction(txn, merchants)
        self.assertFalse(valid)

    def test_negative_amount_rejected(self):
        txn = {
            "merchant_id": "M1",
            "transaction_amount": "-50",
            "transaction_time": "2024-05-01T10:00"
        }
        merchants = {"M1": {"status": "ACTIVE"}}
        valid, _ = validate_transaction(txn, merchants)
        self.assertFalse(valid)

    def test_invalid_timestamp_handling(self):
        txn = {
            "merchant_id": "M1",
            "transaction_amount": "100",
            "transaction_time": "invalid-date"
        }
        merchants = {"M1": {"status": "ACTIVE"}}
        valid, _ = validate_transaction(txn, merchants)
        self.assertFalse(valid)