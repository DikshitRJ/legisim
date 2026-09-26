"""Exporter for React Flow visualization."""
from typing import Dict, Any, List

def export_to_react_flow(propagator: Any, seed_map: Dict[str, Any], time_step: int) -> Dict[str, Any]:
    """Export network state to React Flow format."""
    nodes = []
    snapshot = propagator.get_snapshot(time_step)
    
    for nid, node_data in seed_map.get("nodes", {}).items():
        # Incorporate computed layers
        layer = propagator._compute_layer(nid)
        idx = propagator.node_idx.get(nid, 0)
        confidence = float(propagator.confidences[time_step, idx]) if hasattr(propagator, 'confidences') else 1.0
        
        nodes.append({
            "id": nid,
            "label": node_data.get("label", nid),
            "layer": layer,
            "domain": node_data.get("domain", "ECONOMIC"),
            "magnitude": snapshot.get(nid, 0.0),
            "confidence": confidence,
            "kind": node_data.get("kind", "effect")
        })
        
    edges = []
    for edge in seed_map.get("edges", []):
        edges.append({
            "id": edge.get("id", f"{edge['source']}-{edge['target']}"),
            "source": edge["source"],
            "target": edge["target"],
            "strength": edge.get("strength", 0.0),
            "lagMonths": edge.get("lagMonths", 0),
            "mechanism": edge.get("mechanism", "")
        })
        
    return {"nodes": nodes, "edges": edges}

def export_time_series(propagator: Any) -> List[Dict[str, Any]]:
    """Export all snapshots as a time series."""
    series = []
    for t in range(propagator.total_steps + 1):
        series.append(propagator.get_snapshot(t))
    return series
