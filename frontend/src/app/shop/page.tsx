"use client";

import React, { useState, Suspense } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import { useQuery } from "@tanstack/react-query";
import { SlidersHorizontal, X, Search, RotateCcw, ArrowUpDown } from "lucide-react";
import { Product, Category } from "@/types";
import { fetchApi } from "@/lib/api";
import ProductCard from "@/components/catalog/ProductCard";
import FilterSidebar from "@/components/catalog/FilterSidebar";

const DEFAULT_CATEGORIES: Category[] = [
  { id: 1, name: "Lace Front Wigs", slug: "lace-front-wigs", image_url: "/images/wigs/categories/lace-front-wigs.webp", description: "Ultra-thin melted invisible HD swiss lace for imperceptible blend.", sort_order: 1 },
  { id: 2, name: "Closure Wigs", slug: "closure-wigs", image_url: "/images/wigs/categories/closure-wigs.webp", description: "Low-maintenance HD and Swiss lace closures with realistic natural parting.", sort_order: 2 },
  { id: 3, name: "Glueless Wigs", slug: "glueless-wigs", image_url: "/images/wigs/categories/glueless-wigs.webp", description: "Pre-cut lace, pre-plucked, zero adhesive needed in 30 seconds.", sort_order: 3 },
  { id: 4, name: "Bob Wigs", slug: "bob-wigs", image_url: "/images/wigs/categories/bob-wigs.webp", description: "Chic blunt cut, asymmetrical, and timeless bob styles for everyday glam.", sort_order: 4 },
  { id: 5, name: "Curly and Wavy Wigs", slug: "curly-and-wavy-wigs", image_url: "/images/wigs/categories/curly-wavy-wigs.webp", description: "Lush bouncy defined curls with high volume and luscious texture.", sort_order: 5 },
  { id: 6, name: "Straight Wigs", slug: "straight-wigs", image_url: "/images/wigs/categories/straight-wigs.webp", description: "Silky, mirror-shine bone straight human hair that stays sleek.", sort_order: 6 },
  { id: 7, name: "Colored Wigs", slug: "colored-wigs", image_url: "/images/wigs/categories/colored-wigs.webp", description: "Trendy piano highlights, 613 platinum blonde, and 99J burgundy.", sort_order: 7 },
  { id: 8, name: "Specialty Wigs", slug: "specialty-wigs", image_url: "/images/wigs/categories/specialty-wigs.webp", description: "Headband wigs, full lace, 360 lace, and pixie units.", sort_order: 8 },
  { id: 9, name: "Hair Extensions", slug: "hair-extensions", image_url: "/images/wigs/categories/hair-extensions.webp", description: "Raw donor virgin hair bundles, closures, and frontals.", sort_order: 9 },
];

function ShopContent() {
  const router = useRouter();
  const searchParams = useSearchParams();

  const [mobileFilterOpen, setMobileFilterOpen] = useState(false);

  // Read filter query params
  const search = searchParams.get("search") || "";
  const category = searchParams.get("category") || searchParams.get("category__slug") || "";
  const subcategory = searchParams.get("subcategory") || searchParams.get("subcategory__slug") || "";
  const collection = searchParams.get("collection") || "";
  const hairType = searchParams.get("hair_type") || searchParams.get("hair_material") || "";
  const texture = searchParams.get("texture") || "";
  const inStock = searchParams.get("in_stock") === "true";
  const ordering = searchParams.get("ordering") || "-created_at";
  const lengthGroup = searchParams.get("length_group") || "";

  // Multi-value parameters (comma-separated or multiple)
  const rawColors = searchParams.get("color") || "";
  const selectedColors = rawColors ? rawColors.split(",").map((s) => s.trim()).filter(Boolean) : [];

  const rawLengths = searchParams.get("length_inches") || searchParams.get("length") || "";
  const selectedLengths = rawLengths ? rawLengths.split(",").map((s) => s.trim()).filter(Boolean) : [];

  const rawOrigins = searchParams.get("hair_origin") || "";
  const selectedOrigins = rawOrigins ? rawOrigins.split(",").map((s) => s.trim()).filter(Boolean) : [];

  // Build query string for API
  const queryParams = new URLSearchParams();
  if (search) queryParams.set("search", search);
  if (category) queryParams.set("category__slug", category);
  if (subcategory) queryParams.set("subcategory__slug", subcategory);
  if (collection) queryParams.set("collection", collection);
  if (hairType) queryParams.set("hair_material", hairType);
  if (texture) queryParams.set("texture", texture);
  if (rawColors) queryParams.set("color", rawColors);
  if (rawLengths) queryParams.set("length_inches", rawLengths);
  if (lengthGroup) queryParams.set("length_group", lengthGroup);
  if (rawOrigins) queryParams.set("hair_origin", rawOrigins);
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

  const categories = (categoriesData?.results && categoriesData.results.length > 0)
    ? categoriesData.results
    : DEFAULT_CATEGORIES;
  const products = productsData?.results || [];
  const totalCount = productsData?.count || 0;

  const updateParam = (key: string, value: string) => {
    const next = new URLSearchParams(searchParams.toString());
    if (value) next.set(key, value);
    else next.delete(key);
    router.push(`/shop?${next.toString()}`);
  };

  const toggleArrayParam = (key: string, currentList: string[], item: string) => {
    const next = new URLSearchParams(searchParams.toString());
    const exists = currentList.includes(item);
    const updated = exists ? currentList.filter((x) => x !== item) : [...currentList, item];
    if (updated.length > 0) {
      next.set(key, updated.join(","));
    } else {
      next.delete(key);
    }
    router.push(`/shop?${next.toString()}`);
  };

  const resetAllFilters = () => {
    router.push("/shop");
    setMobileFilterOpen(false);
  };

  const hasActiveFilters = Boolean(
    search || category || subcategory || collection || hairType || texture ||
    selectedColors.length > 0 || selectedLengths.length > 0 || lengthGroup ||
    selectedOrigins.length > 0 || inStock
  );

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
      {/* Header Banner */}
      <div className="mb-6">
        <h1 className="font-serif text-3xl sm:text-4xl font-bold text-neutral-900 capitalize">
          {category
            ? `${category.replace(/-/g, " ")}`
            : collection
            ? `${collection.replace(/-/g, " ")}`
            : search
            ? `Search: "${search}"`
            : "All Luxury Wigs"}
        </h1>
        <p className="text-xs sm:text-sm text-neutral-500 mt-1">
          Showing {totalCount} authentic virgin human hair wigs & units with Kampala express delivery.
        </p>
      </div>

      {/* Filter Bar & Active Filter Chips */}
      <div className="flex flex-wrap items-center justify-between gap-3 py-3 border-y border-neutral-200 mb-8">
        <div className="flex flex-wrap items-center gap-2">
          {/* Mobile Filter Button */}
          <button
            onClick={() => setMobileFilterOpen(true)}
            className="lg:hidden flex items-center gap-1.5 bg-neutral-100 hover:bg-neutral-200 px-3.5 py-2 rounded-xl text-xs font-semibold text-neutral-800 transition"
          >
            <SlidersHorizontal className="w-3.5 h-3.5" />
            <span>Filters {hasActiveFilters && "•"}</span>
          </button>

          {/* Active Filter Chips */}
          {search && (
            <span className="inline-flex items-center gap-1 bg-brand-50 text-brand-900 border border-brand-200 px-2.5 py-1 rounded-full text-xs font-medium">
              Search: "{search}"
              <button onClick={() => updateParam("search", "")}><X className="w-3 h-3 text-brand-600" /></button>
            </span>
          )}
          {category && (
            <span className="inline-flex items-center gap-1 bg-brand-50 text-brand-900 border border-brand-200 px-2.5 py-1 rounded-full text-xs font-medium capitalize">
              {category.replace(/-/g, " ")}
              <button onClick={() => updateParam("category", "")}><X className="w-3 h-3 text-brand-600" /></button>
            </span>
          )}
          {subcategory && (
            <span className="inline-flex items-center gap-1 bg-brand-50 text-brand-900 border border-brand-200 px-2.5 py-1 rounded-full text-xs font-medium capitalize">
              {subcategory.replace(/-/g, " ")}
              <button onClick={() => updateParam("subcategory", "")}><X className="w-3 h-3 text-brand-600" /></button>
            </span>
          )}
          {collection && (
            <span className="inline-flex items-center gap-1 bg-brand-50 text-brand-900 border border-brand-200 px-2.5 py-1 rounded-full text-xs font-medium capitalize">
              Collection: {collection.replace(/-/g, " ")}
              <button onClick={() => updateParam("collection", "")}><X className="w-3 h-3 text-brand-600" /></button>
            </span>
          )}
          {selectedColors.map((col) => (
            <span key={col} className="inline-flex items-center gap-1 bg-amber-50 text-amber-900 border border-amber-200 px-2.5 py-1 rounded-full text-xs font-medium">
              Color: {col}
              <button onClick={() => toggleArrayParam("color", selectedColors, col)}><X className="w-3 h-3 text-amber-600" /></button>
            </span>
          ))}
          {selectedLengths.map((len) => (
            <span key={len} className="inline-flex items-center gap-1 bg-neutral-100 text-neutral-900 border border-neutral-300 px-2.5 py-1 rounded-full text-xs font-medium">
              Length: {len}"
              <button onClick={() => toggleArrayParam("length_inches", selectedLengths, len)}><X className="w-3 h-3 text-neutral-600" /></button>
            </span>
          ))}
          {lengthGroup && (
            <span className="inline-flex items-center gap-1 bg-neutral-100 text-neutral-900 border border-neutral-300 px-2.5 py-1 rounded-full text-xs font-medium capitalize">
              Group: {lengthGroup.replace("_", " ")}
              <button onClick={() => updateParam("length_group", "")}><X className="w-3 h-3 text-neutral-600" /></button>
            </span>
          )}
          {selectedOrigins.map((orig) => (
            <span key={orig} className="inline-flex items-center gap-1 bg-rose-50 text-rose-900 border border-rose-200 px-2.5 py-1 rounded-full text-xs font-medium capitalize">
              Origin: {orig}
              <button onClick={() => toggleArrayParam("hair_origin", selectedOrigins, orig)}><X className="w-3 h-3 text-rose-600" /></button>
            </span>
          ))}
          {texture && (
            <span className="inline-flex items-center gap-1 bg-brand-50 text-brand-900 border border-brand-200 px-2.5 py-1 rounded-full text-xs font-medium">
              Texture: {texture}
              <button onClick={() => updateParam("texture", "")}><X className="w-3 h-3 text-brand-600" /></button>
            </span>
          )}
          {inStock && (
            <span className="inline-flex items-center gap-1 bg-emerald-50 text-emerald-900 border border-emerald-200 px-2.5 py-1 rounded-full text-xs font-medium">
              In Stock Only
              <button onClick={() => updateParam("in_stock", "")}><X className="w-3 h-3 text-emerald-600" /></button>
            </span>
          )}

          {hasActiveFilters && (
            <button
              onClick={resetAllFilters}
              className="text-xs font-semibold text-brand-600 hover:text-brand-800 underline ml-1"
            >
              Clear all
            </button>
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
            <option value="popularity">Most Popular</option>
            <option value="price_asc">Price: Low to High</option>
            <option value="price_desc">Price: High to Low</option>
            <option value="rating">Highest Rated</option>
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
            selectedSubcategory={subcategory}
            selectedColors={selectedColors}
            selectedLengths={selectedLengths}
            selectedLengthGroup={lengthGroup}
            selectedOrigins={selectedOrigins}
            selectedHairType={hairType}
            selectedTexture={texture}
            inStockOnly={inStock}
            onSelectCategory={(val) => {
              updateParam("category", val);
              updateParam("subcategory", "");
            }}
            onSelectSubcategory={(val) => updateParam("subcategory", val)}
            onToggleColor={(col) => toggleArrayParam("color", selectedColors, col)}
            onToggleLength={(len) => toggleArrayParam("length_inches", selectedLengths, len)}
            onSelectLengthGroup={(grp) => updateParam("length_group", grp)}
            onToggleOrigin={(orig) => toggleArrayParam("hair_origin", selectedOrigins, orig)}
            onSelectHairType={(val) => updateParam("hair_type", val)}
            onSelectTexture={(val) => updateParam("texture", val)}
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
                Try removing some filters or search for another texture like "Bone Straight", "Deep Wave", or another length.
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
              selectedSubcategory={subcategory}
              selectedColors={selectedColors}
              selectedLengths={selectedLengths}
              selectedLengthGroup={lengthGroup}
              selectedOrigins={selectedOrigins}
              selectedHairType={hairType}
              selectedTexture={texture}
              inStockOnly={inStock}
              onSelectCategory={(val) => {
                updateParam("category", val);
                updateParam("subcategory", "");
                setMobileFilterOpen(false);
              }}
              onSelectSubcategory={(val) => {
                updateParam("subcategory", val);
                setMobileFilterOpen(false);
              }}
              onToggleColor={(col) => toggleArrayParam("color", selectedColors, col)}
              onToggleLength={(len) => toggleArrayParam("length_inches", selectedLengths, len)}
              onSelectLengthGroup={(grp) => {
                updateParam("length_group", grp);
                setMobileFilterOpen(false);
              }}
              onToggleOrigin={(orig) => toggleArrayParam("hair_origin", selectedOrigins, orig)}
              onSelectHairType={(val) => {
                updateParam("hair_type", val);
                setMobileFilterOpen(false);
              }}
              onSelectTexture={(val) => {
                updateParam("texture", val);
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
