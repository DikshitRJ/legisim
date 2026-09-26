"""Conditional routing logic for the LegiSim LangGraph engine."""
from typing import Literal
from langgraph.types import Send
from app.graph.state import SimState

def continue_to_react(state: SimState) -> list:
    """Fan-out: map hydrated prompts to Send() objects for react_batch."""
    sends = []
    for prompt_data in state.get("hydrated_prompts", []):
        sends.append(Send("react_batch", {"prompt_data": prompt_data, "conditions": state.get("conditions", {})}))
    return sends

def check_loop(state: SimState) -> Literal["start_step", "viz_planner"]:
    """Route: continue time loop or proceed to visualization."""
    if state.get("step", 0) < state.get("horizon", 12):
        return "start_step"
    return "viz_planner"

def route_critic(state: SimState) -> Literal["write_report", "__end__"]:
    """Route: loop back for revision or finish."""
    report = state.get("report", {})
    revisions = state.get("revisions", 0)
    if revisions < 2 and not report.get("is_valid", False):
        return "write_report"
    return "__end__"
