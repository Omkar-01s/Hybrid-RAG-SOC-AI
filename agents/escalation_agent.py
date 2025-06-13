# agents/

import os
from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain_community.llms import HuggingFaceHub
from langchain_core.prompts import PromptTemplate

# Load API key from .env
load_dotenv()
hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# Initialize LLaMA 3 via Hugging Face
llm = HuggingFaceHub(
    repo_id="meta-llama/Meta-Llama-3-8B-Instruct",
    huggingfacehub_api_token=hf_token,
    model_kwargs={
        "temperature": 0.2,
        "max_new_tokens": 300,
    }
)

# Prompt for escalation reasoning
escalation_prompt = PromptTemplate(
    input_variables=["alert", "summary"],
    template="""
You are a Security Operations Center (SOC) agent.

Given the following security alert and its generated response summary, assess the severity and suggest how to handle it.

Decide on one of these actions:
- Escalate: if threat is serious or affects multiple users/systems.
- Handle_Locally: if it's minor and remediated quickly.
- Log_Only: if no action is required, just audit trail.

🔔 ALERT:
{alert}

📋 SUMMARY:
{summary}

Your response should be a single keyword: Escalate, Handle_Locally, or Log_Only.
"""
)

# Decision agent logic
def decide_escalation_level(alert_text, summary_text):
    chain = LLMChain(llm=llm, prompt=escalation_prompt)
    result = chain.run(alert=alert_text, summary=summary_text)
    return result.strip()
