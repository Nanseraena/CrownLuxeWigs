"use client";

import React, { createContext, useContext, useState, useEffect } from "react";
import { User } from "@/types";
import { fetchApi, getAuthToken, setAuthTokens, clearAuthTokens, getCartToken } from "@/lib/api";

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (identifier: string, password: string) => Promise<void>;
  register: (data: any) => Promise<void>;
  logout: () => void;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  const refreshUser = async () => {
    const token = getAuthToken();
    if (!token) {
      setUser(null);
      setLoading(false);
      return;
    }
    try {
      const data = await fetchApi<User>("/auth/me/");
      setUser(data);
    } catch (err) {
      clearAuthTokens();
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    refreshUser();
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
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000/api/v1";
    const tokenUrl = `${apiUrl.replace(/\/api\/v1\/?$/, "")}/api/token/`;
    const res = await fetch(tokenUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username: identifier, password }),
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || "Invalid username or password.");
    }
    const data = await res.json();
    setAuthTokens(data.access, data.refresh);
    await refreshUser();
    await mergeGuestCart();
  };

  const register = async (formData: any) => {
    const data = await fetchApi<any>("/auth/register/", {
      method: "POST",
      body: JSON.stringify(formData),
    });
    if (data.tokens) {
      setAuthTokens(data.tokens.access, data.tokens.refresh);
      setUser(data.user);
      await mergeGuestCart();
    }
  };

  const logout = () => {
    clearAuthTokens();
    setUser(null);
    window.location.href = "/";
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout, refreshUser }}>
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
