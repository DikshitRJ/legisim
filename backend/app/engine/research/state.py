"""
Research subgraph state definition.
"""

from typing import TypedDict, Annotated, List, Dict
import operator

class ResearchState(TypedDict, total=False):
    policy_text: str
    queries: List[str]
    raw_findings: Annotated[List[str], operator.add]
    summarized_insights: Dict[str, str]

__all__ = ["ResearchState"]
