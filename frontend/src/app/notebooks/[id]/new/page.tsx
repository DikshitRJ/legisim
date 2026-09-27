'use client';

import { useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { ArrowRight, Check, FileText, RotateCcw, Upload } from 'lucide-react';
import Footer from '@/components/layout/Footer';
import Header from '@/components/layout/Header';
import { useCohortCategories } from '@/hooks/useQueries';
import { useStartRun } from '@/hooks/useMutations';

export default function SetupWizardPage() {
  const router = useRouter();
  const params = useParams();
  const notebookId = params.id as string;
  
  // Fetch categories
  const { data: categories, isLoading, isError } = useCohortCategories();
  const startRun = useStartRun();

  // Map categoryId to an array of selected options
  const [selected, setSelected] = useState<Record<string, string[]>>({});
  const [notes, setNotes] = useState('');
  const [fileContents, setFileContents] = useState<string>('');
  const [files, setFiles] = useState<File[]>([]);

  const count = Object.values(selected).reduce((acc, curr) => acc + curr.length, 0);

  function toggle(categoryId: string, option: string) {
    setSelected((current) => {
      const catSelected = current[categoryId] || [];
      if (catSelected.includes(option)) {
        return {
          ...current,
          [categoryId]: catSelected.filter((o) => o !== option),
        };
      } else {
        return {
          ...current,
          [categoryId]: [...catSelected, option],
        };
      }
    });
  }

  async function handleFileUpload(e: React.ChangeEvent<HTMLInputElement>) {
    if (!e.target.files) return;
    const newFiles = Array.from(e.target.files);
    setFiles((prev) => [...prev, ...newFiles]);

    let combinedText = '';
    for (const file of newFiles) {
      if (file.name.endsWith('.pdf')) {
        combinedText += `\n\n--- [File: ${file.name}] ---\n(PDF content extraction requires backend processing. Filename registered.)\n`;
      } else {
        const text = await file.text();
        combinedText += `\n\n--- [File: ${file.name}] ---\n${text}\n`;
      }
    }
    setFileContents((prev) => prev + combinedText);
  }

  async function proceed() {
    const fullPolicyText = `${notes}\n\n${fileContents}`.trim();
    startRun.mutate(
      { policyText: fullPolicyText, cohorts: selected, notebookId },
      {
        onSuccess: (data) => {
          router.push(`/runs/${data.runId}/loading`);
        },
      }
    );
  }

  function resetSelections() {
    setSelected({});
    setNotes('');
    setFileContents('');
    setFiles([]);
  }

  // Handle loading and error
  if (isLoading) {
    return (
      <div className="flex min-h-[calc(100vh-3px)] flex-col bg-[#0e0e0e]">
        <Header showNav />
        <main className="mx-auto w-full max-w-[1008px] flex-1 px-4 py-11 sm:px-7 flex items-center justify-center">
           <div className="text-[#60a5fa]">Loading categories...</div>
        </main>
        <Footer />
      </div>
    );
  }

  if (isError || !categories) {
    return (
      <div className="flex min-h-[calc(100vh-3px)] flex-col bg-[#0e0e0e]">
        <Header showNav />
        <main className="mx-auto w-full max-w-[1008px] flex-1 px-4 py-11 sm:px-7 flex items-center justify-center">
           <div className="text-red-500">Failed to load categories.</div>
        </main>
        <Footer />
      </div>
    );
  }

  return (
    <div className="flex min-h-[calc(100vh-3px)] flex-col bg-[#0e0e0e]">
      <Header showNav />
      <main className="mx-auto w-full max-w-[1008px] flex-1 px-4 py-11 sm:px-7">
        <div className="space-y-6">
          {categories.map((category) => (
            <section key={category.id} aria-labelledby={`${category.id}-heading`} className="rounded-xl bg-[#161616] p-5 shadow-[0_12px_28px_rgba(0,0,0,0.2)] sm:p-7">
              <div className="mb-4 flex items-center gap-3">
                <span className="flex h-7 w-7 items-center justify-center rounded-lg bg-[#1e293b] font-mono text-xs font-bold text-[#60a5fa]">{String(category.number).padStart(2, '0')}</span>
                <h1 id={`${category.id}-heading`} className="text-base font-semibold text-white sm:text-lg">{category.title}</h1>
              </div>
              <div className="flex flex-wrap gap-2.5">
                {category.options.map((option) => {
                  const active = selected[category.id]?.includes(option) ?? false;
                  return (
                    <button key={option} type="button" onClick={() => toggle(category.id, option)} aria-pressed={active} className={`flex items-center gap-2 rounded-lg px-3.5 py-2 text-left text-xs font-medium transition sm:text-sm ${active ? 'bg-[#1e293b] text-[#60a5fa] shadow-[0_0_12px_rgba(59,130,246,0.25)]' : 'bg-[#111111] text-[#cbd5e1] hover:bg-[#1a1f2c] hover:text-white'}`}>
                      <Check className={`h-3.5 w-3.5 shrink-0 transition-opacity ${active ? 'opacity-100 text-[#3b82f6]' : 'opacity-0 text-transparent'}`} />
                      <span>{option}</span>
                    </button>
                  );
                })}
              </div>
            </section>
          ))}

          <section className="rounded-xl bg-[#161616] p-5 shadow-[0_12px_28px_rgba(0,0,0,0.2)] sm:p-7">
            <label htmlFor="policy-notes" className="flex items-center gap-2 text-sm font-semibold text-white"><FileText className="h-4 w-4 text-[#3b82f6]" />Policy Notes &amp; Additional Constraints</label>
            <p className="mt-3 text-xs text-[#94a3b8]">Specify custom exclusions, temporal conditions, or micro-targeting provisions.</p>
            <textarea id="policy-notes" value={notes} onChange={(event) => setNotes(event.target.value)} placeholder="add details here" rows={5} className="mt-3 w-full resize-y rounded-lg bg-[#111111] p-4 text-sm text-[#f8fafc] placeholder:text-[#64748b] focus:bg-[#151515] focus:outline-none" />
            
            <div className="mt-6">
              <label className="flex items-center gap-2 text-sm font-semibold text-white mb-2"><Upload className="h-4 w-4 text-[#3b82f6]" />Upload Policy Documents</label>
              <p className="text-xs text-[#94a3b8] mb-3">Upload markdown, text, or pdf files to provide full context to the agents.</p>
              
              <input type="file" multiple accept=".md,.txt,.pdf,.csv" onChange={handleFileUpload} className="block w-full text-sm text-[#94a3b8] file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-[#1e293b] file:text-[#60a5fa] hover:file:bg-[#253755] transition" />
              
              {files.length > 0 && (
                <div className="mt-4 flex flex-col gap-2">
                  <h4 className="text-xs font-semibold text-[#cbd5e1]">Attached Files:</h4>
                  <ul className="text-xs text-[#94a3b8] list-disc list-inside">
                    {files.map((f, i) => <li key={i}>{f.name} ({(f.size / 1024).toFixed(1)} KB)</li>)}
                  </ul>
                </div>
              )}
            </div>
          </section>

          <section className="flex flex-col-reverse items-center justify-between gap-4 rounded-xl bg-[#161616] p-4 shadow-[0_12px_28px_rgba(0,0,0,0.24)] sm:flex-row sm:p-6">
            <div className="flex items-center gap-2 font-mono text-[11px] uppercase tracking-wide text-[#94a3b8]"><span className="h-2 w-2 animate-pulse rounded-full bg-emerald-500" />PORTAL_STATUS: READY FOR INGESTION {count > 0 && <span className="text-[#60a5fa]">• {count} SELECTED</span>}</div>
            <div className="flex w-full items-center gap-3 sm:w-auto">
              <button type="button" onClick={resetSelections} className="flex flex-1 items-center justify-center gap-2 rounded-lg bg-[#111111] px-5 py-2.5 text-xs font-semibold text-[#94a3b8] transition hover:bg-[#1f2430] hover:text-[#f8fafc] sm:flex-none sm:text-sm"><RotateCcw className="h-4 w-4" />Reset Selections</button>
              <button type="button" onClick={proceed} disabled={startRun.isPending} className="flex flex-1 items-center justify-center gap-2 rounded-lg bg-[#2563eb] px-6 py-2.5 text-xs font-bold text-white shadow-lg shadow-blue-950/30 transition hover:bg-[#1d4ed8] disabled:cursor-wait disabled:opacity-70 sm:flex-none sm:text-sm">{startRun.isPending ? 'Saving…' : 'Proceed / Save Cohort'}<ArrowRight className="h-4 w-4" /></button>
            </div>
          </section>
        </div>
      </main>
      <Footer />
    </div>
  );
}

