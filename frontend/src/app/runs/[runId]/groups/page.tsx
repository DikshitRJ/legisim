'use client';

import React, { useState, useMemo } from 'react';
import { useParams } from 'next/navigation';
import { MessageSquare, Send, UserCheck, ArrowDownRight, ArrowUpRight, Filter } from 'lucide-react';
import { useRunGroups } from '@/hooks/useQueries';
import { motion, AnimatePresence } from 'framer-motion';
import { Confidence } from '@/lib/api/types';

export default function GroupsPage() {
  const params = useParams();
  const runId = params.runId as string;
  
  const { data: groups, isLoading, error } = useRunGroups(runId);
  
  const [chatInput, setChatInput] = useState('');
  const [messages, setMessages] = useState<{role: 'user'|'ai', text: string}[]>([]);
  const [confidenceFilter, setConfidenceFilter] = useState<Confidence | 'All'>('All');
  
  const handleSend = () => {
    if (!chatInput.trim()) return;
    
    setMessages([...messages, { role: 'user', text: chatInput }]);
    setChatInput('');
    
    setTimeout(() => {
      setMessages(prev => [...prev, { 
        role: 'ai', 
        text: "Based on the simulation, this group will struggle to absorb the immediate changes. The AI models predict a high likelihood of them demanding interventions to offset the impact." 
      }]);
    }, 1000);
  };

  const filteredAndSortedGroups = useMemo(() => {
    if (!groups) return [];
    
    let result = [...groups];
    
    if (confidenceFilter !== 'All') {
      result = result.filter(g => g.confidence === confidenceFilter);
    }
    
    // Sort by income impact (most negative first)
    result.sort((a, b) => a.incomeChange - b.incomeChange);
    
    return result;
  }, [groups, confidenceFilter]);

  if (error) {
    return (
      <div className="p-6 max-w-7xl mx-auto flex flex-col gap-8">
        <div className="bg-red-500/10 border border-red-500/20 text-red-400 p-4 rounded-xl">
          Error loading groups data. Please try again.
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 max-w-7xl mx-auto flex flex-col gap-8">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-end gap-4">
        <div>
          <h1 className="text-xl font-bold text-white mb-2">Demographic Cohort Analysis</h1>
          <p className="text-sm text-zinc-400">Granular impact on specific population groups</p>
        </div>
        
        <div className="flex items-center gap-2">
          <Filter className="w-4 h-4 text-zinc-500" />
          <span className="text-sm text-zinc-400 mr-2 uppercase tracking-wide">Confidence:</span>
          <div className="flex bg-[#121212] border border-[#2A2A2A] rounded p-1">
            {['All', 'High', 'Medium', 'Low'].map(level => (
              <button
                key={level}
                onClick={() => setConfidenceFilter(level as any)}
                className={`px-3 py-1 text-xs font-bold uppercase tracking-wide rounded ${
                  confidenceFilter === level 
                    ? 'bg-[#FF671F] text-[#0A0A0A]' 
                    : 'text-[#A1A1AA] hover:text-white'
                } transition-colors`}
              >
                {level}
              </button>
            ))}
          </div>
        </div>
      </div>

      {isLoading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="bg-[#121212] border border-[#2A2A2A] rounded-lg p-5 flex flex-col gap-4 animate-pulse">
              <div className="flex justify-between items-start">
                <div className="space-y-2">
                  <div className="h-5 w-40 bg-[#2A2A2A] rounded"></div>
                  <div className="h-3 w-20 bg-[#2A2A2A] rounded"></div>
                </div>
                <div className="h-6 w-16 bg-[#2A2A2A] rounded"></div>
              </div>
              <div className="h-10 w-full bg-[#2A2A2A] rounded"></div>
              <div className="h-12 w-full bg-[#2A2A2A] rounded"></div>
              <div className="h-8 w-full bg-[#2A2A2A] rounded"></div>
            </div>
          ))}
        </div>
      ) : filteredAndSortedGroups.length === 0 ? (
        <div className="bg-[#121212] border border-[#2A2A2A] rounded-lg p-12 flex flex-col items-center justify-center text-center">
          <UserCheck className="w-12 h-12 text-[#71717A] mb-4" />
          <h3 className="text-lg font-bold text-[#E5E2E1] mb-2">No Cohorts Found</h3>
          <p className="text-[#A1A1AA] text-sm max-w-md">
            {confidenceFilter !== 'All' 
              ? `No groups match the ${confidenceFilter} confidence filter.`
              : "No cohort group data available for this simulation run."}
          </p>
          {confidenceFilter !== 'All' && (
            <button 
              onClick={() => setConfidenceFilter('All')}
              className="mt-4 px-4 py-2 bg-[#FF671F] text-[#0A0A0A] uppercase tracking-wide text-sm font-bold rounded hover:bg-[#E05A1B] transition-colors"
            >
              Clear Filters
            </button>
          )}
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <AnimatePresence>
            {filteredAndSortedGroups.map((c, idx) => (
              <motion.div 
                layout
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, scale: 0.95 }}
                transition={{ duration: 0.2, delay: idx * 0.05 }}
                key={c.id} 
                className="bg-[#121212] border border-[#2A2A2A] rounded-lg p-5 flex flex-col gap-4 hover:border-[#3F3F46] transition-colors relative overflow-hidden"
              >
                {/* Tricolor top bar decoration */}
                <div className="absolute top-0 left-0 right-0 h-1 flex">
                  <div className="flex-1 bg-[#FF671F]"></div>
                  <div className="flex-1 bg-white"></div>
                  <div className="flex-1 bg-[#046A38]"></div>
                </div>
                
                <div className="flex justify-between items-start mt-1">
                  <div>
                    <h3 className="text-lg font-bold text-[#E5E2E1]">{c.name}</h3>
                    <span className="text-xs text-[#A1A1AA] uppercase tracking-wider">Pop: {c.population}</span>
                  </div>
                  <span className={`px-2 py-1 bg-[#1E1E1E] border border-[#2A2A2A] rounded text-[10px] font-bold uppercase tracking-wider ${
                    c.confidence === 'High' ? 'text-[#046A38]' : 
                    c.confidence === 'Low' ? 'text-[#FF671F]' : 
                    'text-[#A1A1AA]'
                  }`}>
                    {c.confidence} Conf
                  </span>
                </div>
                
                <p className="text-sm text-[#E5E2E1] min-h-[40px]">{c.description}</p>
                
                <div>
                  <div className="flex justify-between text-[10px] font-bold uppercase tracking-wider mb-1.5">
                    <span className="text-[#046A38]">Support {c.stance.support}%</span>
                    <span className="text-[#71717A]">Neutral {c.stance.neutral}%</span>
                    <span className="text-[#FF671F]">Oppose {c.stance.oppose}%</span>
                  </div>
                  <div className="w-full h-2 rounded overflow-hidden flex">
                    <div style={{ width: `${c.stance.support}%` }} className="bg-[#046A38] h-full transition-all duration-500"></div>
                    <div style={{ width: `${c.stance.neutral}%` }} className="bg-[#3F3F46] h-full transition-all duration-500"></div>
                    <div style={{ width: `${c.stance.oppose}%` }} className="bg-[#FF671F] h-full transition-all duration-500"></div>
                  </div>
                </div>

                <div className="flex justify-between items-center mt-2 border-t border-[#2A2A2A] pt-4">
                  <span className="text-xs font-bold text-[#A1A1AA] uppercase tracking-wider">Income Impact:</span>
                  <div className={`flex items-center gap-1 text-xl font-bold ${c.incomeChange < 0 ? 'text-[#FF671F]' : c.incomeChange > 0 ? 'text-[#046A38]' : 'text-[#A1A1AA]'}`}>
                    {c.incomeChange < 0 ? <ArrowDownRight className="w-5 h-5" /> : c.incomeChange > 0 ? <ArrowUpRight className="w-5 h-5" /> : null}
                    {c.incomeChange > 0 ? '+' : ''}{c.incomeChange}%
                  </div>
                </div>

                <div className="pt-2">
                  <span className="text-[10px] font-bold text-[#71717A] uppercase tracking-wider mb-3 block">Predicted Behaviors</span>
                  <div className="flex flex-wrap gap-2">
                    {c.behaviors.map((b, i) => (
                      <span key={i} className="text-xs text-[#E5E2E1] bg-[#1E1E1E] border border-[#2A2A2A] rounded px-2.5 py-1">
                        {b}
                      </span>
                    ))}
                  </div>
                </div>
              </motion.div>
            ))}
          </AnimatePresence>
        </div>
      )}

      {/* Ask a Group Chat */}
      <div className="mt-8 bg-[#121212] border border-[#2A2A2A] rounded-lg p-6 relative overflow-hidden">
        {/* Tricolor top bar decoration */}
        <div className="absolute top-0 left-0 right-0 h-1 flex">
          <div className="flex-1 bg-[#FF671F]"></div>
          <div className="flex-1 bg-white"></div>
          <div className="flex-1 bg-[#046A38]"></div>
        </div>
        
        <h3 className="text-lg font-bold text-[#E5E2E1] mb-4 flex items-center gap-2 mt-1">
          <MessageSquare className="w-5 h-5 text-[#FF671F]" />
          Query the Simulation
        </h3>
        
        <div className="bg-[#0A0A0A] border border-[#2A2A2A] rounded-lg h-64 mb-4 p-4 overflow-y-auto flex flex-col gap-4">
          {messages.length === 0 ? (
            <div className="m-auto text-[#71717A] text-sm text-center">
              Ask how specific cohorts will react or what policies might mitigate their losses.<br/>
              Try: &quot;How will farmers react if we provide a direct cash transfer?&quot;
            </div>
          ) : (
            messages.map((m, i) => (
              <div key={i} className={`flex gap-3 max-w-[80%] ${m.role === 'user' ? 'ml-auto flex-row-reverse' : ''}`}>
                <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${m.role === 'user' ? 'bg-[#1E1E1E] text-[#E5E2E1]' : 'bg-[#002868]/20 text-[#002868]'}`}>
                  {m.role === 'user' ? <UserCheck className="w-4 h-4" /> : <MessageSquare className="w-4 h-4" />}
                </div>
                <div className={`p-3 rounded text-sm ${m.role === 'user' ? 'bg-[#1E1E1E] text-[#E5E2E1]' : 'bg-[#121212] text-[#E5E2E1] border border-[#2A2A2A]'}`}>
                  {m.text}
                </div>
              </div>
            ))
          )}
        </div>

        <div className="flex gap-2">
          <input 
            type="text" 
            value={chatInput}
            onChange={(e) => setChatInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
            placeholder="Ask about a group's reaction..." 
            className="flex-1 bg-[#121212] border border-[#2A2A2A] rounded px-4 py-2 text-sm text-[#E5E2E1] focus:outline-none focus:border-[#FF671F] focus:ring-1 focus:ring-[#FF671F] h-12"
          />
          <button 
            onClick={handleSend}
            className="bg-[#FF671F] text-[#0A0A0A] px-6 rounded flex items-center justify-center hover:bg-[#E05A1B] transition-colors h-12 uppercase tracking-wide font-bold text-sm"
          >
            <Send className="w-4 h-4" />
          </button>
        </div>
      </div>

    </div>
  );
}
