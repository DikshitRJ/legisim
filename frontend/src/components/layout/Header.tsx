'use client';

import { useState } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { usePathname } from 'next/navigation';
import { ChevronDown, Settings, LogOut } from 'lucide-react';

export interface HeaderProps {
  showNav?: boolean;
}

export default function Header({ showNav = false }: HeaderProps) {
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const pathname = usePathname();

  return (
    <header className="relative z-50 flex w-full flex-col border-b border-[#1d1d1d] bg-[#101010]">
      <div className="flex h-16 items-center justify-between px-4 sm:px-6">
        <Link href="/notebooks" className="flex min-w-0 items-center gap-3" aria-label="Legisim home">
          <Image
            src="/emblem.svg"
            alt=""
            width={36}
            height={42}
            className="h-10 w-9 shrink-0 object-contain opacity-90"
          />
          <span className="flex min-w-0 flex-col leading-tight">
            <span className="truncate text-[10px] font-semibold tracking-[0.08em] text-[#e5e2e1] sm:text-[11px]">भारत सरकार <span className="text-[#a1a1aa]">|</span> GOVERNMENT OF INDIA</span>
            <span className="mt-1 flex items-baseline gap-1.5 whitespace-nowrap text-[17px] font-bold tracking-tight text-[#e5e2e1]">LEGISIM {showNav && <em className="hidden text-[11px] not-italic tracking-[0.06em] text-[#e2bfb2] sm:inline">LEGISLATIVE SIMULATION PORTAL</em>}</span>
          </span>
        </Link>

        {showNav && (
          <nav aria-label="Primary" className="absolute left-1/2 hidden -translate-x-1/2 items-center gap-5 lg:flex">
            <Link href={pathname.includes('/new') ? pathname : '/notebooks'} className="text-sm font-semibold text-[#e2bfb2] transition-colors hover:text-white">Simulation Wizard</Link>
            <Link href="/notebooks" className="text-sm font-semibold text-[#e2bfb2] transition-colors hover:text-white">Draft Archive</Link>
            <Link href="/settings" className="text-sm font-semibold text-[#e2bfb2] transition-colors hover:text-white">Compliance Matrix</Link>
          </nav>
        )}

        <div className="relative flex items-center gap-2 sm:gap-3">
          <div className="hidden flex-col items-end sm:flex">
            <span className="text-xs font-semibold text-[#e5e2e1]">Dir. Rajesh Verma</span>
            <span className="text-[9px] font-medium uppercase tracking-[0.1em] text-[#b1c5ff]">
              JOINT SECRETARY, MEITY
            </span>
          </div>
          <button
            aria-expanded={dropdownOpen}
            aria-haspopup="menu"
            aria-label="Open officer menu"
            className="flex items-center gap-2 rounded bg-[#1c1b1b] px-2 py-1.5 transition-colors hover:bg-[#2a2a2a]"
            onClick={() => setDropdownOpen(!dropdownOpen)}
          >
            <div className="flex h-8 w-8 items-center justify-center rounded bg-[#002868] text-xs font-bold text-[#b1c5ff]">
              DR
            </div>
            <ChevronDown className="h-4 w-4 text-[#e2bfb2]" />
          </button>

          {dropdownOpen && (
            <div role="menu" className="absolute right-0 top-12 w-48 border border-[#3f3f46] bg-[#1e1e1e] py-1 shadow-2xl">
              <Link href="/settings" role="menuitem" className="flex items-center px-4 py-2.5 text-sm text-[#e5e2e1] transition-colors hover:bg-[#2a2a2a]">
                <Settings className="w-4 h-4 mr-3" />
                Settings
              </Link>
              <Link href="/login" role="menuitem" className="flex items-center px-4 py-2.5 text-sm text-[#ffb4ab] transition-colors hover:bg-[#2a2a2a]">
                <LogOut className="w-4 h-4 mr-3" />
                Log Out
              </Link>
            </div>
          )}
        </div>
      </div>
      
    </header>
  );
}
