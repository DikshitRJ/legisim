import pytest

@pytest.fixture
def mock_sim_state():
    return {
        "run_id": "test_run",
        "policy_text": "Sample",
        "policy": {},
        "population_spec": {},
        "conditions": {},
        "research": {},
        "cohorts": [],
        "active_cohorts": [],
        "hydrated_prompts": [],
        "step": 1,
        "horizon": 5,
        "reactions": [],
        "metrics": [],
        "ripple": {},
        "viz_specs": [],
        "report": {},
        "revisions": 0,
        "warnings": []
    }

@pytest.fixture
def mock_policy():
    return {
        "changes": "Increase taxes",
        "size_of_change": 5.0,
        "tax_subsidy_flag": "tax",
        "target_group": "wealthy",
        "geographic_coverage": "national",
        "start_date": "2024-01-01",
        "rollout_phases": ["Phase 1"]
    }

@pytest.fixture
def mock_metrics():
    return [{"step": i, "household_income_change": i * 0.1, "cost_of_living_change": i * 0.05, "jobs_and_wages_impact": i * 0.01, "business_impact": i * -0.01, "govt_fiscal_effect": i * 1.0, "inequality_poverty": i * -0.1, "regional_spread": {}, "source": "test"} for i in range(12)]

@pytest.fixture
def mock_ripple():
    return {"nodes": [{"id": "A"}, {"id": "B"}], "edges": [{"source": "A", "target": "B"}]}

@pytest.fixture
def mock_reactions():
    return [{"cohort_id": "c1", "behavior_change": "save more", "public_acceptance": 0.8, "confidence": 0.9, "source": "LLM"}]

@pytest.fixture
def mock_research():
    return {"data": "some facts"}

@pytest.fixture
def sample_cohort_card():
    return {"id": "c1", "region": "North", "size": 1000, "age_band": "18-25"}
