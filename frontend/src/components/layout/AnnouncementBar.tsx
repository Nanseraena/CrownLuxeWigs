"use client";

import React, { useState } from "react";
import { Sparkles, X, Truck, Tag } from "lucide-react";

export default function AnnouncementBar() {
  const [visible, setVisible] = useState(true);

  if (!visible) return null;

  return (
    <div className="bg-brand-dark text-white text-xs font-medium py-2 px-4 relative z-50">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        <div className="hidden sm:flex items-center gap-2 text-rose-200">
          <Truck className="w-3.5 h-3.5" />
          <span>Same-Day Delivery in Kampala & Entebbe</span>
        </div>

        <div className="flex-1 text-center flex items-center justify-center gap-2">
          <Sparkles className="w-3.5 h-3.5 text-brand-gold animate-pulse" />
          <span>
            SPRING GLAM SALE: Use code <strong className="text-brand-gold bg-black/40 px-1.5 py-0.5 rounded tracking-wide font-bold">WELCOME10</strong> for 10% OFF
          </span>
          <span className="hidden md:inline text-neutral-400">• Pay via MTN MoMo, Airtel & Cards</span>
        </div>

        <div className="flex items-center gap-4">
          <button
            onClick={() => setVisible(false)}
            className="text-neutral-400 hover:text-white transition p-0.5"
            aria-label="Dismiss banner"
          >
            <X className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>
    </div>
  );
}
