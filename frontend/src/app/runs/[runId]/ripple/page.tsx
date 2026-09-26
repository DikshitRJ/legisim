'use client';

import React from 'react';
import { RippleExplorer } from '@/components/flow/RippleExplorer';
import { useRunRipple } from '@/hooks/useQueries';

export default function RipplePage({ params }: { params: { runId: string } }) {
  const { data: graph, isLoading, error } = useRunRipple(params.runId);

  return (
    <div className="w-full h-[calc(100vh-160px)] bg-canvas relative">
      <div className="absolute top-4 left-6 z-10 bg-surface-2/80 backdrop-blur border border-surface-3 px-4 py-2 rounded-lg">
        <h2 className="text-white font-medium text-sm">Cause-Effect Ripple</h2>
        <p className="text-xs text-text-muted">Trace the cascading impacts of the policy</p>
      </div>
      
      {isLoading ? (
        <div className="flex h-full items-center justify-center">
          <div className="animate-pulse flex flex-col items-center">
            <div className="h-12 w-12 rounded-full border-t-2 border-saffron animate-spin"></div>
            <p className="mt-4 text-text-muted text-sm">Tracing ripple effects...</p>
          </div>
        </div>
      ) : error ? (
        <div className="flex h-full items-center justify-center">
          <div className="text-red-400">Failed to load ripple graph</div>
        </div>
      ) : (
        <RippleExplorer graph={graph} />
      )}
    </div>
  );
}
