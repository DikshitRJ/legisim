"""Distributed Lag model template."""
import numpy as np
from typing import List

class DistributedLag:
    """Effects distributed over time periods.
    Formula: y_t = Σ w_i × x_{t-i}
    """
    def __init__(self, periods: int, lag_type: str = "geometric", decay_rate: float = 0.5):
        self.periods = periods
        self.lag_type = lag_type
        self.decay_rate = decay_rate
        self.weights = self._compute_weights()

    def _compute_weights(self) -> np.ndarray:
        if self.lag_type == "geometric":
            w = np.array([self.decay_rate ** i for i in range(self.periods)])
        elif self.lag_type == "uniform":
            w = np.ones(self.periods) / self.periods
        elif self.lag_type == "front_loaded":
            w = np.array([1.0 / (i + 1) for i in range(self.periods)])
        else:
            raise ValueError(f"Unknown lag type: {self.lag_type}")
        return w / np.sum(w)

    def compute(self, total_shock: float) -> List[float]:
        """Computes the distributed impact over periods."""
        return (self.weights * total_shock).tolist()

    @property
    def formula(self) -> str:
        """Mathematical formula for the model."""
        return "y_t = Σ w_i × x_{t-i}, where Σ w_i = 1"
