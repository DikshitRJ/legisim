"use client";

import { useEffect, useRef, useState } from "react";
import { api, clampProgress, parseProgressEvent, runEventsUrl, type RunStage } from "@/lib/api";

export interface SimulationProgress {
  stage: RunStage | null;
  progress: number;
  message: string | null;
  isComplete: boolean;
  isStreaming: boolean;
  error: Error | null;
}

const initialProgress: SimulationProgress = {
  stage: null,
  progress: 0,
  message: null,
  isComplete: false,
  isStreaming: false,
  error: null,
};

/**
 * Reads SSE milestones where available and always maintains documented status
 * polling as a fallback. This keeps the loading screen usable when an SSE
 * deployment cannot authenticate native EventSource bearer requests.
 */
export function useSimulationProgress(runId: string | null | undefined): SimulationProgress {
  const [state, setState] = useState<SimulationProgress>(initialProgress);
  const sourceRef = useRef<EventSource | null>(null);

  useEffect(() => {
    if (!runId) {
      setState(initialProgress);
      return;
    }

    let active = true;
    let pollingTimer: ReturnType<typeof setInterval> | undefined;
    const closeSource = () => {
      sourceRef.current?.close();
      sourceRef.current = null;
    };
    const applyStatus = (stage: RunStage, progress: number, message?: string) => {
      if (!active) return;
      const isComplete = stage === "complete" || progress >= 100;
      setState((current) => ({
        ...current,
        stage,
        progress: clampProgress(progress),
        message: message ?? current.message,
        isComplete,
        error: null,
      }));
      if (isComplete) closeSource();
    };
    const poll = async () => {
      try {
        const status = await api.runs.status(runId);
        applyStatus(status.stage, status.progress);
      } catch (error) {
        if (active) {
          setState((current) => ({
            ...current,
            error: error instanceof Error ? error : new Error("Unable to retrieve simulation progress"),
          }));
        }
      }
    };

    void poll();
    pollingTimer = setInterval(() => void poll(), 5_000);

    try {
      const source = new EventSource(runEventsUrl(runId), { withCredentials: true });
      sourceRef.current = source;
      setState((current) => ({ ...current, isStreaming: true }));
      source.onmessage = (event) => {
        const eventProgress = parseProgressEvent(event.data);
        if (eventProgress.stage && eventProgress.progress !== undefined) {
          applyStatus(eventProgress.stage, eventProgress.progress, eventProgress.message);
        } else if (active && eventProgress.message) {
          setState((current) => ({ ...current, message: eventProgress.message ?? null }));
        }
      };
      source.onerror = () => {
        closeSource();
        if (active) setState((current) => ({ ...current, isStreaming: false }));
      };
    } catch {
      // Polling already started and remains the documented resilient path.
    }

    return () => {
      active = false;
      if (pollingTimer) clearInterval(pollingTimer);
      closeSource();
    };
  }, [runId]);

  return state;
}
