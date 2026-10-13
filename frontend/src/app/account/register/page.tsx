"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { AlertCircle, Loader2 } from "lucide-react";

export default function RegisterPage() {
  const router = useRouter();
  const { register } = useAuth();

  const [formData, setFormData] = useState({
    username: "",
    email: "",
    first_name: "",
    last_name: "",
    password: "",
    phone: "",
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      await register(formData);
      router.push("/account");
    } catch (err: any) {
      setError(err.data?.email || err.data?.username || err.data?.password || err.message || "Registration failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto px-4 py-16 sm:py-24">
      <div className="bg-white p-8 rounded-3xl border border-neutral-200/80 shadow-xl space-y-6">
        <div className="text-center space-y-1">
          <span className="font-serif text-2xl font-bold text-brand-dark">CROWNLUXE</span>
          <h1 className="text-xl font-bold text-neutral-900">Create An Account</h1>
          <p className="text-xs text-neutral-500">Join our VIP Hair Club for rewards and express checkout.</p>
        </div>

        {error && (
          <div className="p-3.5 bg-red-50 text-red-700 text-xs rounded-2xl border border-red-200 flex items-center gap-2">
            <AlertCircle className="w-4 h-4 shrink-0 text-red-600" />
            <span>{typeof error === "string" ? error : JSON.stringify(error)}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-3.5 text-xs">
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block font-semibold text-neutral-700 mb-1">First Name</label>
              <input
                type="text"
                required
                value={formData.first_name}
                onChange={(e) => setFormData({ ...formData, first_name: e.target.value })}
                placeholder="e.g. Florence"
                className="w-full bg-neutral-50 border border-neutral-200 rounded-xl px-3 py-2.5 text-neutral-900 focus:outline-none focus:border-brand-500"
              />
            </div>
            <div>
              <label className="block font-semibold text-neutral-700 mb-1">Last Name</label>
              <input
                type="text"
                required
                value={formData.last_name}
                onChange={(e) => setFormData({ ...formData, last_name: e.target.value })}
                placeholder="e.g. Katusiime"
                className="w-full bg-neutral-50 border border-neutral-200 rounded-xl px-3 py-2.5 text-neutral-900 focus:outline-none focus:border-brand-500"
              />
            </div>
          </div>

          <div>
            <label className="block font-semibold text-neutral-700 mb-1">Username</label>
            <input
              type="text"
              required
              value={formData.username}
              onChange={(e) => setFormData({ ...formData, username: e.target.value })}
              placeholder="e.g. florence_k"
              className="w-full bg-neutral-50 border border-neutral-200 rounded-xl px-3 py-2.5 text-neutral-900 focus:outline-none focus:border-brand-500"
            />
          </div>

          <div>
            <label className="block font-semibold text-neutral-700 mb-1">Email Address</label>
            <input
              type="email"
              required
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              placeholder="florence@example.com"
              className="w-full bg-neutral-50 border border-neutral-200 rounded-xl px-3 py-2.5 text-neutral-900 focus:outline-none focus:border-brand-500"
            />
          </div>

          <div>
            <label className="block font-semibold text-neutral-700 mb-1">Mobile Telephone</label>
            <input
              type="tel"
              value={formData.phone}
              onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
              placeholder="+256 700 000 000"
              className="w-full bg-neutral-50 border border-neutral-200 rounded-xl px-3 py-2.5 text-neutral-900 focus:outline-none focus:border-brand-500"
            />
          </div>

          <div>
            <label className="block font-semibold text-neutral-700 mb-1">Password</label>
            <input
              type="password"
              required
              value={formData.password}
              onChange={(e) => setFormData({ ...formData, password: e.target.value })}
              placeholder="••••••••"
              className="w-full bg-neutral-50 border border-neutral-200 rounded-xl px-3 py-2.5 text-neutral-900 focus:outline-none focus:border-brand-500"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-brand-dark hover:bg-neutral-800 text-white font-bold py-3.5 rounded-xl transition flex items-center justify-center gap-2 shadow-lg shadow-neutral-900/10 disabled:opacity-50 mt-2"
          >
            {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <span>Create Account</span>}
          </button>
        </form>

        <div className="pt-4 border-t border-neutral-100 text-center text-xs text-neutral-500">
          Already have an account?{" "}
          <Link href="/account/login" className="text-brand-600 font-bold hover:underline">
            Sign In
          </Link>
        </div>
      </div>
    </div>
  );
}
