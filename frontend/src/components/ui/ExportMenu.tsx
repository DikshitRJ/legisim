'use client';

import React, { useState } from 'react';
import { Download, FileText, FileSpreadsheet, Presentation, Loader2 } from 'lucide-react';
import { useExportRun } from '@/hooks/useMutations';
import { ExportFormat } from '@/lib/api/types';

interface ExportMenuProps {
  runId: string;
}

export default function ExportMenu({ runId }: ExportMenuProps) {
  const [isOpen, setIsOpen] = useState(false);
  const exportMutation = useExportRun(runId);

  const handleExport = async (format: ExportFormat) => {
    setIsOpen(false);
    try {
      const result = await exportMutation.mutateAsync(format);
      const blob = new Blob([result as any]); // Assuming it returns blob/buffer
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `legisim-report-${runId}.${format}`;
      a.click();
      URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Export failed', error);
    }
  };

  return (
    <div className="relative inline-block text-left">
      <button
        onClick={() => setIsOpen(!isOpen)}
        disabled={exportMutation.isPending}
        className="flex items-center gap-2 bg-surface-2 border border-surface-3 px-4 py-2 rounded-md hover:bg-surface-3 transition-colors text-text-body text-sm font-semibold uppercase tracking-widest h-12"
      >
        {exportMutation.isPending ? (
          <Loader2 className="w-4 h-4 animate-spin" />
        ) : (
          <Download className="w-4 h-4" />
        )}
        Export
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 w-48 bg-surface-2 border border-surface-3 rounded-md shadow-lg z-50">
          <div className="py-1">
            <button
              onClick={() => handleExport('pdf')}
              className="flex items-center gap-3 w-full px-4 py-2 text-sm text-text-body hover:bg-surface-3 transition-colors"
            >
              <FileText className="w-4 h-4 text-saffron" />
              PDF Report
            </button>
            <button
              onClick={() => handleExport('csv')}
              className="flex items-center gap-3 w-full px-4 py-2 text-sm text-text-body hover:bg-surface-3 transition-colors"
            >
              <FileSpreadsheet className="w-4 h-4 text-india-green" />
              CSV Data
            </button>
            <button
              onClick={() => handleExport('pptx')}
              className="flex items-center gap-3 w-full px-4 py-2 text-sm text-text-body hover:bg-surface-3 transition-colors"
            >
              <Presentation className="w-4 h-4 text-blue-500" />
              PPTX Presentation
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
