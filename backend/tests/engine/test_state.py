from app.graph.state import SimState, Policy, Metric
import operator

def test_sim_state_has_required_fields():
    state: SimState = {"run_id": "123"}
    assert "run_id" in state

def test_annotated_reducers_work():
    assert getattr(SimState.__annotations__["reactions"], "__metadata__")[0] == operator.add

def test_policy_typeddict_fields():
    assert "changes" in Policy.__annotations__

def test_metric_typeddict_fields():
    assert "step" in Metric.__annotations__
