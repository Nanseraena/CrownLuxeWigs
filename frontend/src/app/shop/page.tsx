"use client";

import React, { useState, useEffect, Suspense } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import { useQuery } from "@tanstack/react-query";
import { SlidersHorizontal, X, ArrowUpDown, Search, Sparkles } from "lucide-react";
import { Product, Category } from "@/types";
import { fetchApi } from "@/lib/api";
import ProductCard from "@/components/catalog/ProductCard";
import FilterSidebar from "@/components/catalog/FilterSidebar";

function ShopContent() {
  const router = useRouter();
  const searchParams = useSearchParams();

  const [mobileFilterOpen, setMobileFilterOpen] = useState(false);

  // Read filter query params
  const search = searchParams.get("search") || "";
  const category = searchParams.get("category") || "";
  const hairType = searchParams.get("hair_type") || "";
  const texture = searchParams.get("texture") || "";
  const lengthInches = searchParams.get("length_inches") || "";
  const inStock = searchParams.get("in_stock") === "true";
  const ordering = searchParams.get("ordering") || "-created_at";

  // Build query string
  const queryParams = new URLSearchParams();
  if (search) queryParams.set("search", search);
  if (category) queryParams.set("category__slug", category);
  if (hairType) queryParams.set("hair_type", hairType);
  if (texture) queryParams.set("texture", texture);
  if (lengthInches) queryParams.set("length_inches", lengthInches);
  if (inStock) queryParams.set("in_stock", "true");
  if (ordering) queryParams.set("ordering", ordering);

  // Fetch Products
  const { data: productsData, isLoading: productsLoading } = useQuery<{ count: number; results: Product[] }>({
    queryKey: ["products", queryParams.toString()],
    queryFn: () => fetchApi(`/products/?${queryParams.toString()}`),
  });

  // Fetch Categories
  const { data: categoriesData } = useQuery<{ results: Category[] }>({
    queryKey: ["categories"],
    queryFn: () => fetchApi("/categories/"),
  });

  const categories = categoriesData?.results || [];
  const products = productsData?.results || [];
  const totalCount = productsData?.count || 0;

  const updateParam = (key: string, value: string) => {
    const next = new URLSearchParams(searchParams.toString());
    if (value) next.set(key, value);
    else next.delete(key);
    router.push(`/shop?${next.toString()}`);
  };

  const resetAllFilters = () => {
    router.push("/shop");
    setMobileFilterOpen(false);
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
      {/* Breadcrumb & Header */}
      <div className="mb-6">
        <h1 className="font-serif text-3xl sm:text-4xl font-bold text-neutral-900">
          {category ? `${category.replace(/-/g, " ").toUpperCase()}` : search ? `Search: "${search}"` : "All Luxury Wigs"}
        </h1>
        <p className="text-xs sm:text-sm text-neutral-500 mt-1">
          Showing {totalCount} premium virgin wigs & hair extensions available for express delivery.
        </p>
      </div>

      {/* Filter Chips & Sorting Bar */}
      <div className="flex flex-wrap items-center justify-between gap-3 py-3 border-y border-neutral-200 mb-8">
        <div className="flex flex-wrap items-center gap-2">
          {/* Mobile Filter Button */}
          <button
            onClick={() => setMobileFilterOpen(true)}
            className="lg:hidden flex items-center gap-1.5 bg-neutral-100 hover:bg-neutral-200 px-3.5 py-2 rounded-xl text-xs font-semibold text-neutral-800 transition"
          >
            <SlidersHorizontal className="w-3.5 h-3.5" />
            <span>Filters</span>
          </button>

          {/* Active Filter Chips */}
          {search && (
            <span className="inline-flex items-center gap-1 bg-brand-50 text-brand-900 border border-brand-200 px-2.5 py-1 rounded-full text-xs font-medium">
              Keyword: "{search}"
              <button onClick={() => updateParam("search", "")}><X className="w-3 h-3 text-brand-600" /></button>
            </span>
          )}
          {category && (
            <span className="inline-flex items-center gap-1 bg-brand-50 text-brand-900 border border-brand-200 px-2.5 py-1 rounded-full text-xs font-medium">
              Category: {category}
              <button onClick={() => updateParam("category", "")}><X className="w-3 h-3 text-brand-600" /></button>
            </span>
          )}
          {texture && (
            <span className="inline-flex items-center gap-1 bg-brand-50 text-brand-900 border border-brand-200 px-2.5 py-1 rounded-full text-xs font-medium">
              Texture: {texture}
              <button onClick={() => updateParam("texture", "")}><X className="w-3 h-3 text-brand-600" /></button>
            </span>
          )}
          {lengthInches && (
            <span className="inline-flex items-center gap-1 bg-brand-50 text-brand-900 border border-brand-200 px-2.5 py-1 rounded-full text-xs font-medium">
              Length: {lengthInches}"
              <button onClick={() => updateParam("length_inches", "")}><X className="w-3 h-3 text-brand-600" /></button>
            </span>
          )}
          {inStock && (
            <span className="inline-flex items-center gap-1 bg-emerald-50 text-emerald-900 border border-emerald-200 px-2.5 py-1 rounded-full text-xs font-medium">
              In Stock Only
              <button onClick={() => updateParam("in_stock", "")}><X className="w-3 h-3 text-emerald-600" /></button>
            </span>
          )}
        </div>

        {/* Sorting Dropdown */}
        <div className="flex items-center gap-2 text-xs">
          <span className="text-neutral-500 hidden sm:inline">Sort by:</span>
          <select
            value={ordering}
            onChange={(e) => updateParam("ordering", e.target.value)}
            className="bg-white border border-neutral-300 rounded-xl px-3 py-2 text-xs font-semibold text-neutral-800 focus:outline-none focus:border-brand-500"
          >
            <option value="-created_at">Newest Arrivals</option>
            <option value="price_asc">Price: Low to High</option>
            <option value="price_desc">Price: High to Low</option>
            <option value="name">Name (A-Z)</option>
          </select>
        </div>
      </div>

      {/* Main Grid + Sidebar */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
        {/* Desktop Sidebar */}
        <div className="hidden lg:block lg:col-span-1">
          <FilterSidebar
            categories={categories}
            selectedCategory={category}
            selectedHairType={hairType}
            selectedTexture={texture}
            selectedLength={lengthInches}
            inStockOnly={inStock}
            onSelectCategory={(val) => updateParam("category", val)}
            onSelectHairType={(val) => updateParam("hair_type", val)}
            onSelectTexture={(val) => updateParam("texture", val)}
            onSelectLength={(val) => updateParam("length_inches", val)}
            onToggleInStock={(val) => updateParam("in_stock", val ? "true" : "")}
            onResetFilters={resetAllFilters}
          />
        </div>

        {/* Product Cards Grid */}
        <div className="lg:col-span-3">
          {productsLoading ? (
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4 sm:gap-6">
              {[1, 2, 3, 4, 5, 6].map((n) => (
                <div key={n} className="aspect-[3/4] bg-neutral-100 rounded-2xl animate-pulse" />
              ))}
            </div>
          ) : products.length === 0 ? (
            <div className="text-center py-20 bg-neutral-50 rounded-3xl p-8 border border-neutral-200">
              <div className="w-16 h-16 bg-neutral-200 rounded-full flex items-center justify-center mx-auto mb-4 text-neutral-500">
                <Search className="w-8 h-8" />
              </div>
              <h3 className="font-serif text-xl font-bold text-neutral-900 mb-2">No matching wigs found</h3>
              <p className="text-xs text-neutral-500 max-w-sm mx-auto mb-6">
                Try removing some filters or search for another texture like "Bone Straight" or "Deep Wave".
              </p>
              <button
                onClick={resetAllFilters}
                className="bg-brand-dark text-white text-xs font-semibold px-6 py-3 rounded-full hover:bg-neutral-800 transition"
              >
                Clear All Filters
              </button>
            </div>
          ) : (
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4 sm:gap-6">
              {products.map((product) => (
                <ProductCard key={product.id} product={product} />
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Mobile Filter Modal */}
      {mobileFilterOpen && (
        <div className="lg:hidden fixed inset-0 z-50 bg-black/60 backdrop-blur-sm" onClick={() => setMobileFilterOpen(false)}>
          <div
            className="w-4/5 max-w-sm bg-white h-full p-6 overflow-y-auto ml-auto"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-center justify-between pb-4 border-b border-neutral-100 mb-6">
              <span className="font-serif text-lg font-bold text-brand-dark">Filter Wigs</span>
              <button onClick={() => setMobileFilterOpen(false)}>
                <X className="w-5 h-5 text-neutral-500" />
              </button>
            </div>

            <FilterSidebar
              categories={categories}
              selectedCategory={category}
              selectedHairType={hairType}
              selectedTexture={texture}
              selectedLength={lengthInches}
              inStockOnly={inStock}
              onSelectCategory={(val) => {
                updateParam("category", val);
                setMobileFilterOpen(false);
              }}
              onSelectHairType={(val) => {
                updateParam("hair_type", val);
                setMobileFilterOpen(false);
              }}
              onSelectTexture={(val) => {
                updateParam("texture", val);
                setMobileFilterOpen(false);
              }}
              onSelectLength={(val) => {
                updateParam("length_inches", val);
                setMobileFilterOpen(false);
              }}
              onToggleInStock={(val) => {
                updateParam("in_stock", val ? "true" : "");
                setMobileFilterOpen(false);
              }}
              onResetFilters={resetAllFilters}
            />
          </div>
        </div>
      )}
    </div>
  );
}

export default function ShopPage() {
  return (
    <Suspense fallback={<div className="min-h-screen flex items-center justify-center">Loading CrownLuxe Catalog...</div>}>
      <ShopContent />
    </Suspense>
  );
}
