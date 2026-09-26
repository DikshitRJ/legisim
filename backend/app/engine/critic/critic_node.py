"""
Critic node for the LangGraph pipeline.
"""
from typing import Any, Dict
from langchain_core.runnables import RunnableConfig

from backend.app.engine.critic.hard_limits import check_hard_limits
from backend.app.engine.critic.claim_auditor import audit_claims

async def critic(state: dict, config: RunnableConfig = None) -> dict:
    """Critic node: validates report, routes to revision or end."""
    metrics = state.get("metrics", [])
    report_dict = state.get("report", {})
    # Assuming report has 'content' or 'sections' that can be stringified
    report_markdown = str(report_dict)
    upstream_data = state
    revisions_count = state.get("revisions", 0)
    
    # 1. Check hard limits (programmatic)
    passed, violations = check_hard_limits(metrics)
    
    # 2. If hard limits fail, raise ValueError
    if not passed:
        raise ValueError(f"Hard limits violated in simulation metrics: {violations}")
        
    # 3. LLM audit of claims
    feedback = await audit_claims(report_markdown, upstream_data)
    
    # 4. If not passed and revisions < 2: return report with critic_feedback
    if not feedback.passed and revisions_count < 2:
        return {
            "warnings": [f"Critic: {req}" for req in feedback.revisions_required],
            "revisions": revisions_count + 1,
            "report": {**report_dict, "is_valid": False}
        }
        
    # 5. If not passed and revisions >= 2: inject uncertainty warnings
    if not feedback.passed and revisions_count >= 2:
        warnings_text = "\\n\\n**Data Uncertainty Warning:**\\n" + "\\n".join([f"- {req}" for req in feedback.revisions_required])
        return {
            "warnings": [warnings_text],
            "report": {**report_dict, "is_valid": True}
        }
        
    # 6. If passed: return report with is_valid=True
    return {
        "report": {**report_dict, "is_valid": True}
    }
