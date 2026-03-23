import streamlit as st
import pandas as pd
import json
import os

# --- Page Config (IMPORTANT) ---
st.set_page_config(layout="wide")

BASE = os.path.dirname(os.path.abspath(__file__))

# Load data
processed = pd.read_csv(os.path.join(BASE, "outputs/processed_transactions.csv"))
settlement = pd.read_csv(os.path.join(BASE, "outputs/merchant_settlement_report.csv"))

with open(os.path.join(BASE, "outputs/fraud_summary.json")) as f:
    summary = json.load(f)

# Title
st.title("🚨 Fraud Detection Dashboard")

# --- Prepare Data ---
fraud_data = {
    "Type": ["High Value", "Cross Border", "Rapid"],
    "Count": [
        summary["high_value_frauds"],
        summary["cross_border_frauds"],
        summary["rapid_transaction_frauds"]
    ]
}
fraud_df = pd.DataFrame(fraud_data)

merchant_fraud = settlement[["merchant_name", "fraud_transactions"]]
merchant_fraud = merchant_fraud.sort_values(by="fraud_transactions", ascending=False)

# --- Tabs ---
tab1, tab2, tab3 = st.tabs(["📊 Overview", "🏆 Merchants", "📁 Transactions"])

# =======================
# 📊 TAB 1: OVERVIEW
# =======================
with tab1:
    col1, col2, col3 = st.columns(3)

    col1.metric("Total Transactions", summary["total_transactions"])
    col2.metric("Valid Transactions", summary["valid_transactions"])
    col3.metric("Fraud Transactions", summary["fraud_transactions"])

    st.markdown("---")

    colA, colB = st.columns(2)

    with colA:
        st.subheader("📊 Fraud Breakdown")
        st.bar_chart(fraud_df.set_index("Type"))

    with colB:
        st.subheader("🧾 Transaction Status")
        status_counts = processed["transaction_status"].value_counts()
        st.bar_chart(status_counts)

# =======================
# 🏆 TAB 2: MERCHANTS
# =======================
with tab2:
    st.subheader("🏆 Fraud by Merchant")
    st.bar_chart(merchant_fraud.set_index("merchant_name"))

# =======================
# 📁 TAB 3: TRANSACTIONS
# =======================
with tab3:
    st.subheader("📁 Processed Transactions")

    # 🔍 Filter
    status_filter = st.selectbox(
        "Filter by Status",
        ["ALL", "VALID", "SUSPICIOUS"]
    )

    if status_filter != "ALL":
        filtered = processed[processed["transaction_status"] == status_filter]
    else:
        filtered = processed

    # 📊 Table
    st.dataframe(
        filtered,
        use_container_width=True,
        height=400
    )