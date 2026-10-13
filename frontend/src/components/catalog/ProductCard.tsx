"use client";

import React, { useState } from "react";
import Link from "next/link";
import { Heart, Star, ShoppingBag, Eye } from "lucide-react";
import { Product } from "@/types";
import { formatPrice, calculateDiscountPercent } from "@/lib/formatters";
import { useCart } from "@/context/CartContext";

interface ProductCardProps {
  product: Product;
}

export default function ProductCard({ product }: ProductCardProps) {
  const { addItem } = useCart();
  const [isWishlisted, setIsWishlisted] = useState(false);
  const [adding, setAdding] = useState(false);

  const discountPercent = calculateDiscountPercent(product.compare_at_price, product.min_price);
  const imageUrl = product.primary_image?.image_url || "/images/categories/bone-straight.jpg";

  const handleQuickAdd = async (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (product.variants && product.variants.length > 0) {
      setAdding(true);
      try {
        await addItem(product.variants[0].id, 1);
      } finally {
        setAdding(false);
      }
    }
  };

  const toggleWishlist = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsWishlisted(!isWishlisted);
  };

  return (
    <div className="group relative flex flex-col bg-white rounded-2xl overflow-hidden border border-neutral-100/80 hover:shadow-xl transition-all duration-300">
      {/* Product Image Frame */}
      <Link href={`/products/${product.slug}`} className="relative aspect-[3/4] bg-neutral-100 overflow-hidden block">
        <img
          src={imageUrl}
          alt={product.primary_image?.alt_text || product.name}
          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
          loading="lazy"
        />

        {/* Badges Overlay */}
        <div className="absolute top-2.5 left-2.5 flex flex-col gap-1.5 z-10">
          {product.is_best_seller && (
            <span className="bg-amber-400 text-neutral-900 text-[10px] font-extrabold uppercase px-2 py-0.5 rounded-full shadow-sm">
              Best Seller
            </span>
          )}
          {discountPercent && discountPercent > 0 && (
            <span className="bg-red-600 text-white text-[10px] font-extrabold uppercase px-2 py-0.5 rounded-full shadow-sm">
              -{discountPercent}% OFF
            </span>
          )}
          {product.is_new_arrival && (
            <span className="bg-brand-600 text-white text-[10px] font-extrabold uppercase px-2 py-0.5 rounded-full shadow-sm">
              New In
            </span>
          )}
          {product.hair_origin && product.hair_origin !== "unspecified" && (
            <span className="bg-neutral-900/80 backdrop-blur-md text-white text-[9px] font-semibold uppercase px-2 py-0.5 rounded-full shadow-sm">
              {product.hair_origin}
            </span>
          )}
        </div>

        {/* Wishlist Heart Icon */}
        <button
          onClick={toggleWishlist}
          className={`absolute top-2.5 right-2.5 p-2 rounded-full backdrop-blur-md transition z-10 ${
            isWishlisted
              ? "bg-rose-50 text-rose-600 shadow"
              : "bg-white/80 text-neutral-600 hover:text-rose-600 hover:bg-white shadow-sm"
          }`}
          aria-label="Save to wishlist"
        >
          <Heart className={`w-4 h-4 ${isWishlisted ? "fill-rose-600" : ""}`} />
        </button>

        {/* Quick Add Button on Hover (Desktop) */}
        <div className="absolute inset-x-3 bottom-3 opacity-0 group-hover:opacity-100 transition-opacity hidden sm:flex gap-2 z-10">
          <button
            onClick={handleQuickAdd}
            disabled={adding}
            className="flex-1 bg-white/95 hover:bg-brand-dark hover:text-white text-neutral-900 text-xs font-semibold py-2.5 rounded-xl shadow-lg transition flex items-center justify-center gap-1.5"
          >
            <ShoppingBag className="w-3.5 h-3.5" />
            <span>{adding ? "Adding..." : "Quick Add"}</span>
          </button>
        </div>
      </Link>

      {/* Content */}
      <div className="p-3.5 sm:p-4 flex-1 flex flex-col justify-between">
        <div>
          {/* Hair Origin & Texture Subtitle */}
          <div className="flex items-center justify-between text-[11px] text-neutral-500 mb-1">
            <span className="capitalize font-medium text-brand-600">
              {product.hair_origin && product.hair_origin !== "unspecified"
                ? `${product.hair_origin} Virgin`
                : `${product.hair_type} Hair`}
            </span>
            {product.texture && <span className="text-neutral-400">• {product.texture}</span>}
          </div>

          {/* Product Name */}
          <Link href={`/products/${product.slug}`}>
            <h3 className="text-xs sm:text-sm font-semibold text-neutral-900 group-hover:text-brand-600 transition line-clamp-2 leading-snug">
              {product.name}
            </h3>
          </Link>

          {/* Available Colors & Ratings */}
          <div className="flex items-center justify-between gap-2 mt-2">
            <div className="flex items-center gap-1 text-amber-400">
              <Star className="w-3 h-3 fill-amber-400 text-amber-400" />
              <span className="text-[11px] font-bold text-neutral-800">{product.average_rating || "5.0"}</span>
              <span className="text-[10px] text-neutral-400">({product.review_count || 12})</span>
            </div>

            {product.available_colors && product.available_colors.length > 1 && (
              <span className="text-[10px] bg-neutral-100 text-neutral-600 font-semibold px-1.5 py-0.5 rounded-md">
                {product.available_colors.length} Colors
              </span>
            )}
          </div>
        </div>

        {/* Price Row */}
        <div className="mt-3 pt-2.5 border-t border-neutral-100 flex items-baseline justify-between">
          <div className="flex items-baseline gap-2">
            <span className="text-sm sm:text-base font-extrabold text-neutral-900">
              {formatPrice(product.min_price)}
            </span>
            {product.compare_at_price && (
              <span className="text-xs text-neutral-400 line-through">
                {formatPrice(product.compare_at_price)}
              </span>
            )}
          </div>

          {/* Mobile Quick Add icon */}
          <button
            onClick={handleQuickAdd}
            disabled={adding}
            className="sm:hidden p-1.5 bg-neutral-100 hover:bg-brand-dark hover:text-white rounded-lg transition"
            aria-label="Quick add"
          >
            <ShoppingBag className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
}
