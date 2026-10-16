"use client";

import { FormEvent, Suspense, useState } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { Eye, EyeOff, Loader2 } from "lucide-react";
import { fetchApi } from "@/lib/api";

function ResetPasswordForm() {
  const router = useRouter();
  const params = useSearchParams();
  const [password, setPassword] = useState("");
  const [confirmation, setConfirmation] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function submit(event: FormEvent) {
    event.preventDefault();
    if (password !== confirmation) { setError("Passwords do not match."); return; }
    setLoading(true); setError(null);
    try {
      await fetchApi("/auth/password-reset/confirm/", { method: "POST", body: JSON.stringify({ uid: params.get("uid"), token: params.get("token"), password }) });
      router.replace("/account/login?reset=success");
    } catch (requestError: unknown) {
      const detail = requestError instanceof Error ? requestError.message : "Could not reset your password.";
      setError(detail);
    } finally { setLoading(false); }
  }

  const inputType = showPassword ? "text" : "password";
  return <div className="max-w-md mx-auto px-4 py-16 sm:py-24"><div className="bg-white p-8 rounded-3xl border border-neutral-200/80 shadow-xl space-y-6"><div className="text-center space-y-2"><span className="font-serif text-2xl font-bold text-brand-dark">CROWNLUXE</span><h1 className="text-xl font-bold text-neutral-900">Choose a new password</h1><p className="text-xs text-neutral-500">Use at least 8 characters and keep it private.</p></div><form onSubmit={submit} className="space-y-4 text-xs"><div><label className="mb-1 block font-semibold text-neutral-700">New password</label><div className="relative"><input type={inputType} required minLength={8} autoComplete="new-password" value={password} onChange={(event) => setPassword(event.target.value)} className="w-full rounded-xl border border-neutral-200 bg-neutral-50 px-3.5 py-3 pr-11 text-neutral-900 focus:border-brand-500 focus:outline-none" /><button type="button" onClick={() => setShowPassword((value) => !value)} className="absolute inset-y-0 right-0 px-3 text-neutral-500" aria-label={showPassword ? "Hide password" : "Show password"}>{showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}</button></div></div><div><label className="mb-1 block font-semibold text-neutral-700">Confirm password</label><input type={inputType} required minLength={8} autoComplete="new-password" value={confirmation} onChange={(event) => setConfirmation(event.target.value)} className="w-full rounded-xl border border-neutral-200 bg-neutral-50 px-3.5 py-3 text-neutral-900 focus:border-brand-500 focus:outline-none" /></div>{error && <p className="rounded-xl border border-red-200 bg-red-50 p-3 text-red-700">{error}</p>}<button disabled={loading} className="flex w-full items-center justify-center gap-2 rounded-xl bg-brand-dark py-3.5 font-bold text-white transition hover:bg-neutral-800 disabled:opacity-50">{loading && <Loader2 className="h-4 w-4 animate-spin" />}{loading ? "Saving…" : "Reset password"}</button></form><p className="text-center text-xs text-neutral-500"><Link href="/account/login" className="font-bold text-brand-600 hover:underline">Back to sign in</Link></p></div></div>;
}

export default function ResetPasswordPage() {
  return <Suspense fallback={<div className="min-h-screen grid place-items-center text-sm text-neutral-500">Loading reset form…</div>}><ResetPasswordForm /></Suspense>;
}
