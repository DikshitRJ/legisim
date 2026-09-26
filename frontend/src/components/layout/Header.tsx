'use client';

import { useState } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { usePathname, useRouter } from 'next/navigation';
import { ChevronDown, Settings, LogOut } from 'lucide-react';
import { useLogout } from '@/hooks/useMutations';

export interface HeaderProps {
  showNav?: boolean;
}

export default function Header({ showNav = false }: HeaderProps) {
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const pathname = usePathname();
  const router = useRouter();
  const logoutMutation = useLogout();

  const handleLogout = () => {
    logoutMutation.mutate(undefined, {
      onSuccess: () => {
        router.push('/login');
      }
    });
  };

  return (
    <header className="relative z-50 flex w-full flex-col border-b border-surface-3 bg-canvas">
      <div className="flex h-16 items-center justify-between px-4 sm:px-6">
        <Link href="/notebooks" className="flex min-w-0 items-center gap-3" aria-label="Legisim home">
          <Image
            src="/emblem.svg"
            alt="Government Emblem"
            width={36}
            height={42}
            className="h-10 w-9 shrink-0 object-contain invert opacity-90"
          />
          <span className="flex min-w-0 flex-col leading-tight">
            <span className="truncate text-label-mono-security text-on-surface sm:text-[11px] uppercase">
              भारत सरकार <span className="text-text-secondary">|</span> GOVERNMENT OF INDIA
            </span>
            <span className="mt-1 flex items-baseline gap-1.5 whitespace-nowrap text-[17px] font-bold tracking-tight text-on-surface uppercase">
              LEGISIM {showNav && <em className="hidden text-[11px] not-italic tracking-[0.06em] text-saffron sm:inline bg-surface-2 px-1.5 py-0.5 rounded border border-surface-3">LEGISLATIVE SIMULATION PORTAL</em>}
            </span>
          </span>
        </Link>

        {showNav && (
          <nav aria-label="Primary" className="absolute left-1/2 hidden -translate-x-1/2 items-center gap-5 lg:flex">
            <Link href={pathname.includes('/new') ? pathname : '/notebooks'} className="text-sm font-semibold text-saffron transition-colors hover:text-saffron-hover">Simulation Wizard</Link>
            <Link href="/notebooks" className="text-sm font-semibold text-on-surface-variant transition-colors hover:text-on-surface">Draft Archive</Link>
            <Link href="/settings" className="text-sm font-semibold text-on-surface-variant transition-colors hover:text-on-surface">Compliance Matrix</Link>
          </nav>
        )}

        <div className="relative flex items-center gap-2 sm:gap-3">
          <div className="hidden flex-col items-end sm:flex">
            <span className="text-xs font-semibold text-on-surface">Dir. Rajesh Verma</span>
            <span className="text-[9px] font-medium uppercase tracking-[0.1em] text-accent-blue-light">
              JOINT SECRETARY, MEITY
            </span>
          </div>
          <button
            aria-expanded={dropdownOpen}
            aria-haspopup="menu"
            aria-label="Open officer menu"
            className="flex items-center gap-2 rounded bg-surface-container-low px-2 py-1.5 transition-colors hover:bg-surface-container-high"
            onClick={() => setDropdownOpen(!dropdownOpen)}
          >
            <div className="flex h-8 w-8 items-center justify-center rounded bg-navy text-xs font-bold text-accent-blue-light">
              DR
            </div>
            <ChevronDown className="h-4 w-4 text-on-surface-variant" />
          </button>

          {dropdownOpen && (
            <div role="menu" className="absolute right-0 top-12 w-48 border border-surface-3 bg-surface-2 py-1 shadow-2xl">
              <Link href="/settings" role="menuitem" className="flex items-center px-4 py-2.5 text-sm text-on-surface transition-colors hover:bg-surface-3">
                <Settings className="w-4 h-4 mr-3" />
                Settings
              </Link>
              <button onClick={handleLogout} role="menuitem" className="w-full flex items-center px-4 py-2.5 text-sm text-error transition-colors hover:bg-surface-3 text-left">
                <LogOut className="w-4 h-4 mr-3" />
                Log Out
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}
