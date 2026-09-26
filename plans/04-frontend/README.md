# LegiSim Frontend Architecture & Implementation Plan

## 1. Overview
The LegiSim frontend will be built upon the existing high-fidelity prototype located at `/mnt/Data/competitions/incub8/legisim/prototype/`. The core strategy is to **keep the exact same UI and user experience** while replacing hardcoded mock data with robust, production-ready data fetching and state management layers.

### Tech Stack Additions & Upgrades
- **Framework**: Next.js 14 (App Router) - *Retained from prototype*
- **Language**: TypeScript - *Retained*
- **Styling**: Tailwind CSS & framer-motion - *Retained*
- **Data Fetching (NEW)**: TanStack Query (React Query) v5 for server state, caching, and SSE integration.
- **Global State (NEW)**: Zustand for client-side state (filtering, time-slider synchronization, layout state).
- **Component Library (NEW)**: shadcn/ui for accessible, unstyled baseline components (replacing ad-hoc UI where necessary, though prioritizing existing prototype styles).
- **Visualizations (UPGRADED)**: 
  - **Charts**: Apache ECharts (replacing Recharts) for complex, high-performance data visualizations.
  - **Maps**: MapLibre GL + deck.gl (replacing the grid cartogram) for actual geographic plotting of India.
  - **Graphs**: @xyflow/react (React Flow) - *Retained and expanded for Ripple effects*.

## 2. Implementation Strategy

Our approach is a "Ship of Theseus" migration from the prototype:
1. **API Integration First**: Introduce TanStack Query hooks to fetch data. Swap out `import { mockSummary } from '@/data/mock'` with `const { data } = useRunSummary(runId)`.
2. **State Management**: Introduce Zustand for cross-tab state synchronization (e.g., changing the time step on the Timeline tab updates the state available to the Map tab).
3. **Visualization Swaps**: Progressively swap Recharts components with a universal `EChartWrapper` component capable of rendering the AI-generated `chart_spec`.

## 3. Subagent Assignment
To execute this implementation, the following subagents should be utilized:
- `ui-builder`: Primary implementer for TanStack Query hooks, Zustand stores, and complex ECharts/deck.gl components.
- `opencode`: For boilerplate code generation and replacing mock imports across the numerous page files.
- `animation-specialist`: To ensure framer-motion transitions and layout animations from the prototype are preserved during the React component refactoring.

## 4. Directory Structure for Plans
Please refer to the subsequent planning documents for detailed, step-by-step implementation instructions:
- [01-api-integration/plan.md](./01-api-integration/plan.md): Data fetching, SSE, mutations.
- [02-state-management/plan.md](./02-state-management/plan.md): Zustand setup, data cube slicing, URL sync.
- [03-visualization/plan.md](./03-visualization/plan.md): ECharts, MapLibre GL, and React Flow configs.
