"""
LangGraph node for processing cohort reactions using LLMs.
"""

import os
from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

class ReactionOutput(BaseModel):
    stance: str = Field(description="Support, Neutral, or Oppose")
    intensity: float = Field(description="Intensity of the reaction, from 0.0 to 1.0")
    behavior_change: str = Field(description="Expected behavior change")
    reasoning: str = Field(description="Brief reasoning for the reaction")

async def react_single(prompt_data: Dict[str, Any], conditions: Dict[str, Any]) -> Dict[str, Any]:
    """Call LLM for a single cohort reaction with structured output."""
    llm = ChatOpenAI(
        model="glm-4-flash",
        api_key=os.getenv("ZAI_API_KEY", "mock_key"),
        base_url=os.getenv("ZAI_BASE_URL", "https://api.z.ai/v1")
    )
    
    structured_llm = llm.with_structured_output(ReactionOutput)
    
    # prompt_data is assumed to contain 'prompt' which is a list of tuples
    messages = prompt_data.get("prompt", [])
    
    # In production, we'd invoke the LLM. Here we stub it if key is mock
    if os.getenv("ZAI_API_KEY") in (None, "mock_key", ""):
        response = ReactionOutput(
            stance="Neutral",
            intensity=0.5,
            behavior_change="No significant change",
            reasoning="Mocked response due to missing API key."
        )
    else:
        response = await structured_llm.ainvoke(messages)
        
    result = {
        "cohort_id": prompt_data["cohort_id"],
        "reaction": response.model_dump(),
        "conditions_applied": conditions
    }
    return result

async def react_batch_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """LangGraph node called via Send(). Receives {prompt_data, conditions}."""
    reaction = await react_single(state["prompt_data"], state.get("conditions", {}))
    return {"reactions": [reaction]}
