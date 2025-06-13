import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEndpoint


# ✅ Load environment variables
load_dotenv()
hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# ✅ Setup Hugging Face LLM
llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.1", #can use other model
    task="text-generation",
    huggingfacehub_api_token=hf_token,
    temperature=0.3,
    max_new_tokens=512,
)

# ✅ Prompt Template for Playbook Generation
summary_prompt = PromptTemplate(
    input_variables=["alert", "documents"],
    template="""
You are a senior SOC analyst assistant.

Based on the following **security alert** and relevant supporting documents, generate a clear and actionable incident **response playbook**. Include:

1. Summary of the alert
2. Matching previous incident or policy reference
3. Step-by-step remediation actions
4. Compliance/standards info (if any)

🔔 ALERT:
{alert}

📚 DOCUMENTS:
{documents}

Write the response as **Markdown**.
"""
)

# ✅ Prompt Template for Reasoning / Escalation Decisions
reasoning_prompt = PromptTemplate(
    input_variables=["alert", "summary"],
    template="""
Given the following security alert and the response summary, decide on the **escalation level**:

- Escalate
- Handle_Locally
- Log_Only

Base your decision on the severity, type, and content in the summary.

🔔 ALERT:
{alert}

🧠 SUMMARY:
{summary}

Respond with only one of: Escalate, Handle_Locally, Log_Only.
"""
)

# ✅ Chain to generate LLM-based playbook
def generate_summary(alert_text, retrieved_docs):
    doc_texts = "\n".join([doc.page_content for doc in retrieved_docs])
    chain = summary_prompt | llm
    result = chain.invoke({"alert": alert_text, "documents": doc_texts})
    return result

# ✅ Chain to reason through escalation
def reason_through_action(alert_text, summary_text):
    chain = reasoning_prompt | llm
    result = chain.invoke({"alert": alert_text, "summary": summary_text})
    return result.strip()

# ✅ Dummy reranker (to be replaced later)
def rerank_documents(query, documents):
    # TODO: Replace with cross-encoder reranker later
    return documents
