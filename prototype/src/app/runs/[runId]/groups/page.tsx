'use client';

import React, { useState } from 'react';
import { MessageSquare, Send, UserCheck } from 'lucide-react';

const cohorts = [
  {
    id: 1,
    name: 'Rural Farmers',
    population: '140M+',
    desc: 'Heavy reliance on diesel for irrigation and tractors.',
    support: 15, neutral: 25, oppose: 60,
    income: '-12.5%',
    behaviors: ['Delaying purchases of new equipment', 'Switching to lower-yield, lower-input crops', 'Organizing local protests'],
    confidence: 'High'
  },
  {
    id: 2,
    name: 'Truck Operators',
    population: '8M+',
    desc: 'Independent logistics providers and fleet owners.',
    support: 5, neutral: 10, oppose: 85,
    income: '-18.0%',
    behaviors: ['Passing costs to consumers immediately', 'Striking in major transport hubs', 'Defaulting on vehicle loans'],
    confidence: 'High'
  },
  {
    id: 3,
    name: 'Urban Middle Class',
    population: '250M+',
    desc: 'Salaried professionals in metro and Tier 2 cities.',
    support: 45, neutral: 35, oppose: 20,
    income: '-1.5%',
    behaviors: ['Absorbing mild CPI inflation', 'Slight reduction in discretionary spending', 'Supporting fiscal prudence narrative'],
    confidence: 'Medium'
  },
  {
    id: 4,
    name: 'Urban Poor',
    population: '120M+',
    desc: 'Daily wage earners and informal sector workers.',
    support: 20, neutral: 30, oppose: 50,
    income: '-4.8%',
    behaviors: ['Cutting back on nutritious food intake', 'Increased reliance on PDS (ration)', 'Vulnerable to transport cost hikes'],
    confidence: 'High'
  },
  {
    id: 5,
    name: 'Corporate Sector',
    population: 'N/A',
    desc: 'Large manufacturing and service enterprises.',
    support: 70, neutral: 20, oppose: 10,
    income: '+2.1%',
    behaviors: ['Benefiting from macro-economic stability', 'Investing in alternative energy logistics', 'Passing supply chain costs efficiently'],
    confidence: 'Medium'
  }
];

export default function GroupsPage() {
  const [chatInput, setChatInput] = useState('');
  const [messages, setMessages] = useState<{role: 'user'|'ai', text: string}[]>([]);

  const handleSend = () => {
    if (!chatInput.trim()) return;
    
    setMessages([...messages, { role: 'user', text: chatInput }]);
    setChatInput('');
    
    setTimeout(() => {
      setMessages(prev => [...prev, { 
        role: 'ai', 
        text: "Based on the simulation, Rural Farmers will struggle to absorb the immediate 12% rise in input costs. The AI models predict a high likelihood of them demanding increased MSP (Minimum Support Price) to offset the diesel price hike. Without intervention, we model a 12.5% drop in their disposable income within the first harvest cycle." 
      }]);
    }, 1000);
  };

  return (
    <div className="p-6 max-w-7xl mx-auto flex flex-col gap-8">
      <div>
        <h1 className="text-xl font-bold text-white mb-2">Demographic Cohort Analysis</h1>
        <p className="text-sm text-text-secondary">Granular impact on specific population groups</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {cohorts.map((c) => (
          <div key={c.id} className="bg-surface-4 border border-surface-3 rounded-xl p-5 flex flex-col gap-4 hover:border-surface-3/80 transition-colors">
            <div className="flex justify-between items-start">
              <div>
                <h3 className="text-lg font-bold text-white">{c.name}</h3>
                <span className="text-xs text-text-secondary">Pop: {c.population}</span>
              </div>
              <span className="px-2 py-1 bg-surface-2 border border-surface-3 rounded text-xs text-text-muted">
                {c.confidence} Conf
              </span>
            </div>
            
            <p className="text-sm text-text-body min-h-[40px]">{c.desc}</p>
            
            <div>
              <div className="flex justify-between text-xs mb-1">
                <span className="text-india-green">Support {c.support}%</span>
                <span className="text-text-muted">Neu {c.neutral}%</span>
                <span className="text-red-400">Oppose {c.oppose}%</span>
              </div>
              <div className="w-full h-2 rounded-full overflow-hidden flex">
                <div style={{ width: `${c.support}%` }} className="bg-india-green h-full"></div>
                <div style={{ width: `${c.neutral}%` }} className="bg-surface-3 h-full"></div>
                <div style={{ width: `${c.oppose}%` }} className="bg-red-500 h-full"></div>
              </div>
            </div>

            <div className="flex justify-between items-center mt-2 border-t border-surface-3 pt-4">
              <span className="text-sm text-text-secondary">Income Impact:</span>
              <span className={`text-xl font-bold ${c.income.includes('-') ? 'text-red-400' : 'text-india-green'}`}>
                {c.income}
              </span>
            </div>

            <div>
              <span className="text-xs font-semibold text-text-secondary uppercase tracking-wider mb-2 block">Predicted Behaviors</span>
              <ul className="space-y-1.5">
                {c.behaviors.map((b, i) => (
                  <li key={i} className="text-xs text-text-body flex gap-2">
                    <span className="text-accent-blue">•</span> {b}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        ))}
      </div>

      {/* Ask a Group Chat */}
      <div className="mt-8 bg-surface-2 border border-surface-3 rounded-xl p-6">
        <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
          <MessageSquare className="w-5 h-5 text-accent-blue" />
          Query the Simulation
        </h3>
        
        <div className="bg-surface-1 border border-surface-3 rounded-lg h-64 mb-4 p-4 overflow-y-auto flex flex-col gap-4">
          {messages.length === 0 ? (
            <div className="m-auto text-text-muted text-sm text-center">
              Ask how specific cohorts will react or what policies might mitigate their losses.<br/>
              Try: &quot;How will farmers react if we provide a direct cash transfer?&quot;
            </div>
          ) : (
            messages.map((m, i) => (
              <div key={i} className={`flex gap-3 max-w-[80%] ${m.role === 'user' ? 'ml-auto flex-row-reverse' : ''}`}>
                <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${m.role === 'user' ? 'bg-surface-3 text-white' : 'bg-accent-blue/20 text-accent-blue'}`}>
                  {m.role === 'user' ? <UserCheck className="w-4 h-4" /> : <MessageSquare className="w-4 h-4" />}
                </div>
                <div className={`p-3 rounded-lg text-sm ${m.role === 'user' ? 'bg-surface-3 text-white' : 'bg-surface-4 text-text-body border border-surface-3'}`}>
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
            className="flex-1 bg-surface-4 border border-surface-3 rounded-lg px-4 py-2 text-sm text-white focus:outline-none focus:border-accent-blue"
          />
          <button 
            onClick={handleSend}
            className="bg-saffron text-canvas px-4 py-2 rounded-lg flex items-center justify-center hover:bg-saffron-dark transition-colors"
          >
            <Send className="w-4 h-4" />
          </button>
        </div>
      </div>

    </div>
  );
}
