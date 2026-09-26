"""Input-Output Multiplier model template."""
import numpy as np
from typing import List, Dict

class InputOutputMultiplier:
    """Leontief input-output model.
    Formula: X = (I - A)^(-1) × Y
    """
    def __init__(self, io_matrix: List[List[float]], sector_names: List[str]):
        self.io_matrix = np.array(io_matrix)
        self.sector_names = sector_names
        n = len(sector_names)
        self.leontief_inverse = np.linalg.inv(np.eye(n) - self.io_matrix)

    def compute(self, direct_shocks: List[float]) -> Dict[str, float]:
        """Computes total direct and indirect impact per sector."""
        shocks = np.array(direct_shocks)
        total_impact = self.leontief_inverse.dot(shocks)
        return {name: float(impact) for name, impact in zip(self.sector_names, total_impact)}

    @property
    def formula(self) -> str:
        """Mathematical formula for the model."""
        return "X = (I - A)^(-1) × Y"
