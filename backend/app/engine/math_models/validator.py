"""Validator for mathematical model specs."""
import inspect
from typing import Tuple, Dict, Any
from .registry import TEMPLATE_REGISTRY

def validate_model_spec(spec: Dict[str, Any]) -> Tuple[bool, str]:
    """Validates a math model specification dictionary."""
    template_name = spec.get("template")
    if not template_name or template_name not in TEMPLATE_REGISTRY:
        return False, f"Template '{template_name}' not found in registry."
    
    if "source" not in spec or not spec["source"]:
        return False, "Missing source citation."
        
    params = spec.get("parameters", {})
    template_cls = TEMPLATE_REGISTRY[template_name]
    sig = inspect.signature(template_cls.__init__)
    
    for name, param in sig.parameters.items():
        if name == "self":
            continue
        if param.default == inspect.Parameter.empty and name not in params:
            if template_name != "MonteCarloWrapper":
                return False, f"Missing required parameter '{name}' for '{template_name}'."
    
    if template_name == "LinearPassThrough":
        if not (0 <= params.get("share", 0) <= 1):
            return False, "Parameter 'share' must be between 0 and 1."
    elif template_name == "Elasticity":
        el = params.get("elasticity_coefficient", 0)
        if not (-5 <= el <= 5):
            return False, "Parameter 'elasticity_coefficient' must be between -5 and 5."
    elif template_name == "FeedbackLoop":
        gain = params.get("gain", 0)
        damping = params.get("damping", 0)
        if not abs(gain * (1 - damping)) < 1.0:
            return False, "Convergence check failed: abs(gain * (1 - damping)) must be < 1.0"
            
    return True, "Valid"
