'use client';

import React, { useMemo, useState } from 'react';
import {
  Background,
  Controls,
  Handle,
  MarkerType,
  Position,
  ReactFlow,
  type Edge,
  type Node,
  type NodeProps,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';

export interface RippleNodeData {
  id: string;
  label: string;
  layer: number;
  domain: string;
  magnitude: string;
  confidence: string;
  kind: string;
}

export interface RippleEdgeData {
  id: string;
  source: string;
  target: string;
  strength: number;
  lagMonths: number;
  mechanism: string;
}

export interface RippleGraphData {
  nodes: RippleNodeData[];
  edges: RippleEdgeData[];
}

type FlowNodeData = RippleNodeData & { selected?: boolean };

const domainColors: Record<string, string> = {
  policy: 'border-saffron/50 bg-saffron/10 text-saffron',
  transport: 'border-blue-400/40 bg-blue-400/10 text-blue-300',
  agriculture: 'border-india-green/40 bg-india-green/10 text-green-300',
  fiscal: 'border-emerald-400/40 bg-emerald-400/10 text-emerald-300',
  social: 'border-pink-400/40 bg-pink-400/10 text-pink-300',
  economy: 'border-amber-400/40 bg-amber-400/10 text-amber-300',
};

function confidenceColor(confidence: string) {
  if (confidence.toLowerCase() === 'high') return 'text-india-green';
  if (confidence.toLowerCase() === 'medium') return 'text-amber-400';
  return 'text-red-400';
}

function ImpactNode({ data }: NodeProps<Node<FlowNodeData>>) {
  const tag = domainColors[data.domain.toLowerCase()] ?? 'border-surface-3 bg-surface-2 text-text-secondary';
  const root = data.layer === 0;
  return (
    <div className={`min-w-[190px] rounded-lg border bg-surface-4 p-3 shadow-lg transition-shadow ${root ? 'border-saffron shadow-[0_0_20px_rgba(255,103,31,0.16)]' : data.selected ? 'border-accent-blue' : 'border-surface-3'}`}>
      <Handle className="!h-2 !w-2 !border-0 !bg-surface-3" position={Position.Left} type="target" />
      <div className="mb-2 flex items-center justify-between gap-2">
        <span className={`rounded border px-1.5 py-0.5 text-[10px] font-bold uppercase tracking-wide ${tag}`}>{data.domain}</span>
        <span className={`text-[10px] font-semibold ${confidenceColor(data.confidence)}`}>{data.confidence}</span>
      </div>
      <p className="text-sm font-semibold text-white">{data.label}</p>
      <p className="mt-2 text-xs text-text-muted">Impact <span className="font-mono text-text-body">{data.magnitude}</span></p>
      <Handle className="!h-2 !w-2 !border-0 !bg-surface-3" position={Position.Right} type="source" />
    </div>
  );
}

const nodeTypes = { impact: ImpactNode };

function layoutNodes(nodes: RippleNodeData[], selectedId?: string): Node<FlowNodeData>[] {
  const layers = new Map<number, RippleNodeData[]>();
  nodes.forEach((node) => layers.set(node.layer, [...(layers.get(node.layer) ?? []), node]));
  return [...layers.entries()].flatMap(([layer, items]) => items.map((node, index) => ({
    id: node.id,
    type: 'impact',
    position: { x: layer * 290 + 20, y: index * 150 + Math.max(20, (4 - items.length) * 70) },
    data: { ...node, selected: node.id === selectedId },
  })));
}

function edgeColor(strength: number) {
  if (strength >= 0.8) return '#FF671F';
  if (strength >= 0.6) return '#4C9AFF';
  return '#71717A';
}

export function RippleExplorer({ graph }: { graph?: RippleGraphData }) {
  const [selectedId, setSelectedId] = useState<string | undefined>();
  const selected = graph?.nodes.find((node) => node.id === selectedId);
  const nodes = useMemo(() => layoutNodes(graph?.nodes ?? [], selectedId), [graph?.nodes, selectedId]);
  const edges = useMemo<Edge[]>(() => (graph?.edges ?? []).map((edge) => {
    const color = edgeColor(edge.strength);
    return {
      id: edge.id,
      source: edge.source,
      target: edge.target,
      type: 'smoothstep',
      label: `${Math.round(edge.strength * 100)}% · ${edge.lagMonths}mo`,
      labelStyle: { fill: '#A1A1AA', fontSize: 10 },
      markerEnd: { type: MarkerType.ArrowClosed, color },
      style: { stroke: color, strokeWidth: Math.max(1.5, edge.strength * 3) },
    };
  }), [graph?.edges]);

  if (!graph?.nodes.length) {
    return <div className="flex h-[calc(100vh-190px)] min-h-[480px] items-center justify-center rounded-lg border border-surface-3 bg-surface-2 text-sm text-text-muted">No causal relationships were returned for this run.</div>;
  }

  const selectedEdges = graph.edges.filter((edge) => edge.source === selectedId || edge.target === selectedId);
  return (
    <section className="relative h-[calc(100vh-190px)] min-h-[480px] overflow-hidden rounded-lg border border-surface-3 bg-canvas">
      <div className="absolute left-4 top-4 z-10 max-w-xs rounded border border-surface-3 bg-surface-2/95 px-4 py-3 shadow-lg backdrop-blur">
        <h1 className="text-sm font-semibold text-white">Cause–effect ripple</h1>
        <p className="mt-1 text-xs leading-5 text-text-muted">Select a relationship to inspect its evidence signal, relative strength, and projected lag.</p>
      </div>
      {selected ? (
        <aside className="absolute right-4 top-4 z-10 w-72 rounded border border-surface-3 bg-surface-2/95 p-4 shadow-lg backdrop-blur">
          <p className="text-xs font-bold uppercase tracking-wider text-saffron">Selected impact</p>
          <h2 className="mt-1 text-base font-semibold text-white">{selected.label}</h2>
          <dl className="mt-3 space-y-2 text-xs">
            <div className="flex justify-between gap-3"><dt className="text-text-muted">Magnitude</dt><dd className="text-right text-text-body">{selected.magnitude}</dd></div>
            <div className="flex justify-between gap-3"><dt className="text-text-muted">Confidence</dt><dd className={confidenceColor(selected.confidence)}>{selected.confidence}</dd></div>
            <div className="flex justify-between gap-3"><dt className="text-text-muted">Evidence type</dt><dd className="capitalize text-text-body">{selected.kind}</dd></div>
          </dl>
          {selectedEdges.length ? <div className="mt-4 border-t border-surface-3 pt-3"><p className="text-xs font-semibold text-text-secondary">Related mechanisms</p>{selectedEdges.map((edge) => <p className="mt-2 text-xs leading-5 text-text-muted" key={edge.id}>{edge.mechanism}</p>)}</div> : null}
        </aside>
      ) : null}
      <ReactFlow
        className="bg-canvas"
        edges={edges}
        fitView
        minZoom={0.25}
        maxZoom={1.6}
        nodeTypes={nodeTypes}
        nodes={nodes}
        onNodeClick={(_, node) => setSelectedId(node.id)}
        onPaneClick={() => setSelectedId(undefined)}
      >
        <Background color="#2A2A2A" gap={20} size={1} />
        <Controls className="!border-surface-3 !bg-surface-2 !fill-white" showInteractive={false} />
      </ReactFlow>
    </section>
  );
}
