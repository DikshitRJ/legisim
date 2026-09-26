"""Initial intake and research nodes."""
from typing import Dict, Any
from langchain_core.runnables.config import RunnableConfig
from langgraph.types import interrupt, Command
from langgraph.config import get_stream_writer
from app.graph.state import SimState

from app.engine.cohort.population import build_population

async def intake(state: SimState, config: RunnableConfig = None) -> Dict[str, Any]:
    """Intake node."""
    writer = get_stream_writer()
    if writer:
        writer({"event": "node_started", "node": "intake"})
        
    policy_text = state.get("policy_text", "")
    
    # Load all personas from the /personas/ directory
    cohorts = build_population()
    
    return {
        "policy": {"text": policy_text, "summary": "Stub summary"},
        "cohorts": cohorts
    }

async def research(state: SimState, config: RunnableConfig = None) -> Dict[str, Any]:
    """Research node."""
    return {"research_data": {"facts": [], "past_policies": [], "assumptions": []}}

async def review(state: SimState, config: RunnableConfig = None) -> Command:
    """Review node with interrupt."""
    # Interrupt execution for manual review
    interrupt_value = interrupt({"action": "request_review", "message": "Please review the research data."})
    # When resumed, process the feedback
    return Command(
        update={"review_feedback": interrupt_value},
        goto="jev_select"
    )
