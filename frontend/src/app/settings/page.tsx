'use client';

import React from 'react';
import Header from '@/components/layout/Header';
import { Download, FileText, Presentation, Link as LinkIcon, Settings as SettingsIcon, Bell } from 'lucide-react';

export default function SettingsPage() {
  return (
    <div className="min-h-screen bg-canvas text-text-body flex flex-col font-sans">
      <Header />
      
      <div className="p-8 max-w-4xl mx-auto w-full flex flex-col gap-10">
        
        {/* Profile */}
        <div>
          <h1 className="text-2xl font-bold text-white mb-6">Account & Settings</h1>
          <div className="bg-surface-2 border border-surface-3 rounded-xl p-6 flex items-center gap-6">
            <div className="w-20 h-20 rounded-full bg-surface-4 border border-surface-3 flex items-center justify-center text-2xl font-bold text-white">
              DR
            </div>
            <div>
              <h2 className="text-xl font-bold text-white">Dir. Rajesh Verma</h2>
              <p className="text-text-secondary mb-2">JOINT SECRETARY, MEITY</p>
              <div className="flex gap-2">
                <span className="px-2 py-1 bg-surface-4 border border-surface-3 rounded text-xs">Clearance: Level 4</span>
                <span className="px-2 py-1 bg-surface-4 border border-surface-3 rounded text-xs">Dept: Economic Affairs</span>
              </div>
            </div>
          </div>
        </div>

        {/* Export */}
        <div>
          <h2 className="text-lg font-bold text-white mb-4">Export Current Simulation</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <button className="bg-surface-2 border border-surface-3 rounded-xl p-5 flex items-start gap-4 hover:border-saffron transition-colors text-left group">
              <div className="w-10 h-10 rounded-lg bg-red-500/10 text-red-400 flex items-center justify-center shrink-0">
                <FileText className="w-5 h-5" />
              </div>
              <div>
                <h3 className="text-white font-semibold group-hover:text-saffron transition-colors">Executive PDF Report</h3>
                <p className="text-sm text-text-secondary mt-1">Detailed 15-page brief formatted for minister-level review.</p>
              </div>
            </button>

            <button className="bg-surface-2 border border-surface-3 rounded-xl p-5 flex items-start gap-4 hover:border-saffron transition-colors text-left group">
              <div className="w-10 h-10 rounded-lg bg-green-500/10 text-green-400 flex items-center justify-center shrink-0">
                <Download className="w-5 h-5" />
              </div>
              <div>
                <h3 className="text-white font-semibold group-hover:text-saffron transition-colors">Raw CSV Data</h3>
                <p className="text-sm text-text-secondary mt-1">Time-series data for all metrics across 12 months.</p>
              </div>
            </button>

            <button className="bg-surface-2 border border-surface-3 rounded-xl p-5 flex items-start gap-4 hover:border-saffron transition-colors text-left group">
              <div className="w-10 h-10 rounded-lg bg-blue-500/10 text-blue-400 flex items-center justify-center shrink-0">
                <Presentation className="w-5 h-5" />
              </div>
              <div>
                <h3 className="text-white font-semibold group-hover:text-saffron transition-colors">Slide Deck (PPTX)</h3>
                <p className="text-sm text-text-secondary mt-1">Auto-generated presentation with charts and key takeaways.</p>
              </div>
            </button>

            <button className="bg-surface-2 border border-surface-3 rounded-xl p-5 flex items-start gap-4 hover:border-saffron transition-colors text-left group">
              <div className="w-10 h-10 rounded-lg bg-purple-500/10 text-purple-400 flex items-center justify-center shrink-0">
                <LinkIcon className="w-5 h-5" />
              </div>
              <div>
                <h3 className="text-white font-semibold group-hover:text-saffron transition-colors">Shareable Link</h3>
                <p className="text-sm text-text-secondary mt-1">Generate a secure read-only link for inter-department sharing.</p>
              </div>
            </button>
          </div>
        </div>

        {/* Preferences */}
        <div>
          <h2 className="text-lg font-bold text-white mb-4">Preferences</h2>
          <div className="bg-surface-2 border border-surface-3 rounded-xl p-6 space-y-6">
            <div className="flex items-center justify-between">
              <div className="flex gap-3">
                <Bell className="w-5 h-5 text-text-muted mt-0.5" />
                <div>
                  <div className="text-white font-medium">Email Notifications</div>
                  <div className="text-sm text-text-secondary">Receive alerts when long simulations complete.</div>
                </div>
              </div>
              <div className="w-12 h-6 bg-saffron rounded-full relative cursor-pointer">
                <div className="absolute right-1 top-1 w-4 h-4 bg-white rounded-full"></div>
              </div>
            </div>

            <div className="w-full h-px bg-surface-3"></div>

            <div className="flex items-center justify-between">
              <div className="flex gap-3">
                <SettingsIcon className="w-5 h-5 text-text-muted mt-0.5" />
                <div>
                  <div className="text-white font-medium">Advanced AI Models</div>
                  <div className="text-sm text-text-secondary">Use experimental reasoning models (may increase sim time).</div>
                </div>
              </div>
              <div className="w-12 h-6 bg-surface-4 border border-surface-3 rounded-full relative cursor-pointer">
                <div className="absolute left-1 top-1 w-4 h-4 bg-text-muted rounded-full"></div>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}
