'use client';

import React, { useEffect, useState } from 'react';
import { useRouter, useParams } from 'next/navigation';
import { motion, AnimatePresence } from 'framer-motion';
import { Database, Cpu, FileText, CheckCircle2, Loader2 } from 'lucide-react';

const sources = [
  "Census 2011 population data",
  "PLFS employment survey 2023",
  "RBI inflation reports",
  "Ministry of Petroleum pricing data",
  "NSSO consumption expenditure survey",
  "Transport sector operational costs",
];

export default function LoadingPage() {
  const router = useRouter();
  const params = useParams();
  const runId = params.runId;

  const [stage, setStage] = useState(0); // 0: Research, 1: Simulation, 2: Analysis, 3: Done
  const [activeSources, setActiveSources] = useState<string[]>([]);
  const [cohortsDone, setCohortsDone] = useState(0);

  useEffect(() => {
    // Stage 0: Research (0 - 3s)
    let sourceIndex = 0;
    const sourceInterval = setInterval(() => {
      if (sourceIndex < sources.length) {
        setActiveSources(prev => [...prev, sources[sourceIndex]]);
        sourceIndex++;
      }
    }, 400);

    const stage1Timeout = setTimeout(() => {
      clearInterval(sourceInterval);
      setStage(1);
    }, 3000);

    // Stage 1: Simulation (3 - 6s)
    let cohortInterval: NodeJS.Timeout;
    const stage2Timeout = setTimeout(() => {
      cohortInterval = setInterval(() => {
        setCohortsDone(prev => {
          if (prev >= 2000) {
            clearInterval(cohortInterval);
            return 2000;
          }
          return prev + Math.floor(Math.random() * 200) + 50;
        });
      }, 100);
    }, 3000);

    const stage3Timeout = setTimeout(() => {
      clearInterval(cohortInterval);
      setCohortsDone(2000);
      setStage(2);
    }, 6000);

    // Stage 2: Analysis (6 - 8s)
    const doneTimeout = setTimeout(() => {
      setStage(3);
    }, 8000);

    const redirectTimeout = setTimeout(() => {
      router.push(`/runs/${runId}/summary`);
    }, 9000);

    return () => {
      clearInterval(sourceInterval);
      clearInterval(cohortInterval);
      clearTimeout(stage1Timeout);
      clearTimeout(stage2Timeout);
      clearTimeout(stage3Timeout);
      clearTimeout(doneTimeout);
      clearTimeout(redirectTimeout);
    };
  }, [runId, router]);

  return (
    <div className="flex-1 flex flex-col items-center justify-center p-8 relative overflow-hidden bg-canvas h-screen">
      
      {/* Background decoration */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-saffron/5 rounded-full blur-[100px] pointer-events-none" />

      <div className="max-w-2xl w-full z-10 flex flex-col gap-8">
        <div className="text-center mb-4">
          <h1 className="text-3xl font-bold text-white mb-2">Simulating Policy Impact</h1>
          <p className="text-text-secondary">Diesel Subsidy Removal • 12 Month Projection</p>
        </div>

        {/* Stage 1: Research */}
        <div className={`p-6 rounded-xl border transition-colors duration-500 ${stage >= 0 ? 'bg-surface-2 border-surface-3' : 'bg-surface-1/50 border-surface-1 opacity-50'}`}>
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-4">
              <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${stage > 0 ? 'bg-india-green/20 text-india-green' : stage === 0 ? 'bg-saffron/20 text-saffron' : 'bg-surface-3 text-text-muted'}`}>
                <Database className="w-5 h-5" />
              </div>
              <div>
                <h3 className="text-lg font-semibold text-white">Research AI</h3>
                <p className="text-sm text-text-muted">Gathering baseline data and elasticities</p>
              </div>
            </div>
            {stage > 0 ? <CheckCircle2 className="w-6 h-6 text-india-green" /> : stage === 0 ? <Loader2 className="w-6 h-6 text-saffron animate-spin" /> : null}
          </div>
          
          <div className="pl-14 min-h-[80px]">
            <AnimatePresence>
              {activeSources.map((source, i) => (
                <motion.div 
                  key={i}
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="text-sm text-text-secondary flex items-center gap-2 mb-1"
                >
                  <div className="w-1.5 h-1.5 rounded-full bg-accent-blue" />
                  {source}
                </motion.div>
              ))}
            </AnimatePresence>
          </div>
        </div>

        {/* Stage 2: Simulation */}
        <div className={`p-6 rounded-xl border transition-colors duration-500 ${stage >= 1 ? 'bg-surface-2 border-surface-3' : 'bg-surface-1/50 border-surface-1 opacity-50'}`}>
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-4">
              <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${stage > 1 ? 'bg-india-green/20 text-india-green' : stage === 1 ? 'bg-saffron/20 text-saffron' : 'bg-surface-3 text-text-muted'}`}>
                <Cpu className="w-5 h-5" />
              </div>
              <div>
                <h3 className="text-lg font-semibold text-white">Simulation AI</h3>
                <p className="text-sm text-text-muted">Evaluating cohort responses and cascading effects</p>
              </div>
            </div>
            {stage > 1 ? <CheckCircle2 className="w-6 h-6 text-india-green" /> : stage === 1 ? <Loader2 className="w-6 h-6 text-saffron animate-spin" /> : null}
          </div>
          
          <div className="pl-14">
            <div className="flex items-center justify-between text-sm text-text-secondary mb-2">
              <span>Simulating demographic cohorts</span>
              <span className="font-mono">{Math.min(cohortsDone, 2000)} / 2000</span>
            </div>
            <div className="h-2 w-full bg-surface-4 rounded-full overflow-hidden">
              <div 
                className="h-full bg-gradient-to-r from-saffron to-accent-blue transition-all duration-100 ease-linear"
                style={{ width: `${Math.min((cohortsDone / 2000) * 100, 100)}%` }}
              />
            </div>
          </div>
        </div>

        {/* Stage 3: Analysis */}
        <div className={`p-6 rounded-xl border transition-colors duration-500 ${stage >= 2 ? 'bg-surface-2 border-surface-3' : 'bg-surface-1/50 border-surface-1 opacity-50'}`}>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${stage > 2 ? 'bg-india-green/20 text-india-green' : stage === 2 ? 'bg-saffron/20 text-saffron' : 'bg-surface-3 text-text-muted'}`}>
                <FileText className="w-5 h-5" />
              </div>
              <div>
                <h3 className="text-lg font-semibold text-white">Analysis Synthesis</h3>
                <p className="text-sm text-text-muted">Generating insights and visual reports</p>
              </div>
            </div>
            {stage > 2 ? <CheckCircle2 className="w-6 h-6 text-india-green" /> : stage === 2 ? <Loader2 className="w-6 h-6 text-saffron animate-spin" /> : null}
          </div>
        </div>

      </div>
    </div>
  );
}
