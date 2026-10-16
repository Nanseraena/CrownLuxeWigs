"use client";

import { FormEvent, useState } from "react";
import Link from "next/link";
import { CheckCircle2, Loader2, Mail } from "lucide-react";
import { fetchApi } from "@/lib/api";

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [sent, setSent] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function submit(event: FormEvent) {
    event.preventDefault();
    setLoading(true);
    setError(null);
    try {
      await fetchApi("/auth/password-reset/", { method: "POST", body: JSON.stringify({ email }) });
      setSent(true);
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Could not send the reset email. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  return <div className="max-w-md mx-auto px-4 py-16 sm:py-24">
    <div className="bg-white p-8 rounded-3xl border border-neutral-200/80 shadow-xl space-y-6">
      <div className="text-center space-y-2"><span className="font-serif text-2xl font-bold text-brand-dark">CROWNLUXE</span><h1 className="text-xl font-bold text-neutral-900">Reset your password</h1><p className="text-xs text-neutral-500">Enter your account email and we’ll send a secure reset link.</p></div>
      {sent ? <div className="rounded-2xl border border-emerald-200 bg-emerald-50 p-4 text-center text-xs text-emerald-800"><CheckCircle2 className="mx-auto mb-2 h-5 w-5" />If an account exists for <strong>{email}</strong>, a password reset link has been sent.</div> : <form onSubmit={submit} className="space-y-4 text-xs"><div><label className="mb-1 block font-semibold text-neutral-700">Email address</label><div className="relative"><Mail className="absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-neutral-400" /><input type="email" required autoComplete="email" value={email} onChange={(event) => setEmail(event.target.value)} placeholder="you@example.com" className="w-full rounded-xl border border-neutral-200 bg-neutral-50 py-3 pl-10 pr-3.5 text-neutral-900 focus:border-brand-500 focus:outline-none" /></div></div>{error && <p className="rounded-xl border border-red-200 bg-red-50 p-3 text-red-700">{error}</p>}<button disabled={loading} className="flex w-full items-center justify-center gap-2 rounded-xl bg-brand-dark py-3.5 font-bold text-white transition hover:bg-neutral-800 disabled:opacity-50">{loading && <Loader2 className="h-4 w-4 animate-spin" />}{loading ? "Sending…" : "Send reset link"}</button></form>}
      <p className="text-center text-xs text-neutral-500"><Link href="/account/login" className="font-bold text-brand-600 hover:underline">Back to sign in</Link></p>
    </div>
  </div>;
}
