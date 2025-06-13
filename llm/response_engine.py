# llm/response_engine.py

import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.llms import HuggingFaceHub

# Load API key from .env
load_dotenv()
hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# ✅ Define the Hugging Face LLM (LLaMA 3 8B Instruct)
llm = HuggingFaceHub(
    repo_id="meta-llama/Meta-Llama-3-8B-Instruct",
    huggingfacehub_api_token=hf_token,
    model_kwargs={
        "temperature": 0.3,
        "max_new_tokens": 800,
        "top_p": 0.95,
        "repetition_penalty": 1.2
    }
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
    chain = LLMChain(llm=llm, prompt=summary_prompt)
    result = chain.run(alert=alert_text, documents=doc_texts)
    return result

# ✅ Chain to reason through escalation
def reason_through_action(alert_text, summary_text):
    chain = LLMChain(llm=llm, prompt=reasoning_prompt)
    result = chain.run(alert=alert_text, summary=summary_text)
    return result.strip()
