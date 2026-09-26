"""
Core LangGraph state definition for LegiSim pipeline.
"""

from typing import TypedDict, Annotated, List, Dict, Any, Optional
import operator

class Policy(TypedDict):
    changes: str
    size_of_change: float
    tax_subsidy_flag: str
    target_group: str
    geographic_coverage: str
    start_date: str
    rollout_phases: List[str]

class Cohort(TypedDict):
    id: str
    region: str
    size: int
    age_band: str
    gender: str
    income_band: str
    occupation: str
    urban_rural: str
    education: str
    literacy: str
    trust_in_govt: float
    ideological_lean: float
    agreeableness: float
    weight: float

class Reaction(TypedDict):
    cohort_id: str
    behavior_change: str
    public_acceptance: float
    confidence: float
    source: str

class Metric(TypedDict):
    step: int
    household_income_change: float
    cost_of_living_change: float
    jobs_and_wages_impact: float
    business_impact: float
    govt_fiscal_effect: float
    inequality_poverty: float
    regional_spread: Dict[str, float]
    source: str

class SimState(TypedDict, total=False):
    run_id: str
    policy_text: str
    policy: Policy
    population_spec: Dict[str, Any]
    conditions: Dict[str, Any]
    research: Dict[str, Any]
    cohorts: List[Cohort]
    active_cohorts: List[Cohort]
    hydrated_prompts: List[Dict[str, Any]]
    step: int
    horizon: int
    reactions: Annotated[List[Reaction], operator.add]
    metrics: Annotated[List[Metric], operator.add]
    ripple: Dict[str, Any]
    viz_specs: List[Dict[str, Any]]
    report: Dict[str, Any]
    revisions: int
    warnings: Annotated[List[str], operator.add]

__all__ = ["Policy", "Cohort", "Reaction", "Metric", "SimState"]
