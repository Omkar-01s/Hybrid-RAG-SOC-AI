# 🛡️ Security Playbook Generator for SOC Teams  
> 🚨 Hybrid RAG + Agentic AI | Real-time Playbook Generation

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-orange)](https://streamlit.io/)
[![Hugging Face](https://img.shields.io/badge/LLM-LLaMA3-green)](https://huggingface.co/meta-llama)
[![LangChain](https://img.shields.io/badge/LangChain-Enabled-purple)](https://www.langchain.com/)

---

## 📌 Overview

**Security Playbook Generator** is an AI-powered assistant for Security Operations Center (SOC) teams. It processes alert data, retrieves relevant documentation using **Hybrid RAG**, and generates detailed incident playbooks using **LLaMA 3 via Hugging Face**.

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
├── app/ # Streamlit UI
├── data/ # Playbooks, policies, alerts, reports
├── logs/ # Alert logs & schema
├── rag/ # Sparse, dense, hybrid retrievers
├── agents/ # Escalation agent & report writer
├── llm/ # Prompt templates & LLM logic
├── output/ # Generated reports
├── main.py # Core orchestrator
├── requirements.txt # Dependencies
├── Dockerfile # Optional Docker setup
└── .env # Hugging Face token
