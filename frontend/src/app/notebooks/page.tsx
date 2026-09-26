'use client';

import { useMemo, useState } from 'react';
import { useRouter } from 'next/navigation';
import { FolderOpen, Plus, Search } from 'lucide-react';
import Footer from '@/components/layout/Footer';
import Header from '@/components/layout/Header';
import ProtectedRoute from '@/components/layout/ProtectedRoute';

type NotebookPreview = { id: string; title: string; sources: number; description: string; updated: string };

// TODO(api): hydrate this visual preview from GET /api/notebooks; remove when query hooks are available.
const previewNotebooks: NotebookPreview[] = [
  { id: 'dpdp-policy', title: 'Digital Personal Data Protection', sources: 12, description: 'Statutory compliance & citizen privacy impact audit framework', updated: 'Modified 5 days ago' },
  { id: 'green-hydrogen', title: 'National Green Hydrogen Framework', sources: 5, description: 'Subsidies allocation & industrial energy transition cohort model', updated: 'Modified 1 week ago' },
];

export default function NotebooksPage() {
  const router = useRouter();
  const [query, setQuery] = useState('');
  const filtered = useMemo(() => previewNotebooks.filter((notebook) => notebook.title.toLowerCase().includes(query.toLowerCase())), [query]);

  return (
    <ProtectedRoute>
    <div className="flex h-[calc(100vh-3px)] min-h-[620px] flex-col overflow-hidden bg-[#0a0a0a]">
      <Header />
      <main className="flex min-h-0 flex-1">
        <aside className="flex w-[340px] shrink-0 flex-col border-r border-[#242424] bg-[#0c0c0c] max-md:absolute max-md:z-10 max-md:h-full max-md:-translate-x-[calc(100%-3.25rem)] max-md:transition-transform max-md:hover:translate-x-0">
          <div className="border-b border-[#1d1d1d] px-4 pb-4 pt-3.5">
            <div className="mb-3 flex items-center justify-between">
              <div className="flex items-center gap-1.5 text-base font-bold text-[#e5e2e1]">
                <FolderOpen className="h-[18px] w-[18px] text-[#ff9933]" />
                <h1>All Notebooks</h1>
              </div>
              <span className="h-5 min-w-[60px] bg-[#252525] px-2 text-center font-mono text-[10px] leading-5 text-[#71717a]">{previewNotebooks.length} STORED</span>
            </div>
            <label className="relative block">
              <span className="sr-only">Filter notebooks</span>
              <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-[#a1a1aa]" />
              <input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Filter notebooks..." className="h-9 w-full bg-[#1e1e1e] pl-9 pr-3 text-sm text-[#e5e2e1] placeholder:text-[#a1a1aa] focus:bg-[#252525] focus:outline-none" />
            </label>
          </div>
          <div className="min-h-0 flex-1 overflow-y-auto px-2 pt-[392px] max-md:pt-6">
            {filtered.map((notebook) => (
              <button key={notebook.id} onClick={() => router.push(`/notebooks/${notebook.id}/new`)} className="mb-1.5 w-full border border-[#1e1e1e] bg-[#1a1a1a] p-3.5 text-left transition hover:border-[#3f3f46] hover:bg-[#202020]">
                <div className="flex items-start justify-between gap-2">
                  <span className="truncate text-sm font-bold text-[#e5e2e1]">{notebook.title}</span>
                  <span className="shrink-0 bg-[#071326] px-1.5 py-0.5 font-mono text-[9px] uppercase text-[#60a5fa]">{notebook.sources}<br />SOURCES</span>
                </div>
                <p className="mt-3 text-xs leading-5 text-[#e2bfb2]">{notebook.description}</p>
                <span className="mt-2 block text-[10px] text-[#60a5fa]">{notebook.updated}</span>
              </button>
            ))}
          </div>
        </aside>

        <section className="flex min-w-0 flex-1 items-center justify-center bg-[#101010] p-5 sm:p-8">
          <div className="w-full max-w-[514px] border border-[#252525] bg-[#1a1a1a] px-8 py-10 text-center shadow-[0_12px_28px_rgba(0,0,0,0.24)] sm:px-12">
            <div className="mx-auto mb-8 flex h-20 w-20 items-center justify-center rounded-xl bg-[#292929] text-[#ff9933] shadow-inner">
              <Plus className="h-8 w-8" strokeWidth={2.4} />
            </div>
            <h2 className="text-2xl font-bold text-[#e5e2e1]">Create New Notebook</h2>
            <p className="mx-auto mt-3 max-w-[360px] text-sm leading-6 text-[#9ec0e8]">Upload bills, acts, gazettes, or research documents to begin sovereign analysis and synthesis.</p>
            <button onClick={() => router.push('/notebooks/new/new')} className="mt-6 inline-flex h-11 items-center gap-2 bg-[#ff671f] px-7 text-sm font-bold uppercase tracking-[0.11em] text-[#591b00] transition hover:bg-[#e05a1b]">
              <Plus className="h-5 w-5" /> Add Notebook
            </button>
          </div>
        </section>
      </main>
      <Footer />
    </div>
    </ProtectedRoute>
  );
}
