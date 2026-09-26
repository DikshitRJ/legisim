'use client';

import React, { useState } from 'react';
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
    <header className="flex flex-col w-full bg-[#121212] border-b border-[#242424] sticky top-0 z-50">
      <div className="flex items-center justify-between h-16 px-6">
        <div className="flex items-center space-x-4">
          <div className="relative h-9 w-6 flex-shrink-0">
            <Image 
              src="/emblem.svg" 
              alt="Government Emblem" 
              width={24}
              height={36}
              className="object-contain invert brightness-0 contrast-200 opacity-90 h-full w-auto"
            />
          </div>
          <div className="h-8 w-px bg-[#2a2a2a]"></div>
          <div className="flex flex-col justify-center">
            <span className="text-[10px] uppercase tracking-widest text-gray-400 font-medium">
              भारत सरकार | GOVERNMENT OF INDIA
            </span>
            <div className="flex items-center space-x-2">
              <span className="text-sm font-bold text-white tracking-widest">LEGISIM</span>
              <span className="text-[9px] uppercase bg-[#1f1f1f] text-blue-400 border border-[#2a2a2a] px-1.5 py-0.5 rounded tracking-wider font-semibold">
                OFFICER PORTAL
              </span>
            </div>
          </div>
        </div>

        <div className="flex items-center space-x-3 relative">
          <div className="flex flex-col items-end mr-2">
            <span className="text-sm font-semibold text-white">Dir. Rajesh Verma</span>
            <span className="text-[10px] uppercase tracking-wider text-blue-400 font-medium">
              JOINT SECRETARY, MEITY
            </span>
          </div>
          <button 
            className="flex items-center space-x-2 focus:outline-none hover:bg-white/5 rounded-md p-1 transition-colors"
            onClick={() => setDropdownOpen(!dropdownOpen)}
          >
            <div className="w-8 h-8 rounded-md bg-[#1f242d] text-blue-400 font-bold flex items-center justify-center text-sm border border-[#2a3040]">
              DR
            </div>
            <ChevronDown className="w-4 h-4 text-gray-400" />
          </button>

          {dropdownOpen && (
            <div className="absolute right-0 top-12 mt-2 w-48 bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg shadow-xl py-1">
              <Link href="/settings" className="flex items-center px-4 py-2 text-sm text-gray-300 hover:bg-[#252525] hover:text-white transition-colors">
                <Settings className="w-4 h-4 mr-3" />
                Settings
              </Link>
              <Link href="/login" className="flex items-center px-4 py-2 text-sm text-red-400 hover:bg-[#252525] hover:text-red-300 transition-colors">
                <LogOut className="w-4 h-4 mr-3" />
                Log Out
              </Link>
            </div>
          )}
        </div>
      </div>
      
      {showNav && (
        <div className="flex items-center h-12 px-6 border-t border-[#1a1a1a] bg-[#0d0d0d] space-x-8">
          <Link href="#" className="text-sm font-medium text-[#FF9933] border-b-2 border-[#FF9933] pb-3 pt-3">
            Simulation Wizard
          </Link>
          <Link href="#" className="text-sm font-medium text-gray-400 hover:text-gray-200 transition-colors pb-3 pt-3 border-b-2 border-transparent">
            Draft Archive
          </Link>
          <Link href="#" className="text-sm font-medium text-gray-400 hover:text-gray-200 transition-colors pb-3 pt-3 border-b-2 border-transparent">
            Compliance Matrix
          </Link>
        </div>
      )}
    </header>
  );
}
