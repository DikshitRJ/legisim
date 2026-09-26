'use client';

import React, { useEffect } from 'react';
import { useRouter, useParams } from 'next/navigation';
import { motion } from 'framer-motion';
import { CheckCircle2, Loader2, AlertCircle } from 'lucide-react';
import { useSimulationProgress } from '@/hooks/useSimulationProgress';
import { useResumeRun } from '@/hooks/useMutations';

const STAGES = [
  { id: 'research', label: 'Research' },
  { id: 'simulation', label: 'Simulation' },
  { id: 'analysis', label: 'Analysis' },
  { id: 'complete', label: 'Complete' },
];

export default function LoadingPage() {
  const router = useRouter();
  const params = useParams();
  const runId = Array.isArray(params.runId) ? params.runId[0] : params.runId;

  const { stage, progress, message, isComplete, isStreaming, error } = useSimulationProgress(runId);
  const { mutate: resumeRun, isPending: isResuming } = useResumeRun(runId);

  useEffect(() => {
    if (isComplete) {
      const timeout = setTimeout(() => {
        router.push(`/runs/${runId}/summary`);
      }, 500); // slight delay for smooth transition
      return () => clearTimeout(timeout);
    }
  }, [isComplete, router, runId]);

  let currentIndex = STAGES.findIndex((s) => s.id === stage);
  if (currentIndex === -1) {
    if (stage === 'paused') {
      if (progress < 33) currentIndex = 0;
      else if (progress < 66) currentIndex = 1;
      else currentIndex = 2;
    } else {
      currentIndex = 0;
    }
  }
  if (isComplete) currentIndex = 3;

  return (
    <div className="flex-1 flex flex-col items-center justify-center p-8 relative overflow-hidden bg-canvas h-screen">
      {/* Background decoration */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-saffron/5 rounded-full blur-[100px] pointer-events-none" />

      <div className="max-w-2xl w-full z-10 flex flex-col items-center gap-8">
        <div className="text-center mb-4">
          <h1 className="text-3xl font-bold text-white mb-2 uppercase tracking-[0.1em]">LEGISIM</h1>
          <p className="text-text-secondary uppercase tracking-widest text-sm">Legislative Simulation Engine</p>
        </div>

        {error ? (
          <div className="p-6 rounded-xl border border-red-500/50 bg-red-500/10 w-full flex flex-col items-center text-center gap-4">
            <AlertCircle className="w-8 h-8 text-red-500" />
            <div>
              <h3 className="text-lg font-semibold text-white mb-1">Simulation Error</h3>
              <p className="text-sm text-text-secondary">{error.message || 'An unexpected error occurred.'}</p>
            </div>
            <button 
              onClick={() => window.location.reload()}
              className="bg-saffron text-canvas uppercase font-bold tracking-wider px-6 py-3 rounded hover:bg-[#E05A1B] transition-colors"
            >
              Retry
            </button>
          </div>
        ) : (
          <div className="p-8 rounded-xl border border-surface-3 bg-surface-2 w-full shadow-lg relative">
            {/* Top Bar Tricolor */}
            <div className="absolute top-0 left-0 right-0 h-1 flex rounded-t-xl overflow-hidden">
              <div className="flex-1 bg-saffron" />
              <div className="flex-1 bg-white" />
              <div className="flex-1 bg-india-green" />
            </div>

            <div className="flex items-center justify-between mb-8 mt-2">
              <div className="flex items-center gap-3">
                {isStreaming ? (
                  <div className="flex items-center gap-2 px-2 py-1 rounded-full bg-red-500/20 border border-red-500/30">
                    <div className="w-2 h-2 rounded-full bg-red-500 animate-pulse" />
                    <span className="text-xs uppercase text-red-500 tracking-wider font-bold">Live</span>
                  </div>
                ) : (
                   stage === 'paused' ? (
                     <div className="flex items-center gap-2 px-2 py-1 rounded-full bg-yellow-500/20 border border-yellow-500/30">
                      <div className="w-2 h-2 rounded-full bg-yellow-500" />
                      <span className="text-xs uppercase text-yellow-500 tracking-wider font-bold">Paused</span>
                    </div>
                   ) : (
                    <div className="flex items-center gap-2 px-2 py-1 rounded-full bg-surface-3 border border-surface-4">
                      <div className="w-2 h-2 rounded-full bg-text-muted" />
                      <span className="text-xs uppercase text-text-muted tracking-wider font-bold">Offline</span>
                    </div>
                   )
                )}
              </div>
              <div className="text-right">
                <span className="text-sm font-mono text-saffron">{Math.round(progress)}%</span>
              </div>
            </div>

            {/* Stage Indicators */}
            <div className="flex justify-between items-center mb-8 relative">
              <div className="absolute left-0 right-0 top-1/2 -translate-y-1/2 h-0.5 bg-surface-3 z-0" />
              {STAGES.map((s, idx) => {
                const isActive = idx === currentIndex;
                const isPast = idx < currentIndex;
                return (
                  <div key={s.id} className="relative z-10 flex flex-col items-center gap-2">
                    <div className={`w-8 h-8 rounded-full flex items-center justify-center border-2 transition-colors duration-300 ${
                      isActive ? 'border-saffron bg-surface-2 text-saffron' : 
                      isPast ? 'border-india-green bg-india-green text-white' : 
                      'border-surface-4 bg-surface-2 text-surface-4'
                    }`}>
                      {isPast ? <CheckCircle2 className="w-5 h-5" /> : (isActive && isStreaming) ? <Loader2 className="w-4 h-4 animate-spin" /> : <div className="w-2 h-2 rounded-full bg-current" />}
                    </div>
                    <span className={`text-xs uppercase tracking-wider absolute top-10 whitespace-nowrap ${isActive ? 'text-saffron font-bold' : isPast ? 'text-text-secondary' : 'text-text-muted'}`}>
                      {s.label}
                    </span>
                  </div>
                );
              })}
            </div>

            {/* Progress Bar */}
            <div className="h-2 w-full bg-surface-4 rounded-full overflow-hidden mt-12 mb-6">
              <motion.div 
                className="h-full bg-saffron"
                initial={{ width: 0 }}
                animate={{ width: `${progress}%` }}
                transition={{ ease: "linear", duration: 0.5 }}
              />
            </div>

            {/* Current Message */}
            <div className="text-center min-h-[40px] flex items-center justify-center">
              <p className="text-sm text-text-secondary animate-pulse">
                {message || "Initializing simulation environment..."}
              </p>
            </div>

            {/* Human Review Checkpoint */}
            {stage === 'paused' && (
              <div className="mt-8 flex justify-center">
                <button
                  onClick={() => resumeRun({ approved: true })}
                  disabled={isResuming}
                  className="bg-saffron text-canvas uppercase font-bold tracking-wider px-8 py-3 rounded hover:bg-[#E05A1B] transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
                >
                  {isResuming ? <Loader2 className="w-5 h-5 animate-spin" /> : <CheckCircle2 className="w-5 h-5" />}
                  Approve & Continue
                </button>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
