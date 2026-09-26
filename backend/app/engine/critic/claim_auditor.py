"""
LLM-based claim verification for the Critic node.
"""
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
import json

from backend.app.engine.critic.prompts import CRITIC_AUDIT_PROMPT

class CriticFeedback(BaseModel):
    """Structured output for the claim auditor."""
    passed: bool = Field(description="True if all claims match the upstream data, False otherwise")
    revisions_required: list[str] = Field(description="List of specific revisions needed if the audit failed")

async def audit_claims(report_markdown: str, upstream_data: dict) -> CriticFeedback:
    """Use Strong LLM to verify every claim in the report matches upstream data."""
    llm = ChatOpenAI(model="glm-4", temperature=0)
    
    prompt = PromptTemplate(
        template=CRITIC_AUDIT_PROMPT,
        input_variables=["report_markdown", "upstream_data"]
    )
    
    chain = prompt | llm.with_structured_output(CriticFeedback)
    
    result = await chain.ainvoke({
        "report_markdown": report_markdown,
        "upstream_data": json.dumps(upstream_data, indent=2)
    })
    
    return result
