'use client';

import React, { useState } from 'react';
import Header from '@/components/layout/Header';
import { ArrowRight, Loader2, CheckCircle2, XCircle } from 'lucide-react';
import { useNotebooks } from '@/hooks/useQueries';
import { useCompareRuns } from '@/hooks/useMutations';
import ReactECharts from 'echarts-for-react';
import ExportMenu from '@/components/ui/ExportMenu';

export default function ComparePage() {
  const [selectedRuns, setSelectedRuns] = useState<string[]>([]);
  const { data: notebooks, isLoading: isLoadingNotebooks } = useNotebooks();
  const compareMutation = useCompareRuns();

  const handleToggleRun = (id: string) => {
    setSelectedRuns(prev => {
      if (prev.includes(id)) return prev.filter(r => r !== id);
      if (prev.length >= 4) return prev;
      return [...prev, id];
    });
  };

  const handleCompare = () => {
    if (selectedRuns.length > 0) {
      compareMutation.mutate(selectedRuns);
    }
  };

  const comparisonData = compareMutation.data?.comparison;

  const renderComparisonCards = () => {
    if (!comparisonData) return null;
    
    // Convert to a predictable format if possible
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 mt-8">
        {selectedRuns.map((runId) => {
          const runDetails = notebooks?.find(n => n.id === runId);
          return (
            <div key={runId} className="bg-surface-2 border border-surface-3 rounded-xl p-6 shadow-lg flex flex-col">
              <div className="flex justify-between items-start mb-6 pb-4 border-b border-surface-3 flex-wrap gap-4">
                <div>
                  <span className="text-xs font-bold text-text-muted uppercase tracking-widest mb-1 block">Run ID: {runId.substring(0, 8)}...</span>
                  <h2 className="text-xl font-bold text-white">{runDetails?.title || 'Unknown Run'}</h2>
                </div>
                <ExportMenu runId={runId} />
              </div>
              <div className="space-y-4 flex-grow">
                 {Object.entries(comparisonData).map(([key, value]) => {
                   let displayValue = 'N/A';
                   if (value && typeof value === 'object' && runId in value) {
                     displayValue = String((value as Record<string, unknown>)[runId]);
                   } else if (typeof value !== 'object') {
                     displayValue = String(value);
                   } else {
                     try {
                        displayValue = JSON.stringify(value);
                     } catch(e) {
                        displayValue = 'Invalid Data';
                     }
                   }
                   return (
                     <div key={key} className="flex flex-col border-b border-surface-3 pb-2 last:border-0 last:pb-0">
                       <span className="text-sm font-semibold text-text-secondary capitalize">{key.replace(/_/g, ' ')}</span>
                       <span className="text-lg font-bold text-white">{displayValue}</span>
                     </div>
                   );
                 })}
              </div>
            </div>
          )
        })}
      </div>
    );
  };

  const renderChart = () => {
    if (!comparisonData) return null;

    const metrics = Object.keys(comparisonData).filter(m => {
        // Only include numeric metrics for chart
        const metricData = comparisonData[m];
        if (metricData && typeof metricData === 'object') {
            return Object.values(metricData).some(val => typeof val === 'number');
        }
        return false;
    });

    if (metrics.length === 0) return null;

    const series = selectedRuns.map(runId => {
      const runDetails = notebooks?.find(n => n.id === runId);
      return {
        name: runDetails?.title || `Run ${runId.substring(0, 4)}`,
        type: 'bar',
        data: metrics.map(m => {
          const metricData = comparisonData[m];
          if (metricData && typeof metricData === 'object' && runId in metricData) {
             const val = (metricData as Record<string, unknown>)[runId];
             return typeof val === 'number' ? val : 0;
          }
          return 0;
        })
      };
    });

    const option = {
      backgroundColor: 'transparent',
      tooltip: {
        trigger: 'axis',
        axisPointer: { type: 'shadow' }
      },
      legend: {
        textStyle: { color: '#E5E2E1' },
        top: 0
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        top: 40,
        containLabel: true
      },
      xAxis: [
        {
          type: 'category',
          data: metrics.map(m => m.replace(/_/g, ' ')),
          axisLabel: { color: '#A1A1AA', interval: 0, rotate: 15 }
        }
      ],
      yAxis: [
        {
          type: 'value',
          axisLabel: { color: '#A1A1AA' },
          splitLine: { lineStyle: { color: '#2A2A2A' } }
        }
      ],
      series: series,
      color: ['#FF671F', '#046A38', '#002868', '#f59e0b']
    };

    return (
      <div className="mt-8 bg-surface-2 p-6 rounded-xl border border-surface-3 shadow-lg">
        <h3 className="text-xl font-bold text-white mb-6">Metric Comparison</h3>
        <ReactECharts option={option} style={{ height: '400px', width: '100%' }} />
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-canvas text-text-body flex flex-col font-sans">
      <Header />
      
      <div className="p-8 max-w-6xl mx-auto w-full flex-grow">
        <h1 className="text-2xl font-bold text-white mb-6">Scenario Comparison</h1>

        <div className="bg-surface-2 border border-surface-3 rounded-xl p-6 shadow-lg mb-8">
          <h2 className="text-xl font-bold text-white mb-4">Select Runs to Compare (2-4)</h2>
          
          {isLoadingNotebooks ? (
            <div className="flex items-center gap-2 text-text-muted h-32 justify-center">
                <Loader2 className="w-6 h-6 animate-spin" /> 
                <span className="font-semibold uppercase tracking-widest text-sm">Loading available runs...</span>
            </div>
          ) : notebooks && notebooks.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 max-h-80 overflow-y-auto pr-2 custom-scrollbar">
              {notebooks.map((notebook) => (
                <label 
                  key={notebook.id}
                  className={`flex items-start gap-3 p-4 rounded-lg border cursor-pointer transition-colors ${
                    selectedRuns.includes(notebook.id) 
                      ? 'border-saffron bg-surface-3' 
                      : 'border-surface-3 hover:border-text-muted bg-surface-2'
                  }`}
                >
                  <input
                    type="checkbox"
                    className="mt-1 flex-shrink-0 w-4 h-4 text-saffron bg-surface-3 border-surface-3 focus:ring-saffron"
                    checked={selectedRuns.includes(notebook.id)}
                    onChange={() => handleToggleRun(notebook.id)}
                    disabled={!selectedRuns.includes(notebook.id) && selectedRuns.length >= 4}
                  />
                  <div className="flex-grow">
                    <div className="font-bold text-white">{notebook.title}</div>
                    <div className="text-sm text-text-muted mt-1">{notebook.description}</div>
                  </div>
                </label>
              ))}
            </div>
          ) : (
             <div className="text-text-muted">No runs available to compare.</div>
          )}

          <div className="mt-6 flex justify-end">
            <button
              onClick={handleCompare}
              disabled={selectedRuns.length < 2 || compareMutation.isPending}
              className="bg-saffron text-canvas px-6 py-3 rounded-lg font-bold flex items-center gap-2 hover:bg-[#E05A1B] transition-colors uppercase tracking-widest disabled:opacity-50 disabled:cursor-not-allowed h-12"
            >
              {compareMutation.isPending ? <Loader2 className="w-5 h-5 animate-spin" /> : <ArrowRight className="w-5 h-5" />}
              {compareMutation.isPending ? 'Comparing...' : 'Compare Selected Runs'}
            </button>
          </div>
          
          {compareMutation.isError && (
            <div className="mt-4 p-4 bg-red-900/20 border border-red-500/50 rounded-lg text-red-400 flex items-center gap-2">
              <XCircle className="w-5 h-5" />
              Failed to load comparison data. Please try again.
            </div>
          )}
        </div>
        
        {comparisonData && (
          <div className="space-y-8 animate-in fade-in duration-500">
            {renderComparisonCards()}
            {renderChart()}
          </div>
        )}
      </div>
    </div>
  );
}
