"""
Module for aggregating cohort reactions and generating persona spotlights.
"""

import os
import json
from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from .prompts import PERSONA_SPOTLIGHT_PROMPT
from pydantic import BaseModel, Field

class PersonaSpotlight(BaseModel):
    story: str = Field(description="A short human story, max 500 characters", max_length=500)

def aggregate_reactions(reactions: List[Dict[str, Any]], cohorts: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Aggregate reactions by group and region, weighted by cohort weight."""
    cohort_map = {c["cohort_id"]: c for c in cohorts}
    
    total_weight = 0
    support_weight = 0
    oppose_weight = 0
    neutral_weight = 0
    
    behavior_frequencies = {}
    
    for r in reactions:
        cid = r["cohort_id"]
        cohort = cohort_map.get(cid, {})
        weight = cohort.get("weight", 1)
        
        total_weight += weight
        
        stance = r.get("reaction", {}).get("stance", "Neutral").lower()
        if stance == "support":
            support_weight += weight
        elif stance == "oppose":
            oppose_weight += weight
        else:
            neutral_weight += weight
            
        behavior = r.get("reaction", {}).get("behavior_change", "None")
        behavior_frequencies[behavior] = behavior_frequencies.get(behavior, 0) + weight

    oppose_ratio = oppose_weight / total_weight if total_weight > 0 else 0
    if oppose_ratio > 0.5:
        backlash_risk = "High"
    elif oppose_ratio > 0.2:
        backlash_risk = "Medium"
    else:
        backlash_risk = "Low"

    return {
        "weighted_stance": {
            "support": support_weight / total_weight if total_weight > 0 else 0,
            "neutral": neutral_weight / total_weight if total_weight > 0 else 0,
            "oppose": oppose_weight / total_weight if total_weight > 0 else 0
        },
        "behavior_change_frequencies": behavior_frequencies,
        "political_backlash_risk": backlash_risk
    }

async def generate_persona_spotlight(cohort: Dict[str, Any], reaction: Dict[str, Any]) -> Dict[str, Any]:
    """Use Strong LLM to write a short human story."""
    llm = ChatOpenAI(
        model="glm-4-plus",
        api_key=os.getenv("ZAI_API_KEY", "mock_key"),
        base_url=os.getenv("ZAI_BASE_URL", "https://api.z.ai/v1")
    )
    
    structured_llm = llm.with_structured_output(PersonaSpotlight)
    
    prompt = PERSONA_SPOTLIGHT_PROMPT.format(
        cohort_profile=json.dumps(cohort, indent=2),
        reaction_summary=json.dumps(reaction, indent=2)
    )
    
    if os.getenv("ZAI_API_KEY") in (None, "mock_key", ""):
        response = PersonaSpotlight(story=f"A member of {cohort.get('region', 'the')} community faces the new policy.")
    else:
        response = await structured_llm.ainvoke(prompt)
        
    return response.model_dump()
