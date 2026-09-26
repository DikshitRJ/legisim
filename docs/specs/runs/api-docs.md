# Runs API Documentation

This document provides plain English documentation for the API endpoints handling simulation runs, predictions, reports, dashboard metrics, and timeline data in LegiSim.

## Simulation Lifecycle

1. **Start a Run (`POST /api/runs`)**
   The user inputs the policy text and their targeted demographic cohorts. The backend triggers the simulation pipeline (LangGraph + JEV) and immediately returns a `runId`.

2. **Polling for Status (`GET /api/runs/:runId/status`)**
   The frontend can occasionally poll this endpoint to get the current stage (research, simulation, analysis) and a percentage progress.

3. **Live Events (`GET /api/runs/:runId/events`)**
   An SSE (Server-Sent Events) endpoint that streams live milestone updates to the client for the loading screen.

4. **Human Review / Checkpoint (`POST /api/runs/:runId/resume`)**
   If the pipeline requires officer approval (e.g., confirming the policy extraction before full simulation), this endpoint receives the human feedback to resume execution.

## Results & Analysis

Once a simulation is complete, the following endpoints serve detailed analytic outputs:

- **Summary (`GET /api/runs/:runId/summary`)**
  Fetches the executive summary (paragraphs of AI insights) and top-level dashboard metrics (e.g., inflation shift, overall acceptance).

- **Dashboard Charts (`GET /api/runs/:runId/dashboard`)**
  Returns data series formatted for charts: Income changes across deciles, cost of living breakdowns, and job sector impacts.

- **Cohort Groups (`GET /api/runs/:runId/groups`)**
  Fetches detailed impact profiles for distinct demographic groups (e.g., "Urban Gig Workers in Tier 1"), including their stance (support/oppose/neutral) and behavioral changes.

- **Map / Geographic (`GET /api/runs/:runId/map`)**
  Returns aggregated impact metrics grouped by Indian state for rendering the choropleth map.

- **Ripple Graph (`GET /api/runs/:runId/ripple`)**
  Fetches causal graph data containing `nodes` (variables like Fuel Price, Freight Cost) and `edges` (causal links with lags) for the node-graph visualization.

- **Timeline (`GET /api/runs/:runId/timeline`)**
  Returns a month-by-month projection (1-12 months) of key indicators like acceptance, inflation, and income.

- **Data Cube (`GET /api/runs/:runId/cube`)**
  Returns a deeply nested precomputed OLAP cube for advanced pivot-table-like exploration on the frontend.

## Reporting & Actions

- **Report (`GET /api/runs/:runId/report`)**
  Returns the long-form AI-written markdown report analyzing the policy's implications.

- **Chat (`POST /api/runs/:runId/chat`)**
  Enables the officer to have a conversational Q&A specifically grounded in the context of this simulation run.

- **Compare (`POST /api/compare`)**
  Takes an array of `runId`s and returns side-by-side comparison metrics to evaluate multiple policy scenarios.

- **Export (`GET /api/runs/:runId/export/:format`)**
  Downloads the simulation results in a specific format (e.g., PDF report, CSV data, PPTX presentation).
