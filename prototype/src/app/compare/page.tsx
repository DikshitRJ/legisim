'use client';

import React from 'react';
import Header from '@/components/layout/Header';
import { ArrowRight, CheckCircle2, XCircle } from 'lucide-react';

export default function ComparePage() {
  return (
    <div className="min-h-screen bg-canvas text-text-body flex flex-col font-sans">
      <Header />
      
      <div className="p-8 max-w-6xl mx-auto w-full">
        <h1 className="text-2xl font-bold text-white mb-6">Scenario Comparison</h1>
        
        <div className="grid grid-cols-3 gap-6 mb-8">
          {/* Header Column */}
          <div className="pt-20 space-y-8">
            <div className="h-12 flex items-center font-semibold text-text-secondary">Policy Variant</div>
            <div className="h-12 flex items-center font-semibold text-text-secondary">Fiscal Savings</div>
            <div className="h-12 flex items-center font-semibold text-text-secondary">Public Acceptance</div>
            <div className="h-12 flex items-center font-semibold text-text-secondary">Poorest 20% Income</div>
            <div className="h-12 flex items-center font-semibold text-text-secondary">Logistics Disruption Risk</div>
          </div>

          {/* Scenario A */}
          <div className="bg-surface-2 border border-surface-3 rounded-xl p-6 shadow-lg">
            <div className="mb-6 pb-4 border-b border-surface-3">
              <span className="text-xs font-bold text-text-muted uppercase tracking-widest mb-1 block">Baseline</span>
              <h2 className="text-xl font-bold text-white">Sudden Subsidy Removal</h2>
              <p className="text-sm text-text-secondary mt-2">Current simulation without mitigation.</p>
            </div>
            
            <div className="space-y-8">
              <div className="h-12 flex items-center text-xl font-bold text-india-green">
                ₹1.3L Cr
                <CheckCircle2 className="w-5 h-5 ml-2" />
              </div>
              <div className="h-12 flex items-center text-xl font-bold text-red-400">
                34%
                <XCircle className="w-5 h-5 ml-2" />
              </div>
              <div className="h-12 flex items-center text-xl font-bold text-red-400">
                -8.5%
                <XCircle className="w-5 h-5 ml-2" />
              </div>
              <div className="h-12 flex items-center text-xl font-bold text-red-400">
                High (85%)
                <XCircle className="w-5 h-5 ml-2" />
              </div>
            </div>
          </div>

          {/* Scenario B */}
          <div className="bg-surface-2 border-2 border-saffron rounded-xl p-6 shadow-lg relative">
            <div className="absolute -top-3 left-1/2 -translate-x-1/2 bg-saffron text-canvas text-xs font-bold px-3 py-1 rounded-full">
              RECOMMENDED
            </div>
            <div className="mb-6 pb-4 border-b border-surface-3">
              <span className="text-xs font-bold text-text-muted uppercase tracking-widest mb-1 block">Alternative</span>
              <h2 className="text-xl font-bold text-white">Removal + Targeted DBT</h2>
              <p className="text-sm text-text-secondary mt-2">Provides Direct Benefit Transfer to vulnerable cohorts.</p>
            </div>
            
            <div className="space-y-8">
              <div className="h-12 flex items-center text-xl font-bold text-amber-500">
                ₹0.8L Cr
              </div>
              <div className="h-12 flex items-center text-xl font-bold text-india-green">
                62%
                <CheckCircle2 className="w-5 h-5 ml-2" />
              </div>
              <div className="h-12 flex items-center text-xl font-bold text-india-green">
                +1.2%
                <CheckCircle2 className="w-5 h-5 ml-2" />
              </div>
              <div className="h-12 flex items-center text-xl font-bold text-amber-500">
                Medium (40%)
              </div>
            </div>
          </div>
        </div>
        
        <div className="flex justify-end">
          <button className="bg-saffron text-canvas px-6 py-3 rounded-lg font-bold flex items-center gap-2 hover:bg-saffron-dark transition-colors">
            Run Detailed Simulation for Alternative <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
}
