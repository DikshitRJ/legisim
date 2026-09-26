'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useCurrentUser } from '@/hooks/useQueries';

export default function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const { data: user, isPending, isError } = useCurrentUser();

  useEffect(() => {
    if (!isPending && (isError || !user)) {
      router.replace('/login');
    }
  }, [isPending, isError, user, router]);

  if (isPending) {
    return (
      <div className="flex h-screen w-screen items-center justify-center bg-[#0a0a0a]">
        <div className="h-8 w-8 animate-spin rounded-full border-4 border-[#1e1e1e] border-t-[#ff671f]" />
      </div>
    );
  }

  if (isError || !user) {
    return null; // Will redirect in useEffect
  }

  return <>{children}</>;
}
