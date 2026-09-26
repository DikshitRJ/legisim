"""LangGraph node for Model Architect."""
import os
from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from .validator import validate_model_spec

class ModelSpec(BaseModel):
    template: str = Field(description="Name of the mathematical template to use")
    source: str = Field(description="Citation or rationale source for this model")
    parameters: Dict[str, Any] = Field(description="Parameters for the template")
    shock_key: str = Field(description="Key in the shock_values dict to use as input")

class ArchitectOutput(BaseModel):
    specs: List[ModelSpec]

async def model_architect(state: Dict[str, Any]) -> Dict[str, Any]:
    """LangGraph node that selects and parameterizes math models."""
    llm = ChatOpenAI(
        model="glm-4",
        api_key=os.getenv("OPENAI_API_KEY", "dummy"),
        base_url=os.getenv("OPENAI_API_BASE", "https://api.z.ai/v1")
    )
    structured_llm = llm.with_structured_output(ArchitectOutput)
    
    prompt = (
        "You are the Model Architect for LegiSim.\n"
        "Based on the current state and policy, select and parameterize mathematical templates.\n"
        "Available templates: LinearPassThrough, Elasticity, MultiplePriceTransmission, InputOutputMultiplier, BudgetIdentity, DistributedLag, FeedbackLoop, MonteCarloWrapper.\n\n"
        f"State: {state}"
    )
    
    try:
        output = await structured_llm.ainvoke(prompt)
        
        validated_specs = []
        for spec_model in output.specs:
            spec_dict = spec_model.model_dump()
            is_valid, msg = validate_model_spec(spec_dict)
            if is_valid:
                validated_specs.append(spec_dict)
                
        return {"model_specs": validated_specs}
    except Exception as e:
        return {"model_specs": [], "error": str(e)}
