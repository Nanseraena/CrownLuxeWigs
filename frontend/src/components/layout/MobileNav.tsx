"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Home, Compass, Heart, ShoppingBag, User } from "lucide-react";
import { useCart } from "@/context/CartContext";

export default function MobileNav() {
  const pathname = usePathname();
  const { itemCount, setIsDrawerOpen } = useCart();

  const navItems = [
    { label: "Home", href: "/", icon: Home },
    { label: "Shop", href: "/shop", icon: Compass },
    { label: "Wishlist", href: "/wishlist", icon: Heart },
    { label: "Bag", action: () => setIsDrawerOpen(true), icon: ShoppingBag, badge: itemCount },
    { label: "Account", href: "/account", icon: User },
  ];

  return (
    <nav className="lg:hidden fixed bottom-0 left-0 right-0 z-40 bg-white/95 backdrop-blur-md border-t border-neutral-200 py-2 px-3">
      <div className="flex items-center justify-around">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = item.href ? pathname === item.href : false;

          if (item.action) {
            return (
              <button
                key={item.label}
                onClick={item.action}
                className="flex flex-col items-center gap-1 text-neutral-600 hover:text-brand-600 relative p-1"
              >
                <div className="relative">
                  <Icon className="w-5 h-5" />
                  {item.badge !== undefined && item.badge > 0 && (
                    <span className="absolute -top-1 -right-2 bg-brand-600 text-white text-[10px] font-bold w-4 h-4 rounded-full flex items-center justify-center">
                      {item.badge}
                    </span>
                  )}
                </div>
                <span className="text-[10px] font-medium">{item.label}</span>
              </button>
            );
          }

          return (
            <Link
              key={item.label}
              href={item.href!}
              className={`flex flex-col items-center gap-1 p-1 transition ${
                isActive ? "text-brand-600 font-semibold" : "text-neutral-600 hover:text-black"
              }`}
            >
              <Icon className="w-5 h-5" />
              <span className="text-[10px]">{item.label}</span>
            </Link>
          );
        })}
      </div>
    </nav>
  );
}
