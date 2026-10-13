"use client";

import React from "react";
import Link from "next/link";
import Image from "next/image";
import { X, Trash2, Plus, Minus, ShoppingBag, ArrowRight, Sparkles } from "lucide-react";
import { useCart } from "@/context/CartContext";
import { formatPrice } from "@/lib/formatters";

export default function CartDrawer() {
  const { cart, isDrawerOpen, setIsDrawerOpen, updateQuantity, removeItem, itemCount } = useCart();

  if (!isDrawerOpen) return null;

  const subtotal = cart?.subtotal ? parseFloat(cart.subtotal) : 0;
  const freeShippingThreshold = 500000;
  const remainingForFreeShipping = Math.max(0, freeShippingThreshold - subtotal);
  const progressPercent = Math.min(100, (subtotal / freeShippingThreshold) * 100);

  return (
    <div className="fixed inset-0 z-50 overflow-hidden">
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-black/60 backdrop-blur-sm transition-opacity"
        onClick={() => setIsDrawerOpen(false)}
      />

      <div className="fixed inset-y-0 right-0 max-w-full flex pl-10">
        <div className="w-screen max-w-md bg-white shadow-2xl flex flex-col">
          {/* Header */}
          <div className="p-4 sm:p-5 border-b border-neutral-100 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <ShoppingBag className="w-5 h-5 text-brand-dark" />
              <h2 className="font-semibold text-base sm:text-lg text-neutral-900">
                Shopping Bag ({itemCount})
              </h2>
            </div>
            <button
              onClick={() => setIsDrawerOpen(false)}
              className="p-1.5 text-neutral-400 hover:text-black rounded-full hover:bg-neutral-100 transition"
              aria-label="Close bag drawer"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Free Shipping Progress Indicator */}
          <div className="bg-brand-50 px-4 py-3 border-b border-brand-100">
            {remainingForFreeShipping > 0 ? (
              <p className="text-xs text-brand-900 font-medium flex items-center gap-1.5">
                <Sparkles className="w-3.5 h-3.5 text-brand-gold shrink-0" />
                Add <strong className="text-brand-700">{formatPrice(remainingForFreeShipping)}</strong> more to get{" "}
                <span className="font-bold underline">FREE Express Delivery</span>!
              </p>
            ) : (
              <p className="text-xs text-emerald-800 font-bold flex items-center gap-1.5">
                🎉 Congratulations! You unlocked FREE Delivery!
              </p>
            )}
            <div className="w-full bg-neutral-200 h-1.5 rounded-full mt-2 overflow-hidden">
              <div
                className="bg-brand-600 h-full rounded-full transition-all duration-500"
                style={{ width: `${progressPercent}%` }}
              />
            </div>
          </div>

          {/* Items List */}
          <div className="flex-1 overflow-y-auto p-4 sm:p-5 divide-y divide-neutral-100">
            {!cart || cart.items.length === 0 ? (
              <div className="h-full flex flex-col items-center justify-center text-center py-16">
                <div className="w-16 h-16 bg-neutral-100 rounded-full flex items-center justify-center mb-4 text-neutral-400">
                  <ShoppingBag className="w-8 h-8" />
                </div>
                <h3 className="font-serif text-lg font-bold text-neutral-900 mb-1">Your bag is empty</h3>
                <p className="text-xs text-neutral-500 max-w-xs mb-6">
                  Explore our luxury HD lace frontals, bone straight wigs, and effortless glueless bobs.
                </p>
                <button
                  onClick={() => setIsDrawerOpen(false)}
                  className="bg-brand-dark text-white text-xs font-semibold px-6 py-3 rounded-full hover:bg-neutral-800 transition"
                >
                  <Link href="/shop">Start Shopping</Link>
                </button>
              </div>
            ) : (
              cart.items.map((item) => (
                <div key={item.id} className="py-4 flex gap-4">
                  {/* Product Image */}
                  <div className="w-20 h-24 bg-neutral-100 rounded-lg overflow-hidden shrink-0 relative">
                    <img
                      src={item.image?.image_url || "https://images.unsplash.com/photo-1595476108010-b4d1f102b1b1?auto=format&fit=crop&w=300&q=80"}
                      alt={item.product_name}
                      className="w-full h-full object-cover"
                    />
                  </div>

                  {/* Item Details */}
                  <div className="flex-1 min-w-0 flex flex-col justify-between">
                    <div>
                      <div className="flex justify-between items-start gap-2">
                        <h4 className="text-xs sm:text-sm font-semibold text-neutral-900 line-clamp-1">
                          {item.product_name}
                        </h4>
                        <button
                          onClick={() => removeItem(item.id)}
                          className="text-neutral-400 hover:text-red-600 transition p-1"
                          title="Remove item"
                        >
                          <Trash2 className="w-3.5 h-3.5" />
                        </button>
                      </div>

                      {/* Variant chips */}
                      <div className="flex flex-wrap gap-1 mt-1 text-[11px] text-neutral-500">
                        {item.variant_options.length_inches && (
                          <span className="bg-neutral-100 px-1.5 py-0.5 rounded">
                            {item.variant_options.length_inches}"
                          </span>
                        )}
                        {item.variant_options.color && (
                          <span className="bg-neutral-100 px-1.5 py-0.5 rounded">
                            {item.variant_options.color}
                          </span>
                        )}
                        {item.variant_options.lace_type && (
                          <span className="bg-neutral-100 px-1.5 py-0.5 rounded">
                            {item.variant_options.lace_type}
                          </span>
                        )}
                      </div>
                    </div>

                    {/* Quantity controls and price */}
                    <div className="flex items-center justify-between mt-3">
                      <div className="flex items-center border border-neutral-200 rounded-lg bg-neutral-50">
                        <button
                          onClick={() => updateQuantity(item.id, item.quantity - 1)}
                          className="p-1 sm:p-1.5 text-neutral-600 hover:text-black transition"
                          aria-label="Decrease quantity"
                        >
                          <Minus className="w-3 h-3" />
                        </button>
                        <span className="px-2 text-xs font-semibold text-neutral-900">{item.quantity}</span>
                        <button
                          onClick={() => updateQuantity(item.id, item.quantity + 1)}
                          className="p-1 sm:p-1.5 text-neutral-600 hover:text-black transition"
                          aria-label="Increase quantity"
                        >
                          <Plus className="w-3 h-3" />
                        </button>
                      </div>

                      <div className="text-right">
                        <span className="text-xs sm:text-sm font-bold text-neutral-900">
                          {formatPrice(item.line_total)}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>

          {/* Footer & Checkout CTA */}
          {cart && cart.items.length > 0 && (
            <div className="p-4 sm:p-5 border-t border-neutral-100 bg-neutral-50 space-y-3">
              <div className="space-y-1 text-xs">
                <div className="flex justify-between text-neutral-600">
                  <span>Subtotal:</span>
                  <span className="font-semibold text-neutral-900 text-sm">{formatPrice(cart.subtotal)}</span>
                </div>
                <div className="flex justify-between text-neutral-500">
                  <span>Delivery:</span>
                  <span>Calculated at checkout</span>
                </div>
              </div>

              <div className="pt-2 flex gap-2">
                <Link
                  href="/cart"
                  onClick={() => setIsDrawerOpen(false)}
                  className="flex-1 bg-white border border-neutral-300 text-neutral-800 text-xs font-semibold py-3 rounded-xl text-center hover:bg-neutral-100 transition"
                >
                  View Full Bag
                </Link>
                <Link
                  href="/checkout"
                  onClick={() => setIsDrawerOpen(false)}
                  className="flex-[2] bg-brand-dark hover:bg-neutral-800 text-white text-xs font-semibold py-3 rounded-xl flex items-center justify-center gap-1.5 shadow-lg shadow-neutral-900/10 transition"
                >
                  <span>Checkout</span>
                  <ArrowRight className="w-4 h-4" />
                </Link>
              </div>

              <p className="text-[10px] text-center text-neutral-400">
                🔒 Guaranteed safe checkout via MTN MoMo, Airtel Money & Card
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
