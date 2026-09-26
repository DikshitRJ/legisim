'use client';

import React, { useState } from 'react';
import { usePathname, useParams } from 'next/navigation';
import Link from 'next/link';
import Header from '@/components/layout/Header';
import ProtectedRoute from '@/components/layout/ProtectedRoute';
import { Filter, Calendar, MapPin, Briefcase } from 'lucide-react';

export default function RunLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const params = useParams();
  const runId = params.runId as string;
  const [timeValue, setTimeValue] = useState(6); // Default month 6

  if (pathname.includes('/loading')) {
    return (
      <ProtectedRoute>
      <div className="min-h-screen bg-canvas text-text-body flex flex-col font-sans">
        {children}
      </div>
      </ProtectedRoute>
    );
  }

  const tabs = [
    { label: 'Summary', path: `/runs/${runId}/summary` },
    { label: 'Dashboard', path: `/runs/${runId}/dashboard` },
    { label: 'Ripple Explorer', path: `/runs/${runId}/ripple` },
    { label: 'Map', path: `/runs/${runId}/map` },
    { label: 'Timeline', path: `/runs/${runId}/time` },
    { label: 'Groups', path: `/runs/${runId}/groups` },
  ];

  return (
    <ProtectedRoute>
    <div className="min-h-screen bg-canvas text-text-body flex flex-col font-sans overflow-hidden">
      <Header />
      
      {/* Tabs */}
      <div className="bg-surface-1 border-b border-surface-3 h-12 flex items-center px-6 shrink-0">
        <nav className="flex items-center gap-8 h-full">
          {tabs.map(tab => {
            const isActive = pathname === tab.path;
            return (
              <Link 
                key={tab.path} 
                href={tab.path}
                className={`relative h-full flex items-center text-sm font-medium transition-colors ${
                  isActive ? 'text-saffron' : 'text-text-secondary hover:text-white'
                }`}
              >
                {tab.label}
                {isActive && (
                  <span className="absolute bottom-0 left-0 w-full h-[2px] bg-saffron rounded-t-full" />
                )}
              </Link>
            );
          })}
        </nav>
      </div>

      {/* Global Controls - Only if not time page which has its own time controls */}
      {!pathname.includes('/time') && (
        <div className="bg-surface-2 border-b border-surface-3 px-6 py-3 flex items-center justify-between shrink-0">
          <div className="flex items-center gap-4 flex-1 max-w-2xl">
            <span className="text-xs font-semibold text-text-muted uppercase tracking-wider w-20">Timeline</span>
            <input 
              type="range" 
              min="0" max="12" 
              value={timeValue}
              onChange={(e) => setTimeValue(parseInt(e.target.value))}
              className="flex-1 h-1.5 bg-surface-4 rounded-lg appearance-none cursor-pointer accent-saffron"
            />
            <div className="bg-surface-4 px-3 py-1 rounded border border-surface-3 flex items-center gap-2 min-w-[100px] justify-center">
              <Calendar className="w-3.5 h-3.5 text-accent-blue" />
              <span className="text-sm font-medium text-white">Month {timeValue}</span>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <Filter className="w-4 h-4 text-text-muted" />
            <div className="flex items-center gap-2">
              <button className="px-3 py-1 rounded-full bg-surface-4 border border-surface-3 text-xs font-medium text-text-secondary hover:text-white transition-colors flex items-center gap-1.5">
                <MapPin className="w-3 h-3" /> All Regions
              </button>
              <button className="px-3 py-1 rounded-full bg-surface-4 border border-surface-3 text-xs font-medium text-text-secondary hover:text-white transition-colors flex items-center gap-1.5">
                <Briefcase className="w-3 h-3" /> All Sectors
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Main Content Area */}
      <main className="flex-1 overflow-auto">
        {children}
      </main>
    </div>
    </ProtectedRoute>
  );
}
