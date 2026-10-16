"use client";

import React, { FormEvent, Suspense, useEffect, useState } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { AlertCircle, Eye, EyeOff, Loader2 } from "lucide-react";

function safeNextPath(value: string | null) {
  return value && value.startsWith("/") && !value.startsWith("//") ? value : "/account";
}

function LoginForm() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { login, user, loading: authLoading } = useAuth();

  const [identifier, setIdentifier] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const destination = safeNextPath(searchParams.get("next"));
  const resetComplete = searchParams.get("reset") === "success";

  useEffect(() => {
    if (!authLoading && user) router.replace(destination);
  }, [authLoading, destination, router, user]);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      await login(identifier, password);
      router.replace(destination);
    } catch (err: any) {
      setError(err.message || "Invalid username or password.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto px-4 py-16 sm:py-24">
      <div className="bg-white p-8 rounded-3xl border border-neutral-200/80 shadow-xl space-y-6">
        <div className="text-center space-y-1">
          <span className="font-serif text-2xl font-bold text-brand-dark">CROWNLUXE</span>
          <h1 className="text-xl font-bold text-neutral-900">Welcome Back</h1>
          <p className="text-xs text-neutral-500">Sign in to manage orders, wishlist, and saved addresses.</p>
        </div>

        {error && (
          <div className="p-3.5 bg-red-50 text-red-700 text-xs rounded-2xl border border-red-200 flex items-center gap-2">
            <AlertCircle className="w-4 h-4 shrink-0 text-red-600" />
            <span>{error}</span>
          </div>
        )}

        {resetComplete && !error && (
          <div className="p-3.5 bg-emerald-50 text-emerald-800 text-xs rounded-2xl border border-emerald-200">
            Your password was reset. Sign in with your new password.
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4 text-xs">
          <div>
            <label className="block font-semibold text-neutral-700 mb-1">Username or Email</label>
            <input
              type="text"
              required
              autoComplete="username"
              value={identifier}
              onChange={(e) => setIdentifier(e.target.value)}
              placeholder="Email address or username"
              className="w-full bg-neutral-50 border border-neutral-200 rounded-xl px-3.5 py-3 text-neutral-900 focus:outline-none focus:border-brand-500"
            />
          </div>

          <div>
            <div className="flex justify-between items-center mb-1">
              <label className="block font-semibold text-neutral-700">Password</label>
              <Link href="/account/forgot-password" className="text-brand-600 font-bold hover:underline">Forgot password?</Link>
            </div>
            <div className="relative">
              <input type={showPassword ? "text" : "password"} required autoComplete="current-password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="••••••••" className="w-full bg-neutral-50 border border-neutral-200 rounded-xl px-3.5 py-3 pr-11 text-neutral-900 focus:outline-none focus:border-brand-500" />
              <button type="button" onClick={() => setShowPassword((value) => !value)} className="absolute inset-y-0 right-0 px-3 text-neutral-500 hover:text-brand-600" aria-label={showPassword ? "Hide password" : "Show password"}>{showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}</button>
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-brand-dark hover:bg-neutral-800 text-white font-bold py-3.5 rounded-xl transition flex items-center justify-center gap-2 shadow-lg shadow-neutral-900/10 disabled:opacity-50"
          >
            {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <span>Sign In</span>}
          </button>
        </form>

        <div className="pt-4 border-t border-neutral-100 text-center text-xs text-neutral-500">
          Don't have a CrownLuxe account?{" "}
          <Link href={`/account/register?next=${encodeURIComponent(destination)}`} className="text-brand-600 font-bold hover:underline">
            Create Account
          </Link>
        </div>

      </div>
    </div>
  );
}

export default function LoginPage() {
  return <Suspense fallback={<div className="min-h-screen grid place-items-center text-sm text-neutral-500">Loading sign in…</div>}><LoginForm /></Suspense>;
}
