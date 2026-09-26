"""Monte Carlo simulation for the Ripple Engine."""
import numpy as np
import copy
from typing import Dict, List, Any, Tuple
from .propagator import RipplePropagator

def run_monte_carlo(nodes: Dict[str, Any], edges: List[Dict[str, Any]], policy_shock: Dict[str, float], n_runs: int = 100, noise_std: float = 0.1) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Run Monte Carlo simulation with perturbed edge strengths.
    
    Args:
        nodes: Dictionary of node data.
        edges: List of edge dictionaries.
        policy_shock: Dictionary mapping node IDs to initial shock magnitudes.
        n_runs: Number of Monte Carlo iterations.
        noise_std: Standard deviation for Gaussian noise added to edge strengths.
        
    Returns:
        Tuple of (mean, p10, p90, std) arrays, each of shape (total_steps + 1, n_nodes).
    """
    total_steps = 36
    n_nodes = len(nodes)
    if n_nodes == 0:
        return np.zeros(0), np.zeros(0), np.zeros(0), np.zeros(0)
        
    results = np.zeros((n_runs, total_steps + 1, n_nodes))
    
    for i in range(n_runs):
        perturbed_edges = copy.deepcopy(edges)
        for edge in perturbed_edges:
            noise = np.random.normal(0, noise_std)
            edge["strength"] = np.clip(edge["strength"] + noise, -1.0, 1.0)
            
        prop = RipplePropagator(nodes, perturbed_edges, total_steps=total_steps)
        for nid, mag in policy_shock.items():
            prop.set_initial_shock(nid, mag)
            
        history = prop.propagate()
        results[i] = history
        
    mean = np.mean(results, axis=0)
    p10 = np.percentile(results, 10, axis=0)
    p90 = np.percentile(results, 90, axis=0)
    std = np.std(results, axis=0)
    
    return mean, p10, p90, std
