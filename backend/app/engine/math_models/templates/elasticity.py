"""Elasticity model template."""

class Elasticity:
    """Price elasticity of demand (log-log approximation).
    Formula: %ΔQ = ε × %ΔP
    """
    def __init__(self, elasticity_coefficient: float):
        self.elasticity_coefficient = elasticity_coefficient

    def compute(self, price_change_percent: float) -> float:
        """Computes the change in quantity based on price change."""
        return self.elasticity_coefficient * price_change_percent

    @property
    def formula(self) -> str:
        """Mathematical formula for the model."""
        return "%ΔQ = ε × %ΔP"
