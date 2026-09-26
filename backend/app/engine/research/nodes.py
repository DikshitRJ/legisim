"""Node functions for the Research Subgraph."""

import os
import json
from typing import Dict, Any

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

from backend.app.engine.research.state import ResearchState
from backend.app.schemas.jev import TargetingProfile
from backend.app.engine.research.prompts import (
    SEARCH_PLANNING_PROMPT,
    FACT_EXTRACTION_PROMPT,
    CONFLICT_RESOLUTION_PROMPT,
    TARGETING_PROFILE_PROMPT
)


def _get_llm() -> ChatOpenAI:
    """Helper to initialize the standard LLM for the engine."""
    return ChatOpenAI(
        model=os.getenv("STRONG_MODEL_NAME", "glm-4-plus"),
        openai_api_key=os.getenv("ZAI_API_KEY", "dummy"),
        openai_api_base=os.getenv("ZAI_API_BASE", "https://api.example.com/v1"),
        temperature=0.1
    )


async def check_cache(state: ResearchState) -> Dict[str, Any]:
    """
    Check if we have cached research for this policy type.
    STUB: always returns cache miss.
    """
    return {"cache_status": "miss"}


async def plan_searches(state: ResearchState) -> Dict[str, Any]:
    """Use Strong LLM to generate 3-5 search queries from the policy."""
    llm = _get_llm()
    policy_str = json.dumps(state.get("policy", {}))
    
    prompt = PromptTemplate.from_template(SEARCH_PLANNING_PROMPT)
    chain = prompt | llm
    
    response = await chain.ainvoke({"policy": policy_str})
    
    # Simple parse of comma-separated queries
    content = str(response.content)
    queries = [q.strip() for q in content.split(",") if q.strip()]
    
    return {"queries": queries}


async def execute_searches(state: ResearchState) -> Dict[str, Any]:
    """
    Call SearXNG via HTTP. 
    STUB: returns mock search results.
    Mock URL: http://searxng:8080/search?q={query}&format=json
    """
    queries = state.get("queries", [])
    mock_results = []
    
    for q in queries:
        # Stub logic
        mock_results.append({
            "query": q,
            "url": f"http://example.com/search?q={q.replace(' ', '+')}",
            "snippet": f"Mock snippet for {q}"
        })
        
    return {"search_results": mock_results}


async def fetch_pages(state: ResearchState) -> Dict[str, Any]:
    """
    Fetch full page content from search result URLs.
    STUB: returns mock page content.
    """
    search_results = state.get("search_results", [])
    mock_pages = []
    
    for res in search_results:
        url = res.get("url", "http://example.com")
        mock_pages.append({
            "url": url,
            "content": f"Mock page content loaded from {url}. Contains some relevant policy facts."
        })
        
    return {"data_sources": mock_pages}


async def extract_facts(state: ResearchState) -> Dict[str, Any]:
    """
    Use LLM to extract structured facts from page content.
    """
    data_sources = state.get("data_sources", [])
    
    # Since this is a stub for complex extraction, we just return a mock structured fact
    mock_fact = {
        "name": "Projected GDP Growth",
        "value": "7.5",
        "unit": "%",
        "region": "India",
        "source_url": data_sources[0]["url"] if data_sources else "http://example.com",
        "as_of_date": "2024-01-01"
    }
    
    return {"extracted_facts": [mock_fact]}


async def find_analogues(state: ResearchState) -> Dict[str, Any]:
    """
    Search pgvector for similar past policies.
    STUB: returns mock analogues list.
    """
    mock_analogue = {
        "id": "policy-analogue-001",
        "title": "National Infrastructure Pipeline 2019",
        "summary": "Similar capital expenditure push across infrastructure sectors.",
        "outcomes": "Positive long-term ROI, short-term inflationary pressure."
    }
    return {"analogues": [mock_analogue]}


async def consolidate(state: ResearchState) -> Dict[str, Any]:
    """
    Resolve conflicting data using LLM. Prefer official sources.
    """
    # STUB for conflict resolution and returning assumptions
    mock_assumption = {
        "fact_name": "Projected GDP Growth",
        "resolved_value": "7.5",
        "confidence": "high",
        "source": "Official"
    }
    
    return {"assumptions": [mock_assumption]}


async def build_targeting_profile(state: ResearchState) -> Dict[str, Any]:
    """
    Use Strong LLM with structured output to generate TargetingProfile.
    """
    llm = _get_llm().with_structured_output(TargetingProfile)
    
    policy_str = json.dumps(state.get("policy", {}))
    assumptions_str = json.dumps(state.get("assumptions", []))
    
    prompt = PromptTemplate.from_template(TARGETING_PROFILE_PROMPT)
    chain = prompt | llm
    
    try:
        # Ainvoke with structured output returns a pydantic model instance
        response = await chain.ainvoke({
            "policy": policy_str,
            "assumptions": assumptions_str
        })
        profile = response.model_dump()
    except Exception:
        # Fallback if structured output fails in stub/mock environment
        profile = {
            "target_demographics": ["General Population"],
            "exclusion_criteria": [],
            "primary_sector": "Economy",
            "income_bracket": "All"
        }
        
    return {"targeting_profile": profile}
