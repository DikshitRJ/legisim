"""Linear Pass-Through model template."""

class LinearPassThrough:
    """Direct proportional transmission of a shock.
    Formula: Δtarget = Δsource × share × pass_through_rate
    """
    def __init__(self, share: float, pass_through_rate: float = 1.0):
        self.share = share
        self.pass_through_rate = pass_through_rate

    def compute(self, shock_percent: float) -> float:
        """Computes the direct proportional transmission."""
        return shock_percent * self.share * self.pass_through_rate

    @property
    def formula(self) -> str:
        """Mathematical formula for the model."""
        return "Δtarget = Δsource × share × pass_through_rate"
