# 🚨 Fraud Detection & Settlement Engine

## 📌 Project Overview

This project is a Python-based fraud detection and settlement engine designed for a fintech system. It processes transaction data, validates records, detects fraudulent activities using rule-based logic, and generates settlement reports.

Additionally, an interactive dashboard is built using Streamlit to visualize fraud insights.

-----

## ⚙️ Features

### 🔹 Data Processing

* Load transaction and merchant data from CSV files
* Validate transaction records
* Handle invalid data (blocked merchants, invalid timestamps, negative amounts)

### 🔹 Fraud Detection

* High-value transactions (>100000)
* Cross-border transactions
* Crypto high-value transactions (>50000)
* Rapid transactions (multiple transactions in short time)

### 🔹 Settlement Engine

* Calculates settlement only for valid transactions
* Aggregates merchant-wise settlement amounts

### 🔹 Reporting

* Processed transactions CSV
* Merchant settlement report
* Fraud summary JSON

### 🔹 Dashboard (Streamlit)

* Fraud analytics overview
* Merchant-wise fraud insights
* Interactive charts and tables
* Filtering support

---

## 📁 Project Structure

```
fraud_detection_project/
│
├── data/
├── logs/
├── outputs/
├── src/
├── tests/
├── dashboard.py
├── README.md
└── .gitignore
```

---

## ▶️ How to Run

### 1. Run Backend Processing

```bash
cd src
python main.py
```

### 2. Run Dashboard

```bash
streamlit run dashboard.py
```

---

## 🧪 Run Tests

```bash
python -m unittest discover tests -v
```

---

## 📊 Coverage

```bash
python -m coverage run -m unittest discover tests
python -m coverage report
```

---

## 📈 Sample Output

* Fraud analytics dashboard
* CSV and JSON reports
* Merchant fraud insights

---

## 🧠 Key Concepts Used

* Python modular architecture
* Data validation & error handling
* Rule-based fraud detection
* Aggregation logic
* Unit testing (unittest)
* Code coverage
* Streamlit dashboard development

---

## 🚀 Future Improvements

* Machine learning-based fraud detection
* Real-time streaming data processing
* API integration
* Advanced visualization

---

