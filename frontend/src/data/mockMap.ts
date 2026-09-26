export interface StateData {
  code: string;
  name: string;
  incomeChange: number;
  inflationImpact: number;
  acceptance: number;
  jobsAffected: number;
}

export const stateData: StateData[] = [
  { code: 'AP', name: 'Andhra Pradesh', incomeChange: -5.1, inflationImpact: 0.6, acceptance: 31, jobsAffected: 142000 },
  { code: 'AR', name: 'Arunachal Pradesh', incomeChange: -3.2, inflationImpact: 0.4, acceptance: 42, jobsAffected: 8000 },
  { code: 'AS', name: 'Assam', incomeChange: -4.8, inflationImpact: 0.5, acceptance: 35, jobsAffected: 95000 },
  { code: 'BR', name: 'Bihar', incomeChange: -7.2, inflationImpact: 0.8, acceptance: 25, jobsAffected: 310000 },
  { code: 'CG', name: 'Chhattisgarh', incomeChange: -5.5, inflationImpact: 0.6, acceptance: 30, jobsAffected: 78000 },
  { code: 'GA', name: 'Goa', incomeChange: -2.1, inflationImpact: 0.3, acceptance: 48, jobsAffected: 5000 },
  { code: 'GJ', name: 'Gujarat', incomeChange: -3.8, inflationImpact: 0.5, acceptance: 38, jobsAffected: 165000 },
  { code: 'HR', name: 'Haryana', incomeChange: -4.5, inflationImpact: 0.5, acceptance: 33, jobsAffected: 72000 },
  { code: 'HP', name: 'Himachal Pradesh', incomeChange: -3.4, inflationImpact: 0.4, acceptance: 40, jobsAffected: 22000 },
  { code: 'JH', name: 'Jharkhand', incomeChange: -6.1, inflationImpact: 0.7, acceptance: 28, jobsAffected: 98000 },
  { code: 'KA', name: 'Karnataka', incomeChange: -3.5, inflationImpact: 0.4, acceptance: 40, jobsAffected: 148000 },
  { code: 'KL', name: 'Kerala', incomeChange: -3.0, inflationImpact: 0.4, acceptance: 42, jobsAffected: 85000 },
  { code: 'MP', name: 'Madhya Pradesh', incomeChange: -6.4, inflationImpact: 0.7, acceptance: 27, jobsAffected: 215000 },
  { code: 'MH', name: 'Maharashtra', incomeChange: -3.2, inflationImpact: 0.4, acceptance: 39, jobsAffected: 280000 },
  { code: 'MN', name: 'Manipur', incomeChange: -3.8, inflationImpact: 0.4, acceptance: 38, jobsAffected: 9000 },
  { code: 'ML', name: 'Meghalaya', incomeChange: -3.5, inflationImpact: 0.4, acceptance: 39, jobsAffected: 11000 },
  { code: 'MZ', name: 'Mizoram', incomeChange: -3.1, inflationImpact: 0.3, acceptance: 41, jobsAffected: 4000 },
  { code: 'NL', name: 'Nagaland', incomeChange: -3.3, inflationImpact: 0.4, acceptance: 40, jobsAffected: 6000 },
  { code: 'OD', name: 'Odisha', incomeChange: -5.8, inflationImpact: 0.6, acceptance: 29, jobsAffected: 132000 },
  { code: 'PB', name: 'Punjab', incomeChange: -5.2, inflationImpact: 0.6, acceptance: 30, jobsAffected: 85000 },
  { code: 'RJ', name: 'Rajasthan', incomeChange: -5.9, inflationImpact: 0.7, acceptance: 28, jobsAffected: 195000 },
  { code: 'SK', name: 'Sikkim', incomeChange: -2.5, inflationImpact: 0.3, acceptance: 45, jobsAffected: 3000 },
  { code: 'TN', name: 'Tamil Nadu', incomeChange: -3.4, inflationImpact: 0.4, acceptance: 41, jobsAffected: 175000 },
  { code: 'TS', name: 'Telangana', incomeChange: -3.8, inflationImpact: 0.5, acceptance: 37, jobsAffected: 92000 },
  { code: 'TR', name: 'Tripura', incomeChange: -4.2, inflationImpact: 0.5, acceptance: 36, jobsAffected: 12000 },
  { code: 'UP', name: 'Uttar Pradesh', incomeChange: -6.8, inflationImpact: 0.8, acceptance: 26, jobsAffected: 520000 },
  { code: 'UK', name: 'Uttarakhand', incomeChange: -4.0, inflationImpact: 0.5, acceptance: 37, jobsAffected: 28000 },
  { code: 'WB', name: 'West Bengal', incomeChange: -5.0, inflationImpact: 0.6, acceptance: 32, jobsAffected: 245000 },
  { code: 'DL', name: 'Delhi', incomeChange: -2.2, inflationImpact: 0.3, acceptance: 44, jobsAffected: 45000 },
];
