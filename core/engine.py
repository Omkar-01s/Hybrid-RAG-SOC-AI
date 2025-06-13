import json
from rag.hybrid import HybridRetriever
from llm.response_engine import generate_summary
from agents.report_generator import generate_report

# 🔍 Load and parse alert JSON
def parse_alert_input(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)

# 📚 Retrieve relevant documents from hybrid retriever
def retrieve_docs(alert_text):
    retriever = HybridRetriever()
    return retriever.get_relevant_documents(alert_text)

# 🧠 Full playbook generation pipeline
def generate_playbook(alert_file):
    alert = parse_alert_input(alert_file)
    alert_text = alert.get("description", "")
    docs = retrieve_docs(alert_text)
    response = generate_summary(alert_text, docs)
    report_path = generate_report(alert, response)
    return report_path
