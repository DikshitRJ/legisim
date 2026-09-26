export interface CohortCategory {
  id: string;
  number: string;
  title: string;
  options: string[];
}

export const cohortCategories: CohortCategory[] = [
  {
    id: 'age',
    number: '01',
    title: 'Population & Age Groups',
    options: [
      'Child Population (0–6 years)',
      'Adolescents & School-Aged Kids (7–14 years)',
      'Youth / Early Working Age (15–24 years)',
      'Active Productive / Middle Age (25–59 years)',
      'Elderly / Senior Citizens (60+ years)',
    ],
  },
  {
    id: 'income',
    number: '02',
    title: 'Income Groups & Economic Conditions',
    options: [
      'Asset-Based Wealth Quintiles (Poorest to Richest)',
      'Housing Structural Integrity (Pucca, Semi-Pucca, Kutcha)',
      'Household Amenities Access (Electricity, Fuel type, Water source, Sanitation)',
    ],
  },
  {
    id: 'occupation',
    number: '03',
    title: 'Occupations (Economic Activity Status)',
    options: [
      'Main Workers',
      'Marginal Workers',
      'Non-Workers',
      'Cultivators',
      'Agricultural Labourers',
      'Household Industry Workers',
      'Other Workers',
    ],
  },
  {
    id: 'settlement',
    number: '04',
    title: 'Urban vs. Rural Population',
    options: [
      'Rural Revenue Villages',
      'Statutory Towns',
      'Census Towns',
    ],
  },
  {
    id: 'education',
    number: '05',
    title: 'Education & Literacy Levels',
    options: [
      'Literate',
      'Illiterate',
      'Literate without educational level',
      'Primary school level',
      'Middle school level',
      'Matriculation / Secondary school level',
      'Higher Secondary / Intermediate / Pre-University',
      'Non-technical / Technical diploma or certificate',
      'Graduate degree and above',
    ],
  },
  {
    id: 'social',
    number: '06',
    title: 'Existing Public Behaviour & Social Attitudes',
    options: [
      'Migration Patterns (By reason: marriage, work, education, displacement)',
      'Fertility and Nuptiality Trends (Age at marriage, births within last year)',
      'Household Size & Dynamics (Nuclear vs. Joint families)',
      'Scheduled Castes (SC) and Scheduled Tribes (ST)',
      'Religious Affiliations',
    ],
  },
];
