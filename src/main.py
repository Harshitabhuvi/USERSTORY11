import os
import json
from collections import defaultdict
from datetime import datetime, timedelta

from loader import load_csv
from validator import validate_transaction
from fraud_engine import detect_fraud
from settlement_engine import calculate_settlement
from reporter import (
    save_processed,
    save_settlement,
    save_fraud_summary,
    print_top_merchants,
    print_reason_breakdown
)

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load config
with open(os.path.join(BASE, "config.json")) as f:
    CONFIG = json.load(f)

merchants = {m["merchant_id"]: m for m in load_csv(f"{BASE}/data/merchants.csv")}
transactions = load_csv(f"{BASE}/data/transactions.csv")

processed = []

# Track customer transactions within time window
customer_txn_times = defaultdict(list)

for txn in transactions:
    valid, reason = validate_transaction(txn, merchants)

    # Ignore invalid transactions
    if not valid:
        continue

    # --- Rapid transaction logic (config-based time window) ---
    cust_id = txn["customer_id"]
    txn_time = datetime.fromisoformat(txn["transaction_time"])

    # Keep only transactions within configured time window
    customer_txn_times[cust_id] = [
        t for t in customer_txn_times[cust_id]
        if txn_time - t <= timedelta(minutes=CONFIG["TIME_WINDOW_MINUTES"])
    ]

    customer_txn_times[cust_id].append(txn_time)
    recent_count = len(customer_txn_times[cust_id])

    # --- Fraud detection ---
    status, fraud_reason = detect_fraud(
        txn,
        merchants[txn["merchant_id"]],
        recent_count
    )

    txn["transaction_status"] = status
    txn["fraud_reason"] = fraud_reason
    txn["fraud_flag"] = status == "SUSPICIOUS"

    processed.append(txn)

# --- Output generation ---
save_processed(processed)

settlement = calculate_settlement(processed)
save_settlement(settlement, merchants)

save_fraud_summary(processed)

# 🔥 NEW: Dashboard outputs
print_top_merchants(settlement, merchants)
print_reason_breakdown(processed)

print("Processing completed successfully!")