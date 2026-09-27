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


from fastapi import BackgroundTasks

async def create_run(db: AsyncSession, background_tasks: BackgroundTasks, notebook_id: uuid.UUID | None, policy_text: str, cohorts: list) -> SimulationRun:
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
    background_tasks.add_task(start_simulation, str(run.id))
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
            run_id=str(e.run_id),
            event_type=e.event_type,
            payload=e.payload,
            created_at=e.created_at
        ) for e in events
    ]


async def resume_run(db: AsyncSession, background_tasks: BackgroundTasks, run_id: uuid.UUID, approved: bool, feedback: str | None) -> None:
    run = await db.get(SimulationRun, run_id)
    if not run:
        raise NotFoundError("Run not found")
    background_tasks.add_task(resume_simulation, str(run_id), approved, feedback)


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
        income=[],
        cost_of_living=[],
        jobs=[]
    )
    for chart in charts:
        if chart.chart_type == 'income':
            dashboard.income.append(IncomeChartDataPoint.model_validate(chart.data_payload))
        elif chart.chart_type == 'costOfLiving':
            dashboard.cost_of_living.append(CostOfLivingDataPoint.model_validate(chart.data_payload))
        elif chart.chart_type == 'jobs':
            dashboard.jobs.append(JobsDataPoint.model_validate(chart.data_payload))
    return dashboard


async def get_run_groups(db: AsyncSession, run_id: uuid.UUID) -> list[CohortGroup]:
    result = await db.execute(select(RunCohortGroup).where(RunCohortGroup.run_id == run_id))
    groups = result.scalars().all()

    cohort_groups = []
    for g in groups:
        stance = StanceBreakdown(
            support=g.stance_for,
            neutral=g.stance_neutral,
            oppose=g.stance_against
        )
        group = CohortGroup(
            id=str(g.id),
            name=g.name,
            population=str(g.population),
            description=g.details or "",
            stance=stance,
            income_change=g.income_change,
            behaviors=g.behaviors or [],
            confidence="Medium"
        )
        cohort_groups.append(group)
    return cohort_groups


async def get_run_map(db: AsyncSession, run_id: uuid.UUID) -> list[StateData]:
    result = await db.execute(select(RunStateData).where(RunStateData.run_id == run_id))
    states = result.scalars().all()
    return [
        StateData(
            code=s.state_code,
            name=s.state_name,
            income_change=s.income_change,
            inflation_impact=s.inflation_impact,
            acceptance=s.acceptance,
            employment=s.employment
        ) for s in states
    ]


async def get_run_ripple(db: AsyncSession, run_id: uuid.UUID) -> RippleGraph:
    nodes_res = await db.execute(select(RunRippleNode).where(RunRippleNode.run_id == run_id))
    edges_res = await db.execute(select(RunRippleEdge).where(RunRippleEdge.run_id == run_id))

    nodes = [RippleNode.model_validate(n) for n in nodes_res.scalars().all()]
    edges = [
        RippleEdge(
            id=str(e.id),
            source=e.source_node,
            target=e.target_node,
            strength=e.strength,
            lag_months=e.lag_months,
            mechanism=e.mechanism
        ) for e in edges_res.scalars().all()
    ]

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
        comparison={}
    )
