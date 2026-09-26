'use client';

import { useMemo, useState } from 'react';
import { useRouter } from 'next/navigation';
import { FolderOpen, Plus, Search, Loader2, AlertTriangle, X } from 'lucide-react';
import Footer from '@/components/layout/Footer';
import Header from '@/components/layout/Header';
import { useNotebooks } from '@/hooks/useQueries';
import { useCreateNotebook } from '@/hooks/useMutations';

function formatRelativeTime(dateString: string) {
  const date = new Date(dateString);
  const diffInSeconds = Math.floor((Date.now() - date.getTime()) / 1000);
  
  if (diffInSeconds < 60) return 'Modified just now';
  const diffInMinutes = Math.floor(diffInSeconds / 60);
  if (diffInMinutes < 60) return `Modified ${diffInMinutes} minute${diffInMinutes > 1 ? 's' : ''} ago`;
  const diffInHours = Math.floor(diffInMinutes / 60);
  if (diffInHours < 24) return `Modified ${diffInHours} hour${diffInHours > 1 ? 's' : ''} ago`;
  const diffInDays = Math.floor(diffInHours / 24);
  if (diffInDays < 7) return `Modified ${diffInDays} day${diffInDays > 1 ? 's' : ''} ago`;
  const diffInWeeks = Math.floor(diffInDays / 7);
  if (diffInWeeks < 4) return `Modified ${diffInWeeks} week${diffInWeeks > 1 ? 's' : ''} ago`;
  const diffInMonths = Math.floor(diffInDays / 30);
  if (diffInMonths < 12) return `Modified ${diffInMonths} month${diffInMonths > 1 ? 's' : ''} ago`;
  const diffInYears = Math.floor(diffInDays / 365);
  return `Modified ${diffInYears} year${diffInYears > 1 ? 's' : ''} ago`;
}

function CreateNotebookModal({ isOpen, onClose }: { isOpen: boolean; onClose: () => void }) {
  const router = useRouter();
  const createNotebook = useCreateNotebook();
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');

  if (!isOpen) return null;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    createNotebook.mutate({ title, description }, {
      onSuccess: () => {
        onClose();
        setTitle('');
        setDescription('');
      }
    });
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4">
      <div className="w-full max-w-md rounded-lg border border-[#2a2a2a] bg-[#121212] p-6 shadow-xl relative overflow-hidden">
        <div className="absolute top-0 left-0 right-0 flex h-1 w-full">
          <div className="h-full flex-1 bg-[#FF671F]" />
          <div className="h-full flex-1 bg-white" />
          <div className="h-full flex-1 bg-[#046A38]" />
        </div>
        
        <div className="mb-4 mt-2 flex items-center justify-between">
          <h3 className="text-xl font-bold text-[#e5e2e1]">Create New Notebook</h3>
          <button onClick={onClose} className="text-[#a1a1aa] hover:text-[#e5e2e1]">
            <X className="h-5 w-5" />
          </button>
        </div>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="mb-1.5 block text-xs font-bold uppercase tracking-wider text-[#a1a1aa]">Title</label>
            <input 
              required
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="h-[44px] w-full rounded bg-[#121212] px-3 text-sm text-[#e5e2e1] border border-[#2a2a2a] focus:border-[#ff671f] focus:outline-none focus:ring-1 focus:ring-[#ff671f]"
              placeholder="e.g. National Green Hydrogen Framework"
            />
          </div>
          <div>
            <label className="mb-1.5 block text-xs font-bold uppercase tracking-wider text-[#a1a1aa]">Description</label>
            <textarea 
              required
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="min-h-[100px] w-full rounded bg-[#121212] p-3 text-sm text-[#e5e2e1] border border-[#2a2a2a] focus:border-[#ff671f] focus:outline-none focus:ring-1 focus:ring-[#ff671f]"
              placeholder="Brief description of the policy analysis..."
            />
          </div>
          <div className="mt-6 flex justify-end gap-3">
            <button 
              type="button" 
              onClick={onClose}
              className="px-4 py-2 text-sm font-bold uppercase text-[#e5e2e1] hover:text-[#ff671f]"
            >
              Cancel
            </button>
            <button 
              type="submit" 
              disabled={createNotebook.isPending}
              className="inline-flex h-[48px] items-center justify-center rounded bg-[#ff671f] px-6 text-sm font-bold uppercase tracking-wide text-[#0a0a0a] hover:bg-[#e05a1b] disabled:opacity-50"
            >
              {createNotebook.isPending ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : null}
              Create Notebook
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default function NotebooksPage() {
  const router = useRouter();
  const [query, setQuery] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const { data: notebooks, isLoading, isError } = useNotebooks();

  const filtered = useMemo(() => {
    if (!notebooks) return [];
    return notebooks.filter((notebook) => 
      notebook.title.toLowerCase().includes(query.toLowerCase()) || 
      notebook.description.toLowerCase().includes(query.toLowerCase())
    );
  }, [notebooks, query]);

  return (
    <div className="flex h-[calc(100vh-3px)] min-h-[620px] flex-col overflow-hidden bg-[#0a0a0a]">
      <Header />
      <main className="flex min-h-0 flex-1">
        <aside className="flex w-[340px] shrink-0 flex-col border-r border-[#242424] bg-[#0a0a0a] max-md:absolute max-md:z-10 max-md:h-full max-md:-translate-x-[calc(100%-3.25rem)] max-md:transition-transform max-md:hover:translate-x-0">
          <div className="border-b border-[#2a2a2a] px-4 pb-4 pt-3.5">
            <div className="mb-3 flex items-center justify-between">
              <div className="flex items-center gap-1.5 text-base font-bold text-[#e5e2e1]">
                <FolderOpen className="h-[18px] w-[18px] text-[#ff671f]" />
                <h1>All Notebooks</h1>
              </div>
              <span className="h-5 min-w-[60px] bg-[#1e1e1e] px-2 text-center font-mono text-[10px] leading-5 text-[#a1a1aa] rounded">
                {notebooks ? notebooks.length : 0} STORED
              </span>
            </div>
            <label className="relative block">
              <span className="sr-only">Filter notebooks</span>
              <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-[#71717a]" />
              <input 
                value={query} 
                onChange={(event) => setQuery(event.target.value)} 
                placeholder="Filter notebooks..." 
                className="h-[44px] w-full rounded border border-[#2a2a2a] bg-[#121212] pl-9 pr-3 text-sm text-[#e5e2e1] placeholder:text-[#71717a] focus:border-[#ff671f] focus:outline-none focus:ring-1 focus:ring-[#ff671f]" 
              />
            </label>
          </div>
          <div className="min-h-0 flex-1 overflow-y-auto px-2 pt-4">
            {isLoading && (
              <div className="space-y-2">
                {[1, 2, 3].map((i) => (
                  <div key={i} className="h-28 w-full animate-pulse rounded-lg border border-[#2a2a2a] bg-[#121212] p-3.5" />
                ))}
              </div>
            )}
            {isError && (
              <div className="p-4 text-center text-sm text-red-500">
                <AlertTriangle className="mx-auto mb-2 h-6 w-6" />
                Failed to load notebooks.
              </div>
            )}
            {!isLoading && !isError && filtered.length === 0 && (
              <div className="p-4 text-center text-sm text-[#71717a]">
                {query ? 'No notebooks matched your search.' : 'No notebooks found.'}
              </div>
            )}
            {!isLoading && !isError && filtered.map((notebook) => (
              <button 
                key={notebook.id} 
                onClick={() => router.push(`/notebooks/${notebook.id}/new`)} 
                className="mb-2 w-full rounded-lg border border-[#2a2a2a] bg-[#121212] p-3.5 text-left transition hover:border-[#ff671f]"
              >
                <div className="flex items-start justify-between gap-2">
                  <span className="line-clamp-1 text-sm font-bold text-[#e5e2e1]">{notebook.title}</span>
                  <span className="shrink-0 rounded bg-[#002868]/30 px-1.5 py-0.5 font-mono text-[9px] font-bold uppercase tracking-widest text-[#60a5fa]">
                    {notebook.sources} SOURCES
                  </span>
                </div>
                <p className="mt-2 line-clamp-2 text-xs leading-5 text-[#a1a1aa]">{notebook.description}</p>
                <span className="mt-2 block text-[10px] font-medium text-[#ff671f]">
                  {formatRelativeTime(notebook.modifiedAt)}
                </span>
              </button>
            ))}
          </div>
        </aside>

        <section className="flex min-w-0 flex-1 items-center justify-center bg-[#0a0a0a] p-5 sm:p-8">
          <div className="w-full max-w-[514px] rounded-lg border border-[#2a2a2a] bg-[#121212] px-8 py-10 text-center shadow-lg sm:px-12 relative overflow-hidden">
            <div className="absolute top-0 left-0 right-0 flex h-1 w-full">
              <div className="h-full flex-1 bg-[#FF671F]" />
              <div className="h-full flex-1 bg-white" />
              <div className="h-full flex-1 bg-[#046A38]" />
            </div>
            
            <div className="mx-auto mb-8 flex h-20 w-20 items-center justify-center rounded-xl bg-[#1e1e1e] text-[#ff671f] shadow-inner border border-[#2a2a2a]">
              <Plus className="h-8 w-8" strokeWidth={2.4} />
            </div>
            <h2 className="text-2xl font-bold text-[#e5e2e1]">Create New Notebook</h2>
            <p className="mx-auto mt-3 max-w-[360px] text-sm leading-6 text-[#a1a1aa]">
              Upload bills, acts, gazettes, or research documents to begin sovereign analysis and synthesis.
            </p>
            <button 
              onClick={() => setIsModalOpen(true)} 
              className="mt-6 inline-flex h-[48px] items-center gap-2 rounded bg-[#ff671f] px-8 text-sm font-bold uppercase tracking-widest text-[#0a0a0a] transition hover:bg-[#e05a1b]"
            >
              <Plus className="h-5 w-5" /> Add Notebook
            </button>
          </div>
        </section>
      </main>
      <Footer />
      <CreateNotebookModal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} />
    </div>
  );
}
