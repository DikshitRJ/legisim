"use client";

import { useEffect } from "react";
import { usePathname, useRouter, useSearchParams } from "next/navigation";
import { useSimulationStore } from "@/store/useSimulationStore";

const readList = (value: string | null): string[] =>
  value ? value.split(",").map((item) => item.trim()).filter(Boolean) : [];

const sameList = (left: string[], right: string[]) =>
  left.length === right.length && left.every((value, index) => value === right[index]);

/** Keeps shareable run-view filters in the URL without filling browser history. */
export function useSyncStateToUrl(): void {
  const router = useRouter();
  const pathname = usePathname();
  const searchParams = useSearchParams();
  const currentTimeStep = useSimulationStore((state) => state.currentTimeStep);
  const activeRegions = useSimulationStore((state) => state.activeRegions);
  const activeCohorts = useSimulationStore((state) => state.activeCohorts);
  const compareRunId = useSimulationStore((state) => state.compareRunId);
  const setTimeStep = useSimulationStore((state) => state.setTimeStep);
  const toggleRegion = useSimulationStore((state) => state.toggleRegion);
  const toggleCohort = useSimulationStore((state) => state.toggleCohort);
  const setCompareRunId = useSimulationStore((state) => state.setCompareRunId);

  useEffect(() => {
    const parsedTime = Number.parseInt(searchParams.get("t") ?? "0", 10);
    if (Number.isFinite(parsedTime) && Math.max(0, parsedTime) !== currentTimeStep) setTimeStep(parsedTime);

    const urlRegions = readList(searchParams.get("regions"));
    activeRegions.filter((id) => !urlRegions.includes(id)).forEach(toggleRegion);
    urlRegions.filter((id) => !activeRegions.includes(id)).forEach(toggleRegion);

    const urlCohorts = readList(searchParams.get("cohorts"));
    activeCohorts.filter((id) => !urlCohorts.includes(id)).forEach(toggleCohort);
    urlCohorts.filter((id) => !activeCohorts.includes(id)).forEach(toggleCohort);

    const urlCompare = searchParams.get("compare");
    if (urlCompare !== compareRunId) setCompareRunId(urlCompare);
  }, [activeCohorts, activeRegions, compareRunId, currentTimeStep, searchParams, setCompareRunId, setTimeStep, toggleCohort, toggleRegion]);

  useEffect(() => {
    const next = new URLSearchParams(searchParams.toString());
    const assign = (key: string, value: string | null) => {
      if (value) next.set(key, value);
      else next.delete(key);
    };
    assign("t", currentTimeStep ? String(currentTimeStep) : null);
    assign("regions", activeRegions.length ? activeRegions.join(",") : null);
    assign("cohorts", activeCohorts.length ? activeCohorts.join(",") : null);
    assign("compare", compareRunId);

    const nextQuery = next.toString();
    if (nextQuery !== searchParams.toString()) router.replace(nextQuery ? `${pathname}?${nextQuery}` : pathname, { scroll: false });
  }, [activeCohorts, activeRegions, compareRunId, currentTimeStep, pathname, router, searchParams]);
}

export { sameList };
