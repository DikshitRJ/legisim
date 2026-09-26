'use client';

import React, { useState, useMemo } from 'react';
import { useRunMap } from '@/hooks/useQueries';
import { ImpactMap } from '@/components/map/ImpactMap';
import type { StateData } from '@/lib/api/types';
import { ArrowDown, ArrowUp, ArrowUpDown } from 'lucide-react';

export default function MapPage({ params }: { params: { runId: string } }) {
  const { data: statesData, isLoading, isError } = useRunMap(params.runId);
  const [sortConfig, setSortConfig] = useState<{ key: keyof StateData; direction: 'asc' | 'desc' } | null>(null);

  const sortedData = useMemo(() => {
    if (!statesData) return [];
    let sortableItems = [...statesData];
    if (sortConfig !== null) {
      sortableItems.sort((a, b) => {
        const aValue = a[sortConfig.key];
        const bValue = b[sortConfig.key];
        if (aValue < bValue) return sortConfig.direction === 'asc' ? -1 : 1;
        if (aValue > bValue) return sortConfig.direction === 'asc' ? 1 : -1;
        return 0;
      });
    }
    return sortableItems;
  }, [statesData, sortConfig]);

  const requestSort = (key: keyof StateData) => {
    let direction: 'asc' | 'desc' = 'asc';
    if (sortConfig && sortConfig.key === key && sortConfig.direction === 'asc') {
      direction = 'desc';
    }
    setSortConfig({ key, direction });
  };

  const getSortIcon = (key: keyof StateData) => {
    if (!sortConfig || sortConfig.key !== key) {
      return <ArrowUpDown className="w-4 h-4 text-text-muted" />;
    }
    return sortConfig.direction === 'asc' ? (
      <ArrowUp className="w-4 h-4 text-saffron" />
    ) : (
      <ArrowDown className="w-4 h-4 text-saffron" />
    );
  };

  if (isLoading) {
    return (
      <div className="p-6 h-full flex flex-col gap-6 animate-pulse">
        <div className="h-10 bg-surface-2 rounded w-1/4"></div>
        <div className="h-[480px] bg-surface-2 rounded-lg border border-surface-3"></div>
        <div className="h-64 bg-surface-2 rounded-lg border border-surface-3"></div>
      </div>
    );
  }

  if (isError) {
    return (
      <div className="p-6">
        <div className="bg-red-500/10 border border-red-500/20 text-red-400 p-4 rounded-lg">
          Failed to load geographic impact data.
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 flex flex-col gap-6">
      <ImpactMap data={statesData} />

      <section className="rounded-lg border border-surface-3 bg-surface-2 overflow-hidden">
        <div className="p-4 border-b border-surface-3 flex items-center justify-between">
          <h2 className="text-base font-semibold text-white">State Data Table</h2>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm whitespace-nowrap">
            <thead className="bg-surface-1 border-b border-surface-3">
              <tr>
                <th 
                  className="p-4 font-semibold text-text-secondary cursor-pointer hover:bg-surface-3 transition-colors"
                  onClick={() => requestSort('name')}
                >
                  <div className="flex items-center gap-2">State {getSortIcon('name')}</div>
                </th>
                <th 
                  className="p-4 font-semibold text-text-secondary cursor-pointer hover:bg-surface-3 transition-colors"
                  onClick={() => requestSort('code')}
                >
                  <div className="flex items-center gap-2">Code {getSortIcon('code')}</div>
                </th>
                <th 
                  className="p-4 font-semibold text-text-secondary cursor-pointer hover:bg-surface-3 transition-colors"
                  onClick={() => requestSort('incomeChange')}
                >
                  <div className="flex items-center gap-2">Income Change {getSortIcon('incomeChange')}</div>
                </th>
                <th 
                  className="p-4 font-semibold text-text-secondary cursor-pointer hover:bg-surface-3 transition-colors"
                  onClick={() => requestSort('inflationImpact')}
                >
                  <div className="flex items-center gap-2">Inflation Impact {getSortIcon('inflationImpact')}</div>
                </th>
                <th 
                  className="p-4 font-semibold text-text-secondary cursor-pointer hover:bg-surface-3 transition-colors"
                  onClick={() => requestSort('acceptance')}
                >
                  <div className="flex items-center gap-2">Acceptance {getSortIcon('acceptance')}</div>
                </th>
                <th 
                  className="p-4 font-semibold text-text-secondary cursor-pointer hover:bg-surface-3 transition-colors"
                  onClick={() => requestSort('jobsAffected')}
                >
                  <div className="flex items-center gap-2">Jobs Affected {getSortIcon('jobsAffected')}</div>
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-surface-3 text-text-muted">
              {sortedData.map((state) => (
                <tr key={state.code} className="hover:bg-surface-3/50 transition-colors">
                  <td className="p-4 font-medium text-white">{state.name}</td>
                  <td className="p-4">{state.code}</td>
                  <td className={`p-4 ${state.incomeChange < 0 ? 'text-red-400' : 'text-india-green'}`}>
                    {state.incomeChange > 0 ? '+' : ''}{state.incomeChange}%
                  </td>
                  <td className={`p-4 ${state.inflationImpact > 0 ? 'text-red-400' : 'text-india-green'}`}>
                    {state.inflationImpact > 0 ? '+' : ''}{state.inflationImpact}%
                  </td>
                  <td className="p-4">{state.acceptance}%</td>
                  <td className="p-4">{new Intl.NumberFormat('en-IN').format(state.jobsAffected)}</td>
                </tr>
              ))}
              {sortedData.length === 0 && (
                <tr>
                  <td colSpan={6} className="p-8 text-center text-text-muted">
                    No state data available
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}
