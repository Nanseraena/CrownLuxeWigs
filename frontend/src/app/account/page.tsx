"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useQuery } from "@tanstack/react-query";
import { useAuth } from "@/context/AuthContext";
import { fetchApi } from "@/lib/api";
import { Order, Address } from "@/types";
import { formatPrice, formatDate } from "@/lib/formatters";
import { User, Package, MapPin, LogOut, ArrowRight, ShieldCheck, Clock } from "lucide-react";

export default function AccountPage() {
  const router = useRouter();
  const { user, logout, loading: authLoading } = useAuth();
  const [activeTab, setActiveTab] = useState<"orders" | "addresses">("orders");

  // Fetch Orders
  const { data: ordersData } = useQuery<{ results: Order[] }>({
    queryKey: ["user-orders"],
    queryFn: () => fetchApi("/orders/"),
    enabled: !!user,
  });

  // Fetch Addresses
  const { data: addressesData } = useQuery<{ results: Address[] }>({
    queryKey: ["user-addresses"],
    queryFn: () => fetchApi("/addresses/"),
    enabled: !!user,
  });

  if (authLoading) {
    return <div className="max-w-4xl mx-auto px-4 py-20 text-center text-xs">Loading account profile...</div>;
  }

  if (!user) {
    return (
      <div className="max-w-md mx-auto px-4 py-20 text-center space-y-4">
        <h2 className="font-serif text-2xl font-bold">Sign In Required</h2>
        <p className="text-xs text-neutral-500">Please sign in to access your order history and profile.</p>
        <Link
          href="/account/login"
          className="inline-block bg-brand-dark text-white font-semibold text-xs px-6 py-3 rounded-full"
        >
          Sign In
        </Link>
      </div>
    );
  }

  const orders = ordersData?.results || [];
  const addresses = addressesData?.results || [];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
      {/* Profile Header */}
      <div className="bg-neutral-900 text-white rounded-3xl p-6 sm:p-8 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-6 mb-8">
        <div className="flex items-center gap-4">
          <div className="w-14 h-14 bg-brand-600 rounded-full flex items-center justify-center font-serif text-xl font-bold">
            {(user.first_name?.[0] || user.username[0]).toUpperCase()}
          </div>
          <div>
            <h1 className="font-serif text-xl sm:text-2xl font-bold">
              {user.first_name ? `${user.first_name} ${user.last_name}` : user.username}
            </h1>
            <p className="text-xs text-neutral-400">{user.email} • VIP Member</p>
          </div>
        </div>

        <button
          onClick={logout}
          className="flex items-center gap-1.5 bg-white/10 hover:bg-white/20 text-xs px-4 py-2 rounded-xl text-neutral-300 transition"
        >
          <LogOut className="w-3.5 h-3.5" />
          <span>Sign Out</span>
        </button>
      </div>

      {/* Tabs */}
      <div className="flex gap-4 border-b border-neutral-200 mb-8 text-xs font-bold">
        <button
          onClick={() => setActiveTab("orders")}
          className={`pb-3 border-b-2 transition flex items-center gap-1.5 ${
            activeTab === "orders" ? "border-brand-600 text-brand-600" : "border-transparent text-neutral-500 hover:text-black"
          }`}
        >
          <Package className="w-4 h-4" />
          <span>Order History ({orders.length})</span>
        </button>

        <button
          onClick={() => setActiveTab("addresses")}
          className={`pb-3 border-b-2 transition flex items-center gap-1.5 ${
            activeTab === "addresses" ? "border-brand-600 text-brand-600" : "border-transparent text-neutral-500 hover:text-black"
          }`}
        >
          <MapPin className="w-4 h-4" />
          <span>Saved Addresses ({addresses.length})</span>
        </button>
      </div>

      {/* Orders Tab */}
      {activeTab === "orders" && (
        <div className="space-y-4">
          {orders.length === 0 ? (
            <div className="text-center py-16 bg-neutral-50 rounded-3xl border border-neutral-200">
              <Package className="w-10 h-10 text-neutral-400 mx-auto mb-2" />
              <h3 className="font-serif text-lg font-bold text-neutral-900 mb-1">No Orders Placed Yet</h3>
              <p className="text-xs text-neutral-500 mb-6">Explore our wig catalog and discover your next look.</p>
              <Link href="/shop" className="bg-brand-dark text-white text-xs px-6 py-3 rounded-full font-semibold">
                Explore Wigs
              </Link>
            </div>
          ) : (
            orders.map((ord) => (
              <div
                key={ord.id}
                className="bg-white p-5 sm:p-6 rounded-2xl border border-neutral-200/80 shadow-sm flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4"
              >
                <div className="space-y-1 text-xs">
                  <div className="flex items-center gap-2">
                    <span className="font-mono font-bold text-neutral-900 text-sm">{ord.order_number}</span>
                    <span className="text-[10px] uppercase font-bold px-2 py-0.5 rounded bg-brand-50 text-brand-800 border border-brand-200">
                      {ord.status}
                    </span>
                    <span className="text-[10px] uppercase font-bold px-2 py-0.5 rounded bg-emerald-50 text-emerald-800 border border-emerald-200">
                      {ord.payment_status}
                    </span>
                  </div>
                  <p className="text-neutral-500 text-[11px]">Placed on {formatDate(ord.created_at)}</p>
                  <p className="text-neutral-700 font-semibold pt-1">
                    {ord.items.length} item(s) • Total: {formatPrice(ord.total)}
                  </p>
                </div>

                <Link
                  href={`/orders/${ord.order_number}`}
                  className="bg-neutral-100 hover:bg-neutral-200 text-neutral-900 text-xs font-semibold px-4 py-2 rounded-xl transition flex items-center gap-1.5"
                >
                  <span>Track Order</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </Link>
              </div>
            ))
          )}
        </div>
      )}

      {/* Addresses Tab */}
      {activeTab === "addresses" && (
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {addresses.map((addr) => (
            <div key={addr.id} className="bg-white p-5 rounded-2xl border border-neutral-200 space-y-2 text-xs">
              <div className="flex justify-between items-center">
                <span className="font-bold text-neutral-900">{addr.full_name}</span>
                {addr.is_default && (
                  <span className="text-[10px] bg-brand-50 text-brand-800 px-2 py-0.5 rounded font-bold">
                    Default
                  </span>
                )}
              </div>
              <p className="text-neutral-600">{addr.street_address}</p>
              <p className="text-neutral-500">{addr.city_or_zone}, {addr.country}</p>
              <p className="text-neutral-500 text-[11px]">Phone: {addr.phone}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
