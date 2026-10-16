"use client";

import React from "react";
import { useParams } from "next/navigation";
import { useQuery } from "@tanstack/react-query";
import Link from "next/link";
import {
  CheckCircle2, Clock, Truck, Package, ShieldCheck,
  ArrowRight, Phone, MessageSquare, AlertCircle
} from "lucide-react";
import { Order } from "@/types";
import { fetchApi } from "@/lib/api";
import { formatPrice, formatDate } from "@/lib/formatters";

export default function OrderDetailPage() {
  const params = useParams();
  const orderNumber = params?.order_number as string;

  const { data: order, isLoading, error } = useQuery<Order>({
    queryKey: ["order", orderNumber],
    queryFn: () => fetchApi(`/orders/track/${orderNumber}/`),
    enabled: !!orderNumber,
  });

  if (isLoading) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-20 text-center">
        <div className="w-10 h-10 border-4 border-brand-500 border-t-transparent rounded-full animate-spin mx-auto mb-4" />
        <p className="text-xs text-neutral-500">Tracking your CrownLuxe order...</p>
      </div>
    );
  }

  if (error || !order) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-20 text-center">
        <AlertCircle className="w-12 h-12 text-red-500 mx-auto mb-3" />
        <h2 className="font-serif text-2xl font-bold text-neutral-900 mb-2">Order Not Found</h2>
        <p className="text-xs text-neutral-500 mb-6">
          Could not find an order with identifier <strong>{orderNumber}</strong>. Please check your tracking number or contact support.
        </p>
        <Link href="/shop" className="bg-brand-dark text-white text-xs px-6 py-3 rounded-full">
          Back to Shop
        </Link>
      </div>
    );
  }

  // Tracking Timeline steps
  const steps = [
    { title: "Order Placed", status: "completed", date: formatDate(order.created_at) },
    {
      title: "Payment Verified",
      status: order.payment_status === "paid" ? "completed" : "current",
      note: order.payment_status === "paid" ? `Ref: ${order.payment_reference || "Verified"}` : "Pending Payment",
    },
    {
      title: "Processing & Styling",
      status: ["processing", "dispatched", "delivered"].includes(order.status) ? "completed" : "pending",
    },
    {
      title: "Dispatched with Courier",
      status: ["dispatched", "delivered"].includes(order.status) ? "completed" : "pending",
      note: order.tracking_number ? `Courier ID: ${order.tracking_number}` : "",
    },
    {
      title: "Delivered to Doorstep",
      status: order.status === "delivered" ? "completed" : "pending",
    },
  ];

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-10 sm:py-16 space-y-8">
      {/* Success Notification Card */}
      <div className="bg-emerald-50 border border-emerald-200 rounded-3xl p-6 sm:p-8 text-center sm:text-left flex flex-col sm:flex-row items-center gap-6">
        <div className="w-16 h-16 bg-emerald-600 text-white rounded-full flex items-center justify-center shrink-0 shadow-lg shadow-emerald-600/20">
          <CheckCircle2 className="w-8 h-8" />
        </div>
        <div className="flex-1 space-y-1">
          <span className="text-[11px] font-bold uppercase tracking-wider text-emerald-800">
            Order Confirmed • {order.order_number}
          </span>
          <h1 className="font-serif text-2xl sm:text-3xl font-bold text-emerald-950">Thank You!</h1>
          <p className="text-xs text-emerald-800 leading-relaxed">
            Your order has been received. Check your confirmation email for delivery contact details.
          </p>
        </div>
      </div>

      {/* Live Status Progress Bar */}
      <div className="bg-white p-6 sm:p-8 rounded-3xl border border-neutral-200/80 shadow-sm space-y-6">
        <div className="flex items-center justify-between">
          <h2 className="font-serif text-lg font-bold text-neutral-900">Order Progress</h2>
          <span className="text-xs uppercase font-extrabold px-3 py-1 rounded-full bg-brand-50 text-brand-900 border border-brand-200">
            Status: {order.status}
          </span>
        </div>

        {/* Timeline steps */}
        <div className="relative border-l-2 border-neutral-200 ml-4 sm:ml-6 pl-6 sm:pl-8 space-y-8 my-4">
          {steps.map((step, idx) => {
            const isDone = step.status === "completed";
            const isCurrent = step.status === "current";

            return (
              <div key={idx} className="relative">
                {/* Timeline dot */}
                <div
                  className={`absolute -left-[33px] sm:-left-[41px] top-0 w-6 h-6 rounded-full flex items-center justify-center text-white ${
                    isDone
                      ? "bg-emerald-600"
                      : isCurrent
                      ? "bg-amber-500 ring-4 ring-amber-100"
                      : "bg-neutral-300"
                  }`}
                >
                  {isDone ? <CheckCircle2 className="w-3.5 h-3.5" /> : <Clock className="w-3.5 h-3.5" />}
                </div>

                <div>
                  <h4 className={`text-xs sm:text-sm font-bold ${isDone ? "text-neutral-900" : isCurrent ? "text-amber-700" : "text-neutral-400"}`}>
                    {step.title}
                  </h4>
                  {step.date && <p className="text-[11px] text-neutral-500">{step.date}</p>}
                  {step.note && <p className="text-[11px] font-mono text-neutral-600 mt-0.5">{step.note}</p>}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Order Itemized Summary */}
      <div className="bg-white p-6 sm:p-8 rounded-3xl border border-neutral-200/80 shadow-sm space-y-6">
        <h2 className="font-serif text-lg font-bold text-neutral-900">Purchased Items</h2>

        <div className="divide-y divide-neutral-100">
          {order.items.map((item) => (
            <div key={item.id} className="py-4 flex items-center justify-between text-xs">
              <div className="space-y-1">
                <h4 className="font-bold text-sm text-neutral-900">{item.product_name}</h4>
                <p className="text-neutral-500 text-[11px]">SKU: {item.sku} • Qty: {item.quantity}</p>
                {item.variant_description && (
                  <p className="text-[11px] text-neutral-400">
                    {item.variant_description.length_inches ? `${item.variant_description.length_inches}" Inch • ` : ""}
                    {item.variant_description.color || ""} {item.variant_description.texture ? `• ${item.variant_description.texture}` : ""}
                  </p>
                )}
              </div>
              <span className="font-extrabold text-sm text-neutral-900">
                {formatPrice(item.line_total)}
              </span>
            </div>
          ))}
        </div>

        {/* Financial Breakdown */}
        <div className="pt-4 border-t border-neutral-200 space-y-2 text-xs">
          <div className="flex justify-between text-neutral-600">
            <span>Subtotal:</span>
            <span className="font-semibold text-neutral-900">{formatPrice(order.subtotal)}</span>
          </div>
          {parseFloat(order.discount_amount) > 0 && (
            <div className="flex justify-between text-emerald-700 font-semibold">
              <span>Promo Discount ({order.coupon_code}):</span>
              <span>-{formatPrice(order.discount_amount)}</span>
            </div>
          )}
          <div className="flex justify-between text-neutral-600">
            <span>Delivery Fee:</span>
            <span className="font-semibold text-neutral-900">{formatPrice(order.delivery_fee)}</span>
          </div>
          <div className="pt-3 border-t border-neutral-200 flex justify-between items-baseline">
            <span className="text-sm font-bold text-neutral-900">Total Paid / Payable:</span>
            <span className="font-serif text-2xl font-extrabold text-neutral-950">
              {formatPrice(order.total)}
            </span>
          </div>
        </div>
      </div>

      {/* Delivery & Customer Info */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
        <div className="bg-neutral-50 p-6 rounded-3xl border border-neutral-200/80 space-y-2 text-xs">
          <h3 className="font-serif font-bold text-sm text-neutral-900 flex items-center gap-2">
            <Truck className="w-4 h-4 text-brand-600" />
            Delivery Destination
          </h3>
          <p className="text-neutral-700 font-medium">{order.customer_name}</p>
          <p className="text-neutral-600 leading-relaxed">{order.delivery_address}</p>
          <p className="text-neutral-500 text-[11px]">Phone: {order.phone}</p>
        </div>

        <div className="bg-neutral-50 p-6 rounded-3xl border border-neutral-200/80 space-y-2 text-xs">
          <h3 className="font-serif font-bold text-sm text-neutral-900 flex items-center gap-2">
            <ShieldCheck className="w-4 h-4 text-brand-600" />
            Payment Status
          </h3>
          <p className="text-neutral-700 font-medium capitalize">
            Method: {order.payment_method.replace("_", " ")}
          </p>
          <p className="text-neutral-600">
            Status: <span className="font-bold uppercase text-emerald-700">{order.payment_status}</span>
          </p>
          <p className="text-[11px] text-neutral-400">Order Ref: {order.payment_reference || "Pending"}</p>
        </div>
      </div>

      {/* Customer Support CTA */}
      <div className="text-center pt-4 flex flex-col sm:flex-row items-center justify-center gap-4">
        <Link
          href="/shop"
          className="bg-brand-dark hover:bg-neutral-800 text-white text-xs font-semibold px-8 py-3.5 rounded-full transition"
        >
          Continue Shopping
        </Link>
        <a
          href="https://wa.me/256700112233"
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center gap-2 border border-neutral-300 text-neutral-800 text-xs font-semibold px-6 py-3.5 rounded-full hover:bg-neutral-50 transition"
        >
          <MessageSquare className="w-4 h-4 text-emerald-600" />
          <span>Chat With CrownLuxe On WhatsApp</span>
        </a>
      </div>
    </div>
  );
}
