# 🛡️ Security Playbook Generator for SOC Teams  
> 🚨 Hybrid RAG + Agentic AI | Real-time Playbook Generation

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-orange)](https://streamlit.io/)
[![Hugging Face](https://img.shields.io/badge/LLM-LLaMA3-green)](https://huggingface.co/meta-llama)
[![LangChain](https://img.shields.io/badge/LangChain-Enabled-purple)](https://www.langchain.com/)

---

## 📌 Overview

**Modern SOC (Security Operations Center) teams face a growing number of alerts, fragmented documentation, and pressure to respond quickly and accurately. This project is a Generative + Agentic AI solution that:**

- 🔹 **Reads a security alert**
- 🔹 **Retrieves related policies, playbooks, and past incidents using Hybrid RAG (BM25 + Embeddings + LLM reranking)**
- 🔹 **Generates a step-by-step Markdown playbook**
- 🔹 **Decides escalation level (Escalate / Handle Locally / Log Only)**
- 🔹 **Produces downloadable PDF reports using Streamlit interface.**

---

## 🧠 Key Features

- 🔍 **Hybrid Retrieval:** Combines BM25 + Dense Embeddings + LLM re-ranking
- 🦙 **LLM-Powered Playbooks:** Uses LLaMA 3 (Hugging Face API) to generate response plans
- 🧠 **Agentic Reasoning:** Decides whether to escalate or log locally
- 📝 **Report Generation:** Generates Markdown and PDF reports
- 🎛️ **Streamlit UI:** Intuitive frontend for uploading and managing alerts

---

## 📂 Project Structure

soc-playbook-generator/
- ├── app/ # Streamlit UI
- ├── data/ # Playbooks, policies, alerts, reports
- ├── logs/ # Alert logs & schema
- ├── rag/ # hybrid retrievers
- ├── agents/ # Escalation agent & report writer
- ├── llm/ # Prompt templates & LLM logic
- ├── output/ # Generated reports
- ├── main.py # Core orchestrator
- ├── requirements.txt # Dependencies
- ├── Dockerfile # Optional Docker setup
- └── .env # Hugging Face token



---

## ⚙️ Features

| Module | Capability |
|--------|------------|
| **Hybrid Retriever** | Combines BM25 + Dense Embeddings + LLM re-ranking |
| **LLM Chain**        | Uses LLaMA 3 (Hugging Face) for generating summaries |
| **Agentic Escalation** | Uses reasoning prompt to decide if alert should escalate |
| **PDF Report Generator** | Creates clean markdown + downloadable PDF |
| **Streamlit UI**     | Simple interactive UI to upload or view alerts |

---

## 🚀 How to Run

### 1️⃣ Clone the Repo
```bash
git clone https://github.com/your-username/soc-playbook-generator.git
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
streamlit run app/ui.py
```
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
- VectorDB backend for document retrieval (Qdrant/Weaviate)

- Streaming LLM output (LangChain Agents + Callbacks)

- Role-based access for security teams

## 📬 Connect With Me
- Developer: Omkar Shetgaonkar
- 📧 shetgaonkaromkar@gmail.com
- 🔗 linkedin.com/in/omkar-shetgaonkar

