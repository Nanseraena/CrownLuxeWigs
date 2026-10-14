"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Search, ShoppingBag, Heart, User as UserIcon, Menu, X, Sparkles, ChevronDown } from "lucide-react";
import { useCart } from "@/context/CartContext";
import { useAuth } from "@/context/AuthContext";

export default function Navbar() {
  const router = useRouter();
  const { itemCount, setIsDrawerOpen } = useCart();
  const { user, logout } = useAuth();
  const [searchQuery, setSearchQuery] = useState("");
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [userDropdownOpen, setUserDropdownOpen] = useState(false);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      router.push(`/shop?search=${encodeURIComponent(searchQuery.trim())}`);
      setMobileMenuOpen(false);
    }
  };

  const navLinks = [
    { name: "Shop All", href: "/shop" },
    { name: "HD Lace Frontal", href: "/shop?texture=&hair_type=human" },
    { name: "Bone Straight", href: "/shop?texture=Bone+Straight" },
    { name: "Deep Wave & Curly", href: "/shop?texture=Deep+Wave" },
    { name: "Glueless Bobs", href: "/shop?category=bob-wigs" },
    { name: "Piano Highlights & 613", href: "/shop?category=colored-wigs" },
    { name: "Bundles & Extensions", href: "/shop?category=hair-extensions" },
  ];

  return (
    <header className="sticky top-0 z-40 bg-white border-b border-neutral-100 shadow-sm">
      {/* Main Bar */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16 sm:h-20 gap-4">
          {/* Mobile menu button */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="lg:hidden p-2 text-neutral-700 hover:text-black"
            aria-label="Toggle navigation menu"
          >
            {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6 text-brand-dark" />}
          </button>

          {/* Brand Logo */}
          <Link href="/" className="flex flex-col items-center sm:items-start group">
            <span className="font-serif text-2xl sm:text-3xl font-bold tracking-wider text-brand-dark group-hover:text-brand-600 transition">
              CROWN<span className="text-brand-500">LUXE</span>
            </span>
            <span className="text-[9px] sm:text-[10px] tracking-[0.25em] uppercase text-neutral-500 font-medium -mt-1">
              Hair & Wigs • Uganda
            </span>
          </Link>

          {/* Search bar (Desktop & Tablet) */}
          <form onSubmit={handleSearch} className="hidden md:flex flex-1 max-w-md mx-4 relative">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search bone straight, 13x4 HD lace, bob wigs..."
              className="w-full bg-neutral-50 border border-neutral-200 rounded-full py-2.5 pl-11 pr-4 text-sm text-neutral-900 focus:outline-none focus:ring-2 focus:ring-brand-500/20 focus:border-brand-500 transition"
            />
            <Search className="w-4 h-4 text-neutral-400 absolute left-4 top-1/2 -translate-y-1/2" />
            <button
              type="submit"
              className="absolute right-1.5 top-1/2 -translate-y-1/2 bg-brand-dark text-white text-xs px-3.5 py-1.5 rounded-full hover:bg-neutral-800 transition"
            >
              Search
            </button>
          </form>

          {/* Action Icons */}
          <div className="flex items-center gap-1 sm:gap-3">
            {/* Wishlist */}
            <Link
              href="/wishlist"
              className="p-2 text-neutral-700 hover:text-brand-600 transition relative rounded-full hover:bg-neutral-50"
              title="Saved Wishlist"
            >
              <Heart className="w-5 h-5 sm:w-6 sm:h-6" />
            </Link>

            {/* Shopping Bag Button */}
            <button
              onClick={() => setIsDrawerOpen(true)}
              className="p-2 text-neutral-800 hover:text-brand-600 transition relative rounded-full hover:bg-neutral-50 flex items-center"
              aria-label="View shopping bag"
            >
              <ShoppingBag className="w-5 h-5 sm:w-6 sm:h-6" />
              {itemCount > 0 && (
                <span className="absolute top-1 right-1 bg-brand-600 text-white text-[11px] font-bold w-5 h-5 rounded-full flex items-center justify-center animate-scale-up">
                  {itemCount}
                </span>
              )}
            </button>

            {/* User Account Menu */}
            <div className="relative">
              <button
                onClick={() => setUserDropdownOpen(!userDropdownOpen)}
                className="p-2 text-neutral-800 hover:text-brand-600 transition rounded-full hover:bg-neutral-50 flex items-center gap-1"
                aria-label="Account options"
              >
                <UserIcon className="w-5 h-5 sm:w-6 sm:h-6" />
                <ChevronDown className="w-3.5 h-3.5 text-neutral-400 hidden sm:block" />
              </button>

              {userDropdownOpen && (
                <div
                  className="absolute right-0 mt-2 w-52 bg-white rounded-xl shadow-xl border border-neutral-100 py-2 z-50 text-sm"
                  onMouseLeave={() => setUserDropdownOpen(false)}
                >
                  {user ? (
                    <>
                      <div className="px-4 py-2 border-b border-neutral-100">
                        <p className="font-semibold text-neutral-900 truncate">{user.first_name || user.username}</p>
                        <p className="text-xs text-neutral-500 truncate">{user.email}</p>
                      </div>
                      <Link
                        href="/account"
                        onClick={() => setUserDropdownOpen(false)}
                        className="block px-4 py-2 text-neutral-700 hover:bg-neutral-50"
                      >
                        My Account & Orders
                      </Link>
                      <Link
                        href="/wishlist"
                        onClick={() => setUserDropdownOpen(false)}
                        className="block px-4 py-2 text-neutral-700 hover:bg-neutral-50"
                      >
                        My Wishlist
                      </Link>
                      <Link
                        href="/admin-portal"
                        onClick={() => setUserDropdownOpen(false)}
                        className="block px-4 py-2 text-brand-700 font-medium hover:bg-brand-50"
                      >
                        Store Admin Dashboard
                      </Link>
                      <button
                        onClick={() => {
                          setUserDropdownOpen(false);
                          logout();
                        }}
                        className="w-full text-left px-4 py-2 text-red-600 hover:bg-red-50 border-t border-neutral-100 mt-1"
                      >
                        Sign Out
                      </button>
                    </>
                  ) : (
                    <>
                      <div className="p-3 border-b border-neutral-100 text-center">
                        <Link
                          href="/account/login"
                          onClick={() => setUserDropdownOpen(false)}
                          className="block w-full bg-brand-dark text-white font-medium py-2 rounded-lg text-center hover:bg-neutral-800 transition"
                        >
                          Sign In
                        </Link>
                        <p className="text-xs text-neutral-500 mt-2">
                          New to CrownLuxe?{" "}
                          <Link
                            href="/account/register"
                            onClick={() => setUserDropdownOpen(false)}
                            className="text-brand-600 font-semibold underline"
                          >
                            Register
                          </Link>
                        </p>
                      </div>
                      <Link
                        href="/admin-portal"
                        onClick={() => setUserDropdownOpen(false)}
                        className="block px-4 py-2 text-neutral-700 hover:bg-neutral-50"
                      >
                        Store Admin Dashboard
                      </Link>
                      <Link
                        href="/orders/track/CLM-DEMO"
                        onClick={() => setUserDropdownOpen(false)}
                        className="block px-4 py-2 text-neutral-700 hover:bg-neutral-50"
                      >
                        Track An Order
                      </Link>
                    </>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Mobile Search Input */}
        <form onSubmit={handleSearch} className="md:hidden pb-3 relative">
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search wigs, bobs, HD frontals..."
            className="w-full bg-neutral-50 border border-neutral-200 rounded-full py-2 pl-10 pr-4 text-xs text-neutral-900 focus:outline-none focus:border-brand-500"
          />
          <Search className="w-3.5 h-3.5 text-neutral-400 absolute left-3.5 top-1/2 -translate-y-1/2 -mt-1.5" />
        </form>
      </div>

      {/* Categories Bar (SHEIN Style Discovery Sub-header) */}
      <div className="hidden lg:block bg-neutral-50/80 border-t border-neutral-100 text-xs font-medium">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <ul className="flex items-center justify-between py-2.5 overflow-x-auto no-scrollbar gap-6">
            {navLinks.map((link) => (
              <li key={link.name} className="whitespace-nowrap">
                <Link
                  href={link.href}
                  className="text-neutral-700 hover:text-brand-600 transition py-1 relative hover:font-semibold"
                >
                  {link.name}
                </Link>
              </li>
            ))}
            <li className="whitespace-nowrap ml-auto">
              <Link
                href="/shop?ordering=price_asc"
                className="text-brand-600 font-bold flex items-center gap-1 hover:text-brand-700"
              >
                <Sparkles className="w-3.5 h-3.5" />
                FLASH DEALS UNDER 500K
              </Link>
            </li>
          </ul>
        </div>
      </div>

      {/* Mobile Drawer Menu */}
      {mobileMenuOpen && (
        <div className="lg:hidden fixed inset-0 z-50 bg-black/50" onClick={() => setMobileMenuOpen(false)}>
          <div
            className="w-4/5 max-w-sm bg-white h-full p-6 overflow-y-auto"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-center justify-between pb-4 border-b border-neutral-100">
              <span className="font-serif text-xl font-bold text-brand-dark">CROWNLUXE WIGS</span>
              <button onClick={() => setMobileMenuOpen(false)}>
                <X className="w-5 h-5 text-neutral-500" />
              </button>
            </div>

            <div className="py-4 space-y-1">
              <p className="text-[11px] font-bold uppercase tracking-wider text-neutral-400 mb-2">Shop Categories</p>
              {navLinks.map((link) => (
                <Link
                  key={link.name}
                  href={link.href}
                  onClick={() => setMobileMenuOpen(false)}
                  className="block py-2.5 text-sm font-medium text-neutral-800 hover:text-brand-600 border-b border-neutral-50"
                >
                  {link.name}
                </Link>
              ))}
            </div>

            <div className="pt-4 border-t border-neutral-100 space-y-3">
              <p className="text-[11px] font-bold uppercase tracking-wider text-neutral-400">Account & Info</p>
              {user ? (
                <>
                  <Link
                    href="/account"
                    onClick={() => setMobileMenuOpen(false)}
                    className="block text-sm text-neutral-700 py-1"
                  >
                    My Orders & Profile ({user.first_name || user.username})
                  </Link>
                  <button
                    onClick={() => {
                      setMobileMenuOpen(false);
                      logout();
                    }}
                    className="block text-sm text-red-600 py-1"
                  >
                    Log Out
                  </button>
                </>
              ) : (
                <div className="flex gap-2 pt-2">
                  <Link
                    href="/account/login"
                    onClick={() => setMobileMenuOpen(false)}
                    className="flex-1 bg-brand-dark text-white text-center py-2 rounded-lg text-xs font-semibold"
                  >
                    Sign In
                  </Link>
                  <Link
                    href="/account/register"
                    onClick={() => setMobileMenuOpen(false)}
                    className="flex-1 border border-neutral-200 text-center py-2 rounded-lg text-xs font-semibold"
                  >
                    Register
                  </Link>
                </div>
              )}
              <Link
                href="/admin-portal"
                onClick={() => setMobileMenuOpen(false)}
                className="block text-sm text-brand-600 font-medium py-1"
              >
                Store Admin Dashboard
              </Link>
            </div>
          </div>
        </div>
      )}
    </header>
  );
}
