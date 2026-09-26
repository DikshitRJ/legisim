"""Feedback Loop model template."""
from typing import Tuple, List

class FeedbackLoop:
    """Circular causation with convergence.
    Formula: Total = Initial / (1 - gain × (1 - damping))
    """
    def __init__(self, gain: float, damping: float):
        if not abs(gain * (1 - damping)) < 1.0:
            raise ValueError("Convergence check failed: abs(gain * (1 - damping)) must be < 1.0")
        self.gain = gain
        self.damping = damping

    def compute(self, initial_shock: float, max_iter: int = 100, tol: float = 1e-6) -> Tuple[float, List[float]]:
        """Computes the steady state and convergence trajectory."""
        trajectory = [initial_shock]
        current = initial_shock
        for _ in range(max_iter):
            step = current * self.gain * (1 - self.damping)
            if abs(step) < tol:
                break
            current = step
            trajectory.append(current)
            
        steady_state = initial_shock / (1 - self.gain * (1 - self.damping))
        return steady_state, trajectory

    @property
    def formula(self) -> str:
        """Mathematical formula for the model."""
        return "Total = Initial / (1 - gain × (1 - damping))"
