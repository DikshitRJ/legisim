# OpenAPI Specification

## Core Interfaces

```typescript
interface Notebook {
  id: string;
  title: string;
  description: string;
  sources: number;
  modifiedAt: string;
  status: 'active' | 'archived';
}

interface CohortCategory {
  id: string;
  number: string;
  title: string;
  options: string[];
}

interface CohortGroup {
  id: string;
  name: string;
  population: string;
  description: string;
  stance: { support: number; neutral: number; oppose: number };
  incomeChange: number;
  behaviors: string[];
  confidence: 'High' | 'Medium' | 'Low';
}

interface StateData {
  code: string;
  name: string;
  incomeChange: number;
  inflationImpact: number;
  acceptance: number;
  jobsAffected: number;
}

interface RippleNode {
  id: string;
  label: string;
  layer: number;
  domain: string;
  magnitude: string;
  confidence: 'High' | 'Medium' | 'Low';
  kind: 'measured' | 'modelled' | 'judged';
}

interface RippleEdge {
  id: string;
  source: string;
  target: string;
  strength: number;
  lagMonths: number;
  mechanism: string;
}

interface SummarySection {
  title: string;
  content: string;
  confidence: 'High' | 'Medium' | 'Low';
  kind: 'measured' | 'modelled' | 'judged';
}

interface DashboardMetric {
  label: string;
  value: string;
  range: string;
  direction: 'positive' | 'negative';
  kind: 'modelled' | 'measured' | 'judged';
}

interface IncomeChartDataPoint {
  group: string;
  change: number;
  low: number;
  high: number;
}

interface CostOfLivingDataPoint {
  category: string;
  change: number;
}

interface JobsDataPoint {
  sector: string;
  change: number;
  percentage: number;
}

interface TimelineDataPoint {
  month: number;
  label: string;
  incomeChange: number;
  inflationImpact: number;
  acceptance: number;
  employment: number;
}
```

## Endpoints

### Authentication

#### `POST /api/auth/login`
**Description**: Authenticate an officer.
- **Request Body**: `{ officerId: string, password: string }`
- **Response**: `{ token: string, user: { id: string, name: string, role: string } }`
- **Errors**: 401 Unauthorized

#### `POST /api/auth/logout`
**Description**: Invalidate current session.
- **Response**: 200 OK `{ success: boolean }`

#### `GET /api/auth/me`
**Description**: Get current authenticated user info.
- **Response**: `{ id: string, name: string, role: string }`

### Notebooks

#### `GET /api/notebooks`
**Description**: List notebooks.
- **Query Params**: `?status=active|archived`
- **Response**: `Notebook[]`

#### `POST /api/notebooks`
**Description**: Create a new notebook.
- **Request Body**: `{ title: string, description: string }`
- **Response**: `Notebook`

#### `GET /api/notebooks/:id`
**Description**: Get single notebook.
- **Response**: `Notebook`

#### `PUT /api/notebooks/:id`
**Description**: Update notebook details.
- **Request Body**: `{ title?: string, description?: string }`
- **Response**: `Notebook`

#### `DELETE /api/notebooks/:id`
**Description**: Archive a notebook.
- **Response**: 200 OK `{ success: boolean }`

### Cohort Configuration

#### `GET /api/cohort-categories`
**Description**: Returns categories for simulation wizard.
- **Response**: `CohortCategory[]`

### Simulation Runs

#### `POST /api/runs`
**Description**: Start new simulation.
- **Request Body**: `{ policyText: string, cohorts: Record<string, string[]> }`
- **Response**: `{ runId: string, status: 'loading' }`

#### `GET /api/runs/:runId/status`
**Description**: Polling for loading screen.
- **Response**: `{ stage: 'research' | 'simulation' | 'analysis' | 'complete', progress: number }`

#### `GET /api/runs/:runId/events`
**Description**: SSE stream for live progress.

#### `POST /api/runs/:runId/resume`
**Description**: Resume after human review checkpoint.
- **Request Body**: `{ feedback?: string, approved: boolean }`
- **Response**: 200 OK

#### `GET /api/runs/:runId/summary`
**Description**: Executive summary.
- **Response**: `{ sections: SummarySection[], metrics: DashboardMetric[] }`

#### `GET /api/runs/:runId/dashboard`
**Description**: Chart data.
- **Response**: `{ income: IncomeChartDataPoint[], costOfLiving: CostOfLivingDataPoint[], jobs: JobsDataPoint[] }`

#### `GET /api/runs/:runId/groups`
**Description**: Cohort group impacts.
- **Response**: `CohortGroup[]`

#### `GET /api/runs/:runId/map`
**Description**: State-level geographic data.
- **Response**: `StateData[]`

#### `GET /api/runs/:runId/ripple`
**Description**: Ripple graph nodes + edges.
- **Response**: `{ nodes: RippleNode[], edges: RippleEdge[] }`

#### `GET /api/runs/:runId/timeline`
**Description**: 12-month temporal evolution data.
- **Response**: `TimelineDataPoint[]`

#### `GET /api/runs/:runId/cube`
**Description**: Precomputed data cube.
- **Response**: `any` (Cube structure)

#### `GET /api/runs/:runId/report`
**Description**: AI-written report.
- **Response**: `{ markdown: string }`

#### `POST /api/runs/:runId/chat`
**Description**: Ask AI about the simulation.
- **Request Body**: `{ message: string }`
- **Response**: `{ reply: string }`

### Comparison

#### `POST /api/compare`
**Description**: Compare multiple run scenarios.
- **Request Body**: `{ runIds: string[] }`
- **Response**: `{ comparison: any }`

### Export

#### `GET /api/runs/:runId/export/:format`
**Description**: Export data.
- **Params**: `format` (pdf/csv/pptx)
- **Response**: Binary file stream.
