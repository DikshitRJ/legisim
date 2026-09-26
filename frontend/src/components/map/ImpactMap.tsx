'use client';

import React, { useMemo, useState } from 'react';

import type { StateData } from '@/lib/api/types';

type Metric = 'incomeChange' | 'inflationImpact' | 'acceptance' | 'jobsAffected';

const grid: Array<Array<string | null>> = [
  [null, null, 'JK', null, null, null, null, null],
  ['PB', 'HR', 'UK', null, 'AR', null, null, null],
  ['RJ', 'UP', 'DL', null, 'AS', 'NL', null, null],
  ['GJ', 'MP', 'JH', 'WB', 'ML', 'MN', 'MZ', null],
  [null, 'MH', 'CG', 'OD', 'TR', null, null, null],
  ['GA', 'KA', 'TS', 'AP', null, null, null, null],
  [null, 'KL', 'TN', null, null, null, null, null],
];

const metricLabels: Record<Metric, string> = {
  incomeChange: 'Income change',
  inflationImpact: 'Inflation impact',
  acceptance: 'Public acceptance',
  jobsAffected: 'Jobs affected',
};

function colorFor(value: number, metric: Metric) {
  const intensity = metric === 'incomeChange'
    ? Math.min(Math.abs(Math.min(value, 0)) / 10, 1)
    : metric === 'inflationImpact'
      ? Math.min(Math.max(value, 0) / 1.5, 1)
      : metric === 'jobsAffected'
        ? Math.min(Math.abs(value) / 500000, 1)
        : Math.min(Math.max(value, 0) / 100, 1);
  if (metric === 'acceptance') return `rgba(4, 106, 56, ${0.2 + intensity * 0.75})`;
  return `rgba(220, 38, 38, ${0.15 + intensity * 0.78})`;
}

function formatValue(data: StateData, metric: Metric) {
  const value = data[metric];
  if (metric === 'jobsAffected') return new Intl.NumberFormat('en-IN', { notation: 'compact', maximumFractionDigits: 1 }).format(value);
  if (metric === 'inflationImpact') return `${value >= 0 ? '+' : ''}${value.toFixed(1)} pp`;
  return `${value >= 0 && metric !== 'acceptance' ? '+' : ''}${value.toFixed(1)}%`;
}

export function ImpactMap({ data }: { data?: StateData[] }) {
  const [metric, setMetric] = useState<Metric>('incomeChange');
  const [selectedCode, setSelectedCode] = useState<string | null>(null);
  const [hoveredCode, setHoveredCode] = useState<string | null>(null);
  const states = useMemo(() => new Map((data ?? []).map((state) => [state.code.toUpperCase(), state])), [data]);
  const selected = selectedCode ? states.get(selectedCode) : undefined;
  const hovered = hoveredCode ? states.get(hoveredCode) : undefined;

  if (!data?.length) return <div className="flex min-h-[480px] items-center justify-center rounded-lg border border-surface-3 bg-surface-2 text-sm text-text-muted">No regional impact data is available for this run.</div>;

  return (
    <section className="rounded-lg border border-surface-3 bg-surface-2 p-5">
      <div className="flex flex-col gap-4 border-b border-surface-3 pb-4 lg:flex-row lg:items-start lg:justify-between">
        <div>
          <h1 className="text-base font-semibold text-white">Geographic impact</h1>
          <p className="mt-1 text-xs leading-5 text-text-muted">State-level comparison. Select a state for the complete run output.</p>
        </div>
        <div className="relative">
          <select
            value={metric}
            onChange={(e) => setMetric(e.target.value as Metric)}
            className="appearance-none bg-surface-1 border border-surface-3 text-white text-sm rounded px-3 py-2 pr-8 focus:outline-none focus:ring-2 focus:ring-saffron cursor-pointer"
            aria-label="Map metric"
          >
            {(Object.keys(metricLabels) as Metric[]).map((key) => (
              <option key={key} value={key}>
                {metricLabels[key]}
              </option>
            ))}
          </select>
          <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-text-muted">
            <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7" /></svg>
          </div>
        </div>
      </div>
      <div className="grid gap-6 py-6 lg:grid-cols-[minmax(0,1fr)_260px]">
        <div className="overflow-x-auto pb-2">
          <div className="mx-auto grid min-w-[600px] max-w-3xl grid-cols-8 gap-1.5" role="list" aria-label={`Indian states by ${metricLabels[metric].toLowerCase()}`}>
            {grid.flatMap((row, rowIndex) => row.map((code, columnIndex) => {
              const state = code ? states.get(code) : undefined;
              if (!code) return <div aria-hidden="true" className="aspect-square" key={`${rowIndex}-${columnIndex}`} />;
              if (!state) return <div className="aspect-square rounded border border-dashed border-surface-3 bg-surface-1" key={code} title={`${code}: no data`} />;
              const chosen = selectedCode === code;
              const isHovered = hoveredCode === code;
              return (
                <div key={code} className="relative z-0" onMouseEnter={() => setHoveredCode(code)} onMouseLeave={() => setHoveredCode(null)}>
                  <button
                    aria-label={`${state.name}, ${metricLabels[metric]} ${formatValue(state, metric)}`}
                    aria-pressed={chosen}
                    className={`h-full w-full aspect-square rounded border p-1 text-center shadow-sm transition hover:-translate-y-0.5 hover:brightness-125 focus:outline-none focus:ring-2 focus:ring-saffron ${chosen ? 'border-white ring-2 ring-saffron' : 'border-white/15'}`}
                    onClick={() => setSelectedCode(code)}
                    style={{ backgroundColor: colorFor(state[metric], metric) }}
                    type="button"
                  >
                    <span className="block text-sm font-bold text-white drop-shadow">{code}</span>
                    <span className="mt-1 block text-[10px] text-white/90 drop-shadow">{formatValue(state, metric)}</span>
                  </button>
                  {isHovered && (
                    <div className="absolute left-1/2 top-full z-50 mt-2 w-48 -translate-x-1/2 rounded-lg border border-surface-3 bg-surface-1 p-3 shadow-xl pointer-events-none">
                      <div className="mb-2 border-b border-surface-3 pb-1 font-bold text-white">{state.name}</div>
                      <div className="mb-1 flex justify-between text-xs">
                        <span className="text-text-secondary">Income:</span>
                        <span className={state.incomeChange < 0 ? 'text-red-400' : 'text-india-green'}>{formatValue(state, 'incomeChange')}</span>
                      </div>
                      <div className="mb-1 flex justify-between text-xs">
                        <span className="text-text-secondary">Inflation:</span>
                        <span className={state.inflationImpact > 0 ? 'text-red-400' : 'text-india-green'}>{formatValue(state, 'inflationImpact')}</span>
                      </div>
                      <div className="mb-1 flex justify-between text-xs">
                        <span className="text-text-secondary">Acceptance:</span>
                        <span className="text-white">{formatValue(state, 'acceptance')}</span>
                      </div>
                      <div className="flex justify-between text-xs">
                        <span className="text-text-secondary">Jobs:</span>
                        <span className="text-white">{formatValue(state, 'jobsAffected')}</span>
                      </div>
                    </div>
                  )}
                </div>
              );
            }))}
          </div>
        </div>
        <aside className="min-h-44 rounded border border-surface-3 bg-surface-1 p-4">
          {selected ? <>
            <p className="text-xs font-bold uppercase tracking-wider text-saffron">State details</p>
            <h2 className="mt-1 text-base font-semibold text-white">{selected.name}</h2>
            <dl className="mt-4 space-y-3 text-xs">
              <div className="flex justify-between gap-4"><dt className="text-text-muted">Income change</dt><dd className="text-white">{formatValue(selected, 'incomeChange')}</dd></div>
              <div className="flex justify-between gap-4"><dt className="text-text-muted">Inflation impact</dt><dd className="text-white">{formatValue(selected, 'inflationImpact')}</dd></div>
              <div className="flex justify-between gap-4"><dt className="text-text-muted">Public acceptance</dt><dd className="text-white">{formatValue(selected, 'acceptance')}</dd></div>
              <div className="flex justify-between gap-4"><dt className="text-text-muted">Jobs affected</dt><dd className="text-white">{formatValue(selected, 'jobsAffected')}</dd></div>
            </dl>
          </> : <p className="text-sm leading-6 text-text-muted">Choose a state to inspect its projected impact. States without a tile were not returned by the simulation.</p>}
        </aside>
      </div>
      <div className="flex items-center gap-3 border-t border-surface-3 pt-4 text-xs text-text-muted"><span>Lower projected impact</span><div className={`h-2 flex-1 rounded bg-gradient-to-r ${metric === 'acceptance' ? 'from-surface-4 to-india-green' : 'from-surface-4 to-red-500'}`} /><span>{metric === 'acceptance' ? 'Higher acceptance' : 'Higher projected impact'}</span></div>
    </section>
  );
}
