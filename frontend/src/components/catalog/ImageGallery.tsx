"use client";

import React, { useState } from "react";
import { ProductImage } from "@/types";

interface ImageGalleryProps {
  images: ProductImage[];
  productName: string;
}

export default function ImageGallery({ images, productName }: ImageGalleryProps) {
  const [activeIndex, setActiveIndex] = useState(0);

  const displayImages = images && images.length > 0 ? images : [
    {
      id: 0,
      image_url: "/images/wigs/catalog-placeholder.svg",
      alt_text: productName,
      is_primary: true,
      sort_order: 0,
    }
  ];

  const currentImage = displayImages[activeIndex] || displayImages[0];

  return (
    <div className="flex flex-col-reverse lg:flex-row gap-4">
      {/* Thumbnail Strip */}
      {displayImages.length > 1 && (
        <div className="flex lg:flex-col gap-3 overflow-x-auto no-scrollbar py-1 shrink-0">
          {displayImages.map((img, idx) => (
            <button
              key={img.id || idx}
              type="button"
              onClick={() => setActiveIndex(idx)}
              className={`w-16 h-20 sm:w-20 sm:h-24 rounded-xl overflow-hidden border-2 transition shrink-0 ${
                activeIndex === idx
                  ? "border-brand-600 ring-2 ring-brand-500/20 shadow-md"
                  : "border-neutral-200 opacity-70 hover:opacity-100 hover:border-neutral-400"
              }`}
            >
              <img
                src={img.image_url}
                alt={img.alt_text || `${productName} thumbnail ${idx + 1}`}
                className="w-full h-full object-cover"
              />
            </button>
          ))}
        </div>
      )}

      {/* Main Large Image */}
      <div className="flex-1 aspect-[3/4] bg-neutral-100 rounded-2xl overflow-hidden relative border border-neutral-100 shadow-sm">
        <img
          src={currentImage.image_url}
          alt={currentImage.alt_text || productName}
          className="w-full h-full object-cover"
        />
        <div className="absolute bottom-3 right-3 bg-black/50 backdrop-blur-md text-white text-[11px] px-2.5 py-1 rounded-full font-medium">
          {activeIndex + 1} / {displayImages.length}
        </div>
      </div>
    </div>
  );
}
