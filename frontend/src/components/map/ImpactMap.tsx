'use client';

import React, { useMemo, useState } from 'react';

export interface StateImpactData {
  code: string;
  name: string;
  incomeChange: number;
  inflationImpact: number;
  acceptance: number;
  jobsAffected: number;
}

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

function formatValue(data: StateImpactData, metric: Metric) {
  const value = data[metric];
  if (metric === 'jobsAffected') return new Intl.NumberFormat('en-IN', { notation: 'compact', maximumFractionDigits: 1 }).format(value);
  if (metric === 'inflationImpact') return `${value >= 0 ? '+' : ''}${value.toFixed(1)} pp`;
  return `${value >= 0 && metric !== 'acceptance' ? '+' : ''}${value.toFixed(1)}%`;
}

export function ImpactMap({ data }: { data?: StateImpactData[] }) {
  const [metric, setMetric] = useState<Metric>('incomeChange');
  const [selectedCode, setSelectedCode] = useState<string | null>(null);
  const states = useMemo(() => new Map((data ?? []).map((state) => [state.code.toUpperCase(), state])), [data]);
  const selected = selectedCode ? states.get(selectedCode) : undefined;

  if (!data?.length) return <div className="flex min-h-[480px] items-center justify-center rounded-lg border border-surface-3 bg-surface-2 text-sm text-text-muted">No regional impact data is available for this run.</div>;

  return (
    <section className="rounded-lg border border-surface-3 bg-surface-2 p-5">
      <div className="flex flex-col gap-4 border-b border-surface-3 pb-4 lg:flex-row lg:items-start lg:justify-between">
        <div>
          <h1 className="text-base font-semibold text-white">Geographic impact</h1>
          <p className="mt-1 text-xs leading-5 text-text-muted">State-level comparison. Select a state for the complete run output.</p>
        </div>
        <div aria-label="Map metric" className="flex flex-wrap gap-1 rounded border border-surface-3 bg-surface-1 p-1" role="group">
          {(Object.keys(metricLabels) as Metric[]).map((key) => (
            <button aria-pressed={metric === key} className={`rounded px-2.5 py-1.5 text-xs font-semibold transition-colors ${metric === key ? 'bg-saffron text-canvas' : 'text-text-secondary hover:bg-surface-4 hover:text-white'}`} key={key} onClick={() => setMetric(key)} type="button">
              {metricLabels[key]}
            </button>
          ))}
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
              return (
                <button
                  aria-label={`${state.name}, ${metricLabels[metric]} ${formatValue(state, metric)}`}
                  aria-pressed={chosen}
                  className={`aspect-square rounded border p-1 text-center shadow-sm transition hover:-translate-y-0.5 hover:brightness-125 focus:outline-none focus:ring-2 focus:ring-saffron ${chosen ? 'border-white ring-2 ring-saffron' : 'border-white/15'}`}
                  key={code}
                  onClick={() => setSelectedCode(code)}
                  style={{ backgroundColor: colorFor(state[metric], metric) }}
                  type="button"
                >
                  <span className="block text-sm font-bold text-white drop-shadow">{code}</span>
                  <span className="mt-1 block text-[10px] text-white/90 drop-shadow">{formatValue(state, metric)}</span>
                </button>
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
