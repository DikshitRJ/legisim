"""Unit tests for the Runs domain Pydantic V2 schemas."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from app.schemas.compare import CompareRequest, CompareResponse
from app.schemas.ripple import (
    RippleEdge,
    RippleGraph,
    RippleGraphResponse,
    RippleNode,
)
from app.schemas.run import (
    ChatRequest,
    ChatResponse,
    CohortGroup,
    CostOfLivingDataPoint,
    DashboardMetric,
    DataCubeResponse,
    IncomeChartDataPoint,
    JobsDataPoint,
    ReportResponse,
    ResumeRequest,
    RunCreateRequest,
    RunDashboard,
    RunEventResponse,
    RunStartRequest,
    RunStartResponse,
    RunStatus,
    RunSummary,
    StanceBreakdown,
    StateData,
    SummarySection,
    TimelineDataPoint,
)


def test_run_start_request_and_response() -> None:
    """Test RunStartRequest and RunStartResponse serialization and aliasing."""
    req = RunStartRequest(
        policy_text="Universal basic income of Rs 5000/month",
        cohorts={"cat-1": ["persona-1", "persona-2"]},
    )
    req_dump = req.model_dump(by_alias=True)
    assert req_dump["policyText"] == "Universal basic income of Rs 5000/month"
    assert req_dump["cohorts"]["cat-1"] == ["persona-1", "persona-2"]

    # Test alias RunCreateRequest
    assert RunCreateRequest is RunStartRequest

    # Test RunStartResponse
    resp = RunStartResponse(run_id="run-uuid-1234")
    assert resp.run_id == "run-uuid-1234"
    assert resp.status == "loading"
    resp_dump = resp.model_dump(by_alias=True)
    assert resp_dump["runId"] == "run-uuid-1234"
    assert resp_dump["status"] == "loading"

    # CamelCase population
    resp2 = RunStartResponse.model_validate({"runId": "run-uuid-5678", "status": "loading"})
    assert resp2.run_id == "run-uuid-5678"


def test_run_status_validation() -> None:
    """Test RunStatus schema with valid and invalid stages."""
    valid_status = RunStatus(stage="simulation", progress=75.5)
    assert valid_status.stage == "simulation"
    assert valid_status.progress == 75.5

    # Invalid stage should raise ValidationError
    with pytest.raises(ValidationError):
        RunStatus(stage="invalid_stage", progress=10.0)  # type: ignore[arg-type]


def test_summary_section_and_run_summary() -> None:
    """Test SummarySection and RunSummary with case-insensitive confidence."""
    sec1 = SummarySection(
        title="Fiscal Deficit Shift",
        content="Projected deficit expands by 0.3% in FY26.",
        confidence="High",
        kind="modelled",
    )
    # Test lowercase normalization
    sec2 = SummarySection(
        title="Consumption Boost",
        content="Rural consumption estimated to grow by 1.8%.",
        confidence="medium",  # type: ignore[arg-type]
        kind="measured",
    )
    assert sec2.confidence == "Medium"

    metric = DashboardMetric(
        label="Inflation Impact",
        value="+0.45%",
        range="+0.3% to +0.6%",
        direction="positive",
        kind="modelled",
    )
    metric_dump = metric.model_dump(by_alias=True)
    assert metric_dump["direction"] == "positive"
    assert metric_dump["kind"] == "modelled"

    summary = RunSummary(sections=[sec1, sec2], metrics=[metric])
    summary_dump = summary.model_dump(by_alias=True)
    assert len(summary_dump["sections"]) == 2
    assert len(summary_dump["metrics"]) == 1


def test_cohort_group_and_stance_breakdown() -> None:
    """Test StanceBreakdown and CohortGroup camelCase serialization."""
    stance = StanceBreakdown(support=58.5, neutral=26.0, oppose=15.5)
    stance_dump = stance.model_dump(by_alias=True)
    assert stance_dump["support"] == 58.5
    assert stance_dump["neutral"] == 26.0
    assert stance_dump["oppose"] == 15.5

    cohort = CohortGroup(
        id="cg-01",
        name="Urban Gig Workers",
        population="8.5 Million",
        description="Delivery partners and ride-hail drivers in metro areas",
        stance=stance,
        income_change=4.2,
        behaviors=["Higher discretionary spending", "Increased fuel consumption"],
        confidence="high",  # type: ignore[arg-type]
    )
    assert cohort.confidence == "High"
    cohort_dump = cohort.model_dump(by_alias=True)
    assert cohort_dump["id"] == "cg-01"
    assert cohort_dump["incomeChange"] == 4.2
    assert cohort_dump["stance"]["support"] == 58.5
    assert len(cohort_dump["behaviors"]) == 2


def test_state_data() -> None:
    """Test StateData serialization for choropleth mapping."""
    state = StateData(
        code="KA",
        name="Karnataka",
        income_change=3.1,
        inflation_impact=0.35,
        acceptance=68.0,
        jobs_affected=32000.0,
    )
    state_dump = state.model_dump(by_alias=True)
    assert state_dump["code"] == "KA"
    assert state_dump["name"] == "Karnataka"
    assert state_dump["incomeChange"] == 3.1
    assert state_dump["inflationImpact"] == 0.35
    assert state_dump["acceptance"] == 68.0
    assert state_dump["jobsAffected"] == 32000.0


def test_ripple_graph_components() -> None:
    """Test RippleNode, RippleEdge, and RippleGraph structure and aliases."""
    node1 = RippleNode(
        id="node-1",
        label="Fertilizer Subsidy Cut",
        layer=0.0,
        domain="agriculture",
        magnitude="Significant cost escalation",
        confidence="High",
        kind="measured",
    )
    node2 = RippleNode(
        id="node-2",
        label="Food Crop Prices",
        layer=1.0,
        domain="consumer",
        magnitude="Moderate inflation",
        confidence="Medium",
        kind="modelled",
    )
    edge = RippleEdge(
        id="edge-1",
        source="node-1",
        target="node-2",
        strength=0.82,
        lag_months=3,
        mechanism="Input cost pass-through to wholesale markets",
    )
    edge_dump = edge.model_dump(by_alias=True)
    assert edge_dump["source"] == "node-1"
    assert edge_dump["target"] == "node-2"
    assert edge_dump["strength"] == 0.82
    assert edge_dump["lagMonths"] == 3

    graph = RippleGraph(nodes=[node1, node2], edges=[edge])
    graph_dump = graph.model_dump(by_alias=True)
    assert len(graph_dump["nodes"]) == 2
    assert len(graph_dump["edges"]) == 1
    assert RippleGraphResponse is RippleGraph


def test_timeline_data_point() -> None:
    """Test TimelineDataPoint temporal projection model."""
    tl = TimelineDataPoint(
        month=6.0,
        label="Month 6",
        income_change=1.2,
        inflation_impact=0.15,
        acceptance=74.0,
        employment=102.5,
    )
    tl_dump = tl.model_dump(by_alias=True)
    assert tl_dump["month"] == 6.0
    assert tl_dump["incomeChange"] == 1.2
    assert tl_dump["inflationImpact"] == 0.15
    assert tl_dump["acceptance"] == 74.0
    assert tl_dump["employment"] == 102.5


def test_run_dashboard_charts() -> None:
    """Test RunDashboard with chart series."""
    income_pts = [
        IncomeChartDataPoint(group="Bottom 20%", change=3.8, low=2.5, high=5.0),
        IncomeChartDataPoint(group="Top 20%", change=-0.8, low=-1.5, high=-0.1),
    ]
    col_pts = [
        CostOfLivingDataPoint(category="Food & Beverage", change=1.4),
        CostOfLivingDataPoint(category="Transport", change=2.1),
    ]
    jobs_pts = [
        JobsDataPoint(sector="Manufacturing", change=15000.0, percentage=1.8),
        JobsDataPoint(sector="Agriculture", change=-5000.0, percentage=-0.6),
    ]

    dash = RunDashboard(income=income_pts, cost_of_living=col_pts, jobs=jobs_pts)
    dash_dump = dash.model_dump(by_alias=True)
    assert len(dash_dump["income"]) == 2
    assert len(dash_dump["costOfLiving"]) == 2
    assert len(dash_dump["jobs"]) == 2
    assert dash_dump["income"][0]["group"] == "Bottom 20%"
    assert dash_dump["costOfLiving"][0]["category"] == "Food & Beverage"
    assert dash_dump["jobs"][0]["sector"] == "Manufacturing"


def test_resume_request() -> None:
    """Test ResumeRequest approval and feedback."""
    r1 = ResumeRequest(approved=True, feedback="Approved with minor adjustments")
    assert r1.approved is True
    assert r1.feedback == "Approved with minor adjustments"

    r2 = ResumeRequest(approved=False)
    assert r2.approved is False
    assert r2.feedback is None


def test_chat_schemas() -> None:
    """Test ChatRequest and ChatResponse schemas."""
    req = ChatRequest(message="How does this impact rural credit?")
    assert req.message == "How does this impact rural credit?"

    resp = ChatResponse(reply="Rural credit availability is projected to improve by 8%.")
    assert "projected" in resp.reply


def test_compare_schemas() -> None:
    """Test CompareRequest and CompareResponse schemas."""
    req = CompareRequest(run_ids=["run-1", "run-2"])
    req_dump = req.model_dump(by_alias=True)
    assert req_dump["runIds"] == ["run-1", "run-2"]

    resp = CompareResponse(comparison={"delta_inflation": 0.2, "delta_income": 1.5})
    assert resp.comparison["delta_inflation"] == 0.2


def test_report_and_cube_and_event_responses() -> None:
    """Test ReportResponse, DataCubeResponse, and RunEventResponse."""
    rep = ReportResponse(markdown="# Executive Report\n\nDetailed policy simulation analysis.")
    assert rep.markdown.startswith("# Executive Report")

    cube = DataCubeResponse(data={"dim_state": ["MH", "KA"], "metrics": [10, 20]})
    assert cube.data["dim_state"] == ["MH", "KA"]

    now = datetime.now(UTC)
    ev = RunEventResponse(
        id="ev-123",
        run_id="run-456",
        event_type="stage_progress",
        payload={"stage": "simulation", "progress": 50},
        created_at=now,
    )
    ev_dump = ev.model_dump(by_alias=True)
    assert ev_dump["runId"] == "run-456"
    assert ev_dump["eventType"] == "stage_progress"
    assert ev_dump["payload"]["progress"] == 50
