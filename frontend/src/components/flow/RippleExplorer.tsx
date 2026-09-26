'use client';

import React, { useMemo, useState } from 'react';
import {
  Background,
  Controls,
  Handle,
  MarkerType,
  Position,
  ReactFlow,
  MiniMap,
  BaseEdge,
  EdgeLabelRenderer,
  getSmoothStepPath,
  type Edge,
  type Node,
  type NodeProps,
  type EdgeProps
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

type FlowNodeData = Record<string, unknown> & RippleNodeData & { selected?: boolean };

const DOMAIN_COLORS: Record<string, string> = {
  policy: '#FF671F',
  transport: '#3B82F6',
  agriculture: '#046A38',
  business: '#8B5CF6',
  consumer: '#F59E0B',
  income: '#10B981',
  economy: '#002868',
  social: '#EC4899',
  political: '#EF4444',
  fiscal: '#6366F1',
  health: '#14B8A6',
  education: '#F97316',
  energy: '#FBBF24',
  employment: '#22C55E',
};

function ImpactNode({ data }: NodeProps<Node<FlowNodeData>>) {
  const color = DOMAIN_COLORS[data.domain.toLowerCase()] || '#71717A';
  
  const borderStyle = data.confidence.toLowerCase() === 'high' 
    ? 'solid' 
    : data.confidence.toLowerCase() === 'medium' 
      ? 'dashed' 
      : 'dotted';

  const root = data.layer === 0;

  return (
    <div 
      className={`min-w-[200px] rounded-lg bg-surface-4 p-3 shadow-lg transition-all ${data.selected ? 'ring-2 ring-saffron scale-[1.02]' : ''}`}
      style={{
        border: `2px ${borderStyle} ${color}`,
        boxShadow: root ? `0 0 20px ${color}40` : undefined
      }}
    >
      <Handle className="!h-2 !w-2 !border-0 !bg-surface-3" position={Position.Left} type="target" />
      <div className="mb-2 flex items-center justify-between gap-2">
        <span 
          className="rounded px-1.5 py-0.5 text-[10px] font-bold uppercase tracking-wide"
          style={{ backgroundColor: `${color}20`, color: color }}
        >
          {data.domain}
        </span>
        <span className="rounded bg-surface-2 px-1.5 py-0.5 text-[10px] font-semibold text-text-muted capitalize">
          {data.kind}
        </span>
      </div>
      <p className="text-sm font-semibold text-white">{data.label}</p>
      <div className="mt-2 flex justify-between items-center text-xs text-text-muted">
        <span>Impact</span>
        <span className="font-mono font-bold" style={{ color }}>{data.magnitude}</span>
      </div>
      <Handle className="!h-2 !w-2 !border-0 !bg-surface-3" position={Position.Right} type="source" />
    </div>
  );
}

function CustomEdge({
  id,
  sourceX,
  sourceY,
  targetX,
  targetY,
  sourcePosition,
  targetPosition,
  style = {},
  markerEnd,
  data,
  label
}: EdgeProps) {
  const [edgePath, labelX, labelY] = getSmoothStepPath({
    sourceX,
    sourceY,
    sourcePosition,
    targetPosition,
    targetX,
    targetY,
  });

  return (
    <>
      <BaseEdge path={edgePath} markerEnd={markerEnd} style={style} id={id} />
      <EdgeLabelRenderer>
        <div
          style={{
            position: 'absolute',
            transform: `translate(-50%, -50%) translate(${labelX}px,${labelY}px)`,
            pointerEvents: 'all',
          }}
          className="nodrag nopan"
          title={data?.mechanism as string}
        >
          <div className="px-1.5 py-0.5 rounded bg-surface-2 border border-surface-3 text-[10px] text-text-muted shadow-sm hover:text-white cursor-help transition-colors">
            {label}
          </div>
        </div>
      </EdgeLabelRenderer>
    </>
  );
}

const nodeTypes = { impact: ImpactNode };
const edgeTypes = { custom: CustomEdge };

function layoutNodes(nodes: RippleNodeData[], selectedId?: string): Node<FlowNodeData>[] {
  const layers = new Map<number, RippleNodeData[]>();
  nodes.forEach((node) => layers.set(node.layer, [...(layers.get(node.layer) ?? []), node]));
  
  return [...layers.entries()].flatMap(([layer, items]) => items.map((node, index) => ({
    id: node.id,
    type: 'impact',
    position: { x: layer * 300, y: index * 150 },
    data: { ...node, selected: node.id === selectedId },
  })));
}

function edgeColor(strength: number) {
  if (strength > 0.5) return '#FF671F'; // strong positive/negative? Actually magnitude is magnitude. Let's use saffron for strong, neutral for weak.
  if (strength < -0.5) return '#046A38'; 
  return '#71717A';
}

export function RippleExplorer({ graph }: { graph?: RippleGraphData }) {
  const [selectedId, setSelectedId] = useState<string | undefined>();
  const selected = graph?.nodes.find((node) => node.id === selectedId);
  const nodes = useMemo(() => layoutNodes(graph?.nodes ?? [], selectedId), [graph?.nodes, selectedId]);
  
  const edges = useMemo<Edge[]>(() => {
    return (graph?.edges ?? []).map((edge) => {
      const isSelected = selectedId && (edge.source === selectedId || edge.target === selectedId);
      const isFaded = selectedId && !isSelected;
      const opacity = isFaded ? 0.2 : 1;
      
      const absStrength = Math.abs(edge.strength);
      const color = edgeColor(edge.strength);
      
      return {
        id: edge.id,
        source: edge.source,
        target: edge.target,
        type: 'custom',
        animated: true,
        label: `${edge.lagMonths} months`,
        markerEnd: { type: MarkerType.ArrowClosed, color },
        style: { 
          stroke: color, 
          strokeWidth: Math.max(1.5, absStrength * 4),
          opacity,
          transition: 'opacity 0.2s'
        },
        data: { mechanism: edge.mechanism }
      };
    });
  }, [graph?.edges, selectedId]);

  if (!graph?.nodes.length) {
    return (
      <div className="flex h-[calc(100vh-190px)] min-h-[480px] items-center justify-center rounded-lg border border-surface-3 bg-surface-2 text-sm text-text-muted">
        No causal relationships were returned for this run.
      </div>
    );
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
            <div className="flex justify-between gap-3"><dt className="text-text-muted">Magnitude</dt><dd className="text-right text-text-body font-mono">{selected.magnitude}</dd></div>
            <div className="flex justify-between gap-3"><dt className="text-text-muted">Confidence</dt><dd className="text-white capitalize">{selected.confidence}</dd></div>
            <div className="flex justify-between gap-3"><dt className="text-text-muted">Evidence type</dt><dd className="capitalize text-text-body">{selected.kind}</dd></div>
          </dl>
          {selectedEdges.length ? (
            <div className="mt-4 border-t border-surface-3 pt-3">
              <p className="text-xs font-semibold text-text-secondary">Related mechanisms</p>
              <div className="max-h-40 overflow-y-auto pr-2 mt-2 space-y-2">
                {selectedEdges.map((edge) => (
                  <p className="text-xs leading-5 text-text-muted" key={edge.id}>
                    <span className="font-semibold text-white mr-1">[{edge.lagMonths}mo]</span>
                    {edge.mechanism}
                  </p>
                ))}
              </div>
            </div>
          ) : null}
        </aside>
      ) : null}
      
      <ReactFlow
        className="bg-canvas"
        edges={edges}
        fitView
        minZoom={0.1}
        maxZoom={1.5}
        nodeTypes={nodeTypes}
        edgeTypes={edgeTypes}
        nodes={nodes}
        onNodeClick={(_, node) => setSelectedId(node.id)}
        onPaneClick={() => setSelectedId(undefined)}
      >
        <Background color="#2A2A2A" gap={20} size={1} />
        <Controls className="!border-surface-3 !bg-surface-2 !fill-white" showInteractive={false} />
        <MiniMap 
          nodeColor={(node) => {
            const data = node.data as FlowNodeData;
            return DOMAIN_COLORS[data.domain.toLowerCase()] || '#71717A';
          }}
          maskColor="rgba(10, 10, 10, 0.7)"
          className="!bg-surface-2 !border-surface-3"
        />
      </ReactFlow>
    </section>
  );
}
