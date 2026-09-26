export interface CohortGroup {
  id: string;
  name: string;
  population: string;
  description: string;
  stance: { support: number; neutral: number; oppose: number };
  incomeChange: number;
  behaviors: string[];
  confidence: 'High' | 'Medium' | 'Low';
}

export const cohortGroups: CohortGroup[] = [
  {
    id: 'cg-1',
    name: 'Rural Farmers (Cultivators)',
    population: '11.8 Cr',
    description: 'Small and marginal farmers dependent on diesel for irrigation pumps and transport to mandis.',
    stance: { support: 12, neutral: 18, oppose: 70 },
    incomeChange: -12.4,
    behaviors: ['Reduce mechanized farming', 'Shift to manual labor', 'Delay crop transport', 'Protest participation likely'],
    confidence: 'High',
  },
  {
    id: 'cg-2',
    name: 'Urban Middle Class (25-59)',
    population: '8.4 Cr',
    description: 'Salaried professionals in cities with private vehicles and moderate savings.',
    stance: { support: 28, neutral: 35, oppose: 37 },
    incomeChange: -3.1,
    behaviors: ['Switch to public transport', 'Reduce discretionary spending', 'Carpool adoption', 'Some shift to EVs'],
    confidence: 'Medium',
  },
  {
    id: 'cg-3',
    name: 'Truck Operators & Logistics',
    population: '85 Lakh',
    description: 'Long-haul truck drivers and small fleet owners. Diesel is 40-50% of operating cost.',
    stance: { support: 5, neutral: 10, oppose: 85 },
    incomeChange: -18.2,
    behaviors: ['Pass costs to shippers', 'Reduce trip frequency', 'Strike action probable', 'Fleet downsizing'],
    confidence: 'High',
  },
  {
    id: 'cg-4',
    name: 'Agricultural Labourers',
    population: '14.4 Cr',
    description: 'Landless rural workers dependent on daily wages from farming activities.',
    stance: { support: 8, neutral: 22, oppose: 70 },
    incomeChange: -9.6,
    behaviors: ['Seek urban employment', 'Reduce food variety', 'Increase debt borrowing', 'Seasonal migration increase'],
    confidence: 'Medium',
  },
  {
    id: 'cg-5',
    name: 'Urban Poor & Informal Sector',
    population: '6.2 Cr',
    description: 'Rickshaw pullers, street vendors, domestic workers in cities. Highly price-sensitive.',
    stance: { support: 10, neutral: 15, oppose: 75 },
    incomeChange: -8.8,
    behaviors: ['Walk more, use buses', 'Reduce meal frequency', 'Seek additional work', 'Potential unrest participation'],
    confidence: 'Medium',
  },
  {
    id: 'cg-6',
    name: 'Elderly / Senior Citizens (60+)',
    population: '10.4 Cr',
    description: 'Retired individuals on fixed pensions, highly dependent on public services.',
    stance: { support: 15, neutral: 30, oppose: 55 },
    incomeChange: -5.2,
    behaviors: ['Reduce travel', 'Cut medical visits', 'Rely more on family', 'Fixed income erosion'],
    confidence: 'Low',
  },
];
