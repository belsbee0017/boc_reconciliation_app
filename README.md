# BOC Reconciliation and Discrepancy Detection Dashboard

A Python-based data reconciliation dashboard for detecting inconsistencies between customs shipment records and warehouse arrival records.

This project demonstrates a workflow for identifying mismatched or missing shipment records using **Python, SQL joins, and an interactive Streamlit dashboard**.

---

# Project Background

This project was inspired by my internship experience at:

**Bureau of Customs – NAIA**
Management Information Systems and Technology Group
IT Intern | January 2025 – March 2025

During my internship, I assisted in managing operational data and supporting internal documentation for systems used by the MIS & Technology Group.

One of the operational challenges in customs data management is verifying whether **warehouse shipment records match processed customs entries and payment records**.
This project demonstrates a simplified version of a **data reconciliation workflow** used to detect inconsistencies between datasets.

---

# Internship Experience Related to this Project

During my internship, I worked on:

* Assisting in managing operational data used by internal teams
* Supporting documentation of internal system workflows and procedures
* Developing a **Python-based discrepancy detection workflow** to identify inconsistencies between shipment records and payment entries
* Using **SQL-based comparison logic** to reconcile multiple datasets
* Automating reporting using **Excel VBA** to support internal audits and reconciliation tasks

This repository demonstrates a simplified prototype of that workflow using open-source tools.

---

# Technologies Used

Python

Libraries used:

* Pandas – data cleaning and transformation
* NumPy – numerical operations
* SQLite – SQL-based reconciliation queries
* Streamlit – interactive web dashboard
* Matplotlib – data visualization

---

# System Workflow

The application performs the following steps:

### 1. Data Upload

Users upload an Excel file containing:

* **PO3 sheet** – processed customs entry records
* **A02 sheets** – warehouse arrival records

---

### 2. Data Cleaning and Standardization

The system cleans and standardizes the data by:

* Normalizing airway bill numbers
* Removing invalid or empty records
* Converting text fields to a consistent format
* Converting date and numeric columns

This ensures reliable comparison between datasets.

---

### 3. SQL-Based Reconciliation

Cleaned datasets are loaded into an **in-memory SQLite database**.

Several SQL joins are then used to compare the datasets.

#### INNER JOIN

Records present in **both PO3 and A02 datasets**
Represents matched and processed shipments.

#### LEFT JOIN

Records present in **A02 but not in PO3**
Possible cases include abandoned shipments or pending customs processing.

#### RIGHT JOIN (Simulated)

Records present in **PO3 but not in A02**
May indicate payment entries without corresponding warehouse records.

#### FULL OUTER JOIN (Simulated)

Combines all results and classifies anomalies such as:

* MATCHED
* A02_ONLY
* PO3_ONLY
* REVIEW_NEEDED

---

### 4. Duplicate Detection

The system also identifies **duplicate airway bills in A02 sheets**, which may indicate data entry issues.

---

### 5. Dashboard Visualization

The Streamlit dashboard displays:

* Dataset row counts
* Matched and unmatched shipment records
* Anomaly classifications
* Weekly warehouse record counts

Charts are generated using **Matplotlib**.

---

### 6. Export Results

Users can download the reconciliation output as a **CSV file** for review or audit purposes.

---

# Running the Application

Install dependencies:

pip install streamlit pandas numpy matplotlib openpyxl

Run the application:

streamlit run app.py

The dashboard will open in your browser:

http://localhost:8501

---

# Repository Files

app.py
Main Streamlit dashboard application.

requirements.txt
Python dependencies required to run the project.

boc_demo.db
Sample SQLite database used during development.

---

# Author

Brianne Leigh S. Baltazar
Information Technology Student – Mapúa University

GitHub:
https://github.com/belsbee0017
