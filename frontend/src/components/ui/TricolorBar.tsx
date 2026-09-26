export interface TricolorBarProps {
  height?: string;
  className?: string;
}

export function TricolorBar({ height = '3px', className = '' }: TricolorBarProps) {
  return (
    <div 
      className={`flex w-full ${className}`} 
      style={{ height }}
    >
      <div className="h-full flex-1 bg-saffron" />
      <div className="h-full flex-1 bg-white" />
      <div className="h-full flex-1 bg-india-green" />
    </div>
  );
}
