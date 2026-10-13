"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { Lock, Mail, ArrowRight, AlertCircle, Loader2 } from "lucide-react";

export default function LoginPage() {
  const router = useRouter();
  const { login } = useAuth();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      await login(username, password);
      router.push("/account");
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

        <form onSubmit={handleSubmit} className="space-y-4 text-xs">
          <div>
            <label className="block font-semibold text-neutral-700 mb-1">Username or Email</label>
            <input
              type="text"
              required
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="e.g. nakato_e"
              className="w-full bg-neutral-50 border border-neutral-200 rounded-xl px-3.5 py-3 text-neutral-900 focus:outline-none focus:border-brand-500"
            />
          </div>

          <div>
            <div className="flex justify-between items-center mb-1">
              <label className="block font-semibold text-neutral-700">Password</label>
            </div>
            <input
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              className="w-full bg-neutral-50 border border-neutral-200 rounded-xl px-3.5 py-3 text-neutral-900 focus:outline-none focus:border-brand-500"
            />
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
          <Link href="/account/register" className="text-brand-600 font-bold hover:underline">
            Create Account
          </Link>
        </div>

        <div className="bg-neutral-50 p-3 rounded-xl text-[11px] text-neutral-500 text-center font-mono">
          Demo Customer: <strong>nakato_e</strong> / <strong>customer123</strong>
        </div>
      </div>
    </div>
  );
}
