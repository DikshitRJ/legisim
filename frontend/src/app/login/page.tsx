'use client';

import { FormEvent, useState } from 'react';
import { useRouter } from 'next/navigation';

export default function LoginPage() {
  const router = useRouter();
  const [officerId, setOfficerId] = useState('');
  const [password, setPassword] = useState('');
  const [submitting, setSubmitting] = useState(false);

  async function handleSignIn(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmitting(true);

    // TODO(api): replace this UI hand-off with POST /api/auth/login and route only after the session is established.
    router.push('/notebooks');
  }

  return (
    <main className="portal-grid relative flex min-h-[calc(100vh-3px)] overflow-hidden bg-[#0e0e0e] px-5 py-6 sm:px-12 sm:py-12">
      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(255,103,31,0.065),transparent_34%)]" />
      <div className="relative z-10 flex w-full flex-col justify-between">
        <div className="flex justify-end text-right">
          <div className="font-sans text-[10px] font-semibold uppercase tracking-[0.16em] leading-4 text-[#e2bfb2]">
            <div>Secure Access Level 4</div>
            <div className="text-[#a98a7e]">Restricted Portal</div>
          </div>
        </div>

        <section aria-labelledby="login-title" className="mx-auto w-full max-w-[420px] overflow-hidden rounded-lg border border-[#252525] bg-[#1c1b1b] shadow-[0_24px_60px_rgba(0,0,0,0.65)]">
          <div aria-hidden="true" className="flex h-[3px] w-full"><span className="flex-1 bg-[#ff671f]" /><span className="flex-1 bg-[#e5e2e1]" /><span className="flex-1 bg-[#006836]" /></div>
          <div className="p-8 sm:p-10">
            <h1 id="login-title" className="mb-8 text-center text-[30px] font-bold tracking-[0.22em] text-[#e5e2e1] sm:text-[32px]">LEGISIM</h1>
            <form className="flex flex-col gap-5" onSubmit={handleSignIn}>
              <label className="flex flex-col gap-1.5 text-xs font-semibold uppercase tracking-[0.055em] text-[#e5e2e1]">
                Officer ID / Login ID
                <input autoComplete="username" required value={officerId} onChange={(event) => setOfficerId(event.target.value)} placeholder="GOI-XXXX-XXXX" className="h-11 rounded border border-[#252525] bg-[#0e0e0e] px-3.5 text-sm font-normal normal-case tracking-normal text-[#e5e2e1] placeholder:text-[#71717a] transition focus:border-[#ff671f] focus:bg-[#2a2a2a] focus:shadow-[0_0_0_1px_#ff671f,0_0_12px_rgba(255,103,31,0.25)] focus:outline-none" />
              </label>
              <label className="flex flex-col gap-1.5 text-xs font-semibold uppercase tracking-[0.055em] text-[#e5e2e1]">
                Password
                <input autoComplete="current-password" required type="password" value={password} onChange={(event) => setPassword(event.target.value)} placeholder="••••••••••••" className="h-11 rounded border border-[#252525] bg-[#0e0e0e] px-3.5 text-sm font-normal normal-case tracking-normal text-[#e5e2e1] placeholder:text-[#71717a] transition focus:border-[#ff671f] focus:bg-[#2a2a2a] focus:shadow-[0_0_0_1px_#ff671f,0_0_12px_rgba(255,103,31,0.25)] focus:outline-none" />
              </label>
              <button type="submit" disabled={submitting} className="mt-4 h-12 rounded bg-[#ff671f] text-sm font-bold uppercase tracking-[0.15em] text-[#591b00] transition hover:bg-[#e05a1b] disabled:cursor-wait disabled:opacity-80">
                {submitting ? 'Signing in…' : 'Sign In'}
              </button>
            </form>
          </div>
        </section>

        <div className="h-4" />
      </div>
    </main>
  );
}
