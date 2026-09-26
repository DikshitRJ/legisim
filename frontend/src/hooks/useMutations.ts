"use client";

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { api, clearAuthToken, queryKeys, setAuthToken, type ChatResponse, type LoginRequest, type NotebookCreate, type NotebookUpdate, type ResumeRunRequest, type RunStartRequest } from "@/lib/api";

export const useLogin = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload: LoginRequest) => api.auth.login(payload),
    onSuccess: (session) => {
      setAuthToken(session.token);
      queryClient.setQueryData(queryKeys.auth.me, session.user);
    },
  });
};

export const useLogout = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.auth.logout,
    onSettled: () => {
      clearAuthToken();
      queryClient.clear();
    },
  });
};

export const useCreateNotebook = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload: NotebookCreate) => api.notebooks.create(payload),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: queryKeys.notebooks.all }),
  });
};

export const useUpdateNotebook = (notebookId: string) => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload: NotebookUpdate) => api.notebooks.update(notebookId, payload),
    onSuccess: (notebook) => {
      queryClient.setQueryData(queryKeys.notebooks.detail(notebookId), notebook);
      queryClient.invalidateQueries({ queryKey: queryKeys.notebooks.all });
    },
  });
};

export const useArchiveNotebook = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (notebookId: string) => api.notebooks.archive(notebookId),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: queryKeys.notebooks.all }),
  });
};

export const useStartRun = () =>
  useMutation({ mutationFn: (payload: RunStartRequest) => api.runs.create(payload) });

export const useResumeRun = (runId: string) => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload: ResumeRunRequest) => api.runs.resume(runId, payload),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: queryKeys.runs.status(runId) }),
  });
};

export const useSendRunChat = (runId: string) => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (message: string) => api.runs.chat(runId, { message }),
    onMutate: async (message) => {
      const key = [...queryKeys.runs.groups(runId), "chat"] as const;
      await queryClient.cancelQueries({ queryKey: key });
      const previous = queryClient.getQueryData<ChatResponse[]>(key);
      queryClient.setQueryData<ChatResponse[]>(key, (current = []) => [...current, { reply: message }]);
      return { key, previous };
    },
    onError: (_error, _message, context) => {
      if (context) queryClient.setQueryData(context.key, context.previous);
    },
    onSettled: () => queryClient.invalidateQueries({ queryKey: queryKeys.runs.groups(runId) }),
  });
};

export const useCompareRuns = () =>
  useMutation({ mutationFn: (runIds: string[]) => api.compare({ runIds }) });

export const useExportRun = (runId: string) =>
  useMutation({ mutationFn: (format: "pdf" | "csv" | "pptx") => api.runs.export(runId, format) });
