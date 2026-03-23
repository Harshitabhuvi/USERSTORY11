import os
from datetime import datetime
import logging

# Get project root path
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Create logs folder if not exists
log_path = os.path.join(BASE, "logs")
os.makedirs(log_path, exist_ok=True)

log_file = os.path.join(log_path, "fraud_engine.log")

# 🔥 CLEAR OLD HANDLERS
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

# 🔥 OVERWRITE LOG FILE EACH RUN (mode="w")
logging.basicConfig(
    filename=log_file,
    filemode="w",   # ✅ THIS FIXES YOUR ISSUE
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
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