'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import Header from '@/components/layout/Header';
import Footer from '@/components/layout/Footer';
import { Check, NotebookPen, RotateCcw, ArrowRight } from 'lucide-react';

const CATEGORIES = [
  {
    id: 1,
    title: 'Population & Age Groups',
    options: ['Child (0-6)', 'Adolescents (7-14)', 'Youth (15-24)', 'Active Productive (25-59)', 'Elderly (60+)']
  },
  {
    id: 2,
    title: 'Income Groups',
    options: ['Wealth Quintiles', 'Housing Integrity', 'Household Amenities']
  },
  {
    id: 3,
    title: 'Occupations',
    options: ['Main Workers', 'Marginal Workers', 'Non-Workers', 'Cultivators', 'Agricultural Labourers', 'Household Industry Workers', 'Other Workers']
  },
  {
    id: 4,
    title: 'Urban vs. Rural',
    options: ['Rural Revenue Villages', 'Statutory Towns', 'Census Towns']
  },
  {
    id: 5,
    title: 'Education & Literacy',
    options: ['Literate', 'Illiterate', 'Without level', 'Primary', 'Middle', 'Secondary', 'Higher Secondary', 'Diploma', 'Graduate+']
  },
  {
    id: 6,
    title: 'Social Attitudes',
    options: ['Migration Patterns', 'Fertility Trends', 'Household Dynamics', 'SC/ST', 'Religious Affiliations']
  }
];

export default function SetupWizardPage() {
  const router = useRouter();
  const [selectedPills, setSelectedPills] = useState<Record<string, boolean>>({});
  const [notes, setNotes] = useState('');

  const togglePill = (option: string) => {
    setSelectedPills(prev => ({
      ...prev,
      [option]: !prev[option]
    }));
  };

  const resetSelections = () => {
    setSelectedPills({});
    setNotes('');
  };

  const handleProceed = () => {
    router.push('/runs/demo-run-1/loading');
  };

  return (
    <div className="flex flex-col min-h-screen w-full bg-[#0A0A0A] overflow-x-hidden">
      <Header showNav={true} />
      
      <main className="flex-1 w-full max-w-5xl mx-auto px-6 py-8 flex flex-col space-y-6">
        {/* Header Title */}
        <div className="mb-2">
          <h1 className="text-2xl font-bold text-white mb-2">Simulation Configuration</h1>
          <p className="text-[#A1A1AA] text-sm">Define the cohort demographics and policy constraints for the simulation engine.</p>
        </div>

        {/* Categories Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {CATEGORIES.map((category) => (
            <div key={category.id} className="bg-[#161616] border border-[#2a2a2a] rounded-xl p-5 shadow-sm">
              <div className="flex items-center space-x-3 mb-4">
                <div className="w-7 h-7 rounded-md bg-[#1e293b] text-[#60A5FA] font-bold font-mono flex items-center justify-center text-sm border border-[#2a3a5a]">
                  {category.id}
                </div>
                <h2 className="text-base font-semibold text-white">{category.title}</h2>
              </div>
              
              <div className="flex flex-wrap gap-2.5">
                {category.options.map(option => {
                  const isActive = !!selectedPills[option];
                  return (
                    <button
                      key={option}
                      onClick={() => togglePill(option)}
                      className={`flex items-center space-x-1.5 px-3.5 py-2 rounded-lg text-sm font-medium transition-colors border ${
                        isActive 
                          ? 'bg-[#1e293b] text-[#60A5FA] border-[#3B82F6]/30' 
                          : 'bg-[#111111] text-[#cbd5e1] border-[#242424] hover:border-[#3a3a3a] hover:bg-[#1a1a1a]'
                      }`}
                    >
                      <Check className={`w-3.5 h-3.5 ${isActive ? 'text-[#60A5FA]' : 'text-transparent'}`} />
                      <span>{option}</span>
                    </button>
                  );
                })}
              </div>
            </div>
          ))}
        </div>

        {/* Policy Notes */}
        <div className="bg-[#161616] border border-[#2a2a2a] rounded-xl p-5 shadow-sm mt-2">
          <div className="flex items-center space-x-2 mb-2">
            <NotebookPen className="w-5 h-5 text-[#A1A1AA]" />
            <h2 className="text-base font-semibold text-white">Policy Notes & Additional Constraints</h2>
          </div>
          <p className="text-[#71717A] text-xs mb-4">
            Specify custom exclusions, temporal conditions, or other domain-specific parameters.
          </p>
          <textarea
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
            placeholder="E.g., Exclude coastal statutory towns; Focus only on households below 30th percentile wealth..."
            className="w-full bg-[#111111] border border-[#2a2a2a] rounded-lg p-4 text-sm text-[#E5E7EB] placeholder-[#3f3f46] focus:outline-none focus:border-[#3B82F6] focus:ring-1 focus:ring-[#3B82F6] transition-colors resize-none"
            rows={5}
          />
        </div>

        {/* Action Bar */}
        <div className="bg-[#161616] border border-[#2a2a2a] rounded-xl p-5 shadow-sm mt-4 flex flex-col sm:flex-row items-center justify-between">
          <div className="flex items-center space-x-3 mb-4 sm:mb-0">
            <div className="w-2.5 h-2.5 rounded-full bg-[#046A38] shadow-[0_0_8px_#046A38] animate-pulse"></div>
            <span className="font-mono text-[11px] text-[#A1A1AA] uppercase tracking-wider">
              PORTAL_STATUS: <span className="text-[#046A38] font-bold">READY FOR INGESTION</span>
            </span>
          </div>
          
          <div className="flex items-center space-x-4 w-full sm:w-auto">
            <button 
              onClick={resetSelections}
              className="flex items-center justify-center space-x-2 px-4 py-2.5 rounded text-sm text-[#A1A1AA] hover:text-white hover:bg-[#2a2a2a] transition-colors w-full sm:w-auto"
            >
              <RotateCcw className="w-4 h-4" />
              <span>Reset Selections</span>
            </button>
            <button 
              onClick={handleProceed}
              className="flex items-center justify-center space-x-2 px-6 py-2.5 rounded bg-[#2563EB] hover:bg-[#1D4ED8] text-white font-bold text-sm transition-colors w-full sm:w-auto"
            >
              <span>Proceed / Save Cohort</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>
        
      </main>
      
      <Footer />
    </div>
  );
}
