"""Master Graph Definition for LegiSim."""
from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt, Command, Send
from langchain_core.runnables.config import RunnableConfig

from app.graph.state import SimState
from app.graph.edges import continue_to_react, check_loop, route_critic
from app.graph.nodes.initial import intake, review
from app.graph.nodes.jev_filter import jev_select, prompt_hydrate
from app.graph.nodes.loop import start_step, aggregate, economic_step, ripple_expand
from app.engine.research.subgraph import build_research_subgraph
from app.engine.cohort.react_node import react_batch_node as react_batch
from app.engine.viz.viz_node import viz_planner
from app.engine.report.writer_node import write_report
from app.engine.critic.critic_node import critic

def build_simulation_graph():
    """Builds and returns the master simulation StateGraph orchestrator."""
    builder = StateGraph(SimState)
    
    # Add nodes
    builder.add_node("intake", intake)
    builder.add_node("research", build_research_subgraph())
    builder.add_node("review", review)
    builder.add_node("jev_select", jev_select)
    builder.add_node("prompt_hydrate", prompt_hydrate)
    builder.add_node("start_step", start_step)
    builder.add_node("react_batch", react_batch)
    builder.add_node("aggregate", aggregate)
    builder.add_node("economic_step", economic_step)
    builder.add_node("ripple_expand", ripple_expand)
    builder.add_node("viz_planner", viz_planner)
    builder.add_node("write_report", write_report)
    builder.add_node("critic", critic)
    
    # Wire edges
    builder.add_edge(START, "intake")
    builder.add_edge("intake", "research")
    builder.add_edge("research", "review")
    
    # review is connected via Command(goto="jev_select")
    
    builder.add_edge("jev_select", "prompt_hydrate")
    builder.add_edge("prompt_hydrate", "start_step")
    
    builder.add_conditional_edges("start_step", continue_to_react, ["react_batch"])
    builder.add_edge("react_batch", "aggregate")
    builder.add_edge("aggregate", "economic_step")
    builder.add_edge("economic_step", "ripple_expand")
    
    builder.add_conditional_edges("ripple_expand", check_loop, ["start_step", "viz_planner"])
    
    builder.add_edge("viz_planner", "write_report")
    builder.add_edge("write_report", "critic")
    
    builder.add_conditional_edges("critic", route_critic, {"write_report": "write_report", "__end__": END})
    
    return builder.compile()
