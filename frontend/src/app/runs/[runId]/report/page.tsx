'use client';

import React, { useState } from 'react';
import { useRunReport } from '@/hooks/useQueries';
import { useExportRun, useSendRunChat } from '@/hooks/useMutations';
import { Download, FileText, Send, Loader2 } from 'lucide-react';
import ReactMarkdown from 'react-markdown';

export default function ReportPage({ params }: { params: { runId: string } }) {
  const { runId } = params;
  const { data: report, isLoading: isReportLoading } = useRunReport(runId);
  const { mutate: exportRun, isPending: isExporting } = useExportRun(runId);
  const { mutate: sendChat, isPending: isSending } = useSendRunChat(runId);

  const [chatInput, setChatInput] = useState('');
  const [chatHistory, setChatHistory] = useState<{ role: 'user' | 'ai', content: string }[]>([]);

  const handleExport = (format: 'pdf' | 'csv' | 'pptx') => {
    exportRun(format, {
      onSuccess: (data) => {
        // Handle export download here if needed. 
        // For Blob response, typically we'd create a blob URL and trigger download.
        if (data instanceof Blob) {
          const url = window.URL.createObjectURL(data);
          const a = document.createElement('a');
          a.href = url;
          a.download = `report-${runId}.${format}`;
          a.click();
          window.URL.revokeObjectURL(url);
        }
      }
    });
  };

  const handleSendChat = (e: React.FormEvent) => {
    e.preventDefault();
    if (!chatInput.trim()) return;

    const message = chatInput.trim();
    setChatHistory(prev => [...prev, { role: 'user', content: message }]);
    setChatInput('');

    sendChat(message, {
      onSuccess: (response) => {
        if (response?.reply) {
          setChatHistory(prev => [...prev, { role: 'ai', content: response.reply as string }]);
        }
      }
    });
  };

  if (isReportLoading) {
    return (
      <div className="flex items-center justify-center h-full">
        <Loader2 className="w-8 h-8 animate-spin text-saffron" />
      </div>
    );
  }

  return (
    <div className="p-6 max-w-7xl mx-auto flex flex-col gap-8 h-full">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-xl font-bold text-white mb-1">Impact Report</h1>
          <p className="text-sm text-text-secondary">Comprehensive analysis and summary</p>
        </div>
        <div className="flex gap-3">
          <button
            onClick={() => handleExport('pdf')}
            disabled={isExporting}
            className="bg-surface-2 border border-surface-3 px-4 py-2 rounded flex items-center gap-2 hover:bg-surface-3 transition-colors text-white uppercase text-sm font-medium tracking-wider"
          >
            <FileText className="w-4 h-4" /> PDF
          </button>
          <button
            onClick={() => handleExport('csv')}
            disabled={isExporting}
            className="bg-surface-2 border border-surface-3 px-4 py-2 rounded flex items-center gap-2 hover:bg-surface-3 transition-colors text-white uppercase text-sm font-medium tracking-wider"
          >
            <FileText className="w-4 h-4" /> CSV
          </button>
          <button
            onClick={() => handleExport('pptx')}
            disabled={isExporting}
            className="bg-surface-2 border border-surface-3 px-4 py-2 rounded flex items-center gap-2 hover:bg-surface-3 transition-colors text-white uppercase text-sm font-medium tracking-wider"
          >
            <FileText className="w-4 h-4" /> PPTX
          </button>
        </div>
      </div>

      <div className="bg-surface-2 rounded-xl p-8 border border-surface-3 prose prose-invert max-w-none flex-1 overflow-y-auto">
        {report?.markdown ? (
          <ReactMarkdown>{report.markdown}</ReactMarkdown>
        ) : (
          <p className="text-text-muted">No report content available.</p>
        )}
      </div>

      <div className="bg-surface-2 rounded-xl border border-surface-3 flex flex-col h-80">
        <div className="flex-1 p-4 overflow-y-auto flex flex-col gap-4">
          {chatHistory.length === 0 ? (
            <div className="text-center text-text-muted my-auto">
              Ask questions about this report...
            </div>
          ) : (
            chatHistory.map((msg, i) => (
              <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div className={`max-w-[80%] rounded-lg p-3 ${msg.role === 'user' ? 'bg-saffron text-[#0A0A0A]' : 'bg-surface-3 text-white'}`}>
                  {msg.content}
                </div>
              </div>
            ))
          )}
          {isSending && (
            <div className="flex justify-start">
              <div className="max-w-[80%] rounded-lg p-3 bg-surface-3 text-white">
                <Loader2 className="w-4 h-4 animate-spin" />
              </div>
            </div>
          )}
        </div>
        <form onSubmit={handleSendChat} className="border-t border-surface-3 p-4 flex gap-3">
          <input
            type="text"
            value={chatInput}
            onChange={(e) => setChatInput(e.target.value)}
            placeholder="Ask about the report..."
            className="flex-1 bg-[#121212] border border-[#2A2A2A] rounded px-4 h-11 text-white focus:outline-none focus:ring-1 focus:ring-saffron"
            disabled={isSending}
          />
          <button
            type="submit"
            disabled={isSending || !chatInput.trim()}
            className="h-11 px-6 bg-saffron text-[#0A0A0A] font-medium uppercase tracking-wider rounded flex items-center justify-center gap-2 hover:bg-[#E05A1B] transition-colors disabled:opacity-50"
          >
            <Send className="w-4 h-4" /> Send
          </button>
        </form>
      </div>
    </div>
  );
}
