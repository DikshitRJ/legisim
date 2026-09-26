/**
 * API models derived from docs/specs openapi.yaml. Keep wire names intact
 * here; presentation-specific transformations belong in adapters.ts.
 */

export type NotebookStatus = "active" | "archived";

export interface Notebook {
  id: string;
  title: string;
  description: string;
  sources: number;
  modifiedAt: string;
  status: NotebookStatus;
}

export interface NotebookCreate {
  title: string;
  description: string;
}

export interface NotebookUpdate {
  title?: string;
  description?: string;
}

export interface SuccessResponse {
  success: boolean;
}

export interface LoginRequest {
  officerId: string;
  password: string;
}

export interface OfficerProfile {
  id: string;
  name: string;
  role: string;
}

export interface LoginResponse {
  token: string;
  user: OfficerProfile;
}

export interface CohortCategory {
  id: string;
  number: string;
  title: string;
  options: string[];
}

export interface PersonaDemographics {
  age: string;
  income: string;
  location: string;
  education?: string;
  occupation?: string;
  region?: string;
}

export interface Persona {
  id: string;
  demographics: PersonaDemographics;
  assets_and_vulnerabilities: string[];
  economic_dependency: string[];
}

export interface PolicyInput {
  what_changes: string;
  size_of_change: string;
  change_type: string;
  target_group: string;
  geographic_coverage: string;
  start_date?: string;
  rollout_phases?: string[];
}

export interface TargetingProfile {
  policy_id: string;
  summary: string;
  direct_impact_criteria: string;
  indirect_impact_criteria: string;
  geographic_focus: string;
  economic_channels?: string[];
}

export interface JEVPersonaScore {
  id: string;
  score: number;
  relevant: boolean;
}

export interface JEVSelectionResult {
  policy_id: string;
  threshold: number;
  total_evaluated: number;
  total_selected: number;
  results: JEVPersonaScore[];
  execution_time_ms: number;
}

export interface RunStartRequest {
  policyText?: string;
  cohorts?: Record<string, string[]>;
}

export interface RunStartResponse {
  runId: string;
  status: "loading";
}

export type RunStage = "research" | "simulation" | "analysis" | "complete";

export interface RunStatus {
  stage: RunStage;
  progress: number;
}

export type Confidence = "High" | "Medium" | "Low";
export type NormalizedConfidence = Lowercase<Confidence>;
export type EvidenceKind = "measured" | "modelled" | "judged";

export interface SummarySection {
  title: string;
  content: string;
  confidence: Confidence;
  kind: EvidenceKind;
}

export interface DashboardMetric {
  label: string;
  value: string;
  range: string;
  direction: "positive" | "negative";
  kind: EvidenceKind;
}

export interface RunSummary {
  sections: SummarySection[];
  metrics: DashboardMetric[];
}

export interface IncomeChartDataPoint {
  group: string;
  change: number;
  low: number;
  high: number;
}

export interface CostOfLivingDataPoint {
  category: string;
  change: number;
}

export interface JobsDataPoint {
  sector: string;
  change: number;
  percentage: number;
}

export interface RunDashboard {
  income: IncomeChartDataPoint[];
  costOfLiving: CostOfLivingDataPoint[];
  jobs: JobsDataPoint[];
}

export interface CohortGroup {
  id: string;
  name: string;
  population: string;
  description: string;
  stance: { support: number; neutral: number; oppose: number };
  incomeChange: number;
  behaviors: string[];
  confidence: Confidence;
}

export interface StateData {
  code: string;
  name: string;
  incomeChange: number;
  inflationImpact: number;
  acceptance: number;
  jobsAffected: number;
}

/** The ripple OpenAPI documents conflict on confidence casing. */
export interface RippleNode {
  id: string;
  label: string;
  layer: number;
  domain: string;
  magnitude: string;
  confidence: Confidence | NormalizedConfidence;
  kind: EvidenceKind;
}

export interface RippleEdge {
  id: string;
  source: string;
  target: string;
  strength: number;
  lagMonths: number;
  mechanism: string;
}

export interface RippleGraph {
  nodes: RippleNode[];
  edges: RippleEdge[];
}

export interface TimelineDataPoint {
  month: number;
  label: string;
  incomeChange: number;
  inflationImpact: number;
  acceptance: number;
  employment: number;
}

export interface RunReport {
  markdown?: string;
}

export interface ChatRequest {
  message?: string;
}

export interface ChatResponse {
  reply?: string;
}

export interface ResumeRunRequest {
  approved: boolean;
  feedback?: string;
}

export interface CompareRequest {
  runIds?: string[];
}

export interface CompareResponse {
  comparison?: Record<string, unknown>;
}

/** The API deliberately leaves the cube response schema unspecified. */
export type RunCube = Record<string, unknown>;
export type ExportFormat = "pdf" | "csv" | "pptx";

export interface ProgressEvent extends Partial<RunStatus> {
  message?: string;
}
