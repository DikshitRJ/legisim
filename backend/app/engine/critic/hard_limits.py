"""
Programmatic hard limit checks for simulation metrics.
"""

def check_hard_limits(metrics: list[dict]) -> tuple[bool, list[str]]:
    """Check mathematical sanity limits. Returns (passed, violations)."""
    violations = []
    for m in metrics:
        step = m.get('step', 'unknown')
        cost_of_living = m.get("cost_of_living_change", 0)
        household_income = m.get("household_income_change", 0)
        jobs_impact = m.get("jobs_and_wages_impact", 0)

        # Month-over-month inflation > 50%
        if abs(cost_of_living) > 50:
            violations.append(f"Step {step}: inflation {cost_of_living}% exceeds ±50% limit")
        # Household income drops to negative (i.e., < -100%)
        if household_income < -100:
            violations.append(f"Step {step}: household income change {household_income}% is below -100%")
        # Jobs impact beyond ±40%
        if abs(jobs_impact) > 40:
            violations.append(f"Step {step}: jobs impact {jobs_impact}% exceeds ±40% limit")
            
    return (len(violations) == 0, violations)
