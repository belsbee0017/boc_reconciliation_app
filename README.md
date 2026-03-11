# BOC Reconciliation and Discrepancy Detection Dashboard

BOC Reconciliation is a **data reconciliation and discrepancy detection dashboard** designed to compare customs shipment records and warehouse arrival records.

The system analyzes datasets using **Python-based data cleaning, SQL join logic, and interactive dashboard visualization** to detect inconsistencies between operational records.

This project demonstrates a simplified reconciliation workflow inspired by data review processes used in customs operations.

---

# Project Background

In customs and logistics operations, shipment information may appear across multiple datasets such as:

* processed customs entry records
* warehouse arrival records
* shipment documentation systems

Ensuring that these datasets are consistent is important for operational monitoring and audit processes.

However, manual reconciliation of records can be time-consuming and prone to human error.

This project demonstrates how **data cleaning, SQL-based comparison, and automated reporting** can help identify discrepancies across datasets.

---

# Key Features

### Excel Data Upload

Users upload an Excel workbook containing:

* **PO3 sheet** – processed customs entry records
* **A02 sheets** – warehouse arrival records

The system reads and prepares the datasets for reconciliation.

---

### Data Cleaning and Standardization

Before reconciliation, the system automatically:

* standardizes airway bill numbers
* removes empty or invalid records
* normalizes text fields
* converts date fields and numeric values

This ensures both datasets are comparable.

---

### SQL-Based Reconciliation

The system loads the cleaned datasets into an **in-memory SQLite database** and performs multiple SQL join operations.

#### INNER JOIN

Identifies records present in both datasets.

These represent **matched shipment records**.

#### LEFT JOIN

Identifies warehouse records with no matching customs entry.

These may indicate:

* pending customs processing
* abandoned shipments
* missing entries

#### RIGHT JOIN (Simulated)

Identifies customs entries without warehouse arrival records.

These may represent inconsistencies between systems.

#### FULL OUTER JOIN (Simulated)

Combines all results and classifies records into anomaly categories such as:

* MATCHED
* A02_ONLY
* PO3_ONLY
* REVIEW_NEEDED

---

### Duplicate Detection

The system detects duplicate airway bill numbers within warehouse records.

This helps identify:

* repeated shipment entries
* potential data entry errors

---

### Interactive Dashboard

The Streamlit dashboard provides:

* dataset previews
* dataset row counts
* anomaly classification results
* reconciliation output tables
* summary visualizations

Charts are generated using **Matplotlib**.

---

# Technology Stack

Language

* Python

Libraries

* Pandas – data cleaning and transformation
* NumPy – numerical operations
* SQLite – SQL-based reconciliation
* Streamlit – dashboard interface
* Matplotlib – data visualization

---

# Project Structure

```
boc_reconciliation_app/
│
├── app.py
│   Main Streamlit dashboard application containing:
│   - data upload interface
│   - data cleaning functions
│   - SQL reconciliation queries
│   - visualization dashboards
│
├── boc_demo.db
│   Sample SQLite database used during development.
│
├── requirements.txt
│   Python dependencies required to run the application.
│
└── README.md
    Project documentation and usage guide.
```

---

# System Workflow

The application follows this workflow:

Excel Dataset
↓
Data Cleaning (Pandas / NumPy)
↓
SQLite Data Processing
↓
SQL Join Reconciliation
↓
Anomaly Detection
↓
Streamlit Dashboard Visualization
↓
Export Results

---

# Running the Application

Install dependencies:

```
pip install streamlit pandas numpy matplotlib openpyxl
```

Run the application:

```
streamlit run app.py
```

Open the dashboard in your browser:

```
http://localhost:8501
```

---

# Example Use Case

This system can assist analysts in identifying:

* shipments recorded in warehouse datasets but not in customs entries
* customs entries without matching warehouse records
* duplicate shipment identifiers
* potential data inconsistencies across operational datasets

---

# Author

Brianne Leigh S. Baltazar
Information Technology Student – Mapúa University

GitHub
https://github.com/belsbee0017
