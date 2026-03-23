def calculate_settlement(transactions):
    report = {}

    for t in transactions:
        mid = t['merchant_id']
        report.setdefault(mid, {
            "total": 0,
            "valid": 0,
            "fraud": 0,
            "amount": 0
        })

        report[mid]["total"] += 1

        if t["transaction_status"] == "VALID":
            report[mid]["valid"] += 1
            report[mid]["amount"] += float(t["transaction_amount"])
        else:
            report[mid]["fraud"] += 1

    return report