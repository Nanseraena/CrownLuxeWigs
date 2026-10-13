"use client";

import React, { useMemo } from "react";
import { ProductVariant } from "@/types";
import { Check, ShieldAlert, CheckCircle2 } from "lucide-react";
import { formatPrice } from "@/lib/formatters";

interface VariantSelectorProps {
  variants: ProductVariant[];
  selectedVariant: ProductVariant | null;
  onSelectVariant: (variant: ProductVariant) => void;
}

export default function VariantSelector({
  variants,
  selectedVariant,
  onSelectVariant,
}: VariantSelectorProps) {
  if (!variants || variants.length === 0) return null;

  // Extract unique lengths and colors available
  const availableLengths = useMemo(() => {
    const set = new Set<number>();
    variants.forEach((v) => {
      if (v.length_inches) set.add(v.length_inches);
    });
    return Array.from(set).sort((a, b) => a - b);
  }, [variants]);

  const availableColors = useMemo(() => {
    const set = new Set<string>();
    variants.forEach((v) => {
      if (v.color) set.add(v.color);
    });
    return Array.from(set);
  }, [variants]);

  const handleLengthClick = (length: number) => {
    const match = variants.find((v) => v.length_inches === length && (selectedVariant?.color ? v.color === selectedVariant.color : true)) ||
                  variants.find((v) => v.length_inches === length);
    if (match) onSelectVariant(match);
  };

  const handleColorClick = (color: string) => {
    const match = variants.find((v) => v.color === color && (selectedVariant?.length_inches ? v.length_inches === selectedVariant.length_inches : true)) ||
                  variants.find((v) => v.color === color);
    if (match) onSelectVariant(match);
  };

  return (
    <div className="space-y-5 py-4 border-y border-neutral-100">
      {/* Length Picker */}
      {availableLengths.length > 0 && (
        <div>
          <div className="flex items-center justify-between text-xs mb-2.5">
            <span className="font-bold text-neutral-800">
              Hair Length: <span className="text-brand-600 font-extrabold">{selectedVariant?.length_inches || availableLengths[0]}"</span>
            </span>
            <span className="text-neutral-400 text-[11px]">True to Length Guarantee</span>
          </div>

          <div className="flex flex-wrap gap-2">
            {availableLengths.map((len) => {
              const isSelected = selectedVariant?.length_inches === len;
              const hasStock = variants.some((v) => v.length_inches === len && v.stock_quantity > 0);

              return (
                <button
                  key={len}
                  type="button"
                  onClick={() => handleLengthClick(len)}
                  className={`px-3.5 py-2 rounded-xl text-xs font-semibold transition border ${
                    isSelected
                      ? "border-brand-600 bg-brand-50 text-brand-900 shadow-sm"
                      : "border-neutral-200 bg-white text-neutral-700 hover:border-neutral-400"
                  } ${!hasStock ? "opacity-40 cursor-not-allowed line-through" : ""}`}
                >
                  {len}" Inch
                </button>
              );
            })}
          </div>
        </div>
      )}

      {/* Color Picker */}
      {availableColors.length > 0 && (
        <div>
          <div className="flex items-center justify-between text-xs mb-2.5">
            <span className="font-bold text-neutral-800">
              Hair Color: <span className="text-brand-600 font-extrabold">{selectedVariant?.color || availableColors[0]}</span>
            </span>
          </div>

          <div className="flex flex-wrap gap-2">
            {availableColors.map((color) => {
              const isSelected = selectedVariant?.color === color;

              return (
                <button
                  key={color}
                  type="button"
                  onClick={() => handleColorClick(color)}
                  className={`px-3.5 py-2 rounded-xl text-xs font-semibold transition border flex items-center gap-1.5 ${
                    isSelected
                      ? "border-brand-600 bg-brand-50 text-brand-900 shadow-sm"
                      : "border-neutral-200 bg-white text-neutral-700 hover:border-neutral-400"
                  }`}
                >
                  {isSelected && <Check className="w-3.5 h-3.5 text-brand-600" />}
                  <span>{color}</span>
                </button>
              );
            })}
          </div>
        </div>
      )}

      {/* Stock Availability Callout */}
      {selectedVariant && (
        <div className="pt-1 flex items-center justify-between text-xs">
          <div className="flex items-center gap-1.5">
            {selectedVariant.stock_quantity > 5 ? (
              <span className="text-emerald-700 font-semibold flex items-center gap-1">
                <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                In Stock — Ships Today from Kampala
              </span>
            ) : selectedVariant.stock_quantity > 0 ? (
              <span className="text-amber-700 font-semibold flex items-center gap-1">
                <ShieldAlert className="w-4 h-4 text-amber-600" />
                Hurry! Only {selectedVariant.stock_quantity} unit(s) left in stock
              </span>
            ) : (
              <span className="text-red-600 font-semibold">Out of Stock</span>
            )}
          </div>
          <span className="text-[11px] text-neutral-400">SKU: {selectedVariant.sku}</span>
        </div>
      )}
    </div>
  );
}
