import { download, request } from "./client";
import { normalizeRippleGraph } from "./adapters";
import type {
  ChatRequest,
  ChatResponse,
  CohortCategory,
  CompareRequest,
  CompareResponse,
  ExportFormat,
  JEVSelectionResult,
  LoginRequest,
  LoginResponse,
  Notebook,
  NotebookCreate,
  NotebookStatus,
  NotebookUpdate,
  Persona,
  PolicyInput,
  ResumeRunRequest,
  RippleGraph,
  RunCube,
  RunDashboard,
  RunReport,
  RunStartRequest,
  RunStartResponse,
  RunStatus,
  RunSummary,
  StateData,
  SuccessResponse,
  TargetingProfile,
  TimelineDataPoint,
  CohortGroup,
} from "./types";

const encoded = (value: string) => encodeURIComponent(value);

export const api = {
  auth: {
    login: async (payload: LoginRequest) => request<LoginResponse>("/api/auth/login", { method: "POST", body: payload, authenticated: false }),
    logout: () => request<SuccessResponse>("/api/auth/logout", { method: "POST" }),
    me: () => request<LoginResponse["user"]>("/api/auth/me"),
  },
  notebooks: {
    list: (status?: NotebookStatus) => request<Notebook[]>(`/api/notebooks${status ? `?status=${status}` : ""}`),
    get: (id: string) => request<Notebook>(`/api/notebooks/${encoded(id)}`),
    create: (payload: NotebookCreate) => request<Notebook>("/api/notebooks", { method: "POST", body: payload }),
    update: (id: string, payload: NotebookUpdate) => request<Notebook>(`/api/notebooks/${encoded(id)}`, { method: "PUT", body: payload }),
    archive: (id: string) => request<SuccessResponse>(`/api/notebooks/${encoded(id)}`, { method: "DELETE" }),
  },
  cohorts: {
    categories: () => request<CohortCategory[]>("/api/cohort-categories"),
    personas: () => request<Persona[]>("/api/cohorts/personas"),
    targetingProfile: (payload: PolicyInput) => request<TargetingProfile>("/api/cohorts/jev/targeting-profile", { method: "POST", body: payload }),
    select: (payload: { policy_id?: string; targeting_profile?: TargetingProfile; threshold?: number }) =>
      request<JEVSelectionResult>("/api/cohorts/jev/select", { method: "POST", body: payload }),
  },
  runs: {
    create: (payload: RunStartRequest) => request<RunStartResponse>("/api/runs", { method: "POST", body: payload }),
    status: (runId: string) => request<RunStatus>(`/api/runs/${encoded(runId)}/status`),
    resume: (runId: string, payload: ResumeRunRequest) => request<void>(`/api/runs/${encoded(runId)}/resume`, { method: "POST", body: payload }),
    summary: (runId: string) => request<RunSummary>(`/api/runs/${encoded(runId)}/summary`),
    dashboard: (runId: string) => request<RunDashboard>(`/api/runs/${encoded(runId)}/dashboard`),
    groups: (runId: string) => request<CohortGroup[]>(`/api/runs/${encoded(runId)}/groups`),
    map: (runId: string) => request<StateData[]>(`/api/runs/${encoded(runId)}/map`),
    ripple: async (runId: string) => normalizeRippleGraph(await request<RippleGraph>(`/api/runs/${encoded(runId)}/ripple`)),
    timeline: (runId: string) => request<TimelineDataPoint[]>(`/api/runs/${encoded(runId)}/timeline`),
    cube: (runId: string) => request<RunCube>(`/api/runs/${encoded(runId)}/cube`),
    report: (runId: string) => request<RunReport>(`/api/runs/${encoded(runId)}/report`),
    chat: (runId: string, payload: ChatRequest) => request<ChatResponse>(`/api/runs/${encoded(runId)}/chat`, { method: "POST", body: payload }),
    export: (runId: string, format: ExportFormat) => download(`/api/runs/${encoded(runId)}/export/${format}`, format),
  },
  compare: (payload: CompareRequest) => request<CompareResponse>("/api/compare", { method: "POST", body: payload }),
};

export * from "./adapters";
export * from "./client";
export * from "./query-keys";
export * from "./types";
