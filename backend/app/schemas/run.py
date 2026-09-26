"""Pydantic V2 Schemas for the Runs Domain.

Defines request, response, and intermediate validation schemas matching the
runs/openapi.yaml specification for simulation runs, predictions, reports,
dashboard metrics, geographic impacts, and temporal evolution.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import Field, field_validator

from app.schemas.common import CamelModel

# Type aliases for domain enumerations
RunStage = Literal["research", "simulation", "analysis", "complete"]
RunStatusLiteral = Literal["loading"]
ConfidenceTier = Literal["High", "Medium", "Low"]
EvidenceKind = Literal["measured", "modelled", "judged"]
MetricDirection = Literal["positive", "negative"]
RunExportFormat = Literal["pdf", "csv", "pptx"]


class RunStartRequest(CamelModel):
    """Request payload to initiate a new policy simulation run."""

    policy_text: str = Field(..., description="Raw text of the proposed policy or reform")
    cohorts: dict[str, list[str]] = Field(
        default_factory=dict,
        description="Dictionary mapping cohort category IDs to selected persona IDs",
    )


RunCreateRequest = RunStartRequest


class RunStartResponse(CamelModel):
    """Response returned when a simulation run is initiated."""

    run_id: str = Field(..., description="Unique identifier of the simulation run")
    status: RunStatusLiteral = Field(
        default="loading",
        description="Initial status of the run, always 'loading' upon creation",
    )


class RunStatus(CamelModel):
    """Execution status and progress for polling and progress screens."""

    stage: RunStage = Field(
        ...,
        description="Current lifecycle stage of the simulation pipeline",
    )
    progress: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="Percentage progress of the current stage (0.0 to 100.0)",
    )


class SummarySection(CamelModel):
    """Narrative section in the executive summary report."""

    title: str = Field(..., description="Section title or heading")
    content: str = Field(..., description="Analytical narrative markdown or plain text")
    confidence: ConfidenceTier = Field(
        ...,
        description="Confidence rating for this analysis section",
    )
    kind: EvidenceKind = Field(
        ...,
        description="Epistemological classification (measured, modelled, judged)",
    )

    @field_validator("confidence", mode="before")
    @classmethod
    def normalize_confidence(cls, v: Any) -> Any:
        """Normalize confidence level casing."""
        if isinstance(v, str):
            mapping = {"high": "High", "medium": "Medium", "low": "Low"}
            return mapping.get(v.lower(), v)
        return v


class DashboardMetric(CamelModel):
    """Key quantitative dashboard indicator."""

    label: str = Field(..., description="Metric label")
    value: str = Field(..., description="Formatted string display value (e.g. '+1.8%')")
    range: str = Field(..., description="Projected uncertainty range (e.g. '+1.2% to +2.4%')")
    direction: MetricDirection = Field(
        ...,
        description="Direction of impact relative to baseline",
    )
    kind: EvidenceKind = Field(
        ...,
        description="Provenance tag of the metric",
    )


class RunSummary(CamelModel):
    """Comprehensive executive summary with narrative sections and headline metrics."""

    sections: list[SummarySection] = Field(
        ...,
        description="Narrative insight sections of the summary",
    )
    metrics: list[DashboardMetric] = Field(
        ...,
        description="Headline dashboard metrics",
    )


class StanceBreakdown(CamelModel):
    """Population stance percentage breakdown for a cohort."""

    support: float = Field(..., ge=0.0, le=100.0, description="Percentage supporting the policy")
    neutral: float = Field(..., ge=0.0, le=100.0, description="Percentage neutral to the policy")
    oppose: float = Field(..., ge=0.0, le=100.0, description="Percentage opposing the policy")


class CohortGroup(CamelModel):
    """Impact assessment and behavioural shifts for a targeted demographic cohort."""

    id: str = Field(..., description="Unique cohort identifier")
    name: str = Field(..., description="Descriptive cohort name")
    population: str = Field(..., description="Estimated population count or percentage string")
    description: str = Field(..., description="Detailed cohort description and profile")
    stance: StanceBreakdown = Field(
        ...,
        description="Stance breakdown across support, neutral, oppose",
    )
    income_change: float = Field(
        ...,
        description="Projected net income change percentage for this cohort",
    )
    behaviors: list[str] = Field(
        ...,
        description="Anticipated behavioral reactions and micro-economic adaptations",
    )
    confidence: ConfidenceTier = Field(
        ...,
        description="Confidence level in this cohort impact assessment",
    )

    @field_validator("confidence", mode="before")
    @classmethod
    def normalize_confidence(cls, v: Any) -> Any:
        """Normalize confidence level casing."""
        if isinstance(v, str):
            mapping = {"high": "High", "medium": "Medium", "low": "Low"}
            return mapping.get(v.lower(), v)
        return v


class StateData(CamelModel):
    """State-level geographic impact data for choropleth mapping."""

    code: str = Field(..., description="State or territory code (e.g. 'MH', 'DL', 'KA')")
    name: str = Field(..., description="Full state or union territory name")
    income_change: float = Field(
        ...,
        description="State-wide projected average income change percentage",
    )
    inflation_impact: float = Field(
        ...,
        description="State-wide projected inflation delta percentage",
    )
    acceptance: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="Overall policy acceptance percentage in this state",
    )
    jobs_affected: float = Field(
        ...,
        description="Estimated number of jobs affected across the state",
    )


class RippleNode(CamelModel):
    """Node representing a causal effect or policy outcome in the ripple graph."""

    id: str = Field(..., description="Unique identifier for the causal node")
    label: str = Field(..., description="Human-readable label for the effect or outcome")
    layer: float = Field(
        ...,
        description="Causal depth layer (0 for direct impact, 1+ for higher orders)",
    )
    domain: str = Field(..., description="Socio-economic domain of the node")
    magnitude: str = Field(..., description="Natural language description of magnitude of change")
    confidence: ConfidenceTier = Field(
        ...,
        description="Confidence level in this causal outcome",
    )
    kind: EvidenceKind = Field(
        ...,
        description="Epistemological classification (measured, modelled, judged)",
    )

    @field_validator("confidence", mode="before")
    @classmethod
    def normalize_confidence(cls, v: Any) -> Any:
        """Normalize confidence level casing."""
        if isinstance(v, str):
            mapping = {"high": "High", "medium": "Medium", "low": "Low"}
            return mapping.get(v.lower(), v)
        return v


class RippleEdge(CamelModel):
    """Directed link representing causal transmission between ripple nodes."""

    id: str = Field(..., description="Unique identifier for the causal edge")
    source: str = Field(..., description="ID of the source RippleNode")
    target: str = Field(..., description="ID of the target RippleNode")
    strength: float = Field(..., description="Causal transmission strength score")
    lag_months: int = Field(..., ge=0, description="Time delay in months before effect manifests")
    mechanism: str = Field(..., description="Explanation of the causal transmission mechanism")


class RippleGraph(CamelModel):
    """Complete causal ripple graph consisting of nodes and directed edges."""

    nodes: list[RippleNode] = Field(..., description="Collection of causal nodes")
    edges: list[RippleEdge] = Field(..., description="Collection of directed causal edges")


RippleGraphResponse = RippleGraph


class TimelineDataPoint(CamelModel):
    """Monthly projected indicators over a 12-month temporal evolution."""

    month: float = Field(..., description="Simulation timeline month number (e.g. 1.0 to 12.0)")
    label: str = Field(..., description="Human-readable month label (e.g. 'Month 1', 'Jan 2025')")
    income_change: float = Field(..., description="Projected income delta percentage at this point")
    inflation_impact: float = Field(..., description="Projected inflation delta at this point")
    acceptance: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="Projected overall public acceptance percentage at this point",
    )
    employment: float = Field(..., description="Projected employment indicator delta at this point")


class IncomeChartDataPoint(CamelModel):
    """Income change distribution data point across cohorts/deciles."""

    group: str = Field(
        ...,
        description="Income group or decile label (e.g. 'Bottom 20%', 'Decile 1')",
    )
    change: float = Field(..., description="Projected net income change percentage")
    low: float = Field(..., description="Lower bound of uncertainty range")
    high: float = Field(..., description="Upper bound of uncertainty range")


class CostOfLivingDataPoint(CamelModel):
    """Cost of living change data point across spending categories."""

    category: str = Field(..., description="Spending category (e.g. 'Housing', 'Food', 'Fuel')")
    change: float = Field(..., description="Projected cost change percentage")


class JobsDataPoint(CamelModel):
    """Employment change data point across industry sectors."""

    sector: str = Field(..., description="Industry or employment sector name")
    change: float = Field(..., description="Projected net job change (count or index)")
    percentage: float = Field(..., description="Projected percentage shift in sector employment")


class RunDashboard(CamelModel):
    """Dashboard chart series aggregating income, cost of living, and jobs."""

    income: list[IncomeChartDataPoint] = Field(
        ...,
        description="Income distribution shift data points",
    )
    cost_of_living: list[CostOfLivingDataPoint] = Field(
        ...,
        description="Cost of living shifts across commodity categories",
    )
    jobs: list[JobsDataPoint] = Field(
        ...,
        description="Employment shifts across key industry sectors",
    )


class ResumeRequest(CamelModel):
    """Officer checkpoint review payload to resume simulation execution."""

    feedback: str | None = Field(
        default=None,
        description="Optional qualitative guidance or steering feedback from the officer",
    )
    approved: bool = Field(
        ...,
        description="Whether the intermediate checkpoint results are approved to proceed",
    )


class ChatRequest(CamelModel):
    """User query payload for simulation-grounded AI conversational Q&A."""

    message: str = Field(..., min_length=1, description="Question or prompt about the simulation")


class ChatResponse(CamelModel):
    """AI response payload grounded in simulation run context."""

    reply: str = Field(..., description="Contextual answer synthesized by the LLM")


class CompareRequest(CamelModel):
    """Request payload to compare multiple simulation runs side-by-side."""

    run_ids: list[str] = Field(
        ...,
        min_length=1,
        description="List of simulation run IDs to compare",
    )


class CompareResponse(CamelModel):
    """Response containing side-by-side comparison metrics for simulation runs."""

    comparison: dict[str, Any] = Field(
        default_factory=dict,
        description="Comparative analysis matrix and delta metrics",
    )


class ReportResponse(CamelModel):
    """AI-generated long-form markdown report response."""

    markdown: str = Field(..., description="Full synthesized analytical report in markdown format")


class DataCubeResponse(CamelModel):
    """Precomputed multi-dimensional OLAP data cube for exploratory analysis."""

    data: dict[str, Any] = Field(
        default_factory=dict,
        description="OLAP cube dimensional data structure",
    )


class RunEventResponse(CamelModel):
    """Server-sent event payload for real-time simulation progress updates."""

    id: str = Field(..., description="Event UUID")
    run_id: str = Field(..., description="Run UUID")
    event_type: str = Field(..., description="Lifecycle event classification type")
    payload: dict[str, Any] = Field(
        default_factory=dict,
        description="Arbitrary event payload data",
    )
    created_at: datetime = Field(..., description="Timestamp when the event occurred")


__all__: list[str] = [
    "RunStage",
    "RunStatusLiteral",
    "ConfidenceTier",
    "EvidenceKind",
    "MetricDirection",
    "RunExportFormat",
    "RunStartRequest",
    "RunCreateRequest",
    "RunStartResponse",
    "RunStatus",
    "SummarySection",
    "DashboardMetric",
    "RunSummary",
    "StanceBreakdown",
    "CohortGroup",
    "StateData",
    "RippleNode",
    "RippleEdge",
    "RippleGraph",
    "RippleGraphResponse",
    "TimelineDataPoint",
    "IncomeChartDataPoint",
    "CostOfLivingDataPoint",
    "JobsDataPoint",
    "RunDashboard",
    "ResumeRequest",
    "ChatRequest",
    "ChatResponse",
    "CompareRequest",
    "CompareResponse",
    "ReportResponse",
    "DataCubeResponse",
    "RunEventResponse",
]
