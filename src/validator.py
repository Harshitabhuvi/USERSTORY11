import os
from datetime import datetime
import logging

# Get project root path
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Create logs folder if not exists
log_path = os.path.join(BASE, "logs")
os.makedirs(log_path, exist_ok=True)

# Setup logging with correct path
logging.basicConfig(
    filename=os.path.join(log_path, "fraud_engine.log"),
    level=logging.INFO
)

def validate_transaction(txn, merchants):
    txn_id = txn.get("transaction_id", "UNKNOWN")

    if txn['merchant_id'] not in merchants:
        logging.info(f"{txn_id} - Unknown merchant")
        return False, "UNKNOWN_MERCHANT"

    if merchants[txn['merchant_id']]['status'] == 'BLOCKED':
        logging.info(f"{txn_id} - Blocked merchant")
        return False, "BLOCKED_MERCHANT"

    if float(txn['transaction_amount']) <= 0:
        logging.info(f"{txn_id} - Invalid amount")
        return False, "INVALID_AMOUNT"

    try:
        datetime.fromisoformat(txn['transaction_time'])
    except Exception:
        logging.info(f"{txn_id} - Invalid timestamp")
        return False, "INVALID_TIMESTAMP"

    return True, ""