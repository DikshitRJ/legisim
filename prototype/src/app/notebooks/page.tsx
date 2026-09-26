'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import Header from '@/components/layout/Header';
import Footer from '@/components/layout/Footer';
import { FolderOpen, Search, ChevronRight, Plus } from 'lucide-react';

const MOCK_NOTEBOOKS = [
  {
    id: 'nb-1',
    title: 'Industry Policy',
    sources: 8,
    time: '2h ago',
    description: 'Analysis of manufacturing incentives and export subsidies for electronics and semiconductor sectors.',
    active: true
  },
  {
    id: 'nb-2',
    title: 'Farmer Loan Policy',
    sources: 4,
    time: 'yesterday',
    description: 'Evaluation of debt relief measures and their impact on rural credit access and agricultural productivity.',
    active: false
  },
  {
    id: 'nb-3',
    title: 'Telecom Regulatory Amendment',
    sources: 6,
    time: '3 days ago',
    description: 'Review of spectrum allocation guidelines and 5G infrastructure deployment framework.',
    active: false
  },
  {
    id: 'nb-4',
    title: 'Digital Personal Data Protection',
    sources: 12,
    time: '5 days ago',
    description: 'Assessment of compliance requirements for cross-border data flows and data fiduciary obligations.',
    active: false
  },
  {
    id: 'nb-5',
    title: 'National Green Hydrogen Framework',
    sources: 5,
    time: '1 week ago',
    description: 'Strategic roadmap for transition to green hydrogen, including production incentives and demand creation.',
    active: false
  }
];

export default function NotebooksPage() {
  const router = useRouter();
  const [searchQuery, setSearchQuery] = useState('');

  const filteredNotebooks = MOCK_NOTEBOOKS.filter(nb => 
    nb.title.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="flex flex-col h-screen w-full bg-[#0A0A0A] overflow-hidden">
      <Header />
      
      <main className="flex flex-1 overflow-hidden">
        {/* Sidebar */}
        <aside className="w-[340px] flex-shrink-0 bg-[#0A0A0A] border-r border-[#2a2a2a] flex flex-col">
          <div className="p-5 border-b border-[#1a1a1a]">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center space-x-2">
                <FolderOpen className="w-5 h-5 text-[#FF9933]" />
                <h2 className="text-base font-semibold text-white">All Notebooks</h2>
              </div>
              <span className="text-[10px] font-bold bg-[#121212] text-[#60A5FA] px-2 py-0.5 rounded border border-[#1e1e1e]">
                5 STORED
              </span>
            </div>
            
            <div className="relative">
              <Search className="w-4 h-4 text-[#71717A] absolute left-3 top-1/2 transform -translate-y-1/2" />
              <input
                type="text"
                placeholder="Filter notebooks..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full bg-[#121212] border border-[#2a2a2a] rounded-md py-2 pl-9 pr-3 text-sm text-white placeholder-[#71717A] focus:outline-none focus:border-[#3B82F6] transition-colors"
              />
            </div>
          </div>
          
          <div className="flex-1 overflow-y-auto overflow-x-hidden">
            {filteredNotebooks.map((nb, i) => (
              <div 
                key={nb.id}
                className={`group relative p-4 border-b border-[#1a1a1a] cursor-pointer transition-colors ${
                  nb.active ? 'bg-[#121212]' : 'hover:bg-[#121212]'
                }`}
              >
                {nb.active && (
                  <div className="absolute left-0 top-0 bottom-0 w-1 bg-[#FF9933]"></div>
                )}
                
                <div className="flex justify-between items-start mb-1.5">
                  <h3 className="text-[15px] font-semibold text-white pr-2 truncate">{nb.title}</h3>
                  <ChevronRight className={`w-4 h-4 text-[#71717A] flex-shrink-0 opacity-0 group-hover:opacity-100 transition-opacity ${nb.active ? 'opacity-100' : ''}`} />
                </div>
                
                <div className="flex items-center space-x-2 mb-2">
                  <span className="text-[9px] uppercase tracking-wider font-bold bg-[#0e0e0e] text-[#60A5FA] px-1.5 py-0.5 rounded border border-[#1a1a1a]">
                    {nb.sources} SOURCES
                  </span>
                  <span className="text-xs text-[#60A5FA] opacity-80">{nb.time}</span>
                </div>
                
                <p className="text-xs text-[#A1A1AA] line-clamp-2 leading-relaxed">
                  {nb.description}
                </p>
              </div>
            ))}
          </div>
        </aside>

        {/* Main Content */}
        <section className="flex-1 flex items-center justify-center bg-[#0A0A0A] p-8">
          <div className="max-w-lg w-full bg-[#121212] rounded-xl border border-[#2a2a2a] p-10 flex flex-col items-center text-center shadow-lg hover:shadow-xl transition-shadow">
            <div className="w-20 h-20 rounded-full bg-[#1e1e1e] border border-[#2a2a2a] flex items-center justify-center mb-6">
              <Plus className="w-8 h-8 text-[#FF9933]" />
            </div>
            
            <h2 className="text-2xl font-bold text-white mb-3">
              Create New Notebook
            </h2>
            
            <p className="text-[#A1A1AA] text-sm mb-8 leading-relaxed max-w-md">
              Upload bills, acts, gazettes, or research documents to begin sovereign analysis and synthesis.
            </p>
            
            <button 
              onClick={() => router.push('/notebooks/nb-1/new')}
              className="bg-[#FF9933] hover:bg-[#E05A1B] text-[#0A0A0A] font-bold text-sm uppercase tracking-widest px-8 py-3.5 rounded transition-colors"
            >
              + ADD NOTEBOOK
            </button>
          </div>
        </section>
      </main>
      
      <Footer />
    </div>
  );
}
