'use client';

import React from 'react';
import ReactECharts from 'echarts-for-react';

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

const baseChartOptions = {
  backgroundColor: 'transparent',
  textStyle: {
    fontFamily: 'Roboto Flex, sans-serif',
  },
  tooltip: {
    trigger: 'axis',
    backgroundColor: '#1E1E1E',
    borderColor: '#2A2A2A',
    textStyle: { color: '#E5E2E1', fontSize: 12 },
    axisPointer: { type: 'shadow', shadowStyle: { color: 'rgba(42, 42, 42, 0.35)' } }
  },
  grid: {
    top: 20,
    right: 20,
    bottom: 20,
    left: 40,
    containLabel: true
  }
};

export function IncomeChart({ data }: { data?: IncomePoint[] }) {
  if (!data?.length) return <EmptyChart label="income" />;
  
  const options = {
    ...baseChartOptions,
    xAxis: {
      type: 'category',
      data: data.map(d => d.group),
      axisLabel: { color: '#A1A1AA', fontSize: 11 },
      axisLine: { show: false },
      axisTick: { show: false }
    },
    yAxis: {
      type: 'value',
      axisLabel: { color: '#A1A1AA', fontSize: 11, formatter: '{value}%' },
      splitLine: { lineStyle: { color: '#2A2A2A', type: 'dashed' } }
    },
    series: [
      {
        name: 'Change (%)',
        type: 'bar',
        data: data.map(d => ({
          value: d.change,
          itemStyle: { color: d.change < 0 ? '#EF4444' : '#138808', borderRadius: [3, 3, 0, 0] }
        }))
      },
      {
        name: 'Error Margin',
        type: 'custom',
        itemStyle: { color: '#71717A', borderWidth: 1.5 },
        renderItem: function (params: any, api: any) {
          const xValue = api.value(0);
          const highPoint = api.coord([xValue, api.value(1)]);
          const lowPoint = api.coord([xValue, api.value(2)]);
          const halfWidth = api.size([1, 0])[0] * 0.1;
          const style = api.style({ stroke: api.visual('color'), fill: null });
          
          return {
            type: 'group',
            children: [
              {
                type: 'line',
                transition: ['shape'],
                shape: { x1: highPoint[0], y1: highPoint[1], x2: lowPoint[0], y2: lowPoint[1] },
                style: style
              },
              {
                type: 'line',
                transition: ['shape'],
                shape: { x1: highPoint[0] - halfWidth, y1: highPoint[1], x2: highPoint[0] + halfWidth, y2: highPoint[1] },
                style: style
              },
              {
                type: 'line',
                transition: ['shape'],
                shape: { x1: lowPoint[0] - halfWidth, y1: lowPoint[1], x2: lowPoint[0] + halfWidth, y2: lowPoint[1] },
                style: style
              }
            ]
          };
        },
        data: data.map((d, index) => [index, d.high, d.low]),
        z: 100
      }
    ]
  };

  return <ReactECharts option={options} style={{ height: '100%', width: '100%' }} />;
}

export function CostOfLivingChart({ data }: { data?: CostOfLivingPoint[] }) {
  if (!data?.length) return <EmptyChart label="cost-of-living" />;
  
  const options = {
    ...baseChartOptions,
    xAxis: {
      type: 'value',
      axisLabel: { color: '#A1A1AA', fontSize: 11, formatter: '{value}%' },
      splitLine: { lineStyle: { color: '#2A2A2A', type: 'dashed' } }
    },
    yAxis: {
      type: 'category',
      data: data.map(d => d.category),
      axisLabel: { color: '#A1A1AA', fontSize: 11 },
      axisLine: { show: false },
      axisTick: { show: false }
    },
    series: [
      {
        name: 'Change (%)',
        type: 'bar',
        data: data.map(d => ({
          value: d.change,
          itemStyle: { color: '#FF671F', borderRadius: [0, 3, 3, 0] }
        }))
      }
    ]
  };

  return <ReactECharts option={options} style={{ height: '100%', width: '100%' }} />;
}

export function JobsChart({ data }: { data?: JobsPoint[] }) {
  if (!data?.length) return <EmptyChart label="employment" />;
  
  const options = {
    ...baseChartOptions,
    xAxis: [
      {
        type: 'value',
        name: 'Jobs Affected',
        axisLabel: { color: '#A1A1AA', fontSize: 11, formatter: (val: number) => numberFormatter.format(val) },
        splitLine: { lineStyle: { color: '#2A2A2A', type: 'dashed' } }
      },
      {
        type: 'value',
        name: 'Percentage',
        axisLabel: { color: '#A1A1AA', fontSize: 11, formatter: '{value}%' },
        splitLine: { show: false }
      }
    ],
    yAxis: {
      type: 'category',
      data: data.map(d => d.sector),
      axisLabel: { color: '#A1A1AA', fontSize: 11 },
      axisLine: { show: false },
      axisTick: { show: false }
    },
    series: [
      {
        name: 'Jobs affected',
        type: 'bar',
        xAxisIndex: 0,
        data: data.map(d => ({
          value: d.change,
          itemStyle: { color: d.change < 0 ? '#EF4444' : '#138808', borderRadius: [0, 3, 3, 0] }
        }))
      },
      {
        name: 'Percentage (%)',
        type: 'bar',
        xAxisIndex: 1,
        data: data.map(d => ({
          value: d.percentage,
          itemStyle: { color: '#002868', borderRadius: [0, 3, 3, 0] }
        }))
      }
    ]
  };

  return <ReactECharts option={options} style={{ height: '100%', width: '100%' }} />;
}

export function TimelineChart({ data, selectedMonth }: { data?: TimelinePoint[]; selectedMonth?: number }) {
  if (!data?.length) return <EmptyChart label="timeline" />;
  
  const selected = data.find((point) => point.month === selectedMonth);
  
  const options = {
    ...baseChartOptions,
    tooltip: { ...baseChartOptions.tooltip, axisPointer: { type: 'line' } },
    xAxis: {
      type: 'category',
      data: data.map(d => d.label),
      axisLabel: { color: '#A1A1AA', fontSize: 11 },
      axisLine: { show: false },
      axisTick: { show: false }
    },
    yAxis: {
      type: 'value',
      axisLabel: { color: '#A1A1AA', fontSize: 11 },
      splitLine: { lineStyle: { color: '#2A2A2A', type: 'dashed' } }
    },
    series: [
      {
        name: 'Income (%)',
        type: 'line',
        showSymbol: false,
        lineStyle: { width: 2, color: '#EF4444' },
        itemStyle: { color: '#EF4444' },
        data: data.map(d => d.incomeChange)
      },
      {
        name: 'Inflation (pp)',
        type: 'line',
        showSymbol: false,
        lineStyle: { width: 2, color: '#FF671F' },
        itemStyle: { color: '#FF671F' },
        data: data.map(d => d.inflationImpact)
      },
      {
        name: 'Acceptance (%)',
        type: 'line',
        showSymbol: false,
        lineStyle: { width: 2, color: '#138808' },
        itemStyle: { color: '#138808' },
        data: data.map(d => d.acceptance)
      }
    ]
  };
  
  if (selected) {
    (options as any).series.push({
      type: 'line',
      markLine: {
        symbol: ['none', 'none'],
        lineStyle: { color: '#FF671F', type: 'dashed' },
        data: [{ xAxis: selected.label }]
      }
    });
  }

  return <ReactECharts option={options} style={{ height: '100%', width: '100%' }} />;
}
