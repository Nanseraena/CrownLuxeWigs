"use client";

import React, { createContext, useContext, useState, useEffect } from "react";
import { User } from "@/types";
import { ensureCsrfToken, fetchApi, getCartToken } from "@/lib/api";

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (identifier: string, password: string) => Promise<void>;
  register: (data: any) => Promise<void>;
  googleLogin: (credential: string) => Promise<void>;
  logout: () => Promise<void>;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  const refreshUser = async () => {
    try {
      const data = await fetchApi<User>("/auth/me/");
      setUser(data);
    } catch (err) {
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // Sets the CSRF cookie before any state-changing cross-origin request.
    ensureCsrfToken().catch(() => undefined).finally(refreshUser);
  }, []);

  const mergeGuestCart = async () => {
    const guestToken = getCartToken();
    if (guestToken) {
      try {
        await fetchApi("/cart/merge/", {
          method: "POST",
          body: JSON.stringify({ guest_token: guestToken }),
        });
      } catch (e) {
        console.error("Cart merge error:", e);
      }
    }
  };

  const login = async (identifier: string, password: string) => {
    await fetchApi("/auth/login/", {
      method: "POST",
      body: JSON.stringify({ identifier, password }),
    });
    await refreshUser();
    await mergeGuestCart();
  };

  const register = async (formData: any) => {
    const data = await fetchApi<any>("/auth/register/", {
      method: "POST",
      body: JSON.stringify(formData),
    });
    setUser(data.user);
    await mergeGuestCart();
  };

  const googleLogin = async (credential: string) => {
    await fetchApi("/auth/google/", { method: "POST", body: JSON.stringify({ credential }) });
    await refreshUser();
    await mergeGuestCart();
  };

  const logout = async () => {
    try { await fetchApi("/auth/logout/", { method: "POST" }); } catch { /* local UI still signs out */ }
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, register, googleLogin, logout, refreshUser }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
