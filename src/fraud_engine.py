import os
import json

# Load config file
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(BASE, "config.json")) as f:
    CONFIG = json.load(f)


# -------- Rule Functions --------

def high_value_rule(txn, merchant, recent_count):
    amount = float(txn['transaction_amount'])
    return amount > CONFIG["HIGH_VALUE_THRESHOLD"], "HIGH_VALUE_TRANSACTION"


def cross_border_rule(txn, merchant, recent_count):
    return txn['country'] != merchant['country'], "CROSS_BORDER_TRANSACTION"


def crypto_rule(txn, merchant, recent_count):
    amount = float(txn['transaction_amount'])
    return (
        txn['payment_method'] == "CRYPTO" and amount > CONFIG["CRYPTO_THRESHOLD"],
        "CRYPTO_HIGH_VALUE"
    )


def rapid_rule(txn, merchant, recent_count):
    return recent_count > CONFIG["RAPID_TXN_COUNT"], "RAPID_TRANSACTIONS"


# -------- Rule Engine --------

RULES = [
    high_value_rule,
    cross_border_rule,
    crypto_rule,
    rapid_rule
]


def detect_fraud(txn, merchant, recent_count):
    reasons = []

    for rule in RULES:
        triggered, reason = rule(txn, merchant, recent_count)
        if triggered:
            reasons.append(reason)

    if reasons:
        return "SUSPICIOUS", ",".join(reasons)

    return "VALID", ""