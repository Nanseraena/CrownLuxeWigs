"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useQuery } from "@tanstack/react-query";
import { ArrowRight, Sparkles, Star, ShieldCheck, Flame, Tag, Heart, Clock } from "lucide-react";
import { Product, Category, Coupon } from "@/types";
import { fetchApi } from "@/lib/api";
import ProductCard from "@/components/catalog/ProductCard";

export default function HomePage() {
  const [activeTab, setActiveTab] = useState<"best_seller" | "new_arrival">("best_seller");

  // Fetch Categories
  const { data: categoriesData } = useQuery<{ results: Category[] }>({
    queryKey: ["categories"],
    queryFn: () => fetchApi("/categories/"),
  });

  // Fetch Featured / Best Sellers Products
  const { data: productsData, isLoading: productsLoading } = useQuery<{ results: Product[] }>({
    queryKey: ["products", activeTab],
    queryFn: () => fetchApi(`/products/?${activeTab === "best_seller" ? "is_best_seller=true" : "is_new_arrival=true"}`),
  });

  // Fetch Trending Wigs
  const { data: trendingData } = useQuery<{ results: Product[] }>({
    queryKey: ["trending-products"],
    queryFn: () => fetchApi("/products/?is_featured=true"),
  });

  // Fetch Active Coupons
  const { data: coupons } = useQuery<Coupon[]>({
    queryKey: ["active-coupons"],
    queryFn: () => fetchApi("/promotions/active/"),
  });

  const categories = categoriesData?.results || [];
  const products = productsData?.results || [];
  const trendingWigs = trendingData?.results || [];

  return (
    <div className="space-y-16 sm:space-y-24 pb-16">
      {/* 1. HERO SECTION */}
      <section className="relative bg-neutral-900 text-white overflow-hidden min-h-[520px] sm:min-h-[640px] flex items-center">
        {/* Background Image with Dark Vignette */}
        <div className="absolute inset-0 z-0">
          <img
            src="https://images.unsplash.com/photo-1580618672591-eb180b1a973f?auto=format&fit=crop&w=1800&q=85"
            alt="CrownLuxe Luxury Wigs Campaign"
            className="w-full h-full object-cover object-top opacity-40 mix-blend-luminosity scale-105"
          />
          <div className="absolute inset-0 bg-gradient-to-r from-neutral-950 via-neutral-950/80 to-transparent" />
        </div>

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 py-16 sm:py-24">
          <div className="max-w-xl space-y-6">
            <div className="inline-flex items-center gap-2 bg-brand-gold/20 text-brand-gold border border-brand-gold/30 px-3.5 py-1.5 rounded-full text-xs font-semibold tracking-wider uppercase">
              <Sparkles className="w-3.5 h-3.5" />
              <span>100% Virgin Hair • Imperceptible HD Lace</span>
            </div>

            <h1 className="font-serif text-4xl sm:text-6xl font-bold tracking-tight text-white leading-[1.1]">
              Flawless Crowns For <span className="text-brand-300 italic">Royalty</span>.
            </h1>

            <p className="text-sm sm:text-base text-neutral-300 leading-relaxed font-light">
              Experience the melted illusion of ultra-thin HD swiss lace and silky virgin human hair. Ready-to-wear glueless bobs and showstopping bone straight wigs delivered right to your doorstep in Uganda.
            </p>

            <div className="flex flex-wrap items-center gap-4 pt-2">
              <Link
                href="/shop"
                className="bg-brand-500 hover:bg-brand-600 text-white font-semibold text-xs sm:text-sm px-8 py-3.5 rounded-full shadow-lg shadow-brand-600/30 transition flex items-center gap-2 group"
              >
                <span>SHOP ALL WIGS</span>
                <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
              </Link>
              <Link
                href="/shop?texture=Bone+Straight"
                className="bg-white/10 hover:bg-white/20 backdrop-blur-md text-white border border-white/20 font-semibold text-xs sm:text-sm px-6 py-3.5 rounded-full transition"
              >
                Bone Straight Edit
              </Link>
            </div>

            {/* Quick Metrics */}
            <div className="pt-8 border-t border-white/10 grid grid-cols-3 gap-6 text-left">
              <div>
                <p className="font-serif text-2xl font-bold text-white">100%</p>
                <p className="text-[11px] text-neutral-400">Raw Virgin Hair</p>
              </div>
              <div>
                <p className="font-serif text-2xl font-bold text-white">4 Hrs</p>
                <p className="text-[11px] text-neutral-400">Kampala Delivery</p>
              </div>
              <div>
                <p className="font-serif text-2xl font-bold text-white">4.9 ★</p>
                <p className="text-[11px] text-neutral-400">Customer Rating</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 2. SHOP BY CATEGORY CAROUSEL (SHEIN Style Stories / Circles) */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-end justify-between mb-8">
          <div>
            <span className="text-xs font-bold uppercase tracking-widest text-brand-600">Curated Collections</span>
            <h2 className="font-serif text-2xl sm:text-3xl font-bold text-neutral-900 mt-1">Shop by Category</h2>
          </div>
          <Link href="/shop" className="text-xs font-semibold text-brand-600 hover:text-brand-800 flex items-center gap-1">
            <span>Explore All</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-8 gap-4 sm:gap-6">
          {categories.map((cat) => (
            <Link
              key={cat.id}
              href={`/shop?category=${cat.slug}`}
              className="group flex flex-col items-center text-center space-y-2.5"
            >
              <div className="w-20 h-20 sm:w-24 sm:h-24 rounded-full p-1 border-2 border-brand-200 group-hover:border-brand-600 transition-all duration-300 overflow-hidden shadow-sm">
                <img
                  src={cat.image_url || "https://images.unsplash.com/photo-1595476108010-b4d1f102b1b1?auto=format&fit=crop&w=300&q=80"}
                  alt={cat.name}
                  className="w-full h-full object-cover rounded-full group-hover:scale-110 transition-transform duration-500"
                />
              </div>
              <span className="text-xs font-semibold text-neutral-800 group-hover:text-brand-600 transition leading-snug line-clamp-2">
                {cat.name}
              </span>
            </Link>
          ))}
        </div>
      </section>

      {/* 3. PROMOTIONAL COUPONS BANNER */}
      {coupons && coupons.length > 0 && (
        <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-gradient-to-r from-rose-50 via-amber-50 to-rose-100 rounded-3xl p-6 sm:p-8 border border-rose-200/60 shadow-sm">
            <div className="flex flex-col md:flex-row items-center justify-between gap-6">
              <div className="space-y-1 text-center md:text-left">
                <span className="inline-flex items-center gap-1.5 bg-brand-600 text-white text-[10px] font-extrabold uppercase px-2.5 py-1 rounded-full">
                  <Tag className="w-3 h-3" />
                  Exclusive Voucher Discounts
                </span>
                <h3 className="font-serif text-2xl font-bold text-neutral-900 mt-2">
                  Claim Your CrownLuxe Discount Codes
                </h3>
                <p className="text-xs text-neutral-600 max-w-md">
                  Apply these verified promo codes at checkout to save instantly on your favorite virgin hair wigs.
                </p>
              </div>

              <div className="flex flex-wrap gap-3 justify-center">
                {coupons.map((c) => (
                  <div
                    key={c.id}
                    className="bg-white px-4 py-3 rounded-2xl border border-neutral-200 shadow-sm flex items-center gap-3"
                  >
                    <div>
                      <p className="font-mono text-xs font-bold text-brand-600 tracking-wider">{c.code}</p>
                      <p className="text-[11px] text-neutral-500">{c.description}</p>
                    </div>
                    <span className="text-[10px] bg-neutral-100 px-2 py-1 rounded text-neutral-700 font-semibold uppercase">
                      Active
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </section>
      )}

      {/* 4. BEST SELLERS & NEW ARRIVALS (TABBED SHEIN PRODUCT GRID) */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
          <div>
            <span className="text-xs font-bold uppercase tracking-widest text-brand-600">Handpicked Quality</span>
            <h2 className="font-serif text-2xl sm:text-3xl font-bold text-neutral-900 mt-1">Trending Glamour</h2>
          </div>

          {/* Switcher Tabs */}
          <div className="inline-flex p-1 bg-neutral-100 rounded-full border border-neutral-200 self-start sm:self-auto">
            <button
              onClick={() => setActiveTab("best_seller")}
              className={`px-5 py-2 rounded-full text-xs font-bold transition ${
                activeTab === "best_seller"
                  ? "bg-brand-dark text-white shadow-sm"
                  : "text-neutral-600 hover:text-black"
              }`}
            >
              🔥 Best Sellers
            </button>
            <button
              onClick={() => setActiveTab("new_arrival")}
              className={`px-5 py-2 rounded-full text-xs font-bold transition ${
                activeTab === "new_arrival"
                  ? "bg-brand-dark text-white shadow-sm"
                  : "text-neutral-600 hover:text-black"
              }`}
            >
              ✨ New Arrivals
            </button>
          </div>
        </div>

        {/* Product Grid */}
        {productsLoading ? (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 sm:gap-6">
            {[1, 2, 3, 4, 5, 6, 7, 8].map((n) => (
              <div key={n} className="aspect-[3/4] bg-neutral-100 rounded-2xl animate-pulse" />
            ))}
          </div>
        ) : (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 sm:gap-6">
            {products.map((product) => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div>
        )}

        <div className="text-center mt-10">
          <Link
            href="/shop"
            className="inline-flex items-center gap-2 bg-neutral-900 hover:bg-neutral-800 text-white text-xs font-bold px-8 py-3.5 rounded-full transition shadow-md"
          >
            <span>VIEW ALL WIGS & EXTENSIONS</span>
            <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      </section>

      {/* 5. FLASH DEALS / TRENDING SHOWCASE */}
      <section className="bg-neutral-900 text-white py-16 sm:py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col md:flex-row md:items-end justify-between gap-4 mb-10">
            <div>
              <div className="inline-flex items-center gap-1.5 bg-rose-500/20 text-rose-400 border border-rose-500/30 px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider mb-2">
                <Flame className="w-3.5 h-3.5" />
                Featured Staff Picks
              </div>
              <h2 className="font-serif text-2xl sm:text-4xl font-bold text-white">
                The HD Lace Experience
              </h2>
            </div>
            <p className="text-xs text-neutral-400 max-w-sm">
              Watch our swiss transparent lace melt completely against any skin tone. Pre-plucked with natural hairline.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {trendingWigs.slice(0, 3).map((wig) => (
              <div
                key={wig.id}
                className="bg-neutral-800/80 rounded-2xl overflow-hidden border border-neutral-700/60 p-4 flex flex-col justify-between"
              >
                <div className="aspect-[4/3] rounded-xl overflow-hidden mb-4 bg-neutral-900">
                  <img
                    src={wig.primary_image?.image_url || "https://images.unsplash.com/photo-1580618672591-eb180b1a973f?auto=format&fit=crop&w=600&q=80"}
                    alt={wig.name}
                    className="w-full h-full object-cover hover:scale-105 transition duration-500"
                  />
                </div>
                <div>
                  <span className="text-[11px] font-bold text-brand-gold uppercase">{wig.texture}</span>
                  <h3 className="font-semibold text-sm text-white line-clamp-1 mt-0.5">{wig.name}</h3>
                  <p className="text-xs text-neutral-400 line-clamp-2 mt-1">{wig.description}</p>
                </div>
                <div className="mt-4 pt-4 border-t border-neutral-700/60 flex items-center justify-between">
                  <span className="text-sm font-bold text-white">From UGX {parseInt(wig.min_price || "0").toLocaleString()}</span>
                  <Link
                    href={`/products/${wig.slug}`}
                    className="text-xs text-brand-300 font-semibold hover:text-white flex items-center gap-1"
                  >
                    <span>View Wig</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </Link>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* 6. REAL CUSTOMER REVIEWS & UGC */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-xl mx-auto mb-12">
          <span className="text-xs font-bold uppercase tracking-widest text-brand-600">Loved by 5,000+ Queens</span>
          <h2 className="font-serif text-2xl sm:text-3xl font-bold text-neutral-900 mt-1">
            Real Reviews From Real Customers
          </h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {[
            {
              name: "Sarah K.",
              location: "Kololo, Kampala",
              rating: 5,
              wig: "13x4 Bone Straight 26\"",
              comment: "The HD lace literally disappeared into my skin! Delivered to my office in Kololo within 2 hours. Zero tangling after a whole month of daily wear.",
            },
            {
              name: "Brenda A.",
              location: "Entebbe",
              rating: 5,
              wig: "Wear & Go Glueless Blunt Bob",
              comment: "I used to spend 45 minutes putting on wigs with glue. This pre-cut glueless bob takes me 30 seconds. Best hair purchase ever in Uganda!",
            },
            {
              name: "Grace T.",
              location: "Naguru, Kampala",
              rating: 5,
              wig: "Deep Wave Frontal Wig 28\"",
              comment: "Wore this to my sister's wedding and people thought it was my real hair! Paid via MTN MoMo seamlessly. CrownLuxe is top tier.",
            },
          ].map((rev, idx) => (
            <div
              key={idx}
              className="bg-neutral-50 p-6 rounded-2xl border border-neutral-200/80 flex flex-col justify-between"
            >
              <div className="space-y-3">
                <div className="flex items-center gap-1 text-amber-400">
                  {[...Array(rev.rating)].map((_, i) => (
                    <Star key={i} className="w-4 h-4 fill-amber-400 text-amber-400" />
                  ))}
                </div>
                <p className="text-xs text-neutral-700 leading-relaxed italic">"{rev.comment}"</p>
              </div>

              <div className="pt-4 mt-4 border-t border-neutral-200 flex items-center justify-between text-xs">
                <div>
                  <h4 className="font-bold text-neutral-900">{rev.name}</h4>
                  <p className="text-[11px] text-neutral-500">{rev.location}</p>
                </div>
                <span className="text-[10px] bg-emerald-50 text-emerald-800 font-bold px-2 py-0.5 rounded border border-emerald-200">
                  Verified Buyer
                </span>
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
