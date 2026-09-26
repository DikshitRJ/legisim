"""Multiple Price Transmission model template."""
from typing import List

class MultiplePriceTransmission:
    """Multi-hop supply chain transmission through stages with markup and pass_through rates.
    Formula: ΔP_final = ΔP_initial × Π [ (1 + markup_i) × pass_through_i ]
    """
    def __init__(self, markups: List[float], pass_through_rates: List[float]):
        if len(markups) != len(pass_through_rates):
            raise ValueError("markups and pass_through_rates must be of the same length")
        self.markups = markups
        self.pass_through_rates = pass_through_rates

    def compute(self, initial_shock: float) -> float:
        """Computes the final price change across the supply chain."""
        current = initial_shock
        for m, pt in zip(self.markups, self.pass_through_rates):
            current = current * (1 + m) * pt
        return current

    @property
    def formula(self) -> str:
        """Mathematical formula for the model."""
        return "ΔP_final = ΔP_initial × Π [ (1 + markup_i) × pass_through_i ]"
