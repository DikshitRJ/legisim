"""LangGraph setup for the Research Subgraph."""

from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph

from backend.app.engine.research.state import ResearchState
from backend.app.engine.research.nodes import (
    check_cache,
    plan_searches,
    execute_searches,
    fetch_pages,
    extract_facts,
    find_analogues,
    consolidate,
    build_targeting_profile
)


def route_cache(state: ResearchState) -> str:
    """Route based on the cache hit/miss status."""
    return state.get("cache_status", "miss")


def build_research_subgraph() -> CompiledStateGraph:
    """Build and compile the research LangGraph subgraph."""
    graph = StateGraph(ResearchState)
    
    # Add Nodes
    graph.add_node("check_cache", check_cache)
    graph.add_node("plan_searches", plan_searches)
    graph.add_node("execute_searches", execute_searches)
    graph.add_node("fetch_pages", fetch_pages)
    graph.add_node("extract_facts", extract_facts)
    graph.add_node("find_analogues", find_analogues)
    graph.add_node("consolidate", consolidate)
    graph.add_node("build_targeting_profile", build_targeting_profile)
    
    # Add Edges
    graph.add_edge(START, "check_cache")
    
    # Conditional edge from cache check
    graph.add_conditional_edges(
        "check_cache", 
        route_cache, 
        {"hit": END, "miss": "plan_searches"}
    )
    
    # Parallel paths
    graph.add_edge("plan_searches", "execute_searches")
    graph.add_edge("plan_searches", "find_analogues")
    
    # Search pipeline
    graph.add_edge("execute_searches", "fetch_pages")
    graph.add_edge("fetch_pages", "extract_facts")
    
    # Join paths
    graph.add_edge("extract_facts", "consolidate")
    graph.add_edge("find_analogues", "consolidate")
    
    # Final steps
    graph.add_edge("consolidate", "build_targeting_profile")
    graph.add_edge("build_targeting_profile", END)
    
    return graph.compile()
