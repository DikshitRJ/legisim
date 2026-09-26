'use client';

import React, { useState } from 'react';
import { motion } from 'framer-motion';

// Grid layout for Indian states (approximate cartogram)
const stateGrid = [
  [null, null, 'JK', null, null, null, null],
  ['PB', 'HR', 'UK', null, 'AR', null, null],
  ['RJ', 'UP', 'DL', null, 'AS', 'NL', null],
  ['GJ', 'MP', 'JH', 'WB', 'ML', 'MN', 'MZ'],
  [null, 'MH', 'CG', 'OD', 'TR', null, null],
  ['GA', 'KA', 'TS', 'AP', null, null, null],
  [null, 'KL', 'TN', null, null, null, null],
];

const stateData: Record<string, { name: string, income: number, inflation: number, acceptance: number }> = {
  'JK': { name: 'Jammu & Kashmir', income: -4.2, inflation: 2.1, acceptance: 35 },
  'PB': { name: 'Punjab', income: -9.5, inflation: 1.8, acceptance: 15 },
  'HR': { name: 'Haryana', income: -8.2, inflation: 1.7, acceptance: 20 },
  'UK': { name: 'Uttarakhand', income: -5.1, inflation: 2.0, acceptance: 32 },
  'AR': { name: 'Arunachal', income: -3.0, inflation: 2.5, acceptance: 40 },
  'RJ': { name: 'Rajasthan', income: -7.5, inflation: 1.6, acceptance: 25 },
  'UP': { name: 'Uttar Pradesh', income: -8.8, inflation: 1.9, acceptance: 22 },
  'DL': { name: 'Delhi', income: -2.1, inflation: 1.2, acceptance: 45 },
  'AS': { name: 'Assam', income: -5.5, inflation: 2.2, acceptance: 38 },
  'NL': { name: 'Nagaland', income: -3.5, inflation: 2.4, acceptance: 41 },
  'GJ': { name: 'Gujarat', income: -4.5, inflation: 1.5, acceptance: 35 },
  'MP': { name: 'Madhya Pradesh', income: -7.2, inflation: 1.7, acceptance: 28 },
  'JH': { name: 'Jharkhand', income: -6.0, inflation: 1.8, acceptance: 30 },
  'WB': { name: 'West Bengal', income: -5.8, inflation: 1.9, acceptance: 29 },
  'ML': { name: 'Meghalaya', income: -4.0, inflation: 2.3, acceptance: 39 },
  'MN': { name: 'Manipur', income: -3.8, inflation: 2.4, acceptance: 40 },
  'MZ': { name: 'Mizoram', income: -3.6, inflation: 2.5, acceptance: 42 },
  'MH': { name: 'Maharashtra', income: -5.5, inflation: 1.6, acceptance: 33 },
  'CG': { name: 'Chhattisgarh', income: -6.5, inflation: 1.7, acceptance: 31 },
  'OD': { name: 'Odisha', income: -6.2, inflation: 1.8, acceptance: 32 },
  'TR': { name: 'Tripura', income: -4.2, inflation: 2.2, acceptance: 38 },
  'GA': { name: 'Goa', income: -2.5, inflation: 1.4, acceptance: 44 },
  'KA': { name: 'Karnataka', income: -4.8, inflation: 1.5, acceptance: 36 },
  'TS': { name: 'Telangana', income: -5.2, inflation: 1.6, acceptance: 34 },
  'AP': { name: 'Andhra Pradesh', income: -5.8, inflation: 1.7, acceptance: 32 },
  'KL': { name: 'Kerala', income: -3.5, inflation: 1.5, acceptance: 40 },
  'TN': { name: 'Tamil Nadu', income: -4.2, inflation: 1.4, acceptance: 38 },
};

type Metric = 'income' | 'inflation' | 'acceptance';

const getColor = (val: number, metric: Metric) => {
  if (metric === 'income') {
    // scale: 0 to -10 (redder is worse)
    const intensity = Math.min(Math.abs(val) / 10, 1);
    return `rgba(239, 68, 68, ${intensity})`; // Red
  }
  if (metric === 'inflation') {
    // scale: 1 to 3 (redder is higher inflation)
    const intensity = Math.min((val - 1) / 2, 1);
    return `rgba(249, 115, 22, ${intensity})`; // Orange/Saffron
  }
  if (metric === 'acceptance') {
    // scale: 10 to 50 (greener is higher)
    const intensity = Math.min((val - 10) / 40, 1);
    return `rgba(19, 136, 8, ${intensity})`; // Green
  }
  return '#2A2A2A';
};

export default function MapPage() {
  const [metric, setMetric] = useState<Metric>('income');
  const [hoveredState, setHoveredState] = useState<string | null>(null);

  return (
    <div className="p-6 h-full flex flex-col">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-xl font-bold text-white mb-1">Geographic Impact</h1>
          <p className="text-sm text-text-secondary">Grid cartogram view of regional variances</p>
        </div>
        <div className="flex bg-surface-2 rounded-lg p-1 border border-surface-3">
          {(['income', 'inflation', 'acceptance'] as Metric[]).map((m) => (
            <button
              key={m}
              onClick={() => setMetric(m)}
              className={`px-4 py-1.5 text-sm font-medium rounded-md capitalize transition-colors ${
                metric === m ? 'bg-surface-4 text-white shadow-sm' : 'text-text-secondary hover:text-white'
              }`}
            >
              {m}
            </button>
          ))}
        </div>
      </div>

      <div className="flex-1 flex items-center justify-center relative">
        <div className="flex flex-col gap-2">
          {stateGrid.map((row, rowIndex) => (
            <div key={rowIndex} className="flex gap-2">
              {row.map((st, colIndex) => {
                if (!st) return <div key={`${rowIndex}-${colIndex}`} className="w-20 h-20 md:w-24 md:h-24" />;
                
                const data = stateData[st];
                if (!data) return <div key={`${rowIndex}-${colIndex}`} className="w-20 h-20 md:w-24 md:h-24 bg-surface-2 border border-surface-3 rounded-lg flex items-center justify-center text-text-muted">{st}</div>;

                const val = data[metric];
                const bgColor = getColor(val, metric);

                return (
                  <motion.div
                    key={st}
                    whileHover={{ scale: 1.05, zIndex: 10 }}
                    onHoverStart={() => setHoveredState(st)}
                    onHoverEnd={() => setHoveredState(null)}
                    className="w-20 h-20 md:w-24 md:h-24 rounded-lg flex flex-col items-center justify-center relative cursor-pointer border border-surface-3 transition-colors"
                    style={{ backgroundColor: bgColor }}
                  >
                    <span className="font-bold text-white text-lg drop-shadow-md">{st}</span>
                    <span className="text-xs text-white/80 drop-shadow-sm font-medium">
                      {metric === 'income' ? `${val}%` : metric === 'inflation' ? `+${val}%` : `${val}%`}
                    </span>
                    
                    {hoveredState === st && (
                      <div className="absolute top-full mt-2 w-48 bg-surface-1 border border-surface-3 p-3 rounded-lg shadow-xl z-20 pointer-events-none">
                        <div className="font-bold text-white border-b border-surface-3 pb-1 mb-2">{data.name}</div>
                        <div className="flex justify-between text-sm mb-1">
                          <span className="text-text-secondary">Income:</span>
                          <span className={data.income < -5 ? 'text-red-400' : 'text-white'}>{data.income}%</span>
                        </div>
                        <div className="flex justify-between text-sm mb-1">
                          <span className="text-text-secondary">Inflation:</span>
                          <span className="text-orange-400">+{data.inflation}%</span>
                        </div>
                        <div className="flex justify-between text-sm">
                          <span className="text-text-secondary">Acceptance:</span>
                          <span className="text-india-green">{data.acceptance}%</span>
                        </div>
                      </div>
                    )}
                  </motion.div>
                );
              })}
            </div>
          ))}
        </div>
      </div>
      
      <div className="mt-8 flex items-center justify-center gap-4">
        <span className="text-sm text-text-muted">Low Impact / Better</span>
        <div className="w-64 h-3 rounded-full bg-gradient-to-r from-india-green via-surface-4 to-red-500"></div>
        <span className="text-sm text-text-muted">High Impact / Worse</span>
      </div>
    </div>
  );
}
