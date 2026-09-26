export const mockSummary = {
  policyTitle: 'Fuel Price Deregulation — Diesel Subsidy Removal',
  policyDescription: 'Complete removal of diesel subsidies with phased implementation over 6 months. Diesel prices expected to increase by ₹12-15 per litre.',
  overallImpact: 'mixed' as const,
  confidenceLevel: 'Medium' as const,
  sections: [
    {
      title: 'Overview',
      content: 'The removal of diesel subsidies will have cascading effects across transportation, agriculture, and manufacturing sectors. Initial price shock expected in Month 1-2, with market adjustment by Month 4-6. Low-income rural households face disproportionate burden due to higher transport cost share in their budgets.',
      confidence: 'High' as const,
      kind: 'modelled' as const,
    },
    {
      title: 'Direct Economic Effects',
      content: 'Household expenditure on transport increases by 8-12% for rural populations and 4-6% for urban populations. Government saves ₹1.2-1.4 lakh crore annually. Inflation rises 0.4-0.8 percentage points in first quarter.',
      confidence: 'High' as const,
      kind: 'measured' as const,
    },
    {
      title: 'Ripple Effects',
      content: 'Agricultural input costs rise 6-9%, leading to 3-5% food price increases. Logistics sector faces 10-15% cost increase, partially passed to consumers. Public transport demand increases 12-18% as private vehicle usage declines.',
      confidence: 'Medium' as const,
      kind: 'modelled' as const,
    },
    {
      title: 'Group-Specific Impact',
      content: 'Farmers and agricultural labourers face the highest burden (12-15% income impact). Urban middle class absorbs the shock relatively well (2-4% impact). Truck operators and logistics workers see significant livelihood disruption.',
      confidence: 'Medium' as const,
      kind: 'judged' as const,
    },
    {
      title: 'Recommendations',
      content: 'Consider direct benefit transfer of ₹500-800/month to bottom 30% households. Phase implementation over 9 months instead of 6. Introduce public transport subsidies in rural areas to offset mobility costs.',
      confidence: 'Low' as const,
      kind: 'judged' as const,
    },
  ],
};

export const dashboardMetrics = [
  { label: 'Household Income Change', value: '-4.2%', range: '-3.1% to -5.8%', direction: 'negative' as const, kind: 'modelled' as const },
  { label: 'Cost of Living Impact', value: '+6.3%', range: '+4.8% to +8.1%', direction: 'negative' as const, kind: 'measured' as const },
  { label: 'Jobs Affected', value: '2.1M', range: '1.6M to 2.8M', direction: 'negative' as const, kind: 'judged' as const },
  { label: 'Fiscal Savings', value: '₹1.3L Cr', range: '₹1.1L to ₹1.5L Cr', direction: 'positive' as const, kind: 'modelled' as const },
  { label: 'Gini Change', value: '+0.012', range: '+0.008 to +0.018', direction: 'negative' as const, kind: 'modelled' as const },
  { label: 'Public Acceptance', value: '34%', range: '28% to 41%', direction: 'negative' as const, kind: 'judged' as const },
];

export const incomeChartData = [
  { group: 'Bottom 20%', change: -12.4, low: -15.1, high: -9.8 },
  { group: 'Lower Mid', change: -7.8, low: -9.6, high: -6.1 },
  { group: 'Middle', change: -4.2, low: -5.8, high: -3.1 },
  { group: 'Upper Mid', change: -2.1, low: -3.0, high: -1.4 },
  { group: 'Top 20%', change: -0.8, low: -1.2, high: -0.4 },
];

export const costOfLivingData = [
  { category: 'Food', change: 5.2 },
  { category: 'Fuel', change: 18.4 },
  { category: 'Transport', change: 14.2 },
  { category: 'Housing', change: 1.8 },
  { category: 'Health', change: 3.1 },
  { category: 'Education', change: 2.4 },
];

export const jobsData = [
  { sector: 'Agriculture', change: -340000, percentage: -2.1 },
  { sector: 'Transport', change: -520000, percentage: -8.4 },
  { sector: 'Manufacturing', change: -180000, percentage: -1.8 },
  { sector: 'Retail', change: -95000, percentage: -1.2 },
  { sector: 'Services', change: 45000, percentage: 0.3 },
  { sector: 'Public Transport', change: 120000, percentage: 4.2 },
];

export const timelineData = Array.from({ length: 13 }, (_, i) => ({
  month: i,
  label: `Month ${i}`,
  incomeChange: -(Math.sin(i * 0.4) * 5 + 2) * (i < 6 ? 1 : 0.7),
  inflationImpact: Math.max(0, (i < 3 ? i * 0.3 : 0.9 - (i - 3) * 0.08)),
  acceptance: 45 - i * 3 + (i > 6 ? (i - 6) * 2 : 0),
  employment: -(i < 4 ? i * 0.5 : 2 - (i - 4) * 0.15),
}));
