"""SQLAlchemy Models Package.

Re-exports all database models across domains:
- Base & mixins
- Auth / Officers
- Notebooks & Sessions
- Simulation Runs, Events, Summaries, Timeline, Charts, Reports
- Cohorts, Personas, Cards, Targeting Profiles, JEV Results
- Ripple Nodes & Edges
- Analogues (TODO)
"""

from __future__ import annotations

from app.models.base import Base, TimestampMixin, UUIDMixin
from app.models.cohort import CohortCard, JEVSelectionResult, Persona, TargetingProfile
from app.models.notebook import Notebook, NotebookSession
from app.models.officer import Officer, OfficerSession
from app.models.ripple import RippleEdge, RippleNode
from app.models.run import (
    RunChartData,
    RunCohortGroup,
    RunEvent,
    RunReport,
    RunRippleEdge,
    RunRippleNode,
    RunStateData,
    RunSummary,
    RunTimelineData,
    SimulationRun,
)

# TODO: Import and re-export once implemented:
# from app.models.analogue import Analogue

__all__: list[str] = [
    "Base",
    "UUIDMixin",
    "TimestampMixin",
    "Officer",
    "OfficerSession",
    "Notebook",
    "NotebookSession",
    "SimulationRun",
    "RunEvent",
    "RunSummary",
    "RunCohortGroup",
    "RunStateData",
    "RunRippleNode",
    "RunRippleEdge",
    "RunTimelineData",
    "RunChartData",
    "RunReport",
    "Persona",
    "CohortCard",
    "TargetingProfile",
    "JEVSelectionResult",
    "RippleNode",
    "RippleEdge",
    # TODO: Add to __all__ as implemented:
    # "Analogue",
]
