import csv
import json
import os

# Get project root path
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Create outputs folder if not exists
output_path = os.path.join(BASE, "outputs")
os.makedirs(output_path, exist_ok=True)


def save_processed(transactions):
    """
    Saves processed transactions with fraud status
    """
    if not transactions:
        return

    file_path = os.path.join(output_path, "processed_transactions.csv")

    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=transactions[0].keys())
        writer.writeheader()
        writer.writerows(transactions)


def save_settlement(report, merchants):
    """
    Generates merchant settlement report
    """
    rows = []

    for merchant_id, data in report.items():

        if merchant_id not in merchants:
            continue

        rows.append({
            "merchant_id": merchant_id,
            "merchant_name": merchants[merchant_id].get("merchant_name", "UNKNOWN"),
            "total_transactions": data["total"],
            "valid_transactions": data["valid"],
            "fraud_transactions": data["fraud"],
            "settlement_amount": data["amount"]
        })

    if not rows:
        return

    file_path = os.path.join(output_path, "merchant_settlement_report.csv")

    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


def save_fraud_summary(transactions):
    """
    Generates fraud summary JSON report
    """
    summary = {
        "total_transactions": len(transactions),
        "valid_transactions": 0,
        "fraud_transactions": 0,
        "high_value_frauds": 0,
        "cross_border_frauds": 0,
        "rapid_transaction_frauds": 0
    }

    for txn in transactions:
        if txn["transaction_status"] == "VALID":
            summary["valid_transactions"] += 1
        else:
            summary["fraud_transactions"] += 1

        reason = txn.get("fraud_reason", "")

        if "HIGH_VALUE_TRANSACTION" in reason:
            summary["high_value_frauds"] += 1
        if "CROSS_BORDER_TRANSACTION" in reason:
            summary["cross_border_frauds"] += 1
        if "RAPID_TRANSACTIONS" in reason:
            summary["rapid_transaction_frauds"] += 1

    file_path = os.path.join(output_path, "fraud_summary.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=4)

    # 🔥 Print dashboard
    print_dashboard(summary)


# ----------- DASHBOARD FUNCTIONS -----------

def print_dashboard(summary):
    print("\n========== FRAUD ANALYTICS DASHBOARD ==========")
    print(f"Total Transactions       : {summary['total_transactions']}")
    print(f"Valid Transactions       : {summary['valid_transactions']}")
    print(f"Fraud Transactions       : {summary['fraud_transactions']}")
    print("----------------------------------------------")
    print(f"High Value Frauds        : {summary['high_value_frauds']}")
    print(f"Cross Border Frauds      : {summary['cross_border_frauds']}")
    print(f"Rapid Transaction Frauds : {summary['rapid_transaction_frauds']}")
    print("==============================================\n")


def print_top_merchants(report, merchants):
    print("\nTop Fraud-Affected Merchants:")

    sorted_merchants = sorted(
        report.items(),
        key=lambda x: x[1]["fraud"],
        reverse=True
    )[:3]

    for mid, data in sorted_merchants:
        name = merchants.get(mid, {}).get("merchant_name", "UNKNOWN")
        print(f"{name} ({mid}) -> Fraud Txns: {data['fraud']}")


def print_reason_breakdown(transactions):
    print("\nFraud Reason Breakdown:")

    reason_count = {}

    for txn in transactions:
        if txn["transaction_status"] == "SUSPICIOUS":
            reasons = txn.get("fraud_reason", "").split(",")
            for r in reasons:
                if r:
                    reason_count[r] = reason_count.get(r, 0) + 1

    for reason, count in reason_count.items():
        print(f"{reason} -> {count}")