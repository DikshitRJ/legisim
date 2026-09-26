'use client';

import React, { useMemo } from 'react';
import { ReactFlow, Background, Controls, Handle, Position, MarkerType } from '@xyflow/react';
import '@xyflow/react/dist/style.css';

const domains: Record<string, string> = {
  Policy: 'bg-white text-black',
  Transport: 'bg-blue-500/20 text-blue-400 border-blue-500/30',
  Agriculture: 'bg-green-500/20 text-green-400 border-green-500/30',
  Logistics: 'bg-purple-500/20 text-purple-400 border-purple-500/30',
  Economy: 'bg-saffron/20 text-saffron border-saffron/30',
  Social: 'bg-pink-500/20 text-pink-400 border-pink-500/30',
  Fiscal: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30',
};

const CustomNode = ({ data }: any) => {
  const domainClass = domains[data.domain] || domains.Economy;
  const isRoot = data.domain === 'Policy';

  return (
    <div className={`bg-surface-4 border ${isRoot ? 'border-saffron shadow-[0_0_15px_rgba(255,153,51,0.3)]' : 'border-surface-3'} rounded-lg p-3 min-w-[180px] shadow-lg`}>
      <Handle type="target" position={Position.Left} className="w-2 h-2 !bg-surface-3 !border-none" />
      <div className="flex items-center justify-between mb-2">
        <span className={`text-[10px] uppercase font-bold px-2 py-0.5 rounded-full border ${domainClass}`}>
          {data.domain}
        </span>
        {data.confidence && (
          <span className="text-[10px] text-text-muted">{data.confidence}</span>
        )}
      </div>
      <div className={`font-semibold ${isRoot ? 'text-white text-base' : 'text-text-body text-sm'}`}>
        {data.label}
      </div>
      {data.magnitude && (
        <div className="mt-2 text-xs font-mono text-text-secondary">
          Impact: <span className={data.magnitude.includes('+') ? 'text-red-400' : 'text-india-green'}>{data.magnitude}</span>
        </div>
      )}
      <Handle type="source" position={Position.Right} className="w-2 h-2 !bg-surface-3 !border-none" />
    </div>
  );
};

const nodeTypes = { custom: CustomNode };

const initialNodes = [
  // Layer 0
  { id: 'root', type: 'custom', position: { x: 50, y: 300 }, data: { label: 'Diesel Subsidy Removal', domain: 'Policy' } },
  // Layer 1
  { id: 'n1', type: 'custom', position: { x: 350, y: 100 }, data: { label: 'Transport Cost Rise', domain: 'Transport', magnitude: '+15-22%', confidence: 'High' } },
  { id: 'n2', type: 'custom', position: { x: 350, y: 250 }, data: { label: 'Agricultural Input Cost', domain: 'Agriculture', magnitude: '+12%', confidence: 'High' } },
  { id: 'n3', type: 'custom', position: { x: 350, y: 400 }, data: { label: 'Logistics Cost Surge', domain: 'Logistics', magnitude: '+18%', confidence: 'Medium' } },
  { id: 'n4', type: 'custom', position: { x: 350, y: 550 }, data: { label: 'Government Savings', domain: 'Fiscal', magnitude: '₹1.3L Cr', confidence: 'High' } },
  // Layer 2
  { id: 'n1_1', type: 'custom', position: { x: 650, y: 50 }, data: { label: 'Public Transit Demand', domain: 'Transport', magnitude: '+8%', confidence: 'Low' } },
  { id: 'n1_2', type: 'custom', position: { x: 650, y: 150 }, data: { label: 'Food Price Increase', domain: 'Agriculture', magnitude: '+4.5%', confidence: 'High' } },
  { id: 'n2_1', type: 'custom', position: { x: 650, y: 300 }, data: { label: 'Rural Income Decline', domain: 'Economy', magnitude: '-8.5%', confidence: 'High' } },
  { id: 'n3_1', type: 'custom', position: { x: 650, y: 450 }, data: { label: 'Inflation Spike', domain: 'Economy', magnitude: '+1.8% CPI', confidence: 'High' } },
  { id: 'n4_1', type: 'custom', position: { x: 650, y: 600 }, data: { label: 'Subsidy Reallocation', domain: 'Policy', magnitude: 'Capex Shift', confidence: 'Medium' } },
  // Layer 3
  { id: 'n2_1_1', type: 'custom', position: { x: 950, y: 250 }, data: { label: 'Political Backlash', domain: 'Social', magnitude: 'High Risk', confidence: 'Medium' } },
  { id: 'n2_1_2', type: 'custom', position: { x: 950, y: 350 }, data: { label: 'Urban Migration', domain: 'Social', magnitude: '+2%', confidence: 'Low' } },
];

const edgeOpts = {
  type: 'smoothstep',
  animated: true,
  style: { stroke: '#71717A', strokeWidth: 2 },
  markerEnd: { type: MarkerType.ArrowClosed, color: '#71717A' },
};

const initialEdges = [
  { id: 'e-root-n1', source: 'root', target: 'n1', ...edgeOpts },
  { id: 'e-root-n2', source: 'root', target: 'n2', ...edgeOpts },
  { id: 'e-root-n3', source: 'root', target: 'n3', ...edgeOpts },
  { id: 'e-root-n4', source: 'root', target: 'n4', ...edgeOpts },
  
  { id: 'e-n1-n1_1', source: 'n1', target: 'n1_1', ...edgeOpts, style: { stroke: '#3B82F6', strokeWidth: 2 }, markerEnd: { type: MarkerType.ArrowClosed, color: '#3B82F6' } },
  { id: 'e-n1-n1_2', source: 'n1', target: 'n1_2', ...edgeOpts },
  
  { id: 'e-n2-n1_2', source: 'n2', target: 'n1_2', ...edgeOpts },
  { id: 'e-n2-n2_1', source: 'n2', target: 'n2_1', ...edgeOpts, style: { stroke: '#EF4444', strokeWidth: 2 }, markerEnd: { type: MarkerType.ArrowClosed, color: '#EF4444' } },
  
  { id: 'e-n3-n3_1', source: 'n3', target: 'n3_1', ...edgeOpts },
  { id: 'e-n1_2-n3_1', source: 'n1_2', target: 'n3_1', ...edgeOpts },
  
  { id: 'e-n4-n4_1', source: 'n4', target: 'n4_1', ...edgeOpts, style: { stroke: '#10B981', strokeWidth: 2 }, markerEnd: { type: MarkerType.ArrowClosed, color: '#10B981' } },
  
  { id: 'e-n2_1-n2_1_1', source: 'n2_1', target: 'n2_1_1', ...edgeOpts },
  { id: 'e-n2_1-n2_1_2', source: 'n2_1', target: 'n2_1_2', ...edgeOpts },
];

export default function RipplePage() {
  return (
    <div className="w-full h-[calc(100vh-160px)] bg-canvas relative">
      <div className="absolute top-4 left-6 z-10 bg-surface-2/80 backdrop-blur border border-surface-3 px-4 py-2 rounded-lg">
        <h2 className="text-white font-medium text-sm">Cause-Effect Ripple</h2>
        <p className="text-xs text-text-muted">Trace the cascading impacts of the policy</p>
      </div>
      <ReactFlow
        nodes={initialNodes}
        edges={initialEdges}
        nodeTypes={nodeTypes}
        fitView
        className="bg-canvas"
        minZoom={0.5}
        maxZoom={1.5}
      >
        <Background color="#2A2A2A" gap={20} size={2} />
        <Controls className="!bg-surface-2 !border-surface-3 !fill-white" />
      </ReactFlow>
    </div>
  );
}
