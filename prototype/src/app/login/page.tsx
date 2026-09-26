'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function LoginPage() {
  const router = useRouter();
  const [officerId, setOfficerId] = useState('');
  const [password, setPassword] = useState('');

  const handleSignIn = (e: React.FormEvent) => {
    e.preventDefault();
    router.push('/notebooks');
  };

  return (
    <div className="min-h-screen w-full bg-[#0A0A0A] relative flex items-center justify-center overflow-hidden">
      {/* Background Effects */}
      <div className="absolute inset-0 bg-[radial-gradient(#353534_1px,transparent_1px)] [background-size:24px_24px] opacity-20"></div>
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(255,153,51,0.03)_0%,transparent_50%)]"></div>
      
      {/* Top Right Restricted Text */}
      <div className="absolute top-6 right-8 flex flex-col items-end text-right">
        <span className="text-[10px] text-[#A1A1AA] uppercase tracking-[0.2em] font-semibold mb-1">
          SECURE ACCESS LEVEL 4
        </span>
        <span className="text-[10px] text-red-500/80 uppercase tracking-[0.2em] font-bold">
          RESTRICTED PORTAL
        </span>
      </div>

      {/* Login Card */}
      <div className="relative z-10 w-full max-w-[420px] bg-[#1c1b1b] rounded-lg shadow-2xl shadow-black overflow-hidden border border-[#2a2a2a]">
        {/* Tricolor Bar */}
        <div className="h-[3px] w-full flex">
          <div className="flex-1 bg-[#FF9933]"></div>
          <div className="flex-1 bg-white"></div>
          <div className="flex-1 bg-[#138808]"></div>
        </div>

        <div className="p-10">
          <div className="text-center mb-10">
            <h1 className="text-3xl font-bold tracking-[0.22em] text-white uppercase">
              LEGISIM
            </h1>
            <p className="text-[10px] text-[#A1A1AA] uppercase tracking-[0.15em] mt-3">
              Government Policy Simulation Portal
            </p>
          </div>

          <form onSubmit={handleSignIn} className="space-y-6">
            <div className="space-y-2">
              <label className="block text-[10px] text-[#A1A1AA] uppercase tracking-widest font-semibold">
                OFFICER ID / LOGIN ID
              </label>
              <input 
                type="text" 
                value={officerId}
                onChange={(e) => setOfficerId(e.target.value)}
                placeholder="GOI-XXXX-XXXX"
                className="w-full h-11 bg-[#0e0e0e] border border-[#2a2a2a] rounded text-white px-4 focus:outline-none focus:border-[#FF9933] focus:ring-1 focus:ring-[#FF9933] transition-colors placeholder-[#3f3f46] text-sm"
              />
            </div>
            
            <div className="space-y-2">
              <label className="block text-[10px] text-[#A1A1AA] uppercase tracking-widest font-semibold">
                PASSWORD
              </label>
              <input 
                type="password" 
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••••••"
                className="w-full h-11 bg-[#0e0e0e] border border-[#2a2a2a] rounded text-white px-4 focus:outline-none focus:border-[#FF9933] focus:ring-1 focus:ring-[#FF9933] transition-colors placeholder-[#3f3f46] text-sm tracking-widest"
              />
            </div>

            <button 
              type="submit"
              className="w-full h-12 mt-4 bg-[#FF671F] hover:bg-[#E05A1B] text-[#0A0A0A] font-bold uppercase tracking-[0.15em] rounded transition-colors text-sm"
            >
              SIGN IN
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
