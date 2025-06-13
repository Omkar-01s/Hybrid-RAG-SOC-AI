import streamlit as st
from pathlib import Path
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="📈 SOC Dashboard", layout="wide")
st.title("📊 SOC Alert & Report Dashboard")

# ✅ Step 1: Locate report directory
report_dir = Path("output/generated_reports")
report_files = list(report_dir.glob("*"))

if not report_files:
    st.warning("No reports found in output/generated_reports.")
    st.stop()

# ✅ Step 2: Scan and extract summary from reports
records = []
for file in report_files:
    ext = file.suffix
    try:
        with open(file, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except Exception as e:
        st.error(f"Error reading {file.name}: {e}")
        continue

    alert_type = "Unknown"
    escalation = "Unknown"

    if "Alert Type:" in content:
        alert_type = content.split("Alert Type:")[1].split("\n")[0].strip()
    if "Escalation Level:" in content:
        escalation = content.split("Escalation Level:")[1].split("\n")[0].strip()

    # ✅ Try to extract a date from the filename, fallback to file modified time
    try:
        # Example filename: 2025-06-11_alert123.md
        possible_date = file.stem.split("_")[0]
        timestamp = datetime.strptime(possible_date, "%Y-%m-%d")
    except Exception:
        # Fallback: use file's last modified time
        timestamp = datetime.fromtimestamp(os.path.getmtime(file))

    records.append({
        "Filename": file.name,
        "Type": alert_type,
        "Escalation": escalation,
        "Date": timestamp,
        "Path": file,
        "Preview": content[:500]
    })

df = pd.DataFrame(records)
df["Date"] = pd.to_datetime(df["Date"], errors='coerce')

# ✅ Step 3: Sidebar filters
with st.sidebar:
    st.header("🔍 Filter Reports")
    alert_types = df["Type"].unique().tolist()
    selected_types = st.multiselect("Alert Type", alert_types, default=alert_types)

    esc_levels = df["Escalation"].unique().tolist()
    selected_esc = st.multiselect("Escalation Level", esc_levels, default=esc_levels)

    df_filtered = df[df["Type"].isin(selected_types) & df["Escalation"].isin(selected_esc)]

# ✅ Step 4: Display filtered table
st.markdown(f"### 🧾 Found {len(df_filtered)} Reports")
st.dataframe(df_filtered[["Filename", "Type", "Escalation", "Date"]].sort_values("Date", ascending=False))

# ✅ Step 5: Select report to preview and download
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
