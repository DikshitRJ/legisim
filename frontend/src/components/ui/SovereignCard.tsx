import { ReactNode } from 'react';
import { TricolorBar } from './TricolorBar';

export interface SovereignCardProps {
  children: ReactNode;
  className?: string;
  showTricolor?: boolean;
}

export function SovereignCard({ children, className = '', showTricolor = false }: SovereignCardProps) {
  return (
    <div className={`overflow-hidden rounded-xl bg-surface-4 shadow-lg border border-surface-3 ${className}`}>
      {showTricolor && <TricolorBar />}
      {children}
    </div>
  );
}
