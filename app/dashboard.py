import streamlit as st
from pathlib import Path
import pandas as pd
import os
from datetime import datetime

# 🚀 Setup
st.set_page_config(page_title="📈 SOC Alert Dashboard", layout="wide")
st.title("🛡️ SOC Alert & Incident Report Dashboard")

# 📁 Locate report directory
report_dir = Path("output/generated_reports")
report_files = list(report_dir.glob("*"))

if not report_files:
    st.warning("⚠️ No reports found in 'output/generated_reports'.")
    st.stop()

# 🧠 Parse and extract report metadata
records = []
for file in report_files:
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

    # Try date from filename, else use modified time
    try:
        date_str = file.stem.split("_")[0]
        timestamp = datetime.strptime(date_str, "%Y-%m-%d")
    except Exception:
        timestamp = datetime.fromtimestamp(file.stat().st_mtime)

    records.append({
        "Filename": file.name,
        "Type": alert_type,
        "Escalation": escalation,
        "Date": timestamp,
        "Path": file,
        "Preview": content[:500],
        "Full": content
    })

df = pd.DataFrame(records)
df.sort_values("Date", ascending=False, inplace=True)

# 🧠 Sidebar Filters
with st.sidebar:
    st.header("🔍 Filter Reports")
    
    alert_types = df["Type"].dropna().unique().tolist()
    selected_types = st.multiselect("🧨 Alert Types", alert_types, default=alert_types)

    esc_levels = df["Escalation"].dropna().unique().tolist()
    selected_esc = st.multiselect("🚦 Escalation Level", esc_levels, default=esc_levels)

    min_date = df["Date"].min().date()
    max_date = df["Date"].max().date()
    date_range = st.date_input("🗓️ Date Range", (min_date, max_date), min_value=min_date, max_value=max_date)

    # Apply all filters
    df_filtered = df[
        (df["Type"].isin(selected_types)) &
        (df["Escalation"].isin(selected_esc)) &
        (df["Date"].dt.date >= date_range[0]) &
        (df["Date"].dt.date <= date_range[1])
    ]

# 📊 KPIs at top
st.markdown("## 📈 Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Total Reports", len(df_filtered))
col2.metric("Unique Alert Types", df_filtered['Type'].nunique())
col3.metric("Last Report", df_filtered['Date'].max().strftime("%Y-%m-%d"))

st.divider()

# 📋 Filtered Table
st.markdown(f"### 🧾 {len(df_filtered)} Matching Reports")
st.dataframe(
    df_filtered[["Filename", "Type", "Escalation", "Date"]],
    use_container_width=True,
    height=300
)

# 📂 Report Selection
selected_filename = st.selectbox("📄 Select a Report", df_filtered["Filename"].tolist())

if selected_filename:
    report = df_filtered[df_filtered["Filename"] == selected_filename].iloc[0]

    st.markdown(f"### 📝 Preview: `{report['Filename']}`")
    st.code(report["Preview"])

    with st.expander("🔎 Full Report Content"):
        st.text(report["Full"])

    with open(report["Path"], "rb") as f:
        st.download_button(
            label="📥 Download Full Report",
            data=f.read(),
            file_name=report["Filename"],
            mime="application/pdf" if report["Filename"].endswith(".pdf") else "text/markdown"
        )
