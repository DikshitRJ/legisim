"""AI Proposer for new Ripple Edges."""
import json
import copy
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from .prompts import RIPPLE_PROPOSAL_PROMPT
from .seed_map import get_existing_edges
from .schemas import DomainEnum

class ProposedNode(BaseModel):
    id: str
    label: str
    domain: str
    kind: str = "effect"

class ProposedEdge(BaseModel):
    source: str
    target: str
    strength: float = Field(..., ge=-1.0, le=1.0)
    lagMonths: int = Field(default=0)
    mechanism: str
    target_node: Optional[ProposedNode] = None

class ProposalOutput(BaseModel):
    edges: list[ProposedEdge]

async def propose_edges(policy: str, seed_map: Dict[str, Any], research_facts: str, analogues: str) -> List[Dict[str, Any]]:
    """Calls Strong LLM with structured output to propose new edges."""
    # Note: As per instructions, all LLM calls use ChatOpenAI pointing to Z.ai GLM endpoint
    # The actual base_url and api_key would be picked up from environment variables in production
    llm = ChatOpenAI(model="glm-4-plus", temperature=0.2)
    llm_with_tools = llm.with_structured_output(ProposalOutput)
    
    prompt = PromptTemplate.from_template(RIPPLE_PROPOSAL_PROMPT)
    formatted = prompt.format(
        policy=policy,
        seed_map=json.dumps(seed_map, indent=2),
        research_facts=research_facts,
        analogues=analogues
    )
    
    result = await llm_with_tools.ainvoke(formatted)
    return [edge.model_dump() for edge in result.edges]
    
def validate_ai_proposal(proposal: Dict[str, Any], seed_map: Dict[str, Any]) -> bool:
    """Validate proposal against rules."""
    # 1. No duplicate edges
    existing = get_existing_edges(seed_map)
    source = proposal.get("source")
    target = proposal.get("target")
    if not source or not target:
        return False
    if (source, target) in existing:
        return False
        
    # 2. No self-loops
    if source == target:
        return False
        
    # 3. Strength in [-1, 1]
    strength = proposal.get("strength", 0)
    if not (-1.0 <= strength <= 1.0):
        return False
        
    # 4. Mechanism present
    if not proposal.get("mechanism"):
        return False
        
    # 5. Domain valid if new node
    target_node = proposal.get("target_node")
    if target_node:
        try:
            DomainEnum(target_node.get("domain"))
        except ValueError:
            return False
            
    return True

def merge_proposals(seed_graph: Dict[str, Any], proposals: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Deep copy + validated merge of proposals into seed graph."""
    merged = copy.deepcopy(seed_graph)
    if "nodes" not in merged:
        merged["nodes"] = {}
    if "edges" not in merged:
        merged["edges"] = []
        
    for prop in proposals:
        if validate_ai_proposal(prop, merged):
            if prop.get("target_node"):
                tn = prop["target_node"]
                if tn["id"] not in merged["nodes"]:
                    merged["nodes"][tn["id"]] = tn
            
            new_edge = {
                "id": f"{prop['source']}-{prop['target']}",
                "source": prop["source"],
                "target": prop["target"],
                "strength": prop["strength"],
                "lagMonths": prop.get("lagMonths", 0),
                "mechanism": prop["mechanism"]
            }
            merged["edges"].append(new_edge)
            
    return merged
