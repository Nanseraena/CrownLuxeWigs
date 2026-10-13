"use client";

import React from "react";
import { Category } from "@/types";
import { RotateCcw, Check } from "lucide-react";

interface FilterSidebarProps {
  categories: Category[];
  selectedCategory: string;
  selectedHairType: string;
  selectedTexture: string;
  selectedLength: string;
  inStockOnly: boolean;
  onSelectCategory: (slug: string) => void;
  onSelectHairType: (type: string) => void;
  onSelectTexture: (texture: string) => void;
  onSelectLength: (length: string) => void;
  onToggleInStock: (val: boolean) => void;
  onResetFilters: () => void;
}

export default function FilterSidebar({
  categories,
  selectedCategory,
  selectedHairType,
  selectedTexture,
  selectedLength,
  inStockOnly,
  onSelectCategory,
  onSelectHairType,
  onSelectTexture,
  onSelectLength,
  onToggleInStock,
  onResetFilters,
}: FilterSidebarProps) {
  const textures = ["Bone Straight", "Deep Wave", "Body Wave", "Kinky Curly", "Straight Bob"];
  const lengths = ["10", "12", "18", "20", "22", "24", "26", "28", "30"];

  return (
    <aside className="space-y-6">
      {/* Header & Reset */}
      <div className="flex items-center justify-between pb-3 border-b border-neutral-200">
        <h3 className="font-bold text-sm text-neutral-900 tracking-wide uppercase">Filters</h3>
        <button
          onClick={onResetFilters}
          className="text-xs text-brand-600 hover:text-brand-800 flex items-center gap-1 font-semibold"
        >
          <RotateCcw className="w-3 h-3" />
          <span>Reset All</span>
        </button>
      </div>

      {/* In Stock Only Toggle */}
      <div className="bg-neutral-50 p-3 rounded-xl border border-neutral-200 flex items-center justify-between">
        <span className="text-xs font-semibold text-neutral-800">In-Stock Ready to Ship</span>
        <button
          type="button"
          onClick={() => onToggleInStock(!inStockOnly)}
          className={`w-10 h-6 flex items-center rounded-full p-1 transition duration-300 ${
            inStockOnly ? "bg-brand-600 justify-end" : "bg-neutral-300 justify-start"
          }`}
        >
          <div className="bg-white w-4 h-4 rounded-full shadow-md" />
        </button>
      </div>

      {/* Categories */}
      <div>
        <h4 className="text-xs font-bold uppercase tracking-wider text-neutral-500 mb-3">Categories</h4>
        <div className="space-y-1.5 max-h-56 overflow-y-auto no-scrollbar">
          <button
            onClick={() => onSelectCategory("")}
            className={`w-full text-left text-xs py-1.5 px-2 rounded-lg transition ${
              !selectedCategory ? "bg-brand-50 text-brand-800 font-bold" : "text-neutral-600 hover:bg-neutral-50"
            }`}
          >
            All Categories
          </button>
          {categories.map((cat) => (
            <button
              key={cat.id}
              onClick={() => onSelectCategory(cat.slug)}
              className={`w-full text-left text-xs py-1.5 px-2 rounded-lg transition ${
                selectedCategory === cat.slug ? "bg-brand-50 text-brand-800 font-bold" : "text-neutral-600 hover:bg-neutral-50"
              }`}
            >
              {cat.name}
            </button>
          ))}
        </div>
      </div>

      {/* Hair Textures */}
      <div>
        <h4 className="text-xs font-bold uppercase tracking-wider text-neutral-500 mb-3">Texture</h4>
        <div className="flex flex-wrap gap-1.5">
          {textures.map((tex) => {
            const isSelected = selectedTexture === tex;
            return (
              <button
                key={tex}
                onClick={() => onSelectTexture(isSelected ? "" : tex)}
                className={`text-xs px-2.5 py-1.5 rounded-lg border transition ${
                  isSelected
                    ? "border-brand-600 bg-brand-50 text-brand-800 font-bold"
                    : "border-neutral-200 bg-white text-neutral-600 hover:border-neutral-300"
                }`}
              >
                {tex}
              </button>
            );
          })}
        </div>
      </div>

      {/* Length in Inches */}
      <div>
        <h4 className="text-xs font-bold uppercase tracking-wider text-neutral-500 mb-3">Length (Inches)</h4>
        <div className="grid grid-cols-3 gap-1.5">
          {lengths.map((len) => {
            const isSelected = selectedLength === len;
            return (
              <button
                key={len}
                onClick={() => onSelectLength(isSelected ? "" : len)}
                className={`text-xs py-1.5 rounded-lg border text-center transition ${
                  isSelected
                    ? "border-brand-600 bg-brand-50 text-brand-800 font-bold"
                    : "border-neutral-200 bg-white text-neutral-600 hover:border-neutral-300"
                }`}
              >
                {len}"
              </button>
            );
          })}
        </div>
      </div>

      {/* Hair Type */}
      <div>
        <h4 className="text-xs font-bold uppercase tracking-wider text-neutral-500 mb-3">Hair Origin</h4>
        <div className="space-y-1 text-xs">
          {[
            { label: "100% Virgin Human Hair", value: "human" },
            { label: "Synthetic Fiber", value: "synthetic" },
            { label: "Human Hair Blend", value: "blend" },
          ].map((item) => (
            <label key={item.value} className="flex items-center gap-2 cursor-pointer py-1 text-neutral-700">
              <input
                type="radio"
                name="hair_type"
                checked={selectedHairType === item.value}
                onChange={() => onSelectHairType(selectedHairType === item.value ? "" : item.value)}
                className="text-brand-600 focus:ring-brand-500"
              />
              <span>{item.label}</span>
            </label>
          ))}
        </div>
      </div>
    </aside>
  );
}
