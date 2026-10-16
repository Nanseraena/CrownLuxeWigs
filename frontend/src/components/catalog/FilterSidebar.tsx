"use client";

import React, { useState } from "react";
import { Category, Subcategory } from "@/types";
import { RotateCcw, Check, ChevronDown, ChevronRight, Sparkles } from "lucide-react";

export interface FilterSidebarProps {
  categories: Category[];
  selectedCategory: string;
  selectedSubcategory?: string;
  selectedCollection?: string;
  selectedColors: string[];
  selectedLengths: string[];
  selectedLengthGroup?: string;
  selectedOrigins: string[];
  selectedHairType: string;
  selectedTexture: string;
  selectedProductType: string;
  selectedStyle: string;
  selectedConstruction: string;
  inStockOnly: boolean;
  onSelectCategory: (slug: string) => void;
  onSelectSubcategory?: (slug: string) => void;
  onToggleColor: (color: string) => void;
  onToggleLength: (length: string) => void;
  onSelectLengthGroup?: (group: string) => void;
  onToggleOrigin: (origin: string) => void;
  onSelectHairType: (type: string) => void;
  onSelectTexture: (texture: string) => void;
  onSelectProductType: (type: string) => void;
  onSelectStyle: (style: string) => void;
  onSelectConstruction: (construction: string) => void;
  onToggleInStock: (val: boolean) => void;
  onResetFilters: () => void;
}

const COLOR_SWATCHES: Record<string, { bg: string; textDark?: boolean }> = {
  "Natural Black": { bg: "#1B1B1B" },
  "Jet Black": { bg: "#0A0A0A" },
  "Natural Brown": { bg: "#4A3728" },
  "Chocolate Brown": { bg: "#3B2219" },
  "Honey Blonde": { bg: "#D4A359", textDark: true },
  "Platinum Blonde": { bg: "#E8DFB8", textDark: true },
  "Burgundy": { bg: "#5B1426" },
  "Ginger": { bg: "#B25329" },
  "Copper": { bg: "#C45E32" },
  "Piano Highlights": { bg: "linear-gradient(135deg, #2B1810 25%, #E5A93C 25%, #E5A93C 50%, #2B1810 50%, #2B1810 75%, #E5A93C 75%)", textDark: true },
  "Ombre": { bg: "linear-gradient(to bottom, #111111 35%, #D4A359 100%)", textDark: true },
};

const LENGTH_GROUPS = [
  { label: "Short (10\"–14\")", value: "short" },
  { label: "Medium (16\"–20\")", value: "medium" },
  { label: "Long (22\"–26\")", value: "long" },
  { label: "Extra Long (28\"–36\")", value: "extra_long" },
];

const ALL_LENGTHS = ["10", "12", "14", "16", "18", "20", "22", "24", "26", "28", "30", "32"];

const HAIR_ORIGINS = [
  { label: "Brazilian", value: "brazilian" },
  { label: "Peruvian", value: "peruvian" },
  { label: "Malaysian", value: "malaysian" },
  { label: "Indian", value: "indian" },
  { label: "Vietnamese", value: "vietnamese" },
  { label: "Cambodian", value: "cambodian" },
  { label: "Other", value: "other" },
  { label: "Unspecified", value: "unspecified" },
];

const TEXTURES = [
  "Bone Straight",
  "Deep Wave",
  "Water Wave",
  "Body Wave",
  "Loose Wave",
  "Kinky Curly",
  "Silky Straight",
  "Yaki Straight",
  "Straight Bob",
];

export default function FilterSidebar({
  categories,
  selectedCategory,
  selectedSubcategory = "",
  selectedCollection = "",
  selectedColors,
  selectedLengths,
  selectedLengthGroup = "",
  selectedOrigins,
  selectedHairType,
  selectedTexture,
  selectedProductType,
  selectedStyle,
  selectedConstruction,
  inStockOnly,
  onSelectCategory,
  onSelectSubcategory,
  onToggleColor,
  onToggleLength,
  onSelectLengthGroup,
  onToggleOrigin,
  onSelectHairType,
  onSelectTexture,
  onSelectProductType,
  onSelectStyle,
  onSelectConstruction,
  onToggleInStock,
  onResetFilters,
}: FilterSidebarProps) {
  const [expandedCategories, setExpandedCategories] = useState<Record<string, boolean>>({});

  const toggleExpandCat = (slug: string) => {
    setExpandedCategories((prev) => ({ ...prev, [slug]: !prev[slug] }));
  };

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
          aria-label="Toggle in stock filter"
        >
          <div className="bg-white w-4 h-4 rounded-full shadow-md" />
        </button>
      </div>

      {/* 1. COLOR FILTER (Labeled Swatches) */}
      <div>
        <div className="flex items-center justify-between mb-3">
          <h4 className="text-xs font-bold uppercase tracking-wider text-neutral-900">
            Hair Color
          </h4>
          {selectedColors.length > 0 && (
            <span className="text-[10px] font-bold text-brand-600">
              {selectedColors.length} selected
            </span>
          )}
        </div>
        <div className="grid grid-cols-2 gap-2">
          {Object.entries(COLOR_SWATCHES).map(([colorName, style]) => {
            const isSelected = selectedColors.includes(colorName);
            return (
              <button
                key={colorName}
                type="button"
                onClick={() => onToggleColor(colorName)}
                className={`flex items-center gap-2 p-1.5 rounded-xl border text-left transition text-xs ${
                  isSelected
                    ? "border-brand-600 bg-brand-50/70 shadow-sm"
                    : "border-neutral-200 bg-white hover:border-neutral-300"
                }`}
              >
                <div
                  className="w-5 h-5 rounded-full border border-neutral-300 shadow-inner flex items-center justify-center shrink-0"
                  style={{ background: style.bg }}
                >
                  {isSelected && (
                    <Check
                      className={`w-3 h-3 ${style.textDark ? "text-neutral-900" : "text-white"}`}
                    />
                  )}
                </div>
                <span className={`text-[11px] leading-tight truncate ${isSelected ? "font-bold text-brand-900" : "text-neutral-700"}`}>
                  {colorName}
                </span>
              </button>
            );
          })}
        </div>
      </div>

      {/* 2. LENGTH IN INCHES */}
      <div>
        <div className="flex items-center justify-between mb-2.5">
          <h4 className="text-xs font-bold uppercase tracking-wider text-neutral-900">
            Length (Inches)
          </h4>
          {selectedLengths.length > 0 && (
            <span className="text-[10px] font-bold text-brand-600">
              {selectedLengths.length} selected
            </span>
          )}
        </div>

        {/* Quick Length Groups */}
        <div className="grid grid-cols-2 gap-1.5 mb-2.5">
          {LENGTH_GROUPS.map((grp) => {
            const isGrpSelected = selectedLengthGroup === grp.value;
            return (
              <button
                key={grp.value}
                type="button"
                onClick={() => onSelectLengthGroup && onSelectLengthGroup(isGrpSelected ? "" : grp.value)}
                className={`text-[11px] py-1 px-2 rounded-lg border text-center transition font-medium ${
                  isGrpSelected
                    ? "border-brand-600 bg-brand-50 text-brand-900 font-bold shadow-sm"
                    : "border-neutral-200 bg-white text-neutral-600 hover:border-neutral-300"
                }`}
              >
                {grp.label}
              </button>
            );
          })}
        </div>

        {/* Individual Length Pills */}
        <div className="grid grid-cols-4 gap-1.5">
          {ALL_LENGTHS.map((len) => {
            const isSelected = selectedLengths.includes(len);
            return (
              <button
                key={len}
                type="button"
                onClick={() => onToggleLength(len)}
                className={`text-xs py-1.5 rounded-lg border text-center transition ${
                  isSelected
                    ? "border-brand-600 bg-brand-600 text-white font-bold shadow-sm"
                    : "border-neutral-200 bg-white text-neutral-700 hover:border-neutral-300"
                }`}
              >
                {len}"
              </button>
            );
          })}
        </div>
      </div>

      {/* 3. HAIR ORIGIN */}
      <div>
        <div className="flex items-center justify-between mb-2.5">
          <h4 className="text-xs font-bold uppercase tracking-wider text-neutral-900">
            Confirmed Hair Origin
          </h4>
          {selectedOrigins.length > 0 && (
            <span className="text-[10px] font-bold text-brand-600">
              {selectedOrigins.length} selected
            </span>
          )}
        </div>
        <div className="space-y-1.5 text-xs">
          {HAIR_ORIGINS.map((origin) => {
            const isSelected = selectedOrigins.includes(origin.value);
            return (
              <label
                key={origin.value}
                className="flex items-center gap-2.5 cursor-pointer py-1 px-2 rounded-lg hover:bg-neutral-50 transition text-neutral-700 select-none"
              >
                <input
                  type="checkbox"
                  checked={isSelected}
                  onChange={() => onToggleOrigin(origin.value)}
                  className="rounded border-neutral-300 text-brand-600 focus:ring-brand-500 w-3.5 h-3.5"
                />
                <span className={isSelected ? "font-bold text-neutral-900" : "text-neutral-700"}>
                  {origin.label}
                </span>
              </label>
            );
          })}
        </div>
      </div>

      {/* 4. CATEGORIES & SUBCATEGORIES */}
      <div>
        <h4 className="text-xs font-bold uppercase tracking-wider text-neutral-900 mb-2.5">
          Categories
        </h4>
        <div className="space-y-1 max-h-64 overflow-y-auto no-scrollbar text-xs">
          <button
            type="button"
            onClick={() => onSelectCategory("")}
            className={`w-full text-left py-1.5 px-2.5 rounded-lg transition ${
              !selectedCategory ? "bg-brand-50 text-brand-800 font-bold" : "text-neutral-600 hover:bg-neutral-50"
            }`}
          >
            All Categories
          </button>
          {categories.map((cat) => {
            const isCatActive = selectedCategory === cat.slug;
            const hasSubcats = cat.subcategories && cat.subcategories.length > 0;
            const isExpanded = expandedCategories[cat.slug] ?? isCatActive;

            return (
              <div key={cat.id} className="space-y-0.5">
                <div className="flex items-center justify-between">
                  <button
                    type="button"
                    onClick={() => onSelectCategory(cat.slug)}
                    className={`flex-1 text-left py-1.5 px-2.5 rounded-lg transition ${
                      isCatActive ? "bg-brand-50 text-brand-800 font-bold" : "text-neutral-700 hover:bg-neutral-50"
                    }`}
                  >
                    {cat.name}
                  </button>
                  {hasSubcats && (
                    <button
                      type="button"
                      onClick={() => toggleExpandCat(cat.slug)}
                      className="p-1.5 text-neutral-400 hover:text-neutral-600 transition"
                      aria-label="Expand subcategories"
                    >
                      {isExpanded ? <ChevronDown className="w-3.5 h-3.5" /> : <ChevronRight className="w-3.5 h-3.5" />}
                    </button>
                  )}
                </div>

                {hasSubcats && isExpanded && (
                  <div className="pl-4 border-l border-neutral-200 ml-3 space-y-0.5 py-0.5">
                    {cat.subcategories?.map((sub: Subcategory) => {
                      const isSubActive = selectedSubcategory === sub.slug;
                      return (
                        <button
                          key={sub.id}
                          type="button"
                          onClick={() => onSelectSubcategory && onSelectSubcategory(sub.slug)}
                          className={`w-full text-left py-1 px-2 rounded-md text-[11px] transition ${
                            isSubActive
                              ? "bg-brand-100 text-brand-900 font-bold"
                              : "text-neutral-500 hover:text-neutral-900 hover:bg-neutral-50"
                          }`}
                        >
                          {sub.name}
                        </button>
                      );
                    })}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* 5. TEXTURE */}
      <div>
        <h4 className="text-xs font-bold uppercase tracking-wider text-neutral-900 mb-2.5">
          Hair Texture
        </h4>
        <div className="flex flex-wrap gap-1.5">
          {TEXTURES.map((tex) => {
            const isSelected = selectedTexture === tex;
            return (
              <button
                key={tex}
                type="button"
                onClick={() => onSelectTexture(isSelected ? "" : tex)}
                className={`text-[11px] px-2.5 py-1.5 rounded-lg border transition ${
                  isSelected
                    ? "border-brand-600 bg-brand-50 text-brand-800 font-bold shadow-sm"
                    : "border-neutral-200 bg-white text-neutral-600 hover:border-neutral-300"
                }`}
              >
                {tex}
              </button>
            );
          })}
        </div>
      </div>

      {/* 6. HAIR MATERIAL */}
      <div>
        <h4 className="text-xs font-bold uppercase tracking-wider text-neutral-900 mb-2.5">Product Type</h4>
        <div className="flex flex-wrap gap-1.5">
          {[['wig', 'Complete Wigs'], ['bundles', 'Hair Bundles'], ['clip_in', 'Clip-In Extensions'], ['tape_in', 'Tape-In Extensions'], ['closure_piece', 'Closures'], ['frontal_piece', 'Frontals']].map(([value, label]) => (
            <button key={value} type="button" onClick={() => onSelectProductType(selectedProductType === value ? "" : value)} className={`text-[11px] px-2.5 py-1.5 rounded-lg border ${selectedProductType === value ? "border-brand-600 bg-brand-50 text-brand-800 font-bold" : "border-neutral-200 text-neutral-600"}`}>{label}</button>
          ))}
        </div>
      </div>

      <div>
        <h4 className="text-xs font-bold uppercase tracking-wider text-neutral-900 mb-2.5">Wig Style</h4>
        <div className="flex flex-wrap gap-1.5">
          {[['bob', 'Bob'], ['long', 'Long'], ['layered', 'Layered'], ['bangs', 'Bangs'], ['asymmetrical', 'Asymmetrical'], ['pixie', 'Pixie']].map(([value, label]) => (
            <button key={value} type="button" onClick={() => onSelectStyle(selectedStyle === value ? "" : value)} className={`text-[11px] px-2.5 py-1.5 rounded-lg border ${selectedStyle === value ? "border-brand-600 bg-brand-50 text-brand-800 font-bold" : "border-neutral-200 text-neutral-600"}`}>{label}</button>
          ))}
        </div>
      </div>

      <div>
        <h4 className="text-xs font-bold uppercase tracking-wider text-neutral-900 mb-2.5">Construction</h4>
        <div className="flex flex-wrap gap-1.5">
          {[['lace_front', 'Lace Front'], ['closure', 'Closure'], ['glueless', 'Glueless'], ['full_lace', 'Full Lace'], ['headband', 'Headband']].map(([value, label]) => (
            <button key={value} type="button" onClick={() => onSelectConstruction(selectedConstruction === value ? "" : value)} className={`text-[11px] px-2.5 py-1.5 rounded-lg border ${selectedConstruction === value ? "border-brand-600 bg-brand-50 text-brand-800 font-bold" : "border-neutral-200 text-neutral-600"}`}>{label}</button>
          ))}
        </div>
      </div>

      {/* 6. HAIR MATERIAL */}
      <div>
        <h4 className="text-xs font-bold uppercase tracking-wider text-neutral-900 mb-2.5">
          Hair Material
        </h4>
        <div className="space-y-1 text-xs">
          {[
            { label: "100% Virgin Human Hair", value: "human" },
            { label: "Synthetic Fiber", value: "synthetic" },
            { label: "Human Hair Blend", value: "blend" },
          ].map((item) => (
            <label key={item.value} className="flex items-center gap-2 cursor-pointer py-1 px-2 rounded-lg hover:bg-neutral-50 transition text-neutral-700">
              <input
                type="radio"
                name="hair_type"
                checked={selectedHairType === item.value}
                onChange={() => onSelectHairType(selectedHairType === item.value ? "" : item.value)}
                className="text-brand-600 focus:ring-brand-500"
              />
              <span className={selectedHairType === item.value ? "font-bold text-neutral-900" : ""}>{item.label}</span>
            </label>
          ))}
        </div>
      </div>
    </aside>
  );
}
