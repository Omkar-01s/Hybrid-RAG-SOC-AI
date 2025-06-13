import sys
from pathlib import Path

# Add root dir to path
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

import streamlit as st
import json
import os
from pathlib import Path

from core.engine import generate_playbook
from agents.escalation_agent import decide_escalation_level
from llm.response_engine import generate_summary
from rag.hybrid import HybridRetriever

st.set_page_config(page_title="SOC Playbook Generator", layout="wide")
st.title("🛡️ Security Playbook Generator for SOC Teams")

st.sidebar.header("🔍 Load Alert")

# 📁 Option to select a sample alert
alert_files = list(Path("data/alerts").glob("*.json"))
sample_alert = st.sidebar.selectbox(
    "Choose a sample alert file",
    options=[""] + [f.name for f in alert_files]
)

# 📤 Option to upload a new alert JSON file
uploaded_file = st.sidebar.file_uploader("Or upload a new alert (JSON)", type="json")

alert_data = None
alert_file_path = None

# ✅ Load sample or uploaded alert data
if sample_alert:
    alert_file_path = Path("data/alerts") / sample_alert
    with open(alert_file_path, "r") as f:
        alert_data = json.load(f)
elif uploaded_file:
    # Save to temp dir
    os.makedirs("temp", exist_ok=True)
    alert_file_path = Path("temp") / uploaded_file.name
    with open(alert_file_path, "wb") as f:
        f.write(uploaded_file.read())
    with open(alert_file_path, "r") as f:
        alert_data = json.load(f)

# 🚨 Display Alert
if alert_data:
    st.subheader("🚨 Alert Details")
    st.json(alert_data)

    if st.button("🧠 Generate Response & Report"):
        alert_text = alert_data.get("description", "")

        # Step 1️⃣: Retrieve documents using RAG
        retriever = HybridRetriever()
        docs = retriever.get_relevant_documents(alert_text)
        st.markdown("### 📄 Retrieved Documents")
        for doc in docs:
            st.code(doc.page_content.strip()[:500])  # Preview first 500 characters

        # Step 2️⃣: Generate summary using LLM
        summary = generate_summary(alert_text, docs)
        st.markdown("### 📋 AI-Generated Summary")
        st.success(summary)

        # Step 3️⃣: Decide escalation level
        escalation = decide_escalation_level(alert_text, summary)
        st.markdown("### ⚠️ Escalation Level")
        st.info(escalation)

        # Step 4️⃣: Generate report
        report_path = generate_playbook(alert_file_path)
        st.markdown("### 📁 Downloadable Report")

        with open(report_path, "rb") as f:
            st.download_button(
                label="📥 Download Report",
                data=f.read(),
                file_name=report_path.name,
                mime="application/pdf" if report_path.suffix == ".pdf" else "text/markdown"
            )
