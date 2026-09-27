"""LAYA filtering and prompt hydration nodes."""
from typing import Dict, Any
import httpx
import os
from langchain_core.runnables.config import RunnableConfig
from app.graph.state import SimState

async def laya_select(state: SimState, config: RunnableConfig = None) -> Dict[str, Any]:
    """LAYA select node: Filters cohorts using local Laya server."""
    cohorts = state.get("cohorts", [])
    policy = state.get("policy", {})
    targeting_profile = policy.get("target_group", "General Population")
    
    from app.config import settings
    api_url = settings.LAYA_SERVICE_URL
    
    active_cohorts = []
    
    # We'll batch or sequentially evaluate cohorts against the target profile
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            
            for cohort in cohorts:
                # LAYA model evaluates text/JSON for cohort targeting relevance
                payload = {
                    "question": targeting_profile,
                    "text": f"{cohort.get('region')} {cohort.get('occupation')} {cohort.get('income_bracket')}"
                }
                
                try:
                    response = await client.post(api_url, json=payload)
                    if response.status_code == 200:
                        data = response.json()
                        # Assuming the API returns {"relevant": true/false}
                        is_relevant = data.get("relevant", True)
                    else:
                        # Fallback to true if API fails
                        is_relevant = True
                except Exception:
                    # Fallback to true if request fails
                    is_relevant = True
                    
                if is_relevant:
                    active_cohorts.append(cohort)
    except Exception as e:
        # Global fallback if httpx client fails
        active_cohorts = cohorts
        
    return {"active_cohorts": active_cohorts}

async def prompt_hydrate(state: SimState, config: RunnableConfig = None) -> Dict[str, Any]:
    """Prompt hydrate node."""
    active_cohorts = state.get("active_cohorts", [])
    prompts = [{"cohort": c, "prompt_text": f"Stub prompt for {c}"} for c in active_cohorts]
    return {"hydrated_prompts": prompts}
