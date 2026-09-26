"""Pydantic Schemas Package.

Contains request, response, and validation schemas across all domains
utilizing Pydantic V2 models with camelCase aliasing.
"""

from __future__ import annotations

from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    OfficerProfile,
)
from app.schemas.cohort import (
    CohortCategory,
    CohortReactionCreate,
    HydratedPrompt,
    JEVPersonaScore,
    JEVSelectionResult,
    PersonaDemographics,
    PersonaSchema,
    PolicyInput,
    TargetingProfile,
)
from app.schemas.common import (
    CamelModel,
    ErrorResponse,
    HealthResponse,
    PaginatedResponse,
    SuccessResponse,
)
from app.schemas.compare import (
    CompareRequest,
    CompareResponse,
)
from app.schemas.notebook import (
    Notebook,
    NotebookCreate,
    NotebookResponse,
    NotebookStatus,
    NotebookUpdate,
)
from app.schemas.ripple import (
    ConfidenceLevel,
    RippleDomain,
)
from app.schemas.run import (
    ChatRequest,
    ChatResponse,
    CohortGroup,
    CostOfLivingDataPoint,
    DashboardMetric,
    DataCubeResponse,
    EvidenceKind,
    IncomeChartDataPoint,
    JobsDataPoint,
    ReportResponse,
    ResumeRequest,
    RippleEdge,
    RippleGraph,
    RippleGraphResponse,
    RippleNode,
    RunCreateRequest,
    RunDashboard,
    RunEventResponse,
    RunExportFormat,
    RunStartRequest,
    RunStartResponse,
    RunStatus,
    RunSummary,
    StanceBreakdown,
    StateData,
    SummarySection,
    TimelineDataPoint,
)

__all__: list[str] = [
    # Common
    "CamelModel",
    "SuccessResponse",
    "ErrorResponse",
    "HealthResponse",
    "PaginatedResponse",
    # Auth
    "LoginRequest",
    "LoginResponse",
    "OfficerProfile",
    # Notebooks
    "Notebook",
    "NotebookCreate",
    "NotebookUpdate",
    "NotebookResponse",
    "NotebookStatus",
    # Cohorts
    "CohortCategory",
    "PersonaDemographics",
    "PersonaSchema",
    "PolicyInput",
    "TargetingProfile",
    "JEVPersonaScore",
    "JEVSelectionResult",
    "HydratedPrompt",
    "CohortReactionCreate",
    # Runs
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
    "RunExportFormat",
    "EvidenceKind",
    # Ripple
    "RippleDomain",
    "ConfidenceLevel",
]
