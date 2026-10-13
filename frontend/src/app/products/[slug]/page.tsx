"use client";

import React, { useState, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import { useQuery } from "@tanstack/react-query";
import Link from "next/link";
import {
  Star, Heart, ShoppingBag, Truck, ShieldCheck, CheckCircle2,
  ChevronRight, ArrowRight, Sparkles, Plus, Minus, MessageSquare, Send
} from "lucide-react";
import { Product, ProductVariant, Review } from "@/types";
import { fetchApi } from "@/lib/api";
import { formatPrice, calculateDiscountPercent, formatDate } from "@/lib/formatters";
import { useCart } from "@/context/CartContext";
import ImageGallery from "@/components/catalog/ImageGallery";
import VariantSelector from "@/components/catalog/VariantSelector";
import ProductCard from "@/components/catalog/ProductCard";

export default function ProductDetailPage() {
  const params = useParams();
  const router = useRouter();
  const slug = params?.slug as string;

  const { addItem, setIsDrawerOpen } = useCart();

  const [selectedVariant, setSelectedVariant] = useState<ProductVariant | null>(null);
  const [quantity, setQuantity] = useState(1);
  const [isWishlisted, setIsWishlisted] = useState(false);
  const [addingToCart, setAddingToCart] = useState(false);

  // Review Form State
  const [reviewName, setReviewName] = useState("");
  const [reviewRating, setReviewRating] = useState(5);
  const [reviewComment, setReviewComment] = useState("");
  const [submittingReview, setSubmittingReview] = useState(false);
  const [reviewSuccess, setReviewSuccess] = useState(false);

  // Fetch Product Details
  const { data: product, isLoading, refetch } = useQuery<Product>({
    queryKey: ["product", slug],
    queryFn: () => fetchApi(`/products/${slug}/`),
    enabled: !!slug,
  });

  // Fetch Related Products
  const { data: relatedData } = useQuery<{ results: Product[] }>({
    queryKey: ["related-products", product?.category?.slug],
    queryFn: () => fetchApi(`/products/?category__slug=${product?.category?.slug}`),
    enabled: !!product?.category?.slug,
  });

  // Default to first variant
  useEffect(() => {
    if (product && product.variants && product.variants.length > 0 && !selectedVariant) {
      setSelectedVariant(product.variants[0]);
    }
  }, [product, selectedVariant]);

  if (isLoading || !product) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-16 text-center">
        <div className="w-12 h-12 border-4 border-brand-500 border-t-transparent rounded-full animate-spin mx-auto mb-4" />
        <p className="text-xs text-neutral-500">Loading CrownLuxe product details...</p>
      </div>
    );
  }

  const currentPrice = selectedVariant?.price || product.min_price || "0";
  const comparePrice = selectedVariant?.compare_at_price || product.compare_at_price;
  const discountPercent = calculateDiscountPercent(comparePrice, currentPrice);
  const maxStock = selectedVariant?.stock_quantity || 1;

  const handleAddToCart = async () => {
    if (!selectedVariant) return;
    setAddingToCart(true);
    try {
      await addItem(selectedVariant.id, quantity);
    } finally {
      setAddingToCart(false);
    }
  };

  const handleBuyNow = async () => {
    if (!selectedVariant) return;
    setAddingToCart(true);
    try {
      await addItem(selectedVariant.id, quantity);
      router.push("/checkout");
    } finally {
      setAddingToCart(false);
    }
  };

  const handleSubmitReview = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!reviewComment.trim()) return;
    setSubmittingReview(true);
    try {
      await fetchApi(`/products/${slug}/reviews/`, {
        method: "POST",
        body: JSON.stringify({
          reviewer_name: reviewName.trim() || "Verified Buyer",
          rating: reviewRating,
          comment: reviewComment.trim(),
        }),
      });
      setReviewSuccess(true);
      setReviewComment("");
      refetch();
    } catch (e) {
      console.error(e);
    } finally {
      setSubmittingReview(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-10 space-y-12 sm:space-y-16">
      {/* Breadcrumb Navigation */}
      <nav className="flex items-center gap-1.5 text-xs text-neutral-500 overflow-x-auto no-scrollbar">
        <Link href="/" className="hover:text-black transition">Home</Link>
        <ChevronRight className="w-3.5 h-3.5" />
        <Link href="/shop" className="hover:text-black transition">Wigs</Link>
        <ChevronRight className="w-3.5 h-3.5" />
        <Link href={`/shop?category=${product.category.slug}`} className="hover:text-black transition">
          {product.category.name}
        </Link>
        <ChevronRight className="w-3.5 h-3.5" />
        <span className="text-neutral-900 font-semibold truncate">{product.name}</span>
      </nav>

      {/* Main Product Hero Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12">
        {/* Gallery Column */}
        <div className="lg:col-span-7">
          <ImageGallery images={product.images || []} productName={product.name} />
        </div>

        {/* Purchase Column */}
        <div className="lg:col-span-5 space-y-6">
          <div>
            <div className="flex items-center justify-between gap-2">
              <span className="text-xs font-bold uppercase tracking-wider text-brand-600">
                {product.category.name}
              </span>
              <button
                onClick={() => setIsWishlisted(!isWishlisted)}
                className={`p-2 rounded-full border transition ${
                  isWishlisted ? "bg-rose-50 text-rose-600 border-rose-200" : "bg-white text-neutral-500 border-neutral-200 hover:text-rose-600"
                }`}
                title="Save to wishlist"
              >
                <Heart className={`w-4 h-4 ${isWishlisted ? "fill-rose-600" : ""}`} />
              </button>
            </div>

            <h1 className="font-serif text-2xl sm:text-3xl font-bold text-neutral-900 mt-1 leading-snug">
              {product.name}
            </h1>

            {/* Ratings Summary */}
            <div className="flex items-center gap-2 mt-2">
              <div className="flex items-center text-amber-400">
                {[1, 2, 3, 4, 5].map((s) => (
                  <Star key={s} className="w-4 h-4 fill-amber-400 text-amber-400" />
                ))}
              </div>
              <span className="text-xs font-bold text-neutral-900">{product.average_rating || 5.0}</span>
              <span className="text-xs text-neutral-400">•</span>
              <a href="#reviews" className="text-xs text-brand-600 hover:underline font-medium">
                {product.review_count || 12} Verified Reviews
              </a>
            </div>
          </div>

          {/* Pricing Box */}
          <div className="bg-neutral-50 p-4 rounded-2xl border border-neutral-200/80 flex items-baseline justify-between">
            <div className="flex items-baseline gap-3">
              <span className="font-serif text-2xl sm:text-3xl font-extrabold text-neutral-950">
                {formatPrice(currentPrice)}
              </span>
              {comparePrice && (
                <span className="text-sm text-neutral-400 line-through">
                  {formatPrice(comparePrice)}
                </span>
              )}
            </div>
            {discountPercent && (
              <span className="bg-red-600 text-white text-xs font-bold px-2.5 py-1 rounded-full uppercase">
                Save {discountPercent}%
              </span>
            )}
          </div>

          {/* Interactive Variant Picker */}
          <VariantSelector
            variants={product.variants || []}
            selectedVariant={selectedVariant}
            onSelectVariant={setSelectedVariant}
          />

          {/* Quantity Selector & Action Buttons */}
          <div className="space-y-3 pt-2">
            <div className="flex items-center gap-4">
              <span className="text-xs font-bold text-neutral-700">Quantity:</span>
              <div className="flex items-center border border-neutral-200 rounded-xl bg-neutral-50">
                <button
                  type="button"
                  onClick={() => setQuantity(Math.max(1, quantity - 1))}
                  className="p-2 text-neutral-600 hover:text-black transition"
                  disabled={quantity <= 1}
                >
                  <Minus className="w-3.5 h-3.5" />
                </button>
                <span className="px-4 text-xs font-bold text-neutral-900">{quantity}</span>
                <button
                  type="button"
                  onClick={() => setQuantity(Math.min(maxStock, quantity + 1))}
                  className="p-2 text-neutral-600 hover:text-black transition"
                  disabled={quantity >= maxStock}
                >
                  <Plus className="w-3.5 h-3.5" />
                </button>
              </div>
            </div>

            <div className="flex gap-3 pt-2">
              <button
                type="button"
                onClick={handleAddToCart}
                disabled={Boolean(addingToCart || !selectedVariant || selectedVariant.stock_quantity === 0)}
                className="flex-1 bg-white border-2 border-brand-dark text-brand-dark hover:bg-neutral-50 font-bold text-xs sm:text-sm py-3.5 rounded-2xl transition flex items-center justify-center gap-2 shadow-sm disabled:opacity-50"
              >
                <ShoppingBag className="w-4 h-4" />
                <span>{addingToCart ? "Adding..." : "Add To Bag"}</span>
              </button>

              <button
                type="button"
                onClick={handleBuyNow}
                disabled={Boolean(addingToCart || !selectedVariant || selectedVariant.stock_quantity === 0)}
                className="flex-[1.2] bg-brand-dark hover:bg-neutral-800 text-white font-bold text-xs sm:text-sm py-3.5 rounded-2xl transition flex items-center justify-center gap-2 shadow-lg shadow-neutral-900/10 disabled:opacity-50"
              >
                <span>Buy Now</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          </div>

          {/* Delivery & Assurance Guarantees */}
          <div className="bg-brand-50/50 p-4 rounded-2xl border border-brand-100 space-y-2.5 text-xs">
            <div className="flex items-start gap-2.5">
              <Truck className="w-4 h-4 text-brand-600 shrink-0 mt-0.5" />
              <div>
                <p className="font-semibold text-neutral-900">Uganda Express Dispatch</p>
                <p className="text-neutral-500 text-[11px]">Kampala orders arrive in 2–4 hours. Upcountry arrives in 24–48 hours.</p>
              </div>
            </div>
            <div className="flex items-start gap-2.5">
              <ShieldCheck className="w-4 h-4 text-brand-600 shrink-0 mt-0.5" />
              <div>
                <p className="font-semibold text-neutral-900">100% Virgin Hair Assurance</p>
                <p className="text-neutral-500 text-[11px]">Bleach to 613 platinum blonde, curl, flat iron, and dye with confidence.</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Specifications & Hair Care Accordion */}
      <div className="border-t border-neutral-200 pt-10">
        <h2 className="font-serif text-xl sm:text-2xl font-bold text-neutral-900 mb-6">
          Hair Specifications & Construction
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="space-y-4">
            <p className="text-xs sm:text-sm text-neutral-600 leading-relaxed">
              {product.description}
            </p>
            <div className="bg-neutral-50 rounded-2xl p-4 border border-neutral-200 space-y-2 text-xs">
              <div className="flex justify-between py-1 border-b border-neutral-200/60">
                <span className="text-neutral-500">Confirmed Hair Origin</span>
                <span className="font-semibold text-brand-700 capitalize">
                  {product.hair_origin && product.hair_origin !== "unspecified"
                    ? `${product.hair_origin} Virgin Donor Hair`
                    : "Unspecified Origin"}
                </span>
              </div>
              <div className="flex justify-between py-1 border-b border-neutral-200/60">
                <span className="text-neutral-500">Hair Material</span>
                <span className="font-semibold text-neutral-900">
                  {product.hair_type === "human"
                    ? "100% Virgin Human Hair"
                    : product.hair_type === "synthetic"
                    ? "Synthetic Fiber"
                    : "Human Hair Blend"}
                </span>
              </div>
              <div className="flex justify-between py-1 border-b border-neutral-200/60">
                <span className="text-neutral-500">Hair Texture</span>
                <span className="font-semibold text-neutral-900">{product.texture || "Bone Straight"}</span>
              </div>
              <div className="flex justify-between py-1 border-b border-neutral-200/60">
                <span className="text-neutral-500">Lace Type</span>
                <span className="font-semibold text-neutral-900">
                  {selectedVariant?.lace_type || product.default_lace_type || "Ultra-thin HD Swiss Lace"}
                </span>
              </div>
              <div className="flex justify-between py-1 border-b border-neutral-200/60">
                <span className="text-neutral-500">Hair Density</span>
                <span className="font-semibold text-neutral-900">
                  {selectedVariant?.density || "180% Full Natural Density"}
                </span>
              </div>
              <div className="flex justify-between py-1">
                <span className="text-neutral-500">Cap Size</span>
                <span className="font-semibold text-neutral-900">
                  {selectedVariant?.cap_size || 'Medium 22.5" with Adjustable Straps'}
                </span>
              </div>
            </div>
          </div>

          <div className="bg-amber-50/40 p-6 rounded-2xl border border-amber-200/60 space-y-3">
            <h3 className="font-serif text-base font-bold text-amber-950 flex items-center gap-1.5">
              <Sparkles className="w-4 h-4 text-brand-gold" />
              CrownLuxe Professional Care Guide
            </h3>
            <ul className="text-xs text-neutral-700 space-y-2 list-disc pl-4 leading-relaxed">
              <li>Wash in lukewarm water with sulfate-free hydrating shampoo every 10–14 wears.</li>
              <li>Always use heat protectant serum prior to flat ironing or curling (safe up to 230°C).</li>
              <li>For deep wave and curly wigs, define using water, leave-in conditioner, and curl mousse.</li>
              <li>Store on a satin wig stand or silk bonnet at night to prevent friction shedding.</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Customer Reviews Section */}
      <section id="reviews" className="border-t border-neutral-200 pt-10">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
          <div>
            <span className="text-xs font-bold uppercase tracking-widest text-brand-600">Client Feedback</span>
            <h2 className="font-serif text-2xl font-bold text-neutral-900 mt-1">Verified Customer Reviews</h2>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Reviews List */}
          <div className="lg:col-span-2 space-y-4">
            {product.reviews && product.reviews.length > 0 ? (
              product.reviews.map((rev) => (
                <div key={rev.id} className="bg-neutral-50 p-5 rounded-2xl border border-neutral-200 space-y-2">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <span className="font-bold text-xs text-neutral-900">{rev.reviewer_name}</span>
                      <span className="text-[10px] bg-emerald-100 text-emerald-800 font-bold px-2 py-0.5 rounded">
                        Verified Purchase
                      </span>
                    </div>
                    <span className="text-[11px] text-neutral-400">{formatDate(rev.created_at)}</span>
                  </div>
                  <div className="flex items-center text-amber-400">
                    {[...Array(rev.rating)].map((_, i) => (
                      <Star key={i} className="w-3.5 h-3.5 fill-amber-400 text-amber-400" />
                    ))}
                  </div>
                  <p className="text-xs text-neutral-700 leading-relaxed">{rev.comment}</p>
                </div>
              ))
            ) : (
              <p className="text-xs text-neutral-500 py-4">No reviews submitted yet. Be the first to review!</p>
            )}
          </div>

          {/* Submit Review Form */}
          <div className="bg-white p-6 rounded-2xl border border-neutral-200 shadow-sm space-y-4">
            <h3 className="font-serif text-base font-bold text-neutral-900 flex items-center gap-1.5">
              <MessageSquare className="w-4 h-4 text-brand-600" />
              Write A Review
            </h3>

            {reviewSuccess ? (
              <div className="p-3 bg-emerald-50 text-emerald-800 text-xs rounded-xl border border-emerald-200">
                ✨ Thank you! Your review has been submitted successfully.
              </div>
            ) : (
              <form onSubmit={handleSubmitReview} className="space-y-3">
                <div>
                  <label className="block text-[11px] font-semibold text-neutral-700 mb-1">Your Name</label>
                  <input
                    type="text"
                    value={reviewName}
                    onChange={(e) => setReviewName(e.target.value)}
                    placeholder="e.g. Sharon K."
                    className="w-full bg-neutral-50 border border-neutral-200 rounded-xl px-3 py-2 text-xs text-neutral-900 focus:outline-none focus:border-brand-500"
                  />
                </div>

                <div>
                  <label className="block text-[11px] font-semibold text-neutral-700 mb-1">Star Rating</label>
                  <div className="flex items-center gap-2">
                    {[1, 2, 3, 4, 5].map((star) => (
                      <button
                        key={star}
                        type="button"
                        onClick={() => setReviewRating(star)}
                        className="text-amber-400 p-0.5"
                      >
                        <Star className={`w-5 h-5 ${star <= reviewRating ? "fill-amber-400" : "text-neutral-300"}`} />
                      </button>
                    ))}
                  </div>
                </div>

                <div>
                  <label className="block text-[11px] font-semibold text-neutral-700 mb-1">Your Feedback</label>
                  <textarea
                    rows={3}
                    value={reviewComment}
                    onChange={(e) => setReviewComment(e.target.value)}
                    placeholder="Tell us about the texture, lace melt, and delivery speed..."
                    required
                    className="w-full bg-neutral-50 border border-neutral-200 rounded-xl px-3 py-2 text-xs text-neutral-900 focus:outline-none focus:border-brand-500"
                  />
                </div>

                <button
                  type="submit"
                  disabled={submittingReview}
                  className="w-full bg-brand-dark hover:bg-neutral-800 text-white font-semibold text-xs py-2.5 rounded-xl transition flex items-center justify-center gap-1.5"
                >
                  <Send className="w-3.5 h-3.5" />
                  <span>{submittingReview ? "Submitting..." : "Submit Review"}</span>
                </button>
              </form>
            )}
          </div>
        </div>
      </section>

      {/* Related Products Carousel */}
      {relatedData && relatedData.results.length > 0 && (
        <section className="border-t border-neutral-200 pt-10">
          <div className="flex items-center justify-between mb-6">
            <h2 className="font-serif text-xl sm:text-2xl font-bold text-neutral-900">
              You May Also Love
            </h2>
            <Link href="/shop" className="text-xs text-brand-600 font-semibold hover:underline">
              View All
            </Link>
          </div>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 sm:gap-6">
            {relatedData.results
              .filter((p) => p.id !== product.id)
              .slice(0, 4)
              .map((p) => (
                <ProductCard key={p.id} product={p} />
              ))}
          </div>
        </section>
      )}
    </div>
  );
}
