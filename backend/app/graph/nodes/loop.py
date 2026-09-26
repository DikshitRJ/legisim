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

from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

class MetricOutput(BaseModel):
    household_income_change: float = Field(description="Percentage change in household income")
    cost_of_living_change: float = Field(description="Percentage change in cost of living")
    jobs_and_wages_impact: float = Field(description="Impact on jobs and wages, in percentage or absolute scaled number")
    business_impact: float = Field(description="Percentage impact on business revenue")
    govt_fiscal_effect: float = Field(description="Fiscal effect on government, in percentage or absolute scaled number")
    inequality_poverty: float = Field(description="Change in Gini or poverty index")
    regional_spread: Dict[str, float] = Field(description="Dictionary of state codes to impact scores")

async def economic_step(state: SimState, config: RunnableConfig = None) -> Dict[str, Any]:
    """Economic step node."""
    llm = ChatOpenAI(model="glm-4-flash", temperature=0.1)
    
    policy_text = state.get("policy_text", "No policy provided.")
    step = state.get("step", 1)
    
    # We use LLM to generate plausible economic metrics based on the policy
    prompt = f"Given the policy '{policy_text}', estimate the socio-economic impact metrics for step {step} of the simulation."
    
    try:
        structured_llm = llm.with_structured_output(MetricOutput)
        result = await structured_llm.ainvoke(prompt)
        metric_dict = result.model_dump()
        metric_dict["step"] = step
        metric_dict["source"] = "modelled"
        return {"metrics": [metric_dict]}
    except Exception:
        # Fallback if API fails
        fallback_metric = {
            "step": step,
            "household_income_change": -4.2,
            "cost_of_living_change": 6.3,
            "jobs_and_wages_impact": -2.1,
            "business_impact": -1.5,
            "govt_fiscal_effect": 1.3,
            "inequality_poverty": 0.012,
            "regional_spread": {"MH": -2.3, "GJ": -1.8, "UP": -3.5},
            "source": "fallback"
        }
        return {"metrics": [fallback_metric]}

class RippleNode(BaseModel):
    id: str
    label: str
    layer: int
    domain: str
    magnitude: str
    confidence: str
    kind: str

class RippleEdge(BaseModel):
    source: str
    target: str
    strength: float
    lagMonths: int
    mechanism: str

class RippleOutput(BaseModel):
    nodes: list[RippleNode]
    edges: list[RippleEdge]

async def ripple_expand(state: SimState, config: RunnableConfig = None) -> Dict[str, Any]:
    """Ripple expand node."""
    llm = ChatOpenAI(model="glm-4-flash", temperature=0.2)
    
    policy_text = state.get("policy_text", "")
    
    prompt = f"Map out the 1st and 2nd order ripple effects of this policy: '{policy_text}'. Generate 3-5 nodes and connect them with edges."
    
    try:
        structured_llm = llm.with_structured_output(RippleOutput)
        result = await structured_llm.ainvoke(prompt)
        return {"ripple": result.model_dump()}
    except Exception:
        return {"ripple": {
            "nodes": [
                {"id": "n1", "label": "Policy Enacted", "layer": 0, "domain": "policy", "magnitude": "High", "confidence": "High", "kind": "measured"},
                {"id": "n2", "label": "Cost Increase", "layer": 1, "domain": "economy", "magnitude": "Medium", "confidence": "High", "kind": "modelled"}
            ],
            "edges": [
                {"source": "n1", "target": "n2", "strength": 0.8, "lagMonths": 2, "mechanism": "Direct taxation"}
            ]
        }}
