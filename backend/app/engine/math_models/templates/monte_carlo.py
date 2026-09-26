"""Monte Carlo Wrapper model template."""
import numpy as np
from typing import Dict, Any

class MonteCarloWrapper:
    """Wraps any template with parameter uncertainty.
    Formula: E[f(X)], where X ~ N(μ, σ^2)
    """
    def __init__(self, template_class: Any, base_params: Dict[str, Any], param_std_devs: Dict[str, float], n_simulations: int = 1000):
        self.template_class = template_class
        self.base_params = base_params
        self.param_std_devs = param_std_devs
        self.n_simulations = n_simulations

    def compute(self, shock: Any) -> Dict[str, float]:
        """Runs simulations and returns summary statistics."""
        results = []
        for _ in range(self.n_simulations):
            params = {}
            for k, v in self.base_params.items():
                if k in self.param_std_devs:
                    params[k] = np.random.normal(v, self.param_std_devs[k])
                else:
                    params[k] = v
            instance = self.template_class(**params)
            # Handle list vs float shock returns generically (assuming float for basic stats)
            val = instance.compute(shock)
            if isinstance(val, (int, float)):
                results.append(val)
            elif isinstance(val, dict):
                # For dictionaries (like IO model), we might need dict mean, but keeping it simple for single metrics
                pass
            
        if not results:
            return {}
            
        arr = np.array(results)
        return {
            "mean": float(np.mean(arr)),
            "median": float(np.median(arr)),
            "p10": float(np.percentile(arr, 10)),
            "p90": float(np.percentile(arr, 90)),
            "std": float(np.std(arr))
        }

    @property
    def formula(self) -> str:
        """Mathematical formula for the model."""
        return "E[f(X)], where X ~ N(μ, σ^2)"
