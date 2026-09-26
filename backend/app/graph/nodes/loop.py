"""Simulation loop nodes."""
from typing import Dict, Any
from langchain_core.runnables.config import RunnableConfig
from app.graph.state import SimState

async def start_step(state: SimState, config: RunnableConfig = None) -> Dict[str, Any]:
    """Start step node."""
    current_step = state.get("step", 0)
    return {"step": current_step + 1}

async def react_batch(state: Dict[str, Any], config: RunnableConfig = None) -> Dict[str, Any]:
    """React batch node."""
    # state is prompt_data from Send()
    prompt_data = state.get("prompt_data", {})
    return {"reactions": [{"cohort": prompt_data.get("cohort"), "reaction": "Stub reaction"}]}

async def aggregate(state: SimState, config: RunnableConfig = None) -> Dict[str, Any]:
    """Aggregate node."""
    reactions = state.get("reactions", [])
    return {"aggregates": {"total_reactions": len(reactions)}}

async def economic_step(state: SimState, config: RunnableConfig = None) -> Dict[str, Any]:
    """Economic step node."""
    return {"metrics": {"gdp": 1000, "unemployment": 5.0}}

async def ripple_expand(state: SimState, config: RunnableConfig = None) -> Dict[str, Any]:
    """Ripple expand node."""
    return {"ripple_effects": []}
