'use client';

import React, { useMemo } from 'react';
import { useRunTimeline } from '@/hooks/useQueries';
import { useSimulationStore } from '@/store/useSimulationStore';
import { Calendar, Loader2 } from 'lucide-react';
import ReactECharts from 'echarts-for-react';

export default function TimePage({ params }: { params: { runId: string } }) {
  const { runId } = params;
  const { data: timelineData, isLoading } = useRunTimeline(runId);
  const currentTimeStep = useSimulationStore(state => state.currentTimeStep);
  const setTimeStep = useSimulationStore(state => state.setTimeStep);

  const currentMonthData = useMemo(() => {
    if (!timelineData || timelineData.length === 0) return null;
    const monthData = timelineData.find(d => d.month === currentTimeStep);
    return monthData || timelineData[0];
  }, [timelineData, currentTimeStep]);

  const maxMonth = useMemo(() => {
    if (!timelineData || timelineData.length === 0) return 12;
    return Math.max(...timelineData.map(d => d.month));
  }, [timelineData]);

  const chartOption = useMemo(() => {
    if (!timelineData) return {};
    
    return {
      backgroundColor: 'transparent',
      tooltip: {
        trigger: 'axis',
        backgroundColor: '#121212',
        borderColor: '#2A2A2A',
        textStyle: { color: '#E5E2E1' },
      },
      legend: {
        data: ['Income Change', 'Inflation Impact', 'Acceptance', 'Employment'],
        textStyle: { color: '#A1A1AA' },
        top: 0
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        boundaryGap: false,
        data: timelineData.map(d => d.label),
        axisLabel: { color: '#A1A1AA' },
        axisLine: { lineStyle: { color: '#3F3F46' } },
        splitLine: { show: false }
      },
      yAxis: [
        {
          type: 'value',
          axisLabel: { color: '#A1A1AA' },
          splitLine: { lineStyle: { color: '#2A2A2A', type: 'dashed' } }
        }
      ],
      series: [
        {
          name: 'Income Change',
          type: 'line',
          data: timelineData.map(d => d.incomeChange),
          itemStyle: { color: '#FF671F' },
          showSymbol: false,
          markLine: {
            data: [
              { xAxis: timelineData.find(d => d.month === currentTimeStep)?.label || '' }
            ],
            lineStyle: { color: '#FF671F', type: 'dashed' }
          }
        },
        {
          name: 'Inflation Impact',
          type: 'line',
          data: timelineData.map(d => d.inflationImpact),
          itemStyle: { color: '#EF4444' }, // red for inflation
          showSymbol: false
        },
        {
          name: 'Acceptance',
          type: 'line',
          data: timelineData.map(d => d.acceptance),
          itemStyle: { color: '#046A38' }, // green for acceptance
          showSymbol: false
        },
        {
          name: 'Employment',
          type: 'line',
          data: timelineData.map(d => d.employment),
          itemStyle: { color: '#002868' }, // navy for employment
          showSymbol: false
        }
      ]
    };
  }, [timelineData, currentTimeStep]);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-full">
        <Loader2 className="w-8 h-8 animate-spin text-saffron" />
      </div>
    );
  }

  if (!timelineData || timelineData.length === 0) {
    return (
      <div className="flex items-center justify-center h-full">
        <p className="text-text-muted">No timeline data available.</p>
      </div>
    );
  }

  return (
    <div className="p-6 max-w-7xl mx-auto flex flex-col gap-8 h-full">
      {/* Custom Time Slider */}
      <div className="bg-[#121212] rounded-xl p-6 border border-[#2A2A2A]">
        <div className="flex justify-between items-end mb-6">
          <div>
            <h1 className="text-xl font-bold text-white mb-1">Temporal Evolution</h1>
            <p className="text-sm text-[#A1A1AA]">Slide to view simulated metrics over time</p>
          </div>
          <div className="bg-[#1E1E1E] px-4 py-2 rounded-lg border border-[#2A2A2A] flex items-center gap-3">
            <Calendar className="w-5 h-5 text-saffron" />
            <span className="text-xl font-bold text-white">Month {currentTimeStep}</span>
          </div>
        </div>

        <div className="relative pt-4 pb-8">
          <input 
            type="range" 
            min="1" 
            max={maxMonth} 
            value={currentTimeStep || 1}
            onChange={(e) => setTimeStep(parseInt(e.target.value))}
            className="w-full h-2 bg-[#1E1E1E] rounded-lg appearance-none cursor-pointer accent-[#FF671F] relative z-10"
          />
        </div>
      </div>

      {/* Snapshot Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mt-8">
        <div className="bg-[#121212] rounded-xl p-5 border border-[#2A2A2A]">
          <div className="text-sm text-[#A1A1AA] mb-1">Avg Income Change</div>
          <div className={`text-3xl font-bold ${currentMonthData?.incomeChange && currentMonthData.incomeChange < 0 ? 'text-red-400' : 'text-[#046A38]'}`}>
            {currentMonthData?.incomeChange?.toFixed(1) || 0}%
          </div>
        </div>
        <div className="bg-[#121212] rounded-xl p-5 border border-[#2A2A2A]">
          <div className="text-sm text-[#A1A1AA] mb-1">CPI Inflation Impact</div>
          <div className="text-3xl font-bold text-[#FF671F]">
            +{currentMonthData?.inflationImpact?.toFixed(1) || 0}%
          </div>
        </div>
        <div className="bg-[#121212] rounded-xl p-5 border border-[#2A2A2A]">
          <div className="text-sm text-[#A1A1AA] mb-1">Public Acceptance</div>
          <div className="text-3xl font-bold text-[#046A38]">
            {currentMonthData?.acceptance?.toFixed(0) || 0}%
          </div>
        </div>
        <div className="bg-[#121212] rounded-xl p-5 border border-[#2A2A2A]">
          <div className="text-sm text-[#A1A1AA] mb-1">Jobs Impact</div>
          <div className={`text-3xl font-bold ${currentMonthData?.employment && currentMonthData.employment < 0 ? 'text-red-400' : 'text-[#046A38]'}`}>
            {currentMonthData?.employment?.toFixed(2) || 0}
          </div>
        </div>
      </div>

      {/* Multi-line Chart */}
      <div className="bg-[#121212] rounded-xl p-6 border border-[#2A2A2A] flex-1 min-h-[400px]">
        <h3 className="text-white font-medium mb-4">Trend Overview</h3>
        <ReactECharts option={chartOption} style={{ height: '100%', width: '100%' }} />
      </div>
    </div>
  );
}
