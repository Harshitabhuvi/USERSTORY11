import unittest
from src.fraud_engine import detect_fraud

class TestFraudEngine(unittest.TestCase):

    def test_high_value_transaction_flag(self):
        txn = {"transaction_amount": "150000", "country": "IN", "payment_method": "CARD"}
        merchant = {"country": "IN"}
        status, reason = detect_fraud(txn, merchant, 0)
        self.assertEqual(status, "SUSPICIOUS")

    def test_cross_border_transaction_flag(self):
        txn = {"transaction_amount": "500", "country": "US", "payment_method": "CARD"}
        merchant = {"country": "IN"}
        status, reason = detect_fraud(txn, merchant, 0)
        self.assertEqual(status, "SUSPICIOUS")

    def test_crypto_high_value_flag(self):
        txn = {"transaction_amount": "60000", "country": "IN", "payment_method": "CRYPTO"}
        merchant = {"country": "IN"}
        status, reason = detect_fraud(txn, merchant, 0)
        self.assertEqual(status, "SUSPICIOUS")

    def test_multiple_fraud_rules_trigger(self):
        txn = {"transaction_amount": "200000", "country": "US", "payment_method": "CRYPTO"}
        merchant = {"country": "IN"}
        status, reason = detect_fraud(txn, merchant, 5)
        self.assertEqual(status, "SUSPICIOUS")

    def test_rapid_transactions_flagged(self):
        txn = {"transaction_amount": "500", "country": "IN", "payment_method": "CARD"}
        merchant = {"country": "IN"}
        status, reason = detect_fraud(txn, merchant, 4)
        self.assertEqual(status, "SUSPICIOUS")