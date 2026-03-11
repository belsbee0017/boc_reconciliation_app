# BOC Reconciliation and Discrepancy Detection Dashboard

A Python-based data reconciliation dashboard designed to identify discrepancies between customs shipment records and warehouse records.

This project demonstrates a workflow for comparing operational datasets using **data cleaning, SQL joins, and dashboard visualization**.

The system was inspired by my internship work supporting data review processes within the **Bureau of Customs – MIS & Technology Group**.

---

# Project Background

During customs operations, shipment records may exist in multiple datasets such as:

• processed customs entry records
• warehouse arrival records

These datasets must be reconciled to ensure consistency and detect potential issues such as:

* missing records
* duplicate entries
* mismatched shipment identifiers

This project implements a **Python + SQL reconciliation workflow** that automates this comparison process and visualizes discrepancies through an interactive dashboard.

---

# Key Features

### Data Upload

Users upload an Excel file containing:

* **PO3 sheet** – processed customs entry records
* **A02 sheets** – warehouse arrival records

---

### Data Cleaning and Standardization

The system automatically:

* standardizes airway bill numbers
* removes invalid or empty entries
* normalizes text fields
* converts date and numeric values

This ensures datasets are consistent before reconciliation.

---

### SQL-Based Reconciliation

The system loads cleaned data into an **in-memory SQLite database** and performs several join operations.

#### INNER JOIN

Identifies airway bills present in both datasets (matched records).

#### LEFT JOIN

Identifies warehouse records with no matching customs entry.

#### RIGHT JOIN (Simulated)

Identifies customs entries without corresponding warehouse records.

#### FULL OUTER JOIN (Simulated)

Combines results and classifies anomalies such as:

* MATCHED
* A02_ONLY
* PO3_ONLY
* REVIEW_NEEDED

---

### Duplicate Detection

The system detects duplicate airway bills within warehouse records, which may indicate:

* repeated shipment entries
* data entry errors

---

### Interactive Dashboard

The Streamlit dashboard provides:

* dataset previews
* row counts
* anomaly summaries
* dataset comparison results
* visualization of record distributions

Charts are generated using **Matplotlib**.

---

# Technology Stack

Language
Python

Libraries

* Pandas – data cleaning and transformation
* NumPy – numerical processing
* SQLite – SQL-based dataset reconciliation
* Streamlit – dashboard interface
* Matplotlib – visualization

---

# Running the Application

Install dependencies:

pip install streamlit pandas numpy matplotlib openpyxl

Run the dashboard:

streamlit run app.py

Open in browser:

http://localhost:8501

---

# Repository Files

app.py
Main Streamlit dashboard application.

requirements.txt
Project dependencies.

boc_demo.db
Sample SQLite database used during development.

---

# Author

Brianne Leigh S. Baltazar
Information Technology Student – Mapúa University

GitHub
https://github.com/belsbee0017
