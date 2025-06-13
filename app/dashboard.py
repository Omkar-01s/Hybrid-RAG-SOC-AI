# app/dashboard.py

import streamlit as st
from pathlib import Path
import pandas as pd

st.set_page_config(page_title="📈 SOC Dashboard", layout="wide")
st.title("📊 SOC Alert & Report Dashboard")

report_dir = Path("output/generated_reports")
report_files = list(report_dir.glob("*"))

# Step 1: Scan and summarize reports
records = []
for file in report_files:
    ext = file.suffix
    with open(file, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    alert_type = "Unknown"
    escalation = "Unknown"
    timestamp = file.stem.split("_")[0]
    
    # Try to extract info from markdown content
    if "Alert Type:" in content:
        alert_type = content.split("Alert Type:")[1].split("\n")[0].strip()
    if "Escalation Level:" in content:
        escalation = content.split("Escalation Level:")[1].split("\n")[0].strip()

    records.append({
        "Filename": file.name,
        "Type": alert_type,
        "Escalation": escalation,
        "Date": timestamp,
        "Path": file,
        "Preview": content[:500]  # first 500 characters
    })

df = pd.DataFrame(records)
df["Date"] = pd.to_datetime(df["Date"], errors='coerce')

# Step 2: Filter
with st.sidebar:
    st.header("🔍 Filter Reports")
    alert_types = df["Type"].unique().tolist()
    selected_types = st.multiselect("Alert Type", alert_types, default=alert_types)

    esc_levels = df["Escalation"].unique().tolist()
    selected_esc = st.multiselect("Escalation Level", esc_levels, default=esc_levels)

    df_filtered = df[df["Type"].isin(selected_types) & df["Escalation"].isin(selected_esc)]

# Step 3: Display Table
st.markdown(f"### 🧾 Found {len(df_filtered)} Reports")
st.dataframe(df_filtered[["Filename", "Type", "Escalation", "Date"]].sort_values("Date", ascending=False))

# Step 4: Select + Preview Report
selected_report = st.selectbox("📂 View Report", df_filtered["Filename"].tolist())
if selected_report:
    report = df_filtered[df_filtered["Filename"] == selected_report].iloc[0]
    st.subheader("📝 Report Preview")
    st.code(report["Preview"])

    with open(report["Path"], "rb") as f:
        st.download_button(
            label="📥 Download Report",
            data=f.read(),
            file_name=report["Filename"],
            mime="application/pdf" if report["Filename"].endswith(".pdf") else "text/markdown"
        )
