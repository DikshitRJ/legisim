# State Management Plan

## 1. Overview
We will use Zustand for client-side state management, specifically for handling the global simulation state, filtering, and cross-tab data slicing. This allows the user to change the "Time Step" on the timeline tab, and have that same time step reflected instantly when switching to the Map tab.

### Recommended Subagents
- `ui-builder`: To implement Zustand stores and update React components to consume them.

## 2. Zustand Store Implementation

### 2.1 Simulation Store (`/src/store/useSimulationStore.ts`)
This store tracks the current view parameters across the run dashboard.

```typescript
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface SimulationState {
  // Global context
  activeRunId: string | null;
  setActiveRunId: (id: string) => void;
  
  // Data Slicing (The Data Cube)
  currentTimeStep: number;
  setTimeStep: (step: number) => void;
  
  // Filters
  activeRegions: string[];
  toggleRegion: (regionId: string) => void;
  
  activeCohorts: string[];
  toggleCohort: (cohortId: string) => void;
  
  // Scenario Comparison mode
  compareRunId: string | null;
  setCompareRunId: (id: string | null) => void;
}

export const useSimulationStore = create<SimulationState>()(
  persist(
    (set) => ({
      activeRunId: null,
      setActiveRunId: (id) => set({ activeRunId: id }),
      
      currentTimeStep: 0, // 0 = Baseline/Current
      setTimeStep: (step) => set({ currentTimeStep: step }),
      
      activeRegions: [],
      toggleRegion: (regionId) => set((state) => ({
        activeRegions: state.activeRegions.includes(regionId) 
          ? state.activeRegions.filter(r => r !== regionId)
          : [...state.activeRegions, regionId]
      })),
      
      activeCohorts: [],
      toggleCohort: (cohortId) => set((state) => ({
        activeCohorts: state.activeCohorts.includes(cohortId)
          ? state.activeCohorts.filter(c => c !== cohortId)
          : [...state.activeCohorts, cohortId]
      })),
      
      compareRunId: null,
      setCompareRunId: (id) => set({ compareRunId: id })
    }),
    { name: 'legisim-sim-storage' }
  )
);
```

## 3. URL Parameter Synchronization
To ensure charts and specific states are shareable, we must sync the Zustand store with URL parameters using `next/navigation`.

Create a hook `/src/hooks/useSyncStateToUrl.ts`:

```typescript
import { useEffect } from 'react';
import { useRouter, useSearchParams, usePathname } from 'next/navigation';
import { useSimulationStore } from '@/store/useSimulationStore';

export function useSyncStateToUrl() {
  const router = useRouter();
  const pathname = usePathname();
  const searchParams = useSearchParams();
  
  const { currentTimeStep, setTimeStep } = useSimulationStore();

  // On mount/URL change, sync URL to store
  useEffect(() => {
    const t = searchParams.get('t');
    if (t) setTimeStep(parseInt(t, 10));
  }, [searchParams, setTimeStep]);

  // On store change, sync store to URL (debounced or on blur)
  useEffect(() => {
    const params = new URLSearchParams(searchParams.toString());
    if (currentTimeStep !== 0) {
      params.set('t', currentTimeStep.toString());
    } else {
      params.delete('t');
    }
    
    // Use replace to avoid filling history
    router.replace(`${pathname}?${params.toString()}`);
  }, [currentTimeStep, pathname, router, searchParams]);
}
```

## 4. Layout-Level Data Fetching
To prevent refetching the main data cube when navigating between `/runs/[id]/dashboard` and `/runs/[id]/map`, fetch the foundational data in the shared layout: `/src/app/runs/[runId]/layout.tsx`. 

Since TanStack query caches the request, calling `useRunSummary(runId)` in the layout and in the child components will only result in a single network request, smoothly sharing the cache across tabs.

## 5. Acceptance Criteria
- Moving the timeline slider updates `currentTimeStep` in Zustand.
- Switching from the Time tab to the Map tab retains the selected time step.
- Copying the URL and opening in a new window retains the time step and active filters.
