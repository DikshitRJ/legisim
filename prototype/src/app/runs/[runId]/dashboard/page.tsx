'use client';

import React from 'react';
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell, Legend } from 'recharts';

const incomeData = [
  { name: 'Poorest 20%', change: -8.5, low: -10, high: -6 },
  { name: 'Lower Mid', change: -5.2, low: -7, high: -4 },
  { name: 'Middle 20%', change: -3.1, low: -4, high: -2 },
  { name: 'Upper Mid', change: -1.0, low: -2, high: 0 },
  { name: 'Richest 20%', change: 0.5, low: -0.5, high: 1.5 },
];

const costData = [
  { name: 'Food', value: 8.4 },
  { name: 'Fuel', value: 25.0 },
  { name: 'Transport', value: 12.5 },
  { name: 'Housing', value: 1.2 },
  { name: 'Health', value: 2.5 },
  { name: 'Education', value: 0.5 },
];

const jobsData = [
  { name: 'Agriculture', value: -450000 },
  { name: 'Logistics', value: -120000 },
  { name: 'Manufacturing', value: -85000 },
  { name: 'Services', value: -20000 },
  { name: 'Green Energy', value: 55000 },
  { name: 'Infrastructure', value: 150000 },
];

const acceptanceData = [
  { month: 'M0', val: 55 },
  { month: 'M1', val: 32 },
  { month: 'M2', val: 28 },
  { month: 'M3', val: 25 },
  { month: 'M4', val: 27 },
  { month: 'M5', val: 30 },
  { month: 'M6', val: 32 },
  { month: 'M7', val: 34 },
  { month: 'M8', val: 34 },
  { month: 'M9', val: 35 },
  { month: 'M10', val: 36 },
  { month: 'M11', val: 38 },
  { month: 'M12', val: 40 },
];

const CustomTooltip = ({ active, payload, label }: any) => {
  if (active && payload && payload.length) {
    return (
      <div className="bg-surface-1 border border-surface-3 p-3 rounded-lg shadow-xl">
        <p className="text-white font-medium mb-1">{label}</p>
        {payload.map((entry: any, index: number) => (
          <p key={index} style={{ color: entry.color }} className="text-sm font-medium">
            {entry.name}: {entry.value > 1000 || entry.value < -1000 ? (entry.value / 1000).toFixed(1) + 'k' : entry.value}{entry.unit || '%'}
          </p>
        ))}
      </div>
    );
  }
  return null;
};

export default function DashboardPage() {
  return (
    <div className="p-6 max-w-7xl mx-auto space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        
        {/* Chart 1: Income Change */}
        <div className="bg-surface-2 border border-surface-3 rounded-xl p-5 h-80 flex flex-col">
          <h3 className="text-white font-medium mb-4">Income Change by Quintile</h3>
          <div className="flex-1 w-full min-h-0">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={incomeData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#2A2A2A" vertical={false} />
                <XAxis dataKey="name" stroke="#71717A" tick={{ fill: '#A1A1AA', fontSize: 12 }} />
                <YAxis stroke="#71717A" tick={{ fill: '#A1A1AA', fontSize: 12 }} />
                <Tooltip content={<CustomTooltip />} cursor={{ fill: '#2A2A2A', opacity: 0.4 }} />
                <Bar dataKey="change" radius={[4, 4, 4, 4]}>
                  {incomeData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.change < 0 ? '#EF4444' : '#138808'} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Chart 2: Cost of Living */}
        <div className="bg-surface-2 border border-surface-3 rounded-xl p-5 h-80 flex flex-col">
          <h3 className="text-white font-medium mb-4">Cost of Living Increase by Category</h3>
          <div className="flex-1 w-full min-h-0">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={costData} layout="vertical" margin={{ top: 10, right: 10, left: 10, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#2A2A2A" horizontal={false} />
                <XAxis type="number" stroke="#71717A" tick={{ fill: '#A1A1AA', fontSize: 12 }} />
                <YAxis dataKey="name" type="category" stroke="#71717A" tick={{ fill: '#A1A1AA', fontSize: 12 }} width={80} />
                <Tooltip content={<CustomTooltip />} cursor={{ fill: '#2A2A2A', opacity: 0.4 }} />
                <Bar dataKey="value" fill="#FF9933" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Chart 3: Jobs Impact */}
        <div className="bg-surface-2 border border-surface-3 rounded-xl p-5 h-80 flex flex-col">
          <h3 className="text-white font-medium mb-4">Employment Impact by Sector (Count)</h3>
          <div className="flex-1 w-full min-h-0">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={jobsData} layout="vertical" margin={{ top: 10, right: 10, left: 10, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#2A2A2A" horizontal={false} />
                <XAxis type="number" stroke="#71717A" tick={{ fill: '#A1A1AA', fontSize: 12 }} />
                <YAxis dataKey="name" type="category" stroke="#71717A" tick={{ fill: '#A1A1AA', fontSize: 12 }} width={100} />
                <Tooltip content={<CustomTooltip />} cursor={{ fill: '#2A2A2A', opacity: 0.4 }} />
                <Bar dataKey="value" radius={[0, 4, 4, 0]}>
                  {jobsData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.value < 0 ? '#EF4444' : '#138808'} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Chart 4: Acceptance */}
        <div className="bg-surface-2 border border-surface-3 rounded-xl p-5 h-80 flex flex-col">
          <h3 className="text-white font-medium mb-4">Public Acceptance Trend (12 Months)</h3>
          <div className="flex-1 w-full min-h-0">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={acceptanceData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#2A2A2A" vertical={false} />
                <XAxis dataKey="month" stroke="#71717A" tick={{ fill: '#A1A1AA', fontSize: 12 }} />
                <YAxis stroke="#71717A" tick={{ fill: '#A1A1AA', fontSize: 12 }} domain={[0, 100]} />
                <Tooltip content={<CustomTooltip />} />
                <Line type="monotone" dataKey="val" stroke="#3B82F6" strokeWidth={3} dot={{ r: 4, fill: '#121212', stroke: '#3B82F6', strokeWidth: 2 }} activeDot={{ r: 6, fill: '#3B82F6' }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

      </div>
    </div>
  );
}
