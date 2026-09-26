"""Budget Identity model template."""
from typing import Dict, List

class BudgetIdentity:
    """Income = Spending + Savings accounting identity.
    Formula: Income = Σ (P_i × Q_i) + Savings
    """
    def __init__(self, categories: List[str], baseline_shares: List[float]):
        if not abs(sum(baseline_shares) - 1.0) < 1e-5:
            raise ValueError("baseline_shares must sum to 1.0")
        self.categories = categories
        self.baseline_shares = baseline_shares

    def compute(self, price_changes: Dict[str, float], income_change: float = 0.0) -> Dict[str, float]:
        """Applies price_changes, squeezes shares if total_cost > income."""
        total_new_cost = 0.0
        new_shares = {}
        for cat, share in zip(self.categories, self.baseline_shares):
            pc = price_changes.get(cat, 0.0)
            new_shares[cat] = share * (1 + pc)
            total_new_cost += new_shares[cat]
            
        income = 1.0 + income_change
        if total_new_cost > income:
            squeeze_factor = income / total_new_cost
            return {cat: val * squeeze_factor for cat, val in new_shares.items()}
        return new_shares

    @property
    def formula(self) -> str:
        """Mathematical formula for the model."""
        return "Income = Σ (P_i × Q_i) + Savings"
