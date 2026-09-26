'use client';

import { useParams } from 'next/navigation';
import { ChartPanel, CostOfLivingChart, IncomeChart, JobsChart } from '@/components/charts/ImpactCharts';
import { useRunDashboard } from '@/hooks';

function PanelMessage({ children }: { children: React.ReactNode }) {
  return <div className="flex min-h-[420px] items-center justify-center p-6 text-sm text-text-muted">{children}</div>;
}

export default function DashboardPage() {
  const { runId } = useParams<{ runId: string }>();
  const dashboard = useRunDashboard(runId);

  if (dashboard.isLoading) return <PanelMessage>Loading dashboard metrics…</PanelMessage>;
  if (dashboard.isError) return <PanelMessage>Dashboard metrics could not be loaded. Please refresh the page to try again.</PanelMessage>;

  return (
    <div className="mx-auto max-w-7xl p-4 sm:p-6">
      <header className="mb-6">
        <p className="text-xs font-bold uppercase tracking-[0.16em] text-saffron">Simulation results</p>
        <h1 className="mt-1 text-xl font-semibold text-white">Impact dashboard</h1>
        <p className="mt-1 text-sm text-text-secondary">Projected distributional, household, and employment effects for the selected policy scenario.</p>
      </header>
      <div className="grid gap-5 lg:grid-cols-2">
        <ChartPanel description="Percent change from the simulated baseline." title="Income change by group"><IncomeChart data={dashboard.data?.income} /></ChartPanel>
        <ChartPanel description="Estimated change in household expenses." title="Cost of living by category"><CostOfLivingChart data={dashboard.data?.costOfLiving} /></ChartPanel>
        <ChartPanel description="Net jobs affected in the projection window." title="Employment impact by sector"><JobsChart data={dashboard.data?.jobs} /></ChartPanel>
        <section className="flex min-h-[320px] flex-col justify-between rounded-lg border border-surface-3 bg-surface-2 p-5">
          <div><h2 className="text-sm font-semibold text-white">Reading the dashboard</h2><p className="mt-2 max-w-md text-sm leading-6 text-text-secondary">Values are scenario projections, not measured outcomes. Use the confidence and evidence labels in the summary before acting on a result.</p></div>
          <p className="border-t border-surface-3 pt-4 text-xs leading-5 text-text-muted">Data shown here is supplied by the simulation dashboard endpoint. Change the global timeline or filters to refine the rest of the run workspace.</p>
        </section>
      </div>
    </div>
  );
}
