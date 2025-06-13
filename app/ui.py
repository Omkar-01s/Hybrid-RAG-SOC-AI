# app/ui.py

import streamlit as st
import json
from pathlib import Path

from main import generate_playbook
from agents.escalation_agent import decide_escalation_level
from llm.response_engine import generate_summary
from rag.hybrid import HybridRetriever

st.set_page_config(page_title="SOC Playbook Generator", layout="wide")
st.title("🛡️ Security Playbook Generator for SOC Teams")

st.sidebar.header("🔍 Load Alert")

# Option to select a sample alert
alert_files = list(Path("data/alerts").glob("*.json"))
sample_alert = st.sidebar.selectbox(
    "Choose a sample alert file",
    options=[""] + [f.name for f in alert_files]
)

# Option to upload a new alert JSON file
uploaded_file = st.sidebar.file_uploader("Or upload a new alert (JSON)", type="json")

alert_data = None
if sample_alert:
    with open(f"data/alerts/{sample_alert}", "r") as f:
        alert_data = json.load(f)
elif uploaded_file:
    alert_data = json.load(uploaded_file)

if alert_data:
    st.subheader("🚨 Alert Details")
    st.json(alert_data)

    if st.button("🧠 Generate Response & Report"):
        alert_text = alert_data.get("description", "")
        
        # Step 1: RAG - Retrieve documents
        retriever = HybridRetriever()
        docs = retriever.get_relevant_documents(alert_text)
        st.markdown("### 📄 Retrieved Documents")
        for doc in docs:
            st.code(doc.page_content.strip()[:500])  # Preview first 500 characters

        # Step 2: Generate Summary
        summary = generate_summary(alert_text, docs)
        st.markdown("### 📋 AI-Generated Summary")
        st.success(summary)

        # Step 3: Escalation Level
        escalation = decide_escalation_level(alert_text, summary)
        st.markdown("### ⚠️ Escalation Level")
        st.info(escalation)

        # Step 4: Generate Report
        report_path = generate_playbook(Path("data/alerts") / sample_alert if sample_alert else uploaded_file.name)
        st.markdown("### 📁 Downloadable Report")
        st.download_button(
            label="📥 Download Report",
            data=open(report_path, "rb").read(),
            file_name=report_path.name,
            mime="application/pdf" if report_path.suffix == ".pdf" else "text/markdown"
        )
