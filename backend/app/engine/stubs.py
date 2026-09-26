from __future__ import annotations


async def start_simulation(run_id: str) -> None:
    """Stub: Would trigger LangGraph pipeline. Currently no-op."""
    pass

async def resume_simulation(run_id: str, approved: bool, feedback: str | None) -> None:
    """Stub: Resume after human checkpoint."""
    pass

async def chat_with_run(run_id: str, message: str) -> str:
    """Stub: LLM Q&A grounded in run context. Returns mock reply."""
    return f"Based on the simulation results for run {run_id}, this policy shows mixed effects across demographics. [Mock response - LangGraph engine not yet connected]"
