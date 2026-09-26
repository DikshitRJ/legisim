"""
Module for hydrating prompts with cohort and policy data, applying guardrails.
"""

import json
from typing import List, Dict, Any, Tuple, Optional
from .prompts import COHORT_REACTION_SYSTEM_PROMPT, COHORT_REACTION_USER_TEMPLATE

def hydrate_prompt(
    cohort: Dict[str, Any], 
    policy_details: Dict[str, Any], 
    memory: Optional[List[Dict[str, Any]]] = None, 
    analogues: Optional[List[Dict[str, Any]]] = None
) -> List[Tuple[str, str]]:
    """Build the (system, user) message pair for a cohort."""
    memory_str = json.dumps(memory) if memory else "None"
    analogues_str = json.dumps(analogues) if analogues else "None"
    
    user_msg = COHORT_REACTION_USER_TEMPLATE.format(
        cohort_profile=json.dumps(cohort, indent=2),
        policy_context=json.dumps(policy_details, indent=2),
        memory=memory_str,
        analogues=analogues_str
    )
    
    return [
        ("system", COHORT_REACTION_SYSTEM_PROMPT),
        ("user", user_msg)
    ]

def hydrate_all_prompts(
    active_cohorts: List[Dict[str, Any]], 
    policy_details: Dict[str, Any], 
    memory: Optional[Dict[str, Any]] = None
) -> List[Dict[str, Any]]:
    """Hydrate prompts for all active cohorts. Returns list of {cohort_id, cohort, prompt}."""
    hydrated = []
    for cohort in active_cohorts:
        cohort_mem = memory.get(cohort["cohort_id"], []) if memory else None
        prompt_msgs = hydrate_prompt(cohort, policy_details, memory=cohort_mem)
        
        hydrated.append({
            "cohort_id": cohort["cohort_id"],
            "cohort": cohort,
            "prompt": prompt_msgs
        })
    return hydrated
