"""Reporting and visualization nodes."""
from typing import Dict, Any
from langchain_core.runnables.config import RunnableConfig
from app.graph.state import SimState

async def viz_planner(state: SimState, config: RunnableConfig = None) -> Dict[str, Any]:
    """Viz planner node."""
    return {"viz_specs": {"charts": []}}

async def write_report(state: SimState, config: RunnableConfig = None) -> Dict[str, Any]:
    """Write report node."""
    revisions = state.get("revisions", 0)
    return {"report": {"content": "Stub report", "is_valid": False}, "revisions": revisions + 1}

async def critic(state: SimState, config: RunnableConfig = None) -> Dict[str, Any]:
    """Critic node."""
    return {}
