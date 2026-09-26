"""
Context builder for the LegiSim Report Writer.
"""
import statistics
from typing import Any, Dict, List

def _prepare_policy(policy: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "title": policy.get("title", ""),
        "description": policy.get("description", ""),
        "type": policy.get("type", ""),
        "parameters": policy.get("parameters", {})
    }

def _prepare_metrics(metrics: Dict[str, Any]) -> Dict[str, Any]:
    prepared = {}
    for key, values in metrics.items():
        if not values or not isinstance(values, list):
            continue
        num_values = [v for v in values if isinstance(v, (int, float))]
        if not num_values:
            continue
        first = num_values[0]
        last = num_values[-1]
        prepared[key] = {
            "first_step": first,
            "last_step": last,
            "min": min(num_values),
            "max": max(num_values),
            "mean": statistics.mean(num_values),
            "trend": "up" if last > first else "down" if last < first else "flat"
        }
    return prepared

def _prepare_ripple(ripple: Dict[str, Any]) -> Dict[str, Any]:
    edges = ripple.get("edges", [])
    # Sort edges by strength
    sorted_edges = sorted(
        edges, 
        key=lambda e: abs(e.get("strength", 0.0)), 
        reverse=True
    )
    # Extract top chains (simplified, just top edges)
    top_chains = sorted_edges[:10]
    return {
        "top_edges": top_chains,
        "nodes": ripple.get("nodes", [])
    }

def _top_n_behaviors(behaviors: List[str], n: int) -> List[str]:
    counts = {}
    for b in behaviors:
        counts[b] = counts.get(b, 0) + 1
    sorted_behaviors = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    return [b[0] for b in sorted_behaviors[:n]]

def _prepare_reactions(reactions: List[Dict[str, Any]]) -> Dict[str, Any]:
    grouped = {}
    for r in reactions:
        demo = r.get("demographic", "General")
        if demo not in grouped:
            grouped[demo] = []
        grouped[demo].append(r)
    
    prepared = {}
    for demo, reacts in grouped.items():
        stances = [r.get("stance_score", 0.0) for r in reacts]
        weights = [r.get("weight", 1.0) for r in reacts]
        if sum(weights) > 0:
            weighted_avg = sum(s * w for s, w in zip(stances, weights)) / sum(weights)
        else:
            weighted_avg = 0.0
        
        behaviors = []
        for r in reacts:
            behaviors.extend(r.get("behaviors", []))
            
        prepared[demo] = {
            "weighted_stance": weighted_avg,
            "top_behaviors": _top_n_behaviors(behaviors, 3)
        }
    return prepared

def _prepare_research(research: Dict[str, Any]) -> Dict[str, Any]:
    analogues = research.get("analogues", [])
    facts = research.get("facts", [])
    
    return {
        "top_analogues": analogues[:3],
        "top_facts": facts[:10]
    }

def _prepare_regional(regional_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    ranked = sorted(
        regional_data,
        key=lambda r: abs(r.get("impact_score", 0.0)),
        reverse=True
    )
    return {
        "ranked_states": ranked
    }

def prepare_report_context(
    policy: Dict[str, Any],
    metrics: Dict[str, Any],
    ripple: Dict[str, Any],
    reactions: List[Dict[str, Any]],
    research: Dict[str, Any],
    regional_data: List[Dict[str, Any]],
    viz_specs: Dict[str, Any]
) -> Dict[str, Any]:
    """Prepare context for report generation."""
    return {
        "policy": _prepare_policy(policy) if policy else {},
        "metrics": _prepare_metrics(metrics) if metrics else {},
        "ripple": _prepare_ripple(ripple) if ripple else {},
        "reactions": _prepare_reactions(reactions) if reactions else {},
        "research": _prepare_research(research) if research else {},
        "regional": _prepare_regional(regional_data) if regional_data else {},
        "viz_specs": viz_specs or {}
    }
