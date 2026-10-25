"use client";

import React, { useState } from "react";
import Link from "next/link";
import { Phone, Mail, MapPin, Instagram, Facebook, ShieldCheck, Truck, RotateCcw, CreditCard } from "lucide-react";

export default function Footer() {
  const [email, setEmail] = useState("");
  const [subscribed, setSubscribed] = useState(false);

  const handleSubscribe = (e: React.FormEvent) => {
    e.preventDefault();
    if (email) {
      setSubscribed(true);
      setEmail("");
    }
  };

  return (
    <footer className="bg-neutral-900 text-neutral-300 pt-16 pb-24 lg:pb-12 border-t border-neutral-800">
      {/* Trust Badges Bar */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-12 border-b border-neutral-800">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 text-center sm:text-left">
          <div className="flex flex-col sm:flex-row items-center gap-3">
            <div className="p-3 bg-neutral-800 rounded-full text-brand-gold">
              <ShieldCheck className="w-6 h-6" />
            </div>
            <div>
              <h4 className="text-sm font-semibold text-white">100% Virgin Hair</h4>
              <p className="text-xs text-neutral-400">Unprocessed donor bundles</p>
            </div>
          </div>

          <div className="flex flex-col sm:flex-row items-center gap-3">
            <div className="p-3 bg-neutral-800 rounded-full text-brand-gold">
              <Truck className="w-6 h-6" />
            </div>
            <div>
              <h4 className="text-sm font-semibold text-white">Express Delivery</h4>
              <p className="text-xs text-neutral-400">Kampala & countrywide</p>
            </div>
          </div>

          <div className="flex flex-col sm:flex-row items-center gap-3">
            <div className="p-3 bg-neutral-800 rounded-full text-brand-gold">
              <CreditCard className="w-6 h-6" />
            </div>
            <div>
              <h4 className="text-sm font-semibold text-white">MTN & Airtel MoMo</h4>
              <p className="text-xs text-neutral-400">Secure instant payments</p>
            </div>
          </div>

          <div className="flex flex-col sm:flex-row items-center gap-3">
            <div className="p-3 bg-neutral-800 rounded-full text-brand-gold">
              <RotateCcw className="w-6 h-6" />
            </div>
            <div>
              <h4 className="text-sm font-semibold text-white">Quality Guarantee</h4>
              <p className="text-xs text-neutral-400">7-day exchange warranty</p>
            </div>
          </div>
        </div>
      </div>

      {/* Main Footer Links */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-5 gap-8">
          {/* Brand Info */}
          <div className="md:col-span-2 space-y-4">
            <span className="font-serif text-2xl font-bold tracking-wider text-white">
              CROWN<span className="text-brand-500">LUXE</span>
            </span>
            <p className="text-xs leading-relaxed text-neutral-400 max-w-sm">
              Uganda's premier luxury wig & hair boutique. We craft ultra-thin HD melted frontals, bone straight virgin hair, and effortless glueless bobs designed for royalty.
            </p>
            <div className="space-y-2 text-xs text-neutral-400 pt-2">
              <p className="flex items-center gap-2">
                <MapPin className="w-4 h-4 text-brand-500 shrink-0" />
                CrownLuxe Studio, Acacia Mall, Kisementi, Kampala
              </p>
              <p className="flex items-center gap-2">
                <Phone className="w-4 h-4 text-brand-500 shrink-0" />
                <a href="tel:+256700112233" className="hover:text-white">+256 700 112 233</a> / <a href="tel:+256772987654" className="hover:text-white">+256 772 987 654</a>
              </p>
              <p className="flex items-center gap-2">
                <Mail className="w-4 h-4 text-brand-500 shrink-0" />
                <a href="mailto:orders@crownluxe.ug" className="hover:text-white">orders@crownluxe.ug</a>
              </p>
            </div>
          </div>

          {/* Quick Categories */}
          <div>
            <h4 className="text-xs font-bold uppercase tracking-wider text-white mb-4">Shop Wigs</h4>
            <ul className="space-y-2 text-xs">
              <li><Link href="/shop?hair_type=human" className="hover:text-white transition">Human Hair Wigs</Link></li>
              <li><Link href="/shop?texture=Bone+Straight" className="hover:text-white transition">Bone Straight Wigs</Link></li>
              <li><Link href="/shop?texture=Deep+Wave" className="hover:text-white transition">Deep Wave & Curls</Link></li>
              <li><Link href="/shop?category=bob-wigs" className="hover:text-white transition">Glueless Bobs</Link></li>
              <li><Link href="/shop?category=colored-wigs" className="hover:text-white transition">Piano Highlights & 613</Link></li>
              <li><Link href="/shop?category=hair-extensions" className="hover:text-white transition">Virgin Bundles</Link></li>
            </ul>
          </div>

          {/* Customer Service */}
          <div>
            <h4 className="text-xs font-bold uppercase tracking-wider text-white mb-4">Customer Care</h4>
            <ul className="space-y-2 text-xs">
              <li><Link href="/orders/track/CLM-DEMO" className="hover:text-white transition">Track Your Order</Link></li>
              <li><Link href="/account" className="hover:text-white transition">My Account</Link></li>
              <li><Link href="/wishlist" className="hover:text-white transition">Saved Wishlist</Link></li>
              <li><Link href="/checkout" className="hover:text-white transition">Delivery Zones & Fees</Link></li>
              <li><Link href="/admin-portal" className="text-brand-400 hover:text-white transition">Store Admin Portal</Link></li>
            </ul>
          </div>

          {/* Newsletter */}
          <div>
            <h4 className="text-xs font-bold uppercase tracking-wider text-white mb-4">VIP Hair Club</h4>
            <p className="text-xs text-neutral-400 mb-3">
              Subscribe for secret restocks, private sales & 10% off your next purchase.
            </p>
            {subscribed ? (
              <p className="text-xs text-brand-gold font-medium">✨ Thank you for subscribing!</p>
            ) : (
              <form onSubmit={handleSubscribe} className="space-y-2">
                <label htmlFor="newsletter-email" className="sr-only">Email address</label>
                <input
                  id="newsletter-email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="Enter your email"
                  required
                  className="w-full bg-neutral-800 border border-neutral-700 rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-brand-500"
                />
                <button
                  type="submit"
                  className="w-full bg-brand-600 hover:bg-brand-700 text-white font-medium py-2 rounded-lg text-xs transition"
                >
                  Join VIP Club
                </button>
              </form>
            )}
          </div>
        </div>
      </div>

      {/* Copyright & Payment Badges */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-8 border-t border-neutral-800 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-neutral-500">
        <p>© 2026 CrownLuxe Wigs & Hair Uganda. All rights reserved.</p>
        <div className="flex items-center gap-3">
          <span className="text-[10px] uppercase font-semibold text-neutral-400">Supported Payments:</span>
          <span className="bg-yellow-500/20 text-yellow-400 px-2 py-0.5 rounded text-[10px] font-bold">MTN MoMo</span>
          <span className="bg-red-500/20 text-red-400 px-2 py-0.5 rounded text-[10px] font-bold">Airtel Money</span>
          <span className="bg-blue-500/20 text-blue-400 px-2 py-0.5 rounded text-[10px] font-bold">VISA / Mastercard</span>
        </div>
      </div>
    </footer>
  );
}
