"""
Viz Planner node for the LangGraph pipeline.
"""
from typing import Any, Dict
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableConfig
import json

from backend.app.engine.viz.schemas import VizPlannerOutput
from backend.app.engine.viz.prompts import VIZ_PLANNER_PROMPT

async def viz_planner(state: dict, config: RunnableConfig = None) -> dict:
    """Select optimal chart configurations based on simulation results."""
    # Use Strong LLM with structured output (VizPlannerOutput)
    llm = ChatOpenAI(model="glm-4", temperature=0) # Z.ai GLM endpoint
    
    prompt = PromptTemplate(
        template=VIZ_PLANNER_PROMPT,
        input_variables=["simulation_summaries", "key_impacts"]
    )
    
    chain = prompt | llm.with_structured_output(VizPlannerOutput)
    
    simulation_summaries = state.get("simulation_summaries", {})
    key_impacts = state.get("key_impacts", [])
    
    result = await chain.ainvoke({
        "simulation_summaries": json.dumps(simulation_summaries, indent=2),
        "key_impacts": json.dumps(key_impacts, indent=2)
    })
    
    return {"viz_specs": result.model_dump()}
