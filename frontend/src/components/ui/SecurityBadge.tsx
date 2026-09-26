export interface SecurityBadgeProps {
  label: string;
  status?: 'active' | 'restricted';
  className?: string;
}

export function SecurityBadge({ label, status, className = '' }: SecurityBadgeProps) {
  return (
    <div className={`inline-flex items-center gap-1.5 rounded bg-surface-2 px-2 py-1 border border-surface-3 text-label-mono-security text-on-surface uppercase ${className}`}>
      {status && (
        <span 
          className={`h-1.5 w-1.5 rounded-full ${status === 'active' ? 'bg-india-green' : 'bg-error'}`} 
          aria-hidden="true"
        />
      )}
      {label}
    </div>
  );
}
