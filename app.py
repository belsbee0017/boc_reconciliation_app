import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import matplotlib.pyplot as plt

st.set_page_config(page_title="BOC Reconciliation Dashboard", layout="wide")

st.title("BOC Reconciliation and Discrepancy Detection Dashboard")
st.write("Upload an Excel file containing one PO3 sheet and one or more A02 sheets.")

uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx", "xlsm"])


def standardize_airwaybill(series):
    return (
        series.astype(str)
        .str.strip()
        .str.upper()
        .str.replace(r"\.0$", "", regex=True)
        .replace(["NAN", "NONE", ""], np.nan)
    )


def clean_po3(df):
    df = df.copy()
    df.columns = df.columns.str.strip().str.upper()

    keep_cols = [
        "ENTRY_CODE",
        "AWBHBL",
        "PORT",
        "LOCGOODS",
        "REGISTRYDATE",
        "ASSESSMENTDATE",
        "COLLECTIONDATE",
        "CONSIGNEE",
        "BROKER",
        "GOODS_DESCRIPTION",
        "TOTALASSESSMENT",
        "GROSSMASS",
        "HSCODE",
    ]

    existing_cols = [col for col in keep_cols if col in df.columns]
    df = df[existing_cols]

    if "AWBHBL" not in df.columns:
        return pd.DataFrame()

    df["AWBHBL"] = standardize_airwaybill(df["AWBHBL"])
    df = df[df["AWBHBL"].notna()]

    text_cols = ["ENTRY_CODE", "PORT", "LOCGOODS", "CONSIGNEE", "BROKER", "GOODS_DESCRIPTION"]
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.upper()

    for col in ["REGISTRYDATE", "ASSESSMENTDATE", "COLLECTIONDATE"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    if "TOTALASSESSMENT" in df.columns:
        df["TOTALASSESSMENT"] = pd.to_numeric(df["TOTALASSESSMENT"], errors="coerce")

    if "GROSSMASS" in df.columns:
        df["GROSSMASS"] = pd.to_numeric(df["GROSSMASS"], errors="coerce")

    df = df.drop_duplicates(subset=["AWBHBL", "ENTRY_CODE"], keep="first")
    return df


def clean_a02(df, sheet_name):
    df = df.copy()
    df.columns = df.columns.str.strip()

    rename_map = {
        "Port of Discharge": "port_of_discharge",
        "Consignee": "consignee",
        "Flight No. and Voyage No.": "flight_no",
        "Airwaybill": "airwaybill",
        "Goods Description": "goods_description",
        "HS Code": "hs_code",
        "Packages (Number and Kind)": "packages",
        "Duties and Taxes": "duties_taxes",
        "Gross Weight": "gross_weight",
        "Actual Date of Arrival": "actual_date_of_arrival",
    }

    df = df.rename(columns=rename_map)

    needed_cols = [
        "port_of_discharge",
        "consignee",
        "flight_no",
        "airwaybill",
        "goods_description",
        "hs_code",
        "packages",
        "duties_taxes",
        "gross_weight",
        "actual_date_of_arrival",
    ]

    existing_cols = [col for col in needed_cols if col in df.columns]
    df = df[existing_cols]

    if "airwaybill" not in df.columns:
        return pd.DataFrame()

    df["airwaybill"] = standardize_airwaybill(df["airwaybill"])
    df = df[df["airwaybill"].notna()]

    text_cols = ["port_of_discharge", "consignee", "flight_no", "goods_description"]
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.upper()

    if "actual_date_of_arrival" in df.columns:
        df["actual_date_of_arrival"] = pd.to_datetime(df["actual_date_of_arrival"], errors="coerce")

    if "gross_weight" in df.columns:
        df["gross_weight"] = pd.to_numeric(df["gross_weight"], errors="coerce")

    if "duties_taxes" in df.columns:
        df["duties_taxes"] = pd.to_numeric(df["duties_taxes"], errors="coerce")

    df["source_sheet"] = sheet_name
    df = df.drop_duplicates(subset=["airwaybill", "source_sheet"], keep="first")
    return df


if uploaded_file:
    excel_file = pd.ExcelFile(uploaded_file)
    available_sheets = excel_file.sheet_names

    st.subheader("Available Sheets")
    st.write(available_sheets)

    po3_candidates = [s for s in available_sheets if "PO3" in s.upper() or "P03" in s.upper()]
    a02_candidates = [s for s in available_sheets if "A02" in s.upper()]
    matched_candidates = [s for s in available_sheets if "MATCHED" in s.upper()]

    if not po3_candidates:
        st.error("No PO3/P03 sheet found.")
    elif not a02_candidates:
        st.error("No A02 sheets found.")
    else:
        po3_sheet = po3_candidates[0]

        po3_raw = pd.read_excel(uploaded_file, sheet_name=po3_sheet)
        po3_df = clean_po3(po3_raw)

        a02_list = []
        for sheet in a02_candidates:
            temp_df = pd.read_excel(uploaded_file, sheet_name=sheet)
            temp_df = clean_a02(temp_df, sheet)
            if not temp_df.empty:
                a02_list.append(temp_df)

        if not a02_list:
            st.error("A02 sheets were found, but no usable airwaybill data was loaded.")
        else:
            a02_df = pd.concat(a02_list, ignore_index=True)

            st.success("PO3 and A02 sheets loaded successfully.")

            st.subheader("Cleaned Dataset Preview")
            col1, col2 = st.columns(2)

            with col1:
                st.write("PO3 Preview")
                st.dataframe(po3_df.head(10), use_container_width=True)

            with col2:
                st.write("Combined A02 Preview")
                st.dataframe(a02_df.head(10), use_container_width=True)

            st.subheader("Row Counts")
            row_counts = pd.DataFrame({
                "Dataset": ["PO3", "A02 Combined"],
                "Row Count": [len(po3_df), len(a02_df)]
            })
            st.dataframe(row_counts, use_container_width=True)

            fig, ax = plt.subplots()
            ax.bar(row_counts["Dataset"], row_counts["Row Count"])
            ax.set_title("Records per Dataset")
            ax.set_ylabel("Count")
            st.pyplot(fig)

            conn = sqlite3.connect(":memory:")
            po3_df.to_sql("po3_records", conn, index=False, if_exists="replace")
            a02_df.to_sql("a02_records", conn, index=False, if_exists="replace")

            inner_join_sql = """
            SELECT
                p.AWBHBL AS airwaybill,
                p.ENTRY_CODE,
                p.PORT,
                p.LOCGOODS,
                p.COLLECTIONDATE,
                p.TOTALASSESSMENT,
                a.source_sheet,
                a.actual_date_of_arrival,
                a.flight_no,
                a.goods_description,
                a.gross_weight
            FROM po3_records p
            INNER JOIN a02_records a
                ON p.AWBHBL = a.airwaybill
            """

            left_join_sql = """
            SELECT
                a.airwaybill,
                a.source_sheet,
                a.actual_date_of_arrival,
                a.flight_no,
                a.goods_description,
                a.gross_weight
            FROM a02_records a
            LEFT JOIN po3_records p
                ON a.airwaybill = p.AWBHBL
            WHERE p.AWBHBL IS NULL
            """

            right_join_sim_sql = """
            SELECT
                p.AWBHBL AS airwaybill,
                p.ENTRY_CODE,
                p.PORT,
                p.LOCGOODS,
                p.COLLECTIONDATE,
                p.TOTALASSESSMENT
            FROM po3_records p
            LEFT JOIN a02_records a
                ON p.AWBHBL = a.airwaybill
            WHERE a.airwaybill IS NULL
            """

            full_outer_sim_sql = """
            SELECT
                p.AWBHBL AS po3_airwaybill,
                a.airwaybill AS a02_airwaybill,
                p.ENTRY_CODE,
                p.PORT,
                p.LOCGOODS,
                p.TOTALASSESSMENT,
                a.source_sheet,
                a.actual_date_of_arrival,
                CASE
                    WHEN p.AWBHBL IS NOT NULL AND a.airwaybill IS NOT NULL THEN 'MATCHED'
                    WHEN p.AWBHBL IS NULL AND a.airwaybill IS NOT NULL THEN 'A02_ONLY'
                    WHEN p.AWBHBL IS NOT NULL AND a.airwaybill IS NULL THEN 'PO3_ONLY'
                    ELSE 'REVIEW_NEEDED'
                END AS anomaly_type
            FROM po3_records p
            LEFT JOIN a02_records a
                ON p.AWBHBL = a.airwaybill

            UNION ALL

            SELECT
                p.AWBHBL AS po3_airwaybill,
                a.airwaybill AS a02_airwaybill,
                p.ENTRY_CODE,
                p.PORT,
                p.LOCGOODS,
                p.TOTALASSESSMENT,
                a.source_sheet,
                a.actual_date_of_arrival,
                'A02_ONLY' AS anomaly_type
            FROM a02_records a
            LEFT JOIN po3_records p
                ON a.airwaybill = p.AWBHBL
            WHERE p.AWBHBL IS NULL
            """

            duplicate_a02_sql = """
            SELECT
                airwaybill,
                COUNT(*) AS duplicate_count
            FROM a02_records
            GROUP BY airwaybill
            HAVING COUNT(*) > 1
            ORDER BY duplicate_count DESC, airwaybill
            """

            matched_df = pd.read_sql_query(inner_join_sql, conn)
            a02_only_df = pd.read_sql_query(left_join_sql, conn)
            po3_only_df = pd.read_sql_query(right_join_sim_sql, conn)
            full_df = pd.read_sql_query(full_outer_sim_sql, conn)
            duplicate_a02_df = pd.read_sql_query(duplicate_a02_sql, conn)

            full_df["final_flag"] = np.select(
                [
                    full_df["anomaly_type"] == "MATCHED",
                    full_df["anomaly_type"] == "A02_ONLY",
                    full_df["anomaly_type"] == "PO3_ONLY",
                ],
                [
                    "Matched / processed with warehouse record",
                    "Warehouse-only / possible abandoned or pending review",
                    "Processed-only / payment activity without warehouse match",
                ],
                default="Review needed"
            )

            st.subheader("SQL Join Results")

            tab1, tab2, tab3, tab4, tab5 = st.tabs([
                "INNER JOIN",
                "LEFT JOIN",
                "RIGHT JOIN (Simulated)",
                "FULL OUTER JOIN (Simulated)",
                "Duplicates"
            ])

            with tab1:
                st.write("Matched airway bills found in both PO3 and A02.")
                st.dataframe(matched_df, use_container_width=True)

            with tab2:
                st.write("A02 records with no matching PO3 record.")
                st.dataframe(a02_only_df, use_container_width=True)

            with tab3:
                st.write("PO3 records with no matching A02 record.")
                st.dataframe(po3_only_df, use_container_width=True)

            with tab4:
                st.write("Combined reconciliation output with anomaly classification.")
                st.dataframe(full_df, use_container_width=True)

            with tab5:
                st.write("Duplicate airway bills found in A02 sheets.")
                st.dataframe(duplicate_a02_df, use_container_width=True)

            st.subheader("Anomaly Summary")
            summary_df = full_df["anomaly_type"].value_counts().reset_index()
            summary_df.columns = ["anomaly_type", "count"]
            st.dataframe(summary_df, use_container_width=True)

            fig2, ax2 = plt.subplots()
            ax2.bar(summary_df["anomaly_type"], summary_df["count"])
            ax2.set_title("Anomaly Counts by Type")
            ax2.set_ylabel("Count")
            st.pyplot(fig2)

            st.subheader("Weekly A02 Sheet Counts")
            weekly_counts = a02_df["source_sheet"].value_counts().reset_index()
            weekly_counts.columns = ["source_sheet", "count"]
            st.dataframe(weekly_counts, use_container_width=True)

            fig3, ax3 = plt.subplots()
            ax3.bar(weekly_counts["source_sheet"], weekly_counts["count"])
            ax3.set_title("A02 Records per Weekly Sheet")
            ax3.set_ylabel("Count")
            ax3.tick_params(axis="x", rotation=45)
            st.pyplot(fig3)

            st.subheader("Export Results")
            st.download_button(
                label="Download Full Reconciliation CSV",
                data=full_df.to_csv(index=False).encode("utf-8"),
                file_name="boc_reconciliation_results.csv",
                mime="text/csv"
            )

            conn.close()

            if matched_candidates:
                st.subheader("Reference Sheet Found")
                st.write(f"Matched Records sheet detected: {matched_candidates[0]}")