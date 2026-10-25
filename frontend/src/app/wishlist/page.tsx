"use client";

import React from "react";
import Link from "next/link";
import { useQuery } from "@tanstack/react-query";
import { Heart } from "lucide-react";
import { WishlistItem } from "@/types";
import { fetchApi } from "@/lib/api";
import ProductCard from "@/components/catalog/ProductCard";
import { useAuth } from "@/context/AuthContext";

export default function WishlistPage() {
  const { user, loading: authLoading } = useAuth();
  const { data: wishlist = [], isLoading } = useQuery<WishlistItem[]>({
    queryKey: ["wishlist"],
    queryFn: () => fetchApi("/wishlist/"),
    enabled: Boolean(user),
  });

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
      <div className="flex items-center justify-between pb-6 border-b border-neutral-200 mb-8">
        <div>
          <h1 className="font-serif text-2xl sm:text-3xl font-bold text-neutral-900 flex items-center gap-2">
            <Heart className="w-6 h-6 text-rose-500 fill-rose-500" />
            My Wishlist & Saved Wigs
          </h1>
          <p className="text-xs text-neutral-500 mt-1">Keep track of your favorite styles and easily move them to your bag.</p>
        </div>
      </div>

      {!authLoading && !user ? (
        <div className="text-center py-20 bg-neutral-50 rounded-3xl border border-neutral-200">
          <h2 className="font-serif text-xl font-bold text-neutral-900 mb-1">Sign in to see your saved wigs</h2>
          <p className="text-xs text-neutral-600 mb-6">Your wishlist is saved securely to your account.</p>
          <Link href="/account/login?next=/wishlist" className="bg-brand-dark text-white text-xs font-semibold px-6 py-3 rounded-full">Sign In</Link>
        </div>
      ) : isLoading || authLoading ? (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
          {[1, 2, 3, 4].map((n) => (
            <div key={n} className="aspect-[3/4] bg-neutral-100 rounded-2xl animate-pulse" />
          ))}
        </div>
      ) : wishlist.length === 0 ? (
        <div className="text-center py-20 bg-neutral-50 rounded-3xl border border-neutral-200">
          <Heart className="w-12 h-12 text-neutral-400 mx-auto mb-3" />
          <h2 className="font-serif text-xl font-bold text-neutral-900 mb-1">Your Wishlist is Empty</h2>
          <p className="text-xs text-neutral-500 mb-6">Explore our luxury wigs and tap the heart icon on any style you love.</p>
          <Link href="/shop" className="bg-brand-dark text-white text-xs font-semibold px-6 py-3 rounded-full">
            Explore Wigs
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 sm:gap-6">
          {wishlist.map((item) => (
            <ProductCard key={item.id} product={item.product_details} />
          ))}
        </div>
      )}
    </div>
  );
}
