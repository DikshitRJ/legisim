"""JEV filtering and prompt hydration nodes."""
from typing import Dict, Any
import httpx
import os
from langchain_core.runnables.config import RunnableConfig
from app.graph.state import SimState

async def jev_select(state: SimState, config: RunnableConfig = None) -> Dict[str, Any]:
    """JEV select node: Filters cohorts using TypeSafeAI's API."""
    cohorts = state.get("cohorts", [])
    policy = state.get("policy", {})
    targeting_profile = policy.get("target_group", "General Population")
    
    api_url = os.getenv("TYPESAFEAI_JEV_URL", "https://api.typesafeai.com/v1/jev")
    api_key = os.getenv("TYPESAFEAI_API_KEY", "")
    
    active_cohorts = []
    
    # We'll batch or sequentially evaluate cohorts against the target profile
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
            
            for cohort in cohorts:
                # TypeSafeAI JEV model just returns true or false for relevance
                payload = {
                    "profile": targeting_profile,
                    "persona": f"{cohort.get('region')} {cohort.get('occupation')}"
                }
                
                try:
                    response = await client.post(api_url, json=payload, headers=headers)
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
