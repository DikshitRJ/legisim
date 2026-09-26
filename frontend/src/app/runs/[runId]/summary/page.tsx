'use client';

import React from 'react';
import { ArrowUpRight, ArrowDownRight, Info, ShieldAlert } from 'lucide-react';

const metrics = [
  { label: 'Household Income', value: '-4.2%', range: '[-3.1% to -5.5%]', trend: 'down', bad: true },
  { label: 'Cost of Living', value: '+6.3%', range: '[+4.0% to +8.1%]', trend: 'up', bad: true },
  { label: 'Jobs Affected', value: '2.1M', range: '[1.5M to 2.8M]', trend: 'down', bad: true },
  { label: 'Fiscal Savings', value: '₹1.3L Cr', range: '[₹1.1L to ₹1.4L Cr]', trend: 'up', bad: false },
  { label: 'Gini Coefficient', value: '+0.012', range: '[+0.008 to +0.015]', trend: 'up', bad: true },
  { label: 'Acceptance Rate', value: '34%', range: '[25% to 45%]', trend: 'down', bad: true },
];

const insights = [
  {
    title: 'Inflationary Spike in Transport & Logistics',
    content: 'The immediate removal of diesel subsidies triggers a cascading 15-22% increase in freight costs within the first 3 months. This directly impacts essential commodities, particularly perishable foods, leading to a temporary CPI spike of ~1.8%.',
    confidence: 'High',
    kind: 'Measured'
  },
  {
    title: 'Agricultural Sector Vulnerability',
    content: 'Farmers reliant on diesel for irrigation pumps and tractors face an immediate input cost surge of 12%. Without corresponding increases in Minimum Support Prices (MSP) or direct cash transfers, rural disposable income drops sharply by Month 4.',
    confidence: 'Medium',
    kind: 'Modelled'
  },
  {
    title: 'Fiscal Space Expansion',
    content: 'The exchequer saves approximately ₹1.3 Lakh Crore annually. If 40% of these savings are effectively reallocated to capital expenditure (infrastructure), long-term growth models suggest a recovery in employment metrics by Year 2.',
    confidence: 'High',
    kind: 'Modelled'
  },
  {
    title: 'Political Capital & Social Unrest Risk',
    content: 'Acceptance is lowest among rural agrarian cohorts and independent transport operators. Simulation flags high probability of organized strikes in primary logistics hubs (e.g., NCR, Maharashtra) during Months 1-2.',
    confidence: 'Medium',
    kind: 'Judged'
  }
];

export default function SummaryPage() {
  return (
    <div className="p-6 max-w-7xl mx-auto flex gap-6 flex-col lg:flex-row">
      <div className="flex-1 flex flex-col gap-6">
        <div className="bg-surface-2 rounded-xl p-6 border border-surface-3">
          <div className="flex justify-between items-start mb-4">
            <div>
              <h1 className="text-2xl font-bold text-white mb-2">Fuel Price Deregulation — Diesel Subsidy Removal</h1>
              <p className="text-text-secondary">Simulated impact over 12 months with immediate implementation and no compensatory policies.</p>
            </div>
            <div className="flex flex-col items-end gap-2">
              <div className="px-3 py-1 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-500 text-sm font-semibold flex items-center gap-2">
                <ShieldAlert className="w-4 h-4" />
                Mixed Impact
              </div>
              <div className="px-3 py-1 rounded-full bg-surface-4 border border-surface-3 text-text-secondary text-xs">
                Medium Confidence
              </div>
            </div>
          </div>
        </div>

        <div className="flex flex-col gap-4">
          <h2 className="text-lg font-semibold text-white px-1">Key AI Findings</h2>
          {insights.map((insight, i) => (
            <div key={i} className="bg-surface-4 rounded-xl p-6 border border-surface-3 flex flex-col gap-3 hover:border-surface-3/80 transition-colors">
              <h3 className="font-semibold text-white text-lg">{insight.title}</h3>
              <p className="text-sm text-text-body leading-relaxed">{insight.content}</p>
              <div className="flex items-center justify-between mt-2 pt-4 border-t border-surface-3">
                <div className="flex items-center gap-3">
                  <span className={`px-2 py-0.5 rounded text-xs font-medium ${
                    insight.confidence === 'High' ? 'bg-india-green/20 text-india-green' : 
                    insight.confidence === 'Medium' ? 'bg-amber-500/20 text-amber-500' : 
                    'bg-red-500/20 text-red-500'
                  }`}>
                    {insight.confidence} Confidence
                  </span>
                  <span className={`px-2 py-0.5 rounded text-xs font-medium ${
                    insight.kind === 'Measured' ? 'bg-accent-blue/20 text-accent-blue' :
                    insight.kind === 'Modelled' ? 'bg-purple-500/20 text-purple-500' :
                    'bg-saffron/20 text-saffron'
                  }`}>
                    {insight.kind}
                  </span>
                </div>
                <button className="text-xs font-medium text-accent-blue hover:text-white transition-colors">
                  View Evidence
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="w-full lg:w-80 flex flex-col gap-6 shrink-0">
        <h2 className="text-lg font-semibold text-white px-1">Macro Indicators</h2>
        <div className="grid grid-cols-2 lg:grid-cols-1 gap-4">
          {metrics.map((m, i) => (
            <div key={i} className="bg-surface-2 rounded-xl p-5 border border-surface-3 flex flex-col gap-1">
              <span className="text-xs font-medium text-text-secondary uppercase tracking-wider">{m.label}</span>
              <div className="flex items-baseline gap-2 mt-1">
                <span className={`text-2xl font-bold ${
                  m.bad ? (m.trend === 'up' ? 'text-red-400' : 'text-red-400') : 'text-india-green'
                }`}>
                  {m.value}
                </span>
                {m.trend === 'up' ? 
                  <ArrowUpRight className={`w-4 h-4 ${m.bad ? 'text-red-400' : 'text-india-green'}`} /> : 
                  <ArrowDownRight className={`w-4 h-4 ${m.bad ? 'text-red-400' : 'text-india-green'}`} />
                }
              </div>
              <span className="text-xs text-text-muted mt-2 font-mono">{m.range} projected</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
