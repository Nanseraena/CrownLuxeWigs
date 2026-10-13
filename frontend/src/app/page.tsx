"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useQuery } from "@tanstack/react-query";
import { ArrowRight, Sparkles, Star, Flame, Tag, Clock, CheckCircle2, Scissors, ShieldCheck, Heart } from "lucide-react";
import { Product, Category, Coupon, Collection } from "@/types";
import { fetchApi } from "@/lib/api";
import ProductCard from "@/components/catalog/ProductCard";

const DEFAULT_CATEGORIES: Category[] = [
  { id: 1, name: "Lace Front Wigs", slug: "lace-front-wigs", image_url: "/images/categories/hd-lace-front.jpg", description: "Ultra-thin melted invisible HD swiss lace for imperceptible blend.", sort_order: 1 },
  { id: 2, name: "Closure Wigs", slug: "closure-wigs", image_url: "/images/categories/glueless-wigs.jpg", description: "Low-maintenance HD and Swiss lace closures with realistic natural parting.", sort_order: 2 },
  { id: 3, name: "Glueless Wigs", slug: "glueless-wigs", image_url: "/images/categories/glueless-wigs.jpg", description: "Pre-cut lace, pre-plucked, zero adhesive needed in 30 seconds.", sort_order: 3 },
  { id: 4, name: "Bob Wigs", slug: "bob-wigs", image_url: "/images/categories/bob-wigs.jpg", description: "Chic blunt cut, asymmetrical, and timeless bob styles for everyday glam.", sort_order: 4 },
  { id: 5, name: "Curly & Wavy Wigs", slug: "curly-and-wavy-wigs", image_url: "/images/categories/deep-wave.jpg", description: "Lush bouncy defined curls with high volume and luscious texture.", sort_order: 5 },
  { id: 6, name: "Straight Wigs", slug: "straight-wigs", image_url: "/images/categories/bone-straight.jpg", description: "Silky, mirror-shine bone straight human hair that stays sleek.", sort_order: 6 },
  { id: 7, name: "Colored Wigs", slug: "colored-wigs", image_url: "/images/categories/colored-highlights.jpg", description: "Trendy piano highlights, 613 platinum blonde, and 99J burgundy.", sort_order: 7 },
  { id: 8, name: "Specialty Wigs", slug: "specialty-wigs", image_url: "/images/categories/human-hair.jpg", description: "Headband slip-on, 360 lace, and pixie units.", sort_order: 8 },
  { id: 9, name: "Hair Extensions", slug: "hair-extensions", image_url: "/images/categories/hair-bundles.jpg", description: "Raw donor virgin hair bundles, closures, and frontals.", sort_order: 9 },
];

const COLOR_CARDS = [
  {
    name: "Jet & Natural Black",
    colors: "Jet Black,Natural Black",
    hex: "#0A0A0A",
    subtitle: "Classic, high natural sheen",
    bgClass: "from-neutral-950 to-neutral-800 text-white",
  },
  {
    name: "Honey Blonde & Piano",
    colors: "Piano Highlights,Honey Blonde",
    hex: "#D4A359",
    subtitle: "Caramel balayage & sun-kissed ribbons",
    bgClass: "from-amber-100 to-amber-200 text-amber-950",
  },
  {
    name: "Spiced Ginger & Copper",
    colors: "Ginger,Copper",
    hex: "#B25329",
    subtitle: "Warm autumnal spiced ginger tones",
    bgClass: "from-orange-100 to-amber-100 text-orange-950",
  },
  {
    name: "99J Deep Wine Burgundy",
    colors: "Burgundy",
    hex: "#5B1426",
    subtitle: "Vampy cherry wine in direct sunlight",
    bgClass: "from-rose-950 to-rose-900 text-rose-100",
  },
  {
    name: "Mocha & Chocolate Brown",
    colors: "Chocolate Brown,Natural Brown",
    hex: "#3B2219",
    subtitle: "Soft warm chocolate truffle elegance",
    bgClass: "from-amber-900 to-amber-950 text-amber-100",
  },
];

const LENGTH_CARDS = [
  {
    title: "Short Bobs & Pixies",
    range: "10\"–14\"",
    group: "short",
    desc: "Low-maintenance, breeze around neck, sharp jawline framing.",
    img: "/images/categories/bob-wigs.jpg",
  },
  {
    title: "Mid-Length Everyday",
    range: "16\"–20\"",
    group: "medium",
    desc: "Collarbone grazing, professional office glam, versatile wear.",
    img: "/images/categories/glueless-wigs.jpg",
  },
  {
    title: "Long Flowing Luxury",
    range: "22\"–26\"",
    group: "long",
    desc: "Mermaid luster, cascading loose waves, red carpet presence.",
    img: "/images/categories/deep-wave.jpg",
  },
  {
    title: "Extra Long Statement",
    range: "28\"–32\"",
    group: "extra_long",
    desc: "Tailbone glass hair, 250% high density, ultimate showstopper.",
    img: "/images/categories/bone-straight.jpg",
  },
];

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

  const categories = (categoriesData?.results && categoriesData.results.length > 0)
    ? categoriesData.results
    : DEFAULT_CATEGORIES;
  const products = productsData?.results || [];
  const trendingWigs = trendingData?.results || [];

  return (
    <div className="space-y-16 sm:space-y-24 pb-16">
      {/* 1. HERO SECTION */}
      <section className="relative bg-neutral-900 text-white overflow-hidden min-h-[520px] sm:min-h-[640px] flex items-center">
        {/* Background Image with Dark Vignette */}
        <div className="absolute inset-0 z-0">
          <img
            src="/images/categories/hd-lace-front.jpg"
            alt="CrownLuxe Luxury Wigs Campaign"
            className="w-full h-full object-cover object-top opacity-35 mix-blend-luminosity scale-105"
          />
          <div className="absolute inset-0 bg-gradient-to-r from-neutral-950 via-neutral-950/85 to-transparent" />
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

      {/* 2. SHOP BY CATEGORY (SHEIN Stories Circles) */}
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

        <div className="grid grid-cols-3 sm:grid-cols-5 lg:grid-cols-9 gap-3 sm:gap-5">
          {categories.map((cat) => (
            <Link
              key={cat.id}
              href={`/shop?category=${cat.slug}`}
              className="group flex flex-col items-center text-center space-y-2"
            >
              <div className="w-16 h-16 sm:w-20 sm:h-20 rounded-full p-1 border-2 border-brand-200 group-hover:border-brand-600 transition-all duration-300 overflow-hidden shadow-sm">
                <img
                  src={cat.image_url || "/images/categories/bone-straight.jpg"}
                  alt={cat.name}
                  className="w-full h-full object-cover rounded-full group-hover:scale-110 transition-transform duration-500"
                />
              </div>
              <span className="text-[11px] font-semibold text-neutral-800 group-hover:text-brand-600 transition leading-tight line-clamp-2">
                {cat.name}
              </span>
            </Link>
          ))}
        </div>
      </section>

      {/* 3. SHOP BY COLOR (Visual Pinterest-Inspired Color Cards) */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-end justify-between mb-8">
          <div>
            <span className="text-xs font-bold uppercase tracking-widest text-brand-600">Color Palette</span>
            <h2 className="font-serif text-2xl sm:text-3xl font-bold text-neutral-900 mt-1">Shop by Hair Color</h2>
          </div>
          <Link href="/shop" className="text-xs font-semibold text-brand-600 hover:text-brand-800 flex items-center gap-1">
            <span>View All Colors</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
          {COLOR_CARDS.map((card) => (
            <Link
              key={card.name}
              href={`/shop?color=${card.colors}`}
              className={`rounded-2xl p-5 bg-gradient-to-br ${card.bgClass} shadow-sm hover:shadow-lg transition-all duration-300 flex flex-col justify-between min-h-[140px] group border border-white/20`}
            >
              <div className="flex items-center justify-between">
                <div
                  className="w-7 h-7 rounded-full border-2 border-white/80 shadow-sm"
                  style={{ backgroundColor: card.hex }}
                />
                <ArrowRight className="w-4 h-4 opacity-70 group-hover:translate-x-1 group-hover:opacity-100 transition-all" />
              </div>
              <div>
                <h3 className="font-serif text-base font-bold leading-snug">{card.name}</h3>
                <p className="text-[11px] opacity-80 mt-0.5">{card.subtitle}</p>
              </div>
            </Link>
          ))}
        </div>
      </section>

      {/* 4. SHOP BY LENGTH (Short Bobs, Mid-Length, Long, Extra Long) */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-end justify-between mb-8">
          <div>
            <span className="text-xs font-bold uppercase tracking-widest text-brand-600">Length Guide</span>
            <h2 className="font-serif text-2xl sm:text-3xl font-bold text-neutral-900 mt-1">Shop by Length</h2>
          </div>
          <Link href="/shop" className="text-xs font-semibold text-brand-600 hover:text-brand-800 flex items-center gap-1">
            <span>Length Guide</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 sm:gap-6">
          {LENGTH_CARDS.map((lcard) => (
            <Link
              key={lcard.group}
              href={`/shop?length_group=${lcard.group}`}
              className="group block rounded-2xl overflow-hidden bg-neutral-50 border border-neutral-200/80 hover:shadow-lg transition duration-300"
            >
              <div className="aspect-[4/3] overflow-hidden bg-neutral-200">
                <img
                  src={lcard.img}
                  alt={lcard.title}
                  className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                />
              </div>
              <div className="p-4">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-xs text-neutral-900">{lcard.title}</span>
                  <span className="text-[10px] bg-brand-50 text-brand-700 font-extrabold px-2 py-0.5 rounded-full">
                    {lcard.range}
                  </span>
                </div>
                <p className="text-[11px] text-neutral-500 mt-1 line-clamp-2">{lcard.desc}</p>
              </div>
            </Link>
          ))}
        </div>
      </section>

      {/* 5. PROMOTIONAL COUPONS BANNER */}
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

      {/* 6. BEST SELLERS & NEW ARRIVALS (TABBED GRID) */}
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
            {products.slice(0, 8).map((product) => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div>
        )}

        <div className="text-center mt-10">
          <Link
            href="/shop"
            className="inline-flex items-center gap-2 bg-neutral-900 hover:bg-neutral-800 text-white text-xs font-bold px-8 py-3.5 rounded-full transition shadow-md"
          >
            <span>VIEW ALL 30+ LUXURY WIGS</span>
            <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      </section>

      {/* 7. CURATED COLLECTIONS CALLOUT (Beginner-Friendly, Wedding, Office) */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Link
            href="/shop?collection=beginner-friendly-wigs"
            className="group relative rounded-3xl p-8 bg-gradient-to-br from-rose-50 to-pink-100 border border-rose-200/60 overflow-hidden shadow-sm hover:shadow-md transition"
          >
            <span className="text-[10px] font-extrabold uppercase tracking-widest text-rose-700 bg-white/80 px-2.5 py-1 rounded-full">
              Zero Adhesive
            </span>
            <h3 className="font-serif text-2xl font-bold text-neutral-900 mt-4">Beginner-Friendly Wigs</h3>
            <p className="text-xs text-neutral-600 mt-1 max-w-xs">
              Pre-cut lace and 3D dome caps you can slip on in 30 seconds with zero glue.
            </p>
            <span className="inline-flex items-center gap-1.5 text-xs font-bold text-brand-600 mt-6 group-hover:translate-x-1 transition-transform">
              Explore 30s Wigs <ArrowRight className="w-3.5 h-3.5" />
            </span>
          </Link>

          <Link
            href="/shop?collection=wedding-and-special-occasion"
            className="group relative rounded-3xl p-8 bg-gradient-to-br from-amber-50 to-yellow-100 border border-amber-200/60 overflow-hidden shadow-sm hover:shadow-md transition"
          >
            <span className="text-[10px] font-extrabold uppercase tracking-widest text-amber-800 bg-white/80 px-2.5 py-1 rounded-full">
              Red Carpet Glam
            </span>
            <h3 className="font-serif text-2xl font-bold text-neutral-900 mt-4">Wedding & Occasion</h3>
            <p className="text-xs text-neutral-600 mt-1 max-w-xs">
              Melted 13x6 HD Swiss frontals with showstopping 28" Hollywood waves.
            </p>
            <span className="inline-flex items-center gap-1.5 text-xs font-bold text-brand-600 mt-6 group-hover:translate-x-1 transition-transform">
              View Special Edits <ArrowRight className="w-3.5 h-3.5" />
            </span>
          </Link>

          <Link
            href="/shop?collection=work-and-office-looks"
            className="group relative rounded-3xl p-8 bg-gradient-to-br from-neutral-100 to-stone-200 border border-neutral-300/60 overflow-hidden shadow-sm hover:shadow-md transition"
          >
            <span className="text-[10px] font-extrabold uppercase tracking-widest text-neutral-800 bg-white/80 px-2.5 py-1 rounded-full">
              Corporate Chic
            </span>
            <h3 className="font-serif text-2xl font-bold text-neutral-900 mt-4">Work & Office Looks</h3>
            <p className="text-xs text-neutral-600 mt-1 max-w-xs">
              Razor-sharp precision blunt bobs and neat low-maintenance everyday closures.
            </p>
            <span className="inline-flex items-center gap-1.5 text-xs font-bold text-brand-600 mt-6 group-hover:translate-x-1 transition-transform">
              Shop Workwear Wigs <ArrowRight className="w-3.5 h-3.5" />
            </span>
          </Link>
        </div>
      </section>

      {/* 8. FLASH DEALS / THE HD LACE EXPERIENCE */}
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
                    src={wig.primary_image?.image_url || "/images/categories/bone-straight.jpg"}
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

      {/* 9. REAL CUSTOMER REVIEWS */}
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
