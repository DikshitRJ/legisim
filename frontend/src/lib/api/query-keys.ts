export const queryKeys = {
  auth: {
    me: ["auth", "me"] as const,
  },
  notebooks: {
    all: ["notebooks"] as const,
    list: (status?: "active" | "archived") => ["notebooks", "list", status ?? "all"] as const,
    detail: (id: string) => ["notebooks", "detail", id] as const,
  },
  cohorts: {
    categories: ["cohorts", "categories"] as const,
    personas: ["cohorts", "personas"] as const,
  },
  runs: {
    root: (runId: string) => ["runs", runId] as const,
    status: (runId: string) => ["runs", runId, "status"] as const,
    summary: (runId: string) => ["runs", runId, "summary"] as const,
    dashboard: (runId: string) => ["runs", runId, "dashboard"] as const,
    groups: (runId: string) => ["runs", runId, "groups"] as const,
    map: (runId: string) => ["runs", runId, "map"] as const,
    ripple: (runId: string) => ["runs", runId, "ripple"] as const,
    timeline: (runId: string) => ["runs", runId, "timeline"] as const,
    cube: (runId: string) => ["runs", runId, "cube"] as const,
    report: (runId: string) => ["runs", runId, "report"] as const,
  },
  compare: (runIds: readonly string[]) => ["compare", ...runIds] as const,
};
