from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.engine.stubs import chat_with_run, resume_simulation, start_simulation
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
from app.schemas.run import (
    CohortGroup,
    CompareResponse,
    CostOfLivingDataPoint,
    DashboardMetric,
    DataCubeResponse,
    IncomeChartDataPoint,
    JobsDataPoint,
    ReportResponse,
    RippleEdge,
    RippleGraph,
    RippleNode,
    RunDashboard,
    RunEventResponse,
    RunStatus,
    StanceBreakdown,
    StateData,
    TimelineDataPoint,
)
from app.schemas.run import RunSummary as RunSummarySchema


async def create_run(db: AsyncSession, notebook_id: uuid.UUID | None, policy_text: str, cohorts: list) -> SimulationRun:
    run = SimulationRun(
        notebook_id=notebook_id,
        policy_text=policy_text,
        cohort_config=cohorts,
        status='loading',
        progress=0
    )
    db.add(run)
    await db.commit()
    await db.refresh(run)
    await start_simulation(str(run.id))
    return run


async def get_run_status(db: AsyncSession, run_id: uuid.UUID) -> RunStatus:
    run = await db.get(SimulationRun, run_id)
    if not run:
        raise NotFoundError("Run not found")
    return RunStatus(stage=run.status, progress=run.progress or 0)


async def get_run_events(db: AsyncSession, run_id: uuid.UUID) -> list[RunEventResponse]:
    result = await db.execute(select(RunEvent).where(RunEvent.run_id == run_id).order_by(RunEvent.created_at))
    events = result.scalars().all()
    return [
        RunEventResponse(
            id=str(e.id),
            eventType=e.event_type,
            payload=e.payload,
            createdAt=e.created_at
        ) for e in events
    ]


async def resume_run(db: AsyncSession, run_id: uuid.UUID, approved: bool, feedback: str | None) -> None:
    run = await db.get(SimulationRun, run_id)
    if not run:
        raise NotFoundError("Run not found")
    await resume_simulation(str(run_id), approved, feedback)


async def get_run_summary(db: AsyncSession, run_id: uuid.UUID) -> RunSummarySchema:
    result = await db.execute(select(RunSummary).where(RunSummary.run_id == run_id))
    summary = result.scalars().first()
    if not summary:
        raise NotFoundError("Summary not found")

    return RunSummarySchema.model_validate(summary)


async def get_run_dashboard(db: AsyncSession, run_id: uuid.UUID) -> RunDashboard:
    result = await db.execute(select(RunChartData).where(RunChartData.run_id == run_id))
    charts = result.scalars().all()

    # We need to construct RunDashboard
    # A proper implementation would map RunChartData properly based on type or content
    dashboard = RunDashboard(
        metrics=[],
        incomeChart=[],
        costOfLiving=[],
        jobs=[]
    )
    for chart in charts:
        if chart.chart_type == 'metric':
            dashboard.metrics.append(DashboardMetric.model_validate(chart.data))
        elif chart.chart_type == 'income':
            dashboard.income_chart.append(IncomeChartDataPoint.model_validate(chart.data))
        elif chart.chart_type == 'costOfLiving':
            dashboard.cost_of_living.append(CostOfLivingDataPoint.model_validate(chart.data))
        elif chart.chart_type == 'jobs':
            dashboard.jobs.append(JobsDataPoint.model_validate(chart.data))
    return dashboard


async def get_run_groups(db: AsyncSession, run_id: uuid.UUID) -> list[CohortGroup]:
    result = await db.execute(select(RunCohortGroup).where(RunCohortGroup.run_id == run_id))
    groups = result.scalars().all()

    cohort_groups = []
    for g in groups:
        stance = StanceBreakdown(
            for_=g.stance_for,
            against=g.stance_against,
            neutral=g.stance_neutral
        )
        group = CohortGroup(
            name=g.name,
            population=g.population,
            incomeChange=g.income_change,
            stance=stance,
            topConcern=g.top_concern,
            details=g.details
        )
        cohort_groups.append(group)
    return cohort_groups


async def get_run_map(db: AsyncSession, run_id: uuid.UUID) -> list[StateData]:
    result = await db.execute(select(RunStateData).where(RunStateData.run_id == run_id))
    states = result.scalars().all()
    return [StateData.model_validate(s) for s in states]


async def get_run_ripple(db: AsyncSession, run_id: uuid.UUID) -> RippleGraph:
    nodes_res = await db.execute(select(RunRippleNode).where(RunRippleNode.run_id == run_id))
    edges_res = await db.execute(select(RunRippleEdge).where(RunRippleEdge.run_id == run_id))

    nodes = [RippleNode.model_validate(n) for n in nodes_res.scalars().all()]
    edges = [RippleEdge.model_validate(e) for e in edges_res.scalars().all()]

    return RippleGraph(nodes=nodes, edges=edges)


async def get_run_timeline(db: AsyncSession, run_id: uuid.UUID) -> list[TimelineDataPoint]:
    result = await db.execute(select(RunTimelineData).where(RunTimelineData.run_id == run_id).order_by(RunTimelineData.year))
    timeline = result.scalars().all()
    return [TimelineDataPoint.model_validate(t) for t in timeline]


async def get_run_cube(db: AsyncSession, run_id: uuid.UUID) -> DataCubeResponse:
    # return data cube (stub/empty dict for now)
    return DataCubeResponse(data={"dimensions": [], "measures": [], "cells": []})


async def get_run_report(db: AsyncSession, run_id: uuid.UUID) -> ReportResponse:
    result = await db.execute(select(RunReport).where(RunReport.run_id == run_id))
    report = result.scalars().first()
    if not report:
        raise NotFoundError("Report not found")
    return ReportResponse.model_validate(report)


async def chat_with_run_service(run_id: uuid.UUID, message: str) -> str:
    return await chat_with_run(str(run_id), message)


async def compare_runs(db: AsyncSession, run_ids: list[uuid.UUID]) -> CompareResponse:
    # Query multiple runs, compare metrics side-by-side
    runs = []
    for rid in run_ids:
        r = await db.get(SimulationRun, rid)
        if r:
            runs.append({"id": str(r.id), "status": r.status})

    return CompareResponse(
        runs=runs,
        metricsComparison=[]
    )
