import type { Confidence, NormalizedConfidence, ProgressEvent, RippleGraph, RippleNode, RunStatus } from "./types";

const CONFIDENCE_BY_LOWER_CASE: Record<string, NormalizedConfidence> = {
  high: "high",
  medium: "medium",
  low: "low",
};

export function normalizeConfidence(confidence: Confidence | NormalizedConfidence): NormalizedConfidence {
  const value = CONFIDENCE_BY_LOWER_CASE[String(confidence).toLowerCase()];
  if (!value) throw new Error(`Unsupported confidence value: ${String(confidence)}`);
  return value;
}

/** Unifies the conflicting ripple confidence enums in runs and ripple specs. */
export function normalizeRippleGraph(graph: RippleGraph): RippleGraph {
  return {
    ...graph,
    nodes: graph.nodes.map((node: RippleNode) => ({
      ...node,
      confidence: normalizeConfidence(node.confidence),
    })),
  };
}

export function parseProgressEvent(raw: string): ProgressEvent {
  try {
    const value: unknown = JSON.parse(raw);
    if (!value || typeof value !== "object") return { message: raw };
    const data = value as Record<string, unknown>;
    const progressCandidate = data.progress ?? data.percent;
    const progress = typeof progressCandidate === "number" ? clampProgress(progressCandidate) : undefined;
    const stageCandidate = data.stage ?? data.status;
    const stage = isRunStage(stageCandidate) ? stageCandidate : undefined;
    const messageCandidate = data.message ?? data.detail ?? data.text;
    return { progress, stage, message: typeof messageCandidate === "string" ? messageCandidate : undefined };
  } catch {
    // The stream schema is intentionally unspecified in the OpenAPI document.
    return { message: raw };
  }
}

export function isRunStage(value: unknown): value is RunStatus["stage"] {
  return value === "research" || value === "simulation" || value === "analysis" || value === "complete";
}

export function clampProgress(progress: number): number {
  return Math.max(0, Math.min(100, progress));
}
