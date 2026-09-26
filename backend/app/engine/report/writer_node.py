"""
LangGraph node for writing the LegiSim report.
"""
import json
from typing import Any, Dict, List
from pydantic import BaseModel, Field

from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import SystemMessage, HumanMessage

from backend.app.engine.report.prompts import (
    REPORT_WRITER_SYSTEM_PROMPT,
    REPORT_WRITER_USER_PROMPT
)
from backend.app.engine.report.context_builder import prepare_report_context
from backend.app.engine.report.claim_processor import build_claim_registry
from backend.app.engine.report.translator import translate_report

class _ReportSectionOutput(BaseModel):
    id: str = Field(..., description="Section identifier (e.g., executive_summary)")
    title: str = Field(..., description="Section title")
    content_markdown: str = Field(..., description="Markdown content with [claim_XX] tags")

class _ReportSectionsOutput(BaseModel):
    sections: List[_ReportSectionOutput] = Field(..., description="List of report sections")

def _get_report_llm() -> ChatOpenAI:
    return ChatOpenAI(
        model="glm-4-plus",
        temperature=0.3,
        max_tokens=8192
    )

def _extract_regional_data(state: Dict[str, Any]) -> List[Dict[str, Any]]:
    return state.get("regional_data", [])

def _flatten_metrics(metrics: Dict[str, Any]) -> Dict[str, Any]:
    return metrics

async def write_report(state: Dict[str, Any], config: RunnableConfig) -> Dict[str, Any]:
    """
    Main LangGraph node to write the policy simulation report.
    """
    # 1. Prepare context
    policy = state.get("policy", {})
    metrics = _flatten_metrics(state.get("metrics", {}))
    ripple = state.get("ripple", {})
    reactions = state.get("reactions", [])
    research = state.get("research", {})
    regional_data = _extract_regional_data(state)
    viz_specs = state.get("viz_specs", {})
    
    context = prepare_report_context(
        policy, metrics, ripple, reactions, research, regional_data, viz_specs
    )
    
    # 2. Build prompt
    revisions = state.get("revisions", 0)
    revision_instructions = ""
    if revisions > 0:
        critic_feedback = state.get("critic_feedback", "")
        revision_instructions = f"\nREVISION FEEDBACK:\n{critic_feedback}\n"
        
    user_prompt = REPORT_WRITER_USER_PROMPT.format(
        policy_json=json.dumps(context["policy"], indent=2),
        metrics_json=json.dumps(context["metrics"], indent=2),
        ripple_json=json.dumps(context["ripple"], indent=2),
        reactions_json=json.dumps(context["reactions"], indent=2),
        research_json=json.dumps(context["research"], indent=2),
        regional_json=json.dumps(context["regional"], indent=2),
        viz_specs_json=json.dumps(context["viz_specs"], indent=2),
        revision_instructions=revision_instructions
    )
    
    # 3. Call LLM
    llm = _get_report_llm()
    structured_llm = llm.with_structured_output(_ReportSectionsOutput)
    
    messages = [
        SystemMessage(content=REPORT_WRITER_SYSTEM_PROMPT),
        HumanMessage(content=user_prompt)
    ]
    
    output = await structured_llm.ainvoke(messages, config=config)
    
    sections = []
    for s in output.sections:
        sections.append({
            "id": s.id,
            "title": s.title,
            "content": s.content_markdown,
            "content_markdown": s.content_markdown
        })
        
    # 4 & 5. Claims Processing
    claims = build_claim_registry(
        sections,
        context["metrics"],
        context["ripple"],
        context["reactions"],
        context["research"].get("top_analogues", [])
    )
    
    total_claims = len(claims)
    measured = sum(1 for c in claims if c["source_type"] == "measured")
    modelled = sum(1 for c in claims if c["source_type"] == "modelled")
    judged = sum(1 for c in claims if c["source_type"] == "judged")
    
    stats = {
        "total_claims": total_claims,
        "measured_pct": (measured / total_claims * 100) if total_claims else 0.0,
        "modelled_pct": (modelled / total_claims * 100) if total_claims else 0.0,
        "judged_pct": (judged / total_claims * 100) if total_claims else 0.0,
    }
    
    # 6. Assemble
    report = {
        "sections": sections,
        "claims": claims,
        "claim_stats": stats
    }
    
    # 7. Translate
    target_language = state.get("target_language", "en")
    if target_language != "en":
        report = await translate_report(report, target_language, llm)
        
    # 8. Return
    return {
        "report": report,
        "revisions": revisions + 1
    }
