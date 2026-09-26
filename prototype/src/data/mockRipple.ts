export interface RippleNode {
  id: string;
  label: string;
  layer: number;
  domain: string;
  magnitude: string;
  confidence: 'High' | 'Medium' | 'Low';
  kind: 'measured' | 'modelled' | 'judged';
}

export interface RippleEdge {
  id: string;
  source: string;
  target: string;
  strength: number;
  lagMonths: number;
  mechanism: string;
}

export const rippleNodes: RippleNode[] = [
  { id: 'policy', label: 'Diesel Subsidy Removal', layer: 0, domain: 'Policy', magnitude: '₹12-15/L increase', confidence: 'High', kind: 'measured' },
  { id: 'transport-cost', label: 'Transport Cost Rise', layer: 1, domain: 'Transport', magnitude: '+14.2%', confidence: 'High', kind: 'modelled' },
  { id: 'agri-input', label: 'Agricultural Input Cost', layer: 1, domain: 'Agriculture', magnitude: '+6-9%', confidence: 'High', kind: 'modelled' },
  { id: 'logistics', label: 'Logistics Cost Surge', layer: 1, domain: 'Business', magnitude: '+10-15%', confidence: 'Medium', kind: 'modelled' },
  { id: 'food-price', label: 'Food Price Increase', layer: 2, domain: 'Consumer', magnitude: '+3-5%', confidence: 'Medium', kind: 'modelled' },
  { id: 'public-transit', label: 'Public Transit Demand', layer: 2, domain: 'Transport', magnitude: '+12-18%', confidence: 'Medium', kind: 'judged' },
  { id: 'rural-income', label: 'Rural Income Decline', layer: 2, domain: 'Income', magnitude: '-8-12%', confidence: 'Medium', kind: 'modelled' },
  { id: 'inflation', label: 'Inflation Spike', layer: 2, domain: 'Economy', magnitude: '+0.4-0.8pp', confidence: 'High', kind: 'measured' },
  { id: 'migration', label: 'Rural-Urban Migration', layer: 3, domain: 'Social', magnitude: '+4-7%', confidence: 'Low', kind: 'judged' },
  { id: 'political', label: 'Political Backlash', layer: 3, domain: 'Political', magnitude: 'High Risk', confidence: 'Medium', kind: 'judged' },
  { id: 'fiscal-save', label: 'Government Savings', layer: 1, domain: 'Fiscal', magnitude: '₹1.3L Cr/yr', confidence: 'High', kind: 'measured' },
  { id: 'subsidy-redirect', label: 'Subsidy Reallocation', layer: 2, domain: 'Fiscal', magnitude: 'Potential', confidence: 'Low', kind: 'judged' },
];

export const rippleEdges: RippleEdge[] = [
  { id: 'e1', source: 'policy', target: 'transport-cost', strength: 0.9, lagMonths: 0, mechanism: 'Direct price pass-through' },
  { id: 'e2', source: 'policy', target: 'agri-input', strength: 0.8, lagMonths: 1, mechanism: 'Fuel-dependent farming operations' },
  { id: 'e3', source: 'policy', target: 'logistics', strength: 0.85, lagMonths: 0, mechanism: 'Diesel-powered fleet costs' },
  { id: 'e4', source: 'policy', target: 'fiscal-save', strength: 0.95, lagMonths: 0, mechanism: 'Subsidy budget elimination' },
  { id: 'e5', source: 'transport-cost', target: 'food-price', strength: 0.7, lagMonths: 1, mechanism: 'Supply chain cost transmission' },
  { id: 'e6', source: 'transport-cost', target: 'public-transit', strength: 0.6, lagMonths: 1, mechanism: 'Modal shift from private vehicles' },
  { id: 'e7', source: 'agri-input', target: 'rural-income', strength: 0.75, lagMonths: 2, mechanism: 'Reduced farm profitability' },
  { id: 'e8', source: 'agri-input', target: 'food-price', strength: 0.65, lagMonths: 2, mechanism: 'Production cost pass-through' },
  { id: 'e9', source: 'logistics', target: 'inflation', strength: 0.7, lagMonths: 1, mechanism: 'Economy-wide cost push' },
  { id: 'e10', source: 'food-price', target: 'inflation', strength: 0.6, lagMonths: 1, mechanism: 'CPI food weight impact' },
  { id: 'e11', source: 'rural-income', target: 'migration', strength: 0.5, lagMonths: 3, mechanism: 'Economic distress migration' },
  { id: 'e12', source: 'rural-income', target: 'political', strength: 0.7, lagMonths: 2, mechanism: 'Rural voter discontent' },
  { id: 'e13', source: 'fiscal-save', target: 'subsidy-redirect', strength: 0.4, lagMonths: 6, mechanism: 'Budget reallocation potential' },
];
