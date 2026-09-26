# API Integration Plan

## 1. Overview
This phase transitions the LegiSim Next.js prototype from mock data to real API endpoints using TanStack Query. 

### Recommended Subagents
- `ui-builder`: For hook implementation, loading states, and error boundaries.
- `opencode`: For boilerplate hook definitions and replacing import statements across the app.

## 2. TanStack Query Setup

### 2.1 Provider Configuration (`/src/app/providers.tsx`)
Wrap the application in the QueryClientProvider.

```typescript
'use client'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { useState } from 'react'

export default function Providers({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(() => new QueryClient({
    defaultOptions: {
      queries: {
        staleTime: 1000 * 60 * 5, // 5 minutes
        refetchOnWindowFocus: false,
      },
    },
  }))
  return <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
}
```

## 3. Query Hooks (Data Fetching)
Create `/src/hooks/api/useQueries.ts`.

```typescript
import { useQuery } from '@tanstack/react-query';
import { api } from '@/lib/api-client'; // Axios or fetch wrapper

// Notebooks
export const useNotebooks = () => useQuery({
  queryKey: ['notebooks'],
  queryFn: () => api.get('/api/v1/notebooks').then(res => res.data)
});

// Run Data Fetchers
export const useRunSummary = (runId: string) => useQuery({
  queryKey: ['runs', runId, 'summary'],
  queryFn: () => api.get(`/api/v1/runs/${runId}/summary`).then(res => res.data),
  enabled: !!runId
});

export const useRunDashboard = (runId: string) => useQuery({
  queryKey: ['runs', runId, 'dashboard'],
  queryFn: () => api.get(`/api/v1/runs/${runId}/dashboard`).then(res => res.data),
  enabled: !!runId
});

// Replaces prototype mock imports:
// BEFORE: import { getRippleData } from '@/lib/mock-data'
// AFTER: const { data: rippleData, isLoading } = useRunRipple(runId)
export const useRunRipple = (runId: string) => useQuery({
  queryKey: ['runs', runId, 'ripple'],
  queryFn: () => api.get(`/api/v1/runs/${runId}/ripple`).then(res => res.data),
  enabled: !!runId
});

export const useRunTimeline = (runId: string) => useQuery({
  queryKey: ['runs', runId, 'timeline'],
  queryFn: () => api.get(`/api/v1/runs/${runId}/time`).then(res => res.data),
  enabled: !!runId
});
```

## 4. Mutation Hooks (Actions)
Create `/src/hooks/api/useMutations.ts`.

```typescript
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '@/lib/api-client';

export const useCreateNotebook = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: Partial<Notebook>) => api.post('/api/v1/notebooks', data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['notebooks'] })
  });
};

export const useStartRun = () => useMutation({
  mutationFn: (notebookId: string) => api.post(`/api/v1/notebooks/${notebookId}/runs`),
});

export const useSendChat = (runId: string) => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (message: string) => api.post(`/api/v1/runs/${runId}/chat`, { message }),
    // Optimistic update pattern
    onMutate: async (newMessage) => {
      await queryClient.cancelQueries({ queryKey: ['runs', runId, 'groups', 'chat'] });
      const previousChat = queryClient.getQueryData(['runs', runId, 'groups', 'chat']);
      queryClient.setQueryData(['runs', runId, 'groups', 'chat'], (old: any) => [...old, { id: 'temp', role: 'user', content: newMessage }]);
      return { previousChat };
    },
    onError: (err, newMsg, context) => {
      queryClient.setQueryData(['runs', runId, 'groups', 'chat'], context?.previousChat);
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ['runs', runId, 'groups', 'chat'] });
    }
  });
};
```

## 5. SSE Integration for Loading Screen
The prototype `/runs/[runId]/loading` page currently uses a hardcoded `setTimeout` sequence. We will replace this with an SSE hook to stream real simulation progress.

```typescript
// /src/hooks/useSimulationProgress.ts
import { useEffect, useState } from 'react';

export function useSimulationProgress(runId: string) {
  const [progress, setProgress] = useState({ percent: 0, status: 'Initializing...' });
  const [isComplete, setIsComplete] = useState(false);

  useEffect(() => {
    if (!runId) return;
    const eventSource = new EventSource(`/api/v1/runs/${runId}/progress/stream`);
    
    eventSource.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setProgress({ percent: data.percent, status: data.status });
      if (data.percent >= 100 || data.status === 'COMPLETED') {
        setIsComplete(true);
        eventSource.close();
      }
    };

    eventSource.onerror = () => eventSource.close();
    return () => eventSource.close();
  }, [runId]);

  return { progress, isComplete };
}
```

## 6. Acceptance Criteria
- All mock data imports are completely removed from pages and components.
- Loading states (using shadcn skeletons) are displayed during data fetch.
- SSE correctly populates the loading screen up to 100%, then redirects to the `/runs/[runId]/summary` page.
- Optimistic updates make chat interactions feel instant.
