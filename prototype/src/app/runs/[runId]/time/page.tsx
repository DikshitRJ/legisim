'use client';

import React, { useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts';
import { Calendar } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const timeData = Array.from({ length: 13 }).map((_, i) => ({
  month: i,
  label: `M${i}`,
  income: -1 - (i < 4 ? i * 2 : 8 - (i - 4) * 0.2),
  inflation: 0.5 + (i < 3 ? i * 0.6 : 1.8 - (i - 3) * 0.1),
  acceptance: 55 - (i < 4 ? i * 7 : 27 - (i - 4) * 1.5),
  employment: 0 - (i < 6 ? i * 50 : 300 - (i - 6) * 10), // in thousands
}));

const events = [
  { month: 0, title: 'Policy Implemented', desc: 'Subsidy officially removed' },
  { month: 2, title: 'Freight Strikes', desc: 'Transport unions protest cost hike' },
  { month: 4, title: 'Harvest Season', desc: 'Agri-input costs peak' },
  { month: 8, title: 'Market Adjustment', desc: 'New equilibrium forming' },
  { month: 12, title: 'Capex Kick-in', desc: 'Reallocated funds boost infrastructure' },
];

export default function TimePage() {
  const [currentMonth, setCurrentMonth] = useState(6);
  const currentData = timeData[currentMonth];

  return (
    <div className="p-6 max-w-7xl mx-auto flex flex-col gap-8 h-full">
      {/* Custom Time Slider */}
      <div className="bg-surface-2 rounded-xl p-6 border border-surface-3">
        <div className="flex justify-between items-end mb-6">
          <div>
            <h1 className="text-xl font-bold text-white mb-1">Temporal Evolution</h1>
            <p className="text-sm text-text-secondary">Slide to view simulated metrics over 12 months</p>
          </div>
          <div className="bg-surface-4 px-4 py-2 rounded-lg border border-surface-3 flex items-center gap-3">
            <Calendar className="w-5 h-5 text-accent-blue" />
            <span className="text-xl font-bold text-white">Month {currentMonth}</span>
          </div>
        </div>

        <div className="relative pt-4 pb-8">
          <input 
            type="range" 
            min="0" 
            max="12" 
            value={currentMonth}
            onChange={(e) => setCurrentMonth(parseInt(e.target.value))}
            className="w-full h-2 bg-surface-4 rounded-lg appearance-none cursor-pointer accent-saffron relative z-10"
          />
          
          {/* Event Markers */}
          <div className="absolute top-10 left-0 w-full">
            {events.map((evt, i) => (
              <div 
                key={i} 
                className="absolute transform -translate-x-1/2 flex flex-col items-center group cursor-pointer"
                style={{ left: `${(evt.month / 12) * 100}%` }}
                onClick={() => setCurrentMonth(evt.month)}
              >
                <div className={`w-3 h-3 rounded-full border-2 ${currentMonth >= evt.month ? 'bg-saffron border-saffron' : 'bg-surface-2 border-surface-4'} transition-colors`} />
                <div className="mt-2 text-center opacity-70 group-hover:opacity-100 transition-opacity w-32">
                  <div className="text-[10px] font-bold text-text-secondary uppercase">M{evt.month}</div>
                  <div className="text-xs text-white font-medium leading-tight">{evt.title}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Snapshot Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mt-8">
        <div className="bg-surface-4 rounded-xl p-5 border border-surface-3">
          <div className="text-sm text-text-secondary mb-1">Avg Income Change</div>
          <div className={`text-3xl font-bold ${currentData.income < 0 ? 'text-red-400' : 'text-india-green'}`}>
            {currentData.income.toFixed(1)}%
          </div>
        </div>
        <div className="bg-surface-4 rounded-xl p-5 border border-surface-3">
          <div className="text-sm text-text-secondary mb-1">CPI Inflation Impact</div>
          <div className="text-3xl font-bold text-orange-400">
            +{currentData.inflation.toFixed(1)}%
          </div>
        </div>
        <div className="bg-surface-4 rounded-xl p-5 border border-surface-3">
          <div className="text-sm text-text-secondary mb-1">Public Acceptance</div>
          <div className="text-3xl font-bold text-india-green">
            {currentData.acceptance.toFixed(0)}%
          </div>
        </div>
        <div className="bg-surface-4 rounded-xl p-5 border border-surface-3">
          <div className="text-sm text-text-secondary mb-1">Jobs Impact</div>
          <div className={`text-3xl font-bold ${currentData.employment < 0 ? 'text-red-400' : 'text-india-green'}`}>
            {(currentData.employment / 1000).toFixed(2)}M
          </div>
        </div>
      </div>

      {/* Multi-line Chart */}
      <div className="bg-surface-2 rounded-xl p-6 border border-surface-3 flex-1 min-h-[300px]">
        <h3 className="text-white font-medium mb-4">Trend Overview</h3>
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={timeData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#2A2A2A" vertical={false} />
            <XAxis dataKey="label" stroke="#71717A" tick={{ fill: '#A1A1AA', fontSize: 12 }} />
            <YAxis stroke="#71717A" tick={{ fill: '#A1A1AA', fontSize: 12 }} />
            <Tooltip contentStyle={{ backgroundColor: '#121212', borderColor: '#2A2A2A' }} />
            <ReferenceLine x={`M${currentMonth}`} stroke="#FF9933" strokeDasharray="3 3" />
            <Line type="monotone" dataKey="income" name="Income %" stroke="#EF4444" strokeWidth={2} dot={false} />
            <Line type="monotone" dataKey="inflation" name="Inflation %" stroke="#F97316" strokeWidth={2} dot={false} />
            <Line type="monotone" dataKey="acceptance" name="Acceptance %" stroke="#10B981" strokeWidth={2} dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </div>

    </div>
  );
}
