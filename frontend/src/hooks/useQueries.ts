"use client";

import { useQuery } from "@tanstack/react-query";
import { api, queryKeys, type NotebookStatus } from "@/lib/api";

const enabled = (value: string | null | undefined): value is string => Boolean(value);

export const useCurrentUser = () =>
  useQuery({ queryKey: queryKeys.auth.me, queryFn: api.auth.me, retry: false });

export const useNotebooks = (status?: NotebookStatus) =>
  useQuery({ queryKey: queryKeys.notebooks.list(status), queryFn: () => api.notebooks.list(status) });

export const useNotebook = (notebookId: string | null | undefined) =>
  useQuery({
    queryKey: queryKeys.notebooks.detail(notebookId ?? ""),
    queryFn: () => api.notebooks.get(notebookId!),
    enabled: enabled(notebookId),
  });

export const useCohortCategories = () =>
  useQuery({ queryKey: queryKeys.cohorts.categories, queryFn: api.cohorts.categories });

export const usePersonas = () =>
  useQuery({ queryKey: queryKeys.cohorts.personas, queryFn: api.cohorts.personas });

export const useRunStatus = (runId: string | null | undefined) =>
  useQuery({
    queryKey: queryKeys.runs.status(runId ?? ""),
    queryFn: () => api.runs.status(runId!),
    enabled: enabled(runId),
    refetchInterval: (query) => (query.state.data?.stage === "complete" ? false : 5_000),
  });

export const useRunSummary = (runId: string | null | undefined) =>
  useQuery({ queryKey: queryKeys.runs.summary(runId ?? ""), queryFn: () => api.runs.summary(runId!), enabled: enabled(runId) });

export const useRunDashboard = (runId: string | null | undefined) =>
  useQuery({ queryKey: queryKeys.runs.dashboard(runId ?? ""), queryFn: () => api.runs.dashboard(runId!), enabled: enabled(runId) });

export const useRunGroups = (runId: string | null | undefined) =>
  useQuery({ queryKey: queryKeys.runs.groups(runId ?? ""), queryFn: () => api.runs.groups(runId!), enabled: enabled(runId) });

export const useRunMap = (runId: string | null | undefined) =>
  useQuery({ queryKey: queryKeys.runs.map(runId ?? ""), queryFn: () => api.runs.map(runId!), enabled: enabled(runId) });

export const useRunRipple = (runId: string | null | undefined) =>
  useQuery({ queryKey: queryKeys.runs.ripple(runId ?? ""), queryFn: () => api.runs.ripple(runId!), enabled: enabled(runId) });

export const useRunTimeline = (runId: string | null | undefined) =>
  useQuery({ queryKey: queryKeys.runs.timeline(runId ?? ""), queryFn: () => api.runs.timeline(runId!), enabled: enabled(runId) });

export const useRunCube = (runId: string | null | undefined) =>
  useQuery({ queryKey: queryKeys.runs.cube(runId ?? ""), queryFn: () => api.runs.cube(runId!), enabled: enabled(runId) });

export const useRunReport = (runId: string | null | undefined) =>
  useQuery({ queryKey: queryKeys.runs.report(runId ?? ""), queryFn: () => api.runs.report(runId!), enabled: enabled(runId) });
