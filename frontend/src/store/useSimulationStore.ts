import { create } from "zustand";
import { persist } from "zustand/middleware";

export interface SimulationState {
  activeRunId: string | null;
  currentTimeStep: number;
  activeRegions: string[];
  activeCohorts: string[];
  compareRunId: string | null;
  selectedRippleNodeId: string | null;
  setActiveRunId: (runId: string | null) => void;
  setTimeStep: (timeStep: number) => void;
  toggleRegion: (regionId: string) => void;
  toggleCohort: (cohortId: string) => void;
  setCompareRunId: (runId: string | null) => void;
  setSelectedRippleNodeId: (nodeId: string | null) => void;
  resetRunView: () => void;
}

const toggle = (items: string[], item: string): string[] =>
  items.includes(item) ? items.filter((value) => value !== item) : [...items, item];

const runViewDefaults = {
  currentTimeStep: 0,
  activeRegions: [] as string[],
  activeCohorts: [] as string[],
  compareRunId: null,
  selectedRippleNodeId: null,
};

/**
 * View-only state that should survive navigation but never substitutes for API
 * data. Persisting it makes a copied results link reopen with familiar filters.
 */
export const useSimulationStore = create<SimulationState>()(
  persist(
    (set) => ({
      activeRunId: null,
      ...runViewDefaults,
      setActiveRunId: (activeRunId) =>
        set((state) =>
          state.activeRunId === activeRunId
            ? { activeRunId }
            : { activeRunId, ...runViewDefaults },
        ),
      setTimeStep: (currentTimeStep) => set({ currentTimeStep: Math.max(0, Math.floor(currentTimeStep)) }),
      toggleRegion: (regionId) => set((state) => ({ activeRegions: toggle(state.activeRegions, regionId) })),
      toggleCohort: (cohortId) => set((state) => ({ activeCohorts: toggle(state.activeCohorts, cohortId) })),
      setCompareRunId: (compareRunId) => set({ compareRunId }),
      setSelectedRippleNodeId: (selectedRippleNodeId) => set({ selectedRippleNodeId }),
      resetRunView: () => set(runViewDefaults),
    }),
    {
      name: "legisim.simulation-view.v1",
      partialize: (state) => ({
        activeRunId: state.activeRunId,
        ...runViewDefaults,
        currentTimeStep: state.currentTimeStep,
        activeRegions: state.activeRegions,
        activeCohorts: state.activeCohorts,
        compareRunId: state.compareRunId,
      }),
    },
  ),
);
