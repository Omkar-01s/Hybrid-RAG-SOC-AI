import json
from rag.hybrid import HybridRetriever
from llm.response_engine import generate_summary
from agents.report_generator import generate_report


# 1️⃣ Parse alert JSON from file
def parse_alert_input(filepath):
    with open(filepath, 'r') as file:
        alert_data = json.load(file)
    return alert_data


# 2️⃣ Run Hybrid Retriever on alert description
def retrieve_docs(alert_text):
    retriever = HybridRetriever()
    docs = retriever.get_relevant_documents(alert_text)
    return docs


# 3️⃣ Full playbook generation pipeline
def generate_playbook(alert_file):
    alert = parse_alert_input(alert_file)
    alert_text = alert.get("description", "")
    
    docs = retrieve_docs(alert_text)
    
    response = generate_summary(alert_text, docs)
    
    report_path = generate_report(alert, response)
    
    return report_path


# 4️⃣ CLI Execution Entry Point
if __name__ == '__main__':
    import sys
    alert_file_path = sys.argv[1] if len(sys.argv) > 1 else "data/alerts/suspicious_login.json"
    report = generate_playbook(alert_file_path)
    print(f"✅ Playbook report generated: {report}")
