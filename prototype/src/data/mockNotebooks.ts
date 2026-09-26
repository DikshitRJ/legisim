export interface Notebook {
  id: string;
  title: string;
  description: string;
  sources: number;
  modifiedAt: string;
  status: 'active' | 'archived';
}

export const mockNotebooks: Notebook[] = [
  {
    id: 'nb-1',
    title: 'Industry Policy',
    description: 'Manufacturing output, tariff simulations & export zone incentives',
    sources: 8,
    modifiedAt: '2h ago',
    status: 'active',
  },
  {
    id: 'nb-2',
    title: 'Farmer Loan Policy',
    description: 'Credit waiver fiscal impact & state-wise priority lending allocations',
    sources: 4,
    modifiedAt: 'yesterday',
    status: 'active',
  },
  {
    id: 'nb-3',
    title: 'Telecom Regulatory Amendment',
    description: 'Spectrum auction cohort reaction & statutory revenue forecasting',
    sources: 6,
    modifiedAt: '3 days ago',
    status: 'active',
  },
  {
    id: 'nb-4',
    title: 'Digital Personal Data Protection',
    description: 'Statutory compliance & citizen privacy impact audit framework',
    sources: 12,
    modifiedAt: '5 days ago',
    status: 'active',
  },
  {
    id: 'nb-5',
    title: 'National Green Hydrogen Framework',
    description: 'Subsidies allocation & industrial energy transition cohort model',
    sources: 5,
    modifiedAt: '1 week ago',
    status: 'active',
  },
];
