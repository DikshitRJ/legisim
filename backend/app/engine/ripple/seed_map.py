"""Seed map loading and validation."""
import json
import os
from typing import Dict, Any, Set, Tuple
from .schemas import RippleNodeSchema, RippleEdgeSchema

DEFAULT_SEED_MAP_PATH = os.path.join(
    os.path.dirname(__file__), "data", "seed_map_v1.json"
)

def load_seed_map(path: str = None) -> Dict[str, Any]:
    """Load seed map from JSON file. Returns {nodes: dict, edges: list}."""
    path = path or DEFAULT_SEED_MAP_PATH
    if not os.path.exists(path):
        return {"nodes": {}, "edges": []}
        
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    nodes = {}
    for node_data in data.get("nodes", []):
        node = RippleNodeSchema(**node_data)
        nodes[node.id] = node.model_dump()
        
    edges = []
    for edge_data in data.get("edges", []):
        edge = RippleEdgeSchema(**edge_data)
        edges.append(edge.model_dump())
        
    return {"nodes": nodes, "edges": edges}

def get_node_ids(seed_map: Dict[str, Any]) -> Set[str]:
    """Get all node IDs from seed map."""
    return set(seed_map.get("nodes", {}).keys())

def get_existing_edges(seed_map: Dict[str, Any]) -> Set[Tuple[str, str]]:
    """Get all edge pairs (source, target) from seed map."""
    return {(edge["source"], edge["target"]) for edge in seed_map.get("edges", [])}
