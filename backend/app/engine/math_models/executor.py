"""Executor for mathematical models."""
from typing import List, Dict, Any
from .registry import TEMPLATE_REGISTRY

def execute_model_specs(specs: List[Dict[str, Any]], shock_values: Dict[str, Any]) -> Dict[str, Any]:
    """Executes a list of validated model specs against shock values."""
    results = {}
    for i, spec in enumerate(specs):
        template_name = spec["template"]
        params = spec.get("parameters", {}).copy()
        template_cls = TEMPLATE_REGISTRY[template_name]
        
        try:
            if template_name == "MonteCarloWrapper":
                wrapped_name = params.get("template_class")
                if isinstance(wrapped_name, str) and wrapped_name in TEMPLATE_REGISTRY:
                    params["template_class"] = TEMPLATE_REGISTRY[wrapped_name]
                    
            instance = template_cls(**params)
            
            shock_key = spec.get("shock_key", "default")
            shock = shock_values.get(shock_key, 0.0)
            
            val = instance.compute(shock)
            
            results[f"model_{i}_{template_name}"] = {
                "value": val,
                "template": template_name,
                "source": spec.get("source", "Unknown"),
                "kind": "modelled"
            }
        except Exception as e:
            results[f"model_{i}_{template_name}"] = {
                "error": str(e),
                "kind": "error"
            }
    return results
