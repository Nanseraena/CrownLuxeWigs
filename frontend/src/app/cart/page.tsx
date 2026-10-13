"use client";

import React, { useState } from "react";
import Link from "next/link";
import { Trash2, Plus, Minus, ArrowRight, ShoppingBag, Tag, ShieldCheck, Sparkles } from "lucide-react";
import { useCart } from "@/context/CartContext";
import { formatPrice } from "@/lib/formatters";
import { fetchApi } from "@/lib/api";

export default function CartPage() {
  const { cart, updateQuantity, removeItem, clearCart, itemCount } = useCart();
  const [couponCode, setCouponCode] = useState("");
  const [couponLoading, setCouponLoading] = useState(false);
  const [appliedDiscount, setAppliedDiscount] = useState<number>(0);
  const [couponMessage, setCouponMessage] = useState<string | null>(null);

  const subtotal = cart?.subtotal ? parseFloat(cart.subtotal) : 0;
  const deliveryEstimate = 10000;
  const finalTotal = Math.max(0, subtotal - appliedDiscount + deliveryEstimate);

  const handleApplyCoupon = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!couponCode.trim()) return;
    setCouponLoading(true);
    setCouponMessage(null);
    try {
      const res = await fetchApi<any>("/promotions/apply/", {
        method: "POST",
        body: JSON.stringify({ code: couponCode.trim(), subtotal }),
      });
      if (res.valid) {
        setAppliedDiscount(parseFloat(res.discount_amount));
        setCouponMessage(`✅ ${res.message} (-${formatPrice(res.discount_amount)})`);
      }
    } catch (err: any) {
      setAppliedDiscount(0);
      setCouponMessage(`⚠️ ${err.message || "Invalid coupon code"}`);
    } finally {
      setCouponLoading(false);
    }
  };

  if (!cart || cart.items.length === 0) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-20 text-center">
        <div className="w-20 h-20 bg-neutral-100 rounded-full flex items-center justify-center mx-auto mb-4 text-neutral-400">
          <ShoppingBag className="w-10 h-10" />
        </div>
        <h1 className="font-serif text-3xl font-bold text-neutral-900 mb-2">Your Shopping Bag Is Empty</h1>
        <p className="text-xs sm:text-sm text-neutral-500 max-w-sm mx-auto mb-8">
          Browse our 100% virgin human hair wigs, HD invisible melted frontals, and glueless bobs.
        </p>
        <Link
          href="/shop"
          className="bg-brand-dark hover:bg-neutral-800 text-white font-semibold text-xs px-8 py-3.5 rounded-full transition shadow-md"
        >
          Explore Catalog
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
      <div className="flex items-center justify-between pb-6 border-b border-neutral-200 mb-8">
        <div>
          <h1 className="font-serif text-2xl sm:text-3xl font-bold text-neutral-900">
            Shopping Bag ({itemCount} {itemCount === 1 ? "item" : "items"})
          </h1>
          <p className="text-xs text-neutral-500 mt-1">Review your selected wig variants and proceed to checkout.</p>
        </div>
        <button
          onClick={clearCart}
          className="text-xs text-neutral-500 hover:text-red-600 transition underline"
        >
          Clear All
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12">
        {/* Cart Items List */}
        <div className="lg:col-span-8 divide-y divide-neutral-100">
          {cart.items.map((item) => (
            <div key={item.id} className="py-6 flex flex-col sm:flex-row gap-5 items-start sm:items-center">
              <div className="w-24 h-32 bg-neutral-100 rounded-xl overflow-hidden shrink-0">
                <img
                  src={item.image?.image_url || "https://images.unsplash.com/photo-1595476108010-b4d1f102b1b1?auto=format&fit=crop&w=300&q=80"}
                  alt={item.product_name}
                  className="w-full h-full object-cover"
                />
              </div>

              <div className="flex-1 min-w-0 space-y-2">
                <div className="flex items-start justify-between gap-2">
                  <div>
                    <Link href={`/products/${item.product_slug}`}>
                      <h3 className="font-semibold text-sm sm:text-base text-neutral-900 hover:text-brand-600 transition">
                        {item.product_name}
                      </h3>
                    </Link>
                    <p className="text-[11px] text-neutral-400">SKU: {item.sku}</p>
                  </div>
                  <button
                    onClick={() => removeItem(item.id)}
                    className="text-neutral-400 hover:text-red-600 p-1 transition"
                    title="Remove item"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>

                {/* Variant Options Chips */}
                <div className="flex flex-wrap gap-1.5 text-xs text-neutral-600">
                  {item.variant_options.length_inches && (
                    <span className="bg-neutral-100 px-2 py-0.5 rounded font-medium">
                      Length: {item.variant_options.length_inches}"
                    </span>
                  )}
                  {item.variant_options.color && (
                    <span className="bg-neutral-100 px-2 py-0.5 rounded font-medium">
                      Color: {item.variant_options.color}
                    </span>
                  )}
                  {item.variant_options.lace_type && (
                    <span className="bg-neutral-100 px-2 py-0.5 rounded font-medium">
                      Lace: {item.variant_options.lace_type}
                    </span>
                  )}
                </div>

                <div className="flex items-center justify-between pt-2">
                  {/* Quantity Stepper */}
                  <div className="flex items-center border border-neutral-200 rounded-xl bg-neutral-50">
                    <button
                      type="button"
                      onClick={() => updateQuantity(item.id, item.quantity - 1)}
                      className="p-1.5 sm:p-2 text-neutral-600 hover:text-black transition"
                    >
                      <Minus className="w-3.5 h-3.5" />
                    </button>
                    <span className="px-3 text-xs font-bold text-neutral-900">{item.quantity}</span>
                    <button
                      type="button"
                      onClick={() => updateQuantity(item.id, item.quantity + 1)}
                      className="p-1.5 sm:p-2 text-neutral-600 hover:text-black transition"
                    >
                      <Plus className="w-3.5 h-3.5" />
                    </button>
                  </div>

                  {/* Unit & Line Price */}
                  <div className="text-right">
                    <span className="text-sm sm:text-base font-extrabold text-neutral-900">
                      {formatPrice(item.line_total)}
                    </span>
                    {item.quantity > 1 && (
                      <p className="text-[10px] text-neutral-400">{formatPrice(item.unit_price)} each</p>
                    )}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Order Summary Sidebar */}
        <div className="lg:col-span-4 space-y-6">
          <div className="bg-neutral-50 p-6 rounded-3xl border border-neutral-200/80 space-y-5">
            <h2 className="font-serif text-lg font-bold text-neutral-900">Order Summary</h2>

            {/* Subtotal, Discount, Delivery */}
            <div className="space-y-3 text-xs">
              <div className="flex justify-between text-neutral-600">
                <span>Items Subtotal</span>
                <span className="font-semibold text-neutral-900 text-sm">{formatPrice(subtotal)}</span>
              </div>

              {appliedDiscount > 0 && (
                <div className="flex justify-between text-emerald-700 font-semibold">
                  <span>Coupon Discount</span>
                  <span>-{formatPrice(appliedDiscount)}</span>
                </div>
              )}

              <div className="flex justify-between text-neutral-600">
                <span>Estimated Delivery (Kampala)</span>
                <span className="font-semibold text-neutral-900">{formatPrice(deliveryEstimate)}</span>
              </div>

              <div className="pt-3 border-t border-neutral-200 flex justify-between items-baseline">
                <span className="text-sm font-bold text-neutral-900">Estimated Total</span>
                <span className="font-serif text-2xl font-extrabold text-neutral-950">{formatPrice(finalTotal)}</span>
              </div>
            </div>

            {/* Coupon Code Input */}
            <form onSubmit={handleApplyCoupon} className="pt-2 space-y-2">
              <label className="block text-[11px] font-semibold text-neutral-700">Have a Promo Code?</label>
              <div className="flex gap-2">
                <input
                  type="text"
                  value={couponCode}
                  onChange={(e) => setCouponCode(e.target.value.toUpperCase())}
                  placeholder="e.g. WELCOME10"
                  className="flex-1 bg-white border border-neutral-200 rounded-xl px-3 py-2 text-xs text-neutral-900 focus:outline-none focus:border-brand-500 uppercase font-mono"
                />
                <button
                  type="submit"
                  disabled={couponLoading || !couponCode}
                  className="bg-neutral-900 hover:bg-neutral-800 text-white font-semibold text-xs px-4 py-2 rounded-xl transition disabled:opacity-50"
                >
                  {couponLoading ? "..." : "Apply"}
                </button>
              </div>
              {couponMessage && (
                <p className="text-[11px] font-medium mt-1">{couponMessage}</p>
              )}
            </form>

            {/* Checkout Button */}
            <Link
              href="/checkout"
              className="w-full bg-brand-dark hover:bg-neutral-800 text-white font-bold text-xs py-4 rounded-2xl transition flex items-center justify-center gap-2 shadow-lg shadow-neutral-900/10"
            >
              <span>PROCEED TO CHECKOUT</span>
              <ArrowRight className="w-4 h-4" />
            </Link>

            <div className="pt-3 border-t border-neutral-200 flex items-center justify-center gap-1.5 text-[11px] text-neutral-500">
              <ShieldCheck className="w-4 h-4 text-brand-600" />
              <span>Payments verified via MTN MoMo, Airtel Money & Card</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
