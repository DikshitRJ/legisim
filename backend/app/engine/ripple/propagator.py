"""Ripple Effect Propagator using adjacency matrices."""
import numpy as np
from scipy.sparse import lil_matrix
from typing import Dict, List, Any
from collections import deque

class RipplePropagator:
    """Propagates shocks through the ripple network over time."""
    def __init__(self, nodes: Dict[str, Any], edges: List[Dict[str, Any]], total_steps: int = 36):
        self.nodes = {nid: dict(data) for nid, data in nodes.items()}
        self.edges = edges
        self.total_steps = total_steps
        
        self.node_ids = list(self.nodes.keys())
        self.n_nodes = len(self.node_ids)
        self.node_idx = {nid: i for i, nid in enumerate(self.node_ids)}
        
        self._compute_layers()
        
        self.adjacency = lil_matrix((self.n_nodes, self.n_nodes), dtype=np.float64)
        for edge in self.edges:
            if edge["source"] in self.node_idx and edge["target"] in self.node_idx:
                u = self.node_idx[edge["source"]]
                v = self.node_idx[edge["target"]]
                self.adjacency[u, v] = edge["strength"]
                
        self.history = np.zeros((self.total_steps + 1, self.n_nodes), dtype=np.float64)
        self.confidences = np.ones((self.total_steps + 1, self.n_nodes), dtype=np.float64)
        
    def _compute_layers(self) -> None:
        """Compute BFS layers from policy node(s)."""
        policy_nodes = [nid for nid, data in self.nodes.items() if data.get("kind") == "policy"]
        if not policy_nodes:
            in_degrees = {nid: 0 for nid in self.node_ids}
            for edge in self.edges:
                if edge["target"] in in_degrees:
                    in_degrees[edge["target"]] += 1
            policy_nodes = [nid for nid, deg in in_degrees.items() if deg == 0]
            
        for nid in self.node_ids:
            self.nodes[nid]["layer"] = -1
            
        queue = deque()
        for nid in policy_nodes:
            self.nodes[nid]["layer"] = 0
            queue.append(nid)
            
        adj = {nid: [] for nid in self.node_ids}
        for edge in self.edges:
            if edge["source"] in adj:
                adj[edge["source"]].append(edge["target"])
            
        while queue:
            curr = queue.popleft()
            curr_layer = self.nodes[curr]["layer"]
            for neighbor in adj.get(curr, []):
                if neighbor in self.nodes:
                    if self.nodes[neighbor]["layer"] == -1 or self.nodes[neighbor]["layer"] > curr_layer + 1:
                        self.nodes[neighbor]["layer"] = curr_layer + 1
                        queue.append(neighbor)
                        
        max_layer = max((self.nodes[nid]["layer"] for nid in self.node_ids if self.nodes[nid]["layer"] != -1), default=0)
        for nid in self.node_ids:
            if self.nodes[nid]["layer"] == -1:
                self.nodes[nid]["layer"] = max_layer + 1
                
    def _compute_layer(self, node_id: str) -> int:
        """Return the precomputed layer for a node."""
        return self.nodes.get(node_id, {}).get("layer", 0)

    def set_initial_shock(self, node_id: str, magnitude: float) -> None:
        """Set initial magnitude for a node at step 0."""
        if node_id in self.node_idx:
            idx = self.node_idx[node_id]
            self.history[0, idx] = magnitude

    def propagate(self) -> np.ndarray:
        """Run all time steps and return the history array."""
        adj_dense = self.adjacency.toarray()
        for t in range(self.total_steps):
            self.history[t+1] = self.history[t] @ adj_dense
            self.confidences[t+1] = self.confidences[t] * 0.95
        return self.history

    def get_node_timeline(self, node_id: str) -> List[float]:
        """Get the full time series for a single node."""
        if node_id not in self.node_idx:
            return [0.0] * (self.total_steps + 1)
        idx = self.node_idx[node_id]
        return self.history[:, idx].tolist()
        
    def get_snapshot(self, time_step: int) -> Dict[str, float]:
        """Get magnitudes of all nodes at a specific time step."""
        if time_step < 0 or time_step > self.total_steps:
            return {}
        return {nid: float(self.history[time_step, idx]) for nid, idx in self.node_idx.items()}

    def to_react_flow(self, time_step: int) -> Dict[str, Any]:
        """Convert network to React Flow format for a given time step."""
        from .exporter import export_to_react_flow
        return export_to_react_flow(self, {"nodes": self.nodes, "edges": self.edges}, time_step)
