# 🛡️ Security Playbook Generator for SOC Teams  
> 🚨 Hybrid RAG + Agentic AI | Real-time Alert-to-Report System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-orange)](https://streamlit.io/)
[![Hugging Face](https://img.shields.io/badge/LLM-LLaMA3-green)](https://huggingface.co/meta-llama)
[![LangChain](https://img.shields.io/badge/LangChain-Enabled-purple)](https://www.langchain.com/)

---

## 📌 Overview

**Security Playbook Generator** is an intelligent SOC assistant that transforms alerts into detailed, actionable playbooks using Generative and Agentic AI. It enhances analyst efficiency and improves decision-making with:

- **Hybrid Retrieval:** Find related policies, incidents & playbooks via BM25 + Embeddings + LLM Re-ranking
- **LLM Playbook Generator:** Uses LLaMA 3 (via Hugging Face) to generate markdown playbooks
- **Agentic Escalation:** Determines if an alert should escalate or be handled locally
- **PDF Report Generation:** One-click downloadable reports
- 🎛**Modern Dashboard:** View, filter, and analyze reports in a production-ready Streamlit interface

---

## 🧠 Key Features

| Feature                      | Description |
|-----------------------------|-------------|
| 🔍 **Hybrid RAG**           | Combines BM25, Dense Embeddings, and LLM Re-ranking |
| 🤖 **Agent Decision Maker** | Determines escalation level (Escalate / Handle Locally / Log Only) |
| 📝 **LLM Markdown Playbooks** | Step-by-step mitigation plans using LLaMA 3 |
| 📄 **PDF + Markdown Reports** | Clean, consistent report output |
| 📊 **Interactive Dashboard** | KPI cards, preview, filtering, downloads |
| 🗂️ **Auto Report Indexing** | Auto-scans `output/generated_reports/` for updates |

---

## 🗂️ Project Structure

#### soc-playbook-generator/
#### ├── app/                               Streamlit UI & dashboards
#### ├── core/                              Main orchestrators
#### ├── data/                              Playbooks, policies, alerts, incident reports
#### ├── rag/                               Hybrid Retriever (BM25 + Embeddings + Reranker)
#### ├── agents/                            Escalation logic & report writer
#### ├── llm/                               LLM integration and prompt chains
#### ├── output/generated_reports/          Markdown / PDF reports
#### ├── logs/                              Alert logs, schema tracking
#### ├── main.py                            Main script to trigger chain end-to-end
#### ├── requirements.txt                   Python dependencies
#### ├── .env                               Hugging Face API token (example)
#### └── README.md

---

## Features

| Module | Capability |
|--------|------------|
| **Hybrid Retriever** | Combines BM25 + Dense Embeddings + LLM re-ranking |
| **LLM Chain**        | Uses LLaMA 3 (Hugging Face) for generating summaries |
| **Agentic Escalation** | Uses reasoning prompt to decide if alert should escalate |
| **PDF Report Generator** | Creates clean markdown + downloadable PDF |
| **Streamlit UI**     | Simple interactive UI to upload or view alerts |

---

## 🚀 How to Run

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Omkar-01s/Hybrid-RAG-SOC-AI.git
cd soc-playbook-generator

```

### 2️⃣ Setup Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3️⃣ Create .env file
```bash
HUGGINGFACEHUB_API_TOKEN=your_hugging_face_token
```
You can get your token from: https://huggingface.co/settings/tokens

4️⃣ Run with Streamlit
```bash
streamlit run app/dashboard.py
```

### 🎛️ SOC Dashboard Features
#### The Streamlit-based dashboard provides:

#### ✅ Real-time Filtering: by Alert Type, Escalation Level, and Date Range

#### ✅ KPI Cards: Total Reports, Unique Alerts, Last Report Timestamp

#### ✅ Previews & Full Content: Scroll through reports, toggle details

#### ✅ Download Button: PDF or Markdown versions

#### ✅ Expander UI: Neatly toggles full content without clutter

### 📈 Sample Workflow
#### 1.Drop an alert file in data/alerts/

#### 2.Run main.py to generate a report:
```bash
python main.py --alert data/alerts/suspicious_login.json
```
#### 3.Open Streamlit dashboard to:

- Filter alerts (by severity/type/date)

- Read preview or full report

- Download the final PDF

## 🧠 Sample Use Case
- Upload suspicious_login.json from data/alerts/

- System fetches past playbooks & policies using hybrid RAG

- LLM generates a Markdown playbook + escalation decision

- Generates downloadable PDF report inside /output/



## 👨‍🏫 Inspired by Industry Use-Cases
- This system mimics how real SOCs work with:

- Centralized threat intelligence

- Policy mapping to ISO/NIST

- Analyst-assisted auto-escalation

## 🧠 Future Enhancements
#### VectorDB backend for document retrieval (Qdrant/Weaviate)

#### Streaming LLM output (LangChain Agents + Callbacks)

#### Role-based access for security teams

## 📬 Connect With Me
#### Developer: Omkar Shetgaonkar
#### 📧 shetgaonkaromkar@gmail.com
#### 🔗 linkedin.com/in/omkar-shetgaonkar

