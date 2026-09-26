'use client';

import React from 'react';
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Line,
  LineChart,
  ReferenceLine,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';

export interface IncomePoint {
  group: string;
  change: number;
  low: number;
  high: number;
}

export interface CostOfLivingPoint {
  category: string;
  change: number;
}

export interface JobsPoint {
  sector: string;
  change: number;
  percentage: number;
}

export interface TimelinePoint {
  month: number;
  label: string;
  incomeChange: number;
  inflationImpact: number;
  acceptance: number;
  employment: number;
}

const numberFormatter = new Intl.NumberFormat('en-IN', { maximumFractionDigits: 1 });

function ChartTooltip({ active, payload, label }: { active?: boolean; payload?: Array<{ name?: string; value?: number; color?: string }>; label?: string }) {
  if (!active || !payload?.length) return null;

  return (
    <div className="rounded border border-surface-3 bg-surface-1 px-3 py-2 shadow-xl">
      <p className="mb-1 text-xs font-semibold text-white">{label}</p>
      {payload.map((entry, index) => (
        <p className="text-xs" key={`${entry.name}-${index}`} style={{ color: entry.color }}>
          {entry.name}: {typeof entry.value === 'number' ? numberFormatter.format(entry.value) : '—'}
        </p>
      ))}
    </div>
  );
}

export function ChartPanel({ title, description, children }: { title: string; description?: string; children: React.ReactNode }) {
  return (
    <section className="flex min-h-[320px] flex-col rounded-lg border border-surface-3 bg-surface-2 p-5">
      <div className="mb-4">
        <h2 className="text-sm font-semibold text-white">{title}</h2>
        {description ? <p className="mt-1 text-xs text-text-muted">{description}</p> : null}
      </div>
      <div className="min-h-0 flex-1">{children}</div>
    </section>
  );
}

function EmptyChart({ label }: { label: string }) {
  return <div className="flex h-full min-h-48 items-center justify-center text-sm text-text-muted">No {label.toLowerCase()} data is available for this run.</div>;
}

const axisTick = { fill: '#A1A1AA', fontSize: 11 };
const grid = <CartesianGrid stroke="#2A2A2A" strokeDasharray="3 3" vertical={false} />;

export function IncomeChart({ data }: { data?: IncomePoint[] }) {
  if (!data?.length) return <EmptyChart label="income" />;
  return (
    <ResponsiveContainer height="100%" width="100%">
      <BarChart aria-label="Income change by population group" data={data} margin={{ top: 8, right: 8, left: -18, bottom: 8 }}>
        {grid}
        <XAxis dataKey="group" interval={0} stroke="#71717A" tick={axisTick} />
        <YAxis stroke="#71717A" tick={axisTick} tickFormatter={(value) => `${value}%`} />
        <Tooltip content={<ChartTooltip />} cursor={{ fill: '#2A2A2A', opacity: 0.35 }} />
        <ReferenceLine stroke="#71717A" y={0} />
        <Bar dataKey="change" name="Change (%)" radius={[3, 3, 3, 3]}>
          {data.map((point) => <Cell fill={point.change < 0 ? '#EF4444' : '#138808'} key={point.group} />)}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
}

export function CostOfLivingChart({ data }: { data?: CostOfLivingPoint[] }) {
  if (!data?.length) return <EmptyChart label="cost-of-living" />;
  return (
    <ResponsiveContainer height="100%" width="100%">
      <BarChart aria-label="Cost of living change by category" data={data} layout="vertical" margin={{ top: 8, right: 12, left: 12, bottom: 8 }}>
        <CartesianGrid stroke="#2A2A2A" strokeDasharray="3 3" horizontal={false} />
        <XAxis type="number" stroke="#71717A" tick={axisTick} tickFormatter={(value) => `${value}%`} />
        <YAxis dataKey="category" type="category" width={80} stroke="#71717A" tick={axisTick} />
        <Tooltip content={<ChartTooltip />} cursor={{ fill: '#2A2A2A', opacity: 0.35 }} />
        <Bar dataKey="change" fill="#FF671F" name="Change (%)" radius={[0, 3, 3, 0]} />
      </BarChart>
    </ResponsiveContainer>
  );
}

export function JobsChart({ data }: { data?: JobsPoint[] }) {
  if (!data?.length) return <EmptyChart label="employment" />;
  return (
    <ResponsiveContainer height="100%" width="100%">
      <BarChart aria-label="Employment change by sector" data={data} layout="vertical" margin={{ top: 8, right: 12, left: 20, bottom: 8 }}>
        <CartesianGrid stroke="#2A2A2A" strokeDasharray="3 3" horizontal={false} />
        <XAxis type="number" stroke="#71717A" tick={axisTick} tickFormatter={(value) => numberFormatter.format(value)} />
        <YAxis dataKey="sector" type="category" width={90} stroke="#71717A" tick={axisTick} />
        <Tooltip content={<ChartTooltip />} cursor={{ fill: '#2A2A2A', opacity: 0.35 }} />
        <ReferenceLine stroke="#71717A" x={0} />
        <Bar dataKey="change" name="Jobs affected" radius={[0, 3, 3, 0]}>
          {data.map((point) => <Cell fill={point.change < 0 ? '#EF4444' : '#138808'} key={point.sector} />)}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
}

export function TimelineChart({ data, selectedMonth }: { data?: TimelinePoint[]; selectedMonth?: number }) {
  if (!data?.length) return <EmptyChart label="timeline" />;
  const selected = data.find((point) => point.month === selectedMonth);
  return (
    <ResponsiveContainer height="100%" width="100%">
      <LineChart aria-label="Projected trends by month" data={data} margin={{ top: 8, right: 12, left: -14, bottom: 8 }}>
        {grid}
        <XAxis dataKey="label" stroke="#71717A" tick={axisTick} />
        <YAxis stroke="#71717A" tick={axisTick} />
        <Tooltip content={<ChartTooltip />} />
        {selected ? <ReferenceLine stroke="#FF671F" strokeDasharray="4 4" x={selected.label} /> : null}
        <Line dataKey="incomeChange" dot={false} name="Income (%)" stroke="#EF4444" strokeWidth={2} type="monotone" />
        <Line dataKey="inflationImpact" dot={false} name="Inflation (pp)" stroke="#FF671F" strokeWidth={2} type="monotone" />
        <Line dataKey="acceptance" dot={false} name="Acceptance (%)" stroke="#138808" strokeWidth={2} type="monotone" />
      </LineChart>
    </ResponsiveContainer>
  );
}
