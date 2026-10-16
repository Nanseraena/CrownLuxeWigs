"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  TrendingUp, ShoppingBag, AlertTriangle, Clock, CheckCircle2,
  ExternalLink, Eye, RefreshCw, DollarSign
} from "lucide-react";
import { fetchApi } from "@/lib/api";
import { formatPrice, formatDate } from "@/lib/formatters";

interface DashboardStats {
  total_orders: number;
  total_revenue: string;
  pending_orders: number;
  low_stock_count: number;
  low_stock_items: Array<{
    id: number;
    product_name: string;
    sku: string;
    stock_quantity: number;
    price: string;
  }>;
  recent_orders: Array<{
    id: number;
    order_number: string;
    customer_name: string;
    phone: string;
    total: string;
    status: string;
    payment_status: string;
    created_at: string;
  }>;
}

export default function AdminPortalPage() {
  const queryClient = useQueryClient();
  const [updatingOrder, setUpdatingOrder] = useState<string | null>(null);

  const { data: stats, isLoading, refetch } = useQuery<DashboardStats>({
    queryKey: ["admin-dashboard-stats"],
    queryFn: () => fetchApi("/admin/dashboard-stats/"),
  });

  const handleUpdateStatus = async (orderNumber: string, newStatus: string) => {
    setUpdatingOrder(orderNumber);
    try {
      await fetchApi(`/orders/${orderNumber}/`, {
        method: "PATCH",
        body: JSON.stringify({ status: newStatus }),
      });
      refetch();
    } catch (e) {
      console.error("Status update error:", e);
    } finally {
      setUpdatingOrder(null);
    }
  };

  if (isLoading || !stats) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-20 text-center text-xs">
        <RefreshCw className="w-8 h-8 animate-spin mx-auto text-brand-600 mb-3" />
        <p>Loading CrownLuxe Store Management Metrics...</p>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12 space-y-8">
      {/* Top Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6 border-b border-neutral-200">
        <div>
          
          <h1 className="font-serif text-2xl sm:text-3xl font-bold text-neutral-900 mt-0.5">
            Admin Analytics & Fulfillment Portal
          </h1>
          <p className="text-xs text-neutral-500 mt-1">
            Real-time store KPIs, order processing, and inventory alerts.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={() => refetch()}
            className="flex items-center gap-1.5 bg-neutral-100 hover:bg-neutral-200 text-neutral-800 text-xs font-semibold px-3.5 py-2 rounded-xl transition"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            <span>Refresh</span>
          </button>
          <a
            href="http://127.0.0.1:8000/admin/"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-1.5 bg-brand-dark hover:bg-neutral-800 text-white text-xs font-semibold px-4 py-2 rounded-xl transition shadow-sm"
          >
            <span>Django Full Admin</span>
            <ExternalLink className="w-3.5 h-3.5" />
          </a>
        </div>
      </div>

      {/* KPI Stats Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
        <div className="bg-white p-5 rounded-2xl border border-neutral-200 shadow-sm space-y-2">
          <div className="flex items-center justify-between text-neutral-500 text-xs">
            <span>Verified Revenue</span>
            <div className="p-2 bg-emerald-50 text-emerald-600 rounded-xl">
              <DollarSign className="w-4 h-4" />
            </div>
          </div>
          <p className="font-serif text-xl sm:text-2xl font-bold text-neutral-900">
            {formatPrice(stats.total_revenue)}
          </p>
          <p className="text-[11px] text-emerald-700 font-medium">From verified MoMo & Card orders</p>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-neutral-200 shadow-sm space-y-2">
          <div className="flex items-center justify-between text-neutral-500 text-xs">
            <span>Total Orders</span>
            <div className="p-2 bg-blue-50 text-blue-600 rounded-xl">
              <ShoppingBag className="w-4 h-4" />
            </div>
          </div>
          <p className="font-serif text-xl sm:text-2xl font-bold text-neutral-900">
            {stats.total_orders}
          </p>
          <p className="text-[11px] text-neutral-500">All customer checkout orders</p>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-neutral-200 shadow-sm space-y-2">
          <div className="flex items-center justify-between text-neutral-500 text-xs">
            <span>Pending Dispatch</span>
            <div className="p-2 bg-amber-50 text-amber-600 rounded-xl">
              <Clock className="w-4 h-4" />
            </div>
          </div>
          <p className="font-serif text-xl sm:text-2xl font-bold text-neutral-900">
            {stats.pending_orders}
          </p>
          <p className="text-[11px] text-amber-700 font-medium">Needs packaging or courier</p>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-neutral-200 shadow-sm space-y-2">
          <div className="flex items-center justify-between text-neutral-500 text-xs">
            <span>Low Stock Alerts</span>
            <div className="p-2 bg-red-50 text-red-600 rounded-xl">
              <AlertTriangle className="w-4 h-4" />
            </div>
          </div>
          <p className="font-serif text-xl sm:text-2xl font-bold text-red-600">
            {stats.low_stock_count}
          </p>
          <p className="text-[11px] text-red-700 font-medium">Variants with ≤ 5 units left</p>
        </div>
      </div>

      {/* Low Stock Alerts Table */}
      {stats.low_stock_items && stats.low_stock_items.length > 0 && (
        <div className="bg-white p-6 rounded-3xl border border-neutral-200/80 shadow-sm space-y-4">
          <h2 className="font-serif text-lg font-bold text-neutral-900 flex items-center gap-2">
            <AlertTriangle className="w-5 h-5 text-amber-500" />
            Low Stock Inventory Alert
          </h2>

          <div className="overflow-x-auto">
            <table className="w-full text-xs text-left">
              <thead className="bg-neutral-50 text-neutral-500 uppercase font-semibold">
                <tr>
                  <th className="py-2.5 px-3">Product Name</th>
                  <th className="py-2.5 px-3">SKU</th>
                  <th className="py-2.5 px-3">Price</th>
                  <th className="py-2.5 px-3">Units Left</th>
                  <th className="py-2.5 px-3 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-neutral-100">
                {stats.low_stock_items.map((item) => (
                  <tr key={item.id} className="hover:bg-neutral-50/50">
                    <td className="py-2.5 px-3 font-semibold text-neutral-900">{item.product_name}</td>
                    <td className="py-2.5 px-3 font-mono text-neutral-500">{item.sku}</td>
                    <td className="py-2.5 px-3 font-bold">{formatPrice(item.price)}</td>
                    <td className="py-2.5 px-3 font-extrabold text-red-600">{item.stock_quantity} remaining</td>
                    <td className="py-2.5 px-3 text-right">
                      <a
                        href="http://127.0.0.1:8000/admin/catalog/productvariant/"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-brand-600 hover:underline font-bold"
                      >
                        Restock
                      </a>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Recent Orders & Fulfillment Status Updater */}
      <div className="bg-white p-6 rounded-3xl border border-neutral-200/80 shadow-sm space-y-4">
        <h2 className="font-serif text-lg font-bold text-neutral-900 flex items-center gap-2">
          <ShoppingBag className="w-5 h-5 text-brand-dark" />
          Recent Orders & Live Fulfillment
        </h2>

        <div className="overflow-x-auto">
          <table className="w-full text-xs text-left">
            <thead className="bg-neutral-50 text-neutral-500 uppercase font-semibold">
              <tr>
                <th className="py-2.5 px-3">Order #</th>
                <th className="py-2.5 px-3">Customer</th>
                <th className="py-2.5 px-3">Phone</th>
                <th className="py-2.5 px-3">Total</th>
                <th className="py-2.5 px-3">Payment</th>
                <th className="py-2.5 px-3">Fulfillment Status</th>
                <th className="py-2.5 px-3 text-right">Track</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-neutral-100">
              {stats.recent_orders.map((ord) => (
                <tr key={ord.id} className="hover:bg-neutral-50/50">
                  <td className="py-3 px-3 font-mono font-bold text-neutral-900">{ord.order_number}</td>
                  <td className="py-3 px-3 font-medium text-neutral-800">{ord.customer_name}</td>
                  <td className="py-3 px-3 text-neutral-500">{ord.phone}</td>
                  <td className="py-3 px-3 font-extrabold text-neutral-950">{formatPrice(ord.total)}</td>
                  <td className="py-3 px-3">
                    <span
                      className={`px-2 py-0.5 rounded text-[10px] font-extrabold uppercase ${
                        ord.payment_status === "paid"
                          ? "bg-emerald-100 text-emerald-800"
                          : "bg-amber-100 text-amber-800"
                      }`}
                    >
                      {ord.payment_status}
                    </span>
                  </td>
                  <td className="py-3 px-3">
                    <select
                      value={ord.status}
                      disabled={updatingOrder === ord.order_number}
                      onChange={(e) => handleUpdateStatus(ord.order_number, e.target.value)}
                      className="bg-white border border-neutral-300 rounded-lg px-2 py-1 text-xs font-semibold focus:outline-none focus:border-brand-500"
                    >
                      <option value="pending">Pending</option>
                      <option value="processing">Processing / Styling</option>
                      <option value="dispatched">Dispatched with Courier</option>
                      <option value="delivered">Delivered</option>
                      <option value="cancelled">Cancelled</option>
                    </select>
                  </td>
                  <td className="py-3 px-3 text-right">
                    <Link
                      href={`/orders/${ord.order_number}`}
                      className="text-brand-600 hover:text-brand-900 font-bold inline-flex items-center gap-1"
                    >
                      <Eye className="w-3.5 h-3.5" />
                      <span>View</span>
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
