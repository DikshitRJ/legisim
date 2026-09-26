'use client';

import React from 'react';
import { useParams } from 'next/navigation';
import { ArrowUpRight, ArrowDownRight, Info, ShieldAlert } from 'lucide-react';
import { useRunSummary } from '@/hooks/useQueries';

export default function SummaryPage() {
  const { runId } = useParams<{ runId: string }>();
  const { data: summary, isLoading, isError } = useRunSummary(runId);

  if (isLoading) {
    return <div className="p-6 max-w-7xl mx-auto flex items-center justify-center text-text-muted">Loading summary...</div>;
  }

  if (isError || !summary) {
    return <div className="p-6 max-w-7xl mx-auto flex items-center justify-center text-red-500">Failed to load summary.</div>;
  }

  return (
    <div className="p-6 max-w-7xl mx-auto flex gap-6 flex-col lg:flex-row">
      <div className="flex-1 flex flex-col gap-6">
        <div className="bg-surface-2 rounded-xl p-6 border border-surface-3">
          <div className="flex justify-between items-start mb-4">
            <div>
              <h1 className="text-2xl font-bold text-white mb-2">Policy Simulation Summary</h1>
              <p className="text-text-secondary">Simulated impact over 12 months with immediate implementation and no compensatory policies.</p>
            </div>
          </div>
        </div>

        <div className="flex flex-col gap-4">
          <h2 className="text-lg font-semibold text-white px-1">Key AI Findings</h2>
          {summary.sections.map((insight, i) => (
            <details key={i} className="group bg-surface-4 rounded-xl p-6 border border-surface-3 transition-colors hover:border-surface-3/80 cursor-pointer">
              <summary className="font-semibold text-white text-lg list-none flex justify-between items-center outline-none">
                {insight.title}
                <span className="text-saffron group-open:rotate-180 transition-transform">▼</span>
              </summary>
              <div className="mt-3">
                <p className="text-sm text-text-body leading-relaxed">{insight.content}</p>
                <div className="flex items-center justify-between mt-4 pt-4 border-t border-surface-3">
                  <div className="flex items-center gap-3">
                    <span className={`px-2 py-0.5 rounded text-xs font-medium uppercase tracking-wider ${
                      insight.confidence === 'High' ? 'bg-india-green/20 text-india-green' : 
                      insight.confidence === 'Medium' ? 'bg-amber-500/20 text-amber-500' : 
                      'bg-red-500/20 text-red-500'
                    }`}>
                      {insight.confidence} Confidence
                    </span>
                    <span className={`px-2 py-0.5 rounded text-xs font-medium uppercase tracking-wider ${
                      insight.kind === 'measured' ? 'bg-accent-blue/20 text-accent-blue' :
                      insight.kind === 'modelled' ? 'bg-purple-500/20 text-purple-500' :
                      'bg-saffron/20 text-saffron'
                    }`}>
                      {insight.kind}
                    </span>
                  </div>
                </div>
              </div>
            </details>
          ))}
        </div>
      </div>

      <div className="w-full lg:w-80 flex flex-col gap-6 shrink-0">
        <h2 className="text-lg font-semibold text-white px-1">Macro Indicators</h2>
        <div className="grid grid-cols-2 lg:grid-cols-1 gap-4">
          {summary.metrics.map((m, i) => {
            const isMeasured = m.kind === 'measured';
            const isModelled = m.kind === 'modelled';
            const isJudged = m.kind === 'judged';
            const borderStyle = isMeasured ? 'border-solid' : isModelled ? 'border-dashed' : 'border-dotted';
            
            return (
              <div key={i} className={`bg-surface-2 rounded-xl p-5 border border-surface-3 flex flex-col gap-1 ${borderStyle}`}>
                <div className="flex justify-between items-start">
                  <span className="text-xs font-medium text-text-secondary uppercase tracking-wider">{m.label}</span>
                  <span className={`text-[10px] font-medium uppercase tracking-wider ${
                    isMeasured ? 'text-accent-blue' : isModelled ? 'text-purple-500' : 'text-saffron'
                  }`}>{m.kind}</span>
                </div>
                <div className="flex items-baseline gap-2 mt-1">
                  <span className="text-2xl font-bold text-white">
                    {m.value}
                  </span>
                  {m.direction === 'positive' ? 
                    <ArrowUpRight className="w-4 h-4 text-india-green" /> : 
                    <ArrowDownRight className="w-4 h-4 text-red-500" />
                  }
                </div>
                <span className="text-xs text-text-muted mt-2 font-mono">{m.range}</span>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
