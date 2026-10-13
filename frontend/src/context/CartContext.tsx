"use client";

import React, { createContext, useContext, useState, useEffect, useCallback } from "react";
import { Cart } from "@/types";
import { fetchApi } from "@/lib/api";

interface CartContextType {
  cart: Cart | null;
  loading: boolean;
  itemCount: number;
  isDrawerOpen: boolean;
  setIsDrawerOpen: (open: boolean) => void;
  toastMessage: string | null;
  refreshCart: () => Promise<void>;
  addItem: (variantId: number, quantity?: number) => Promise<void>;
  updateQuantity: (itemId: number, quantity: number) => Promise<void>;
  removeItem: (itemId: number) => Promise<void>;
  clearCart: () => Promise<void>;
}

const CartContext = createContext<CartContextType | undefined>(undefined);

export function CartProvider({ children }: { children: React.ReactNode }) {
  const [cart, setCart] = useState<Cart | null>(null);
  const [loading, setLoading] = useState(false);
  const [isDrawerOpen, setIsDrawerOpen] = useState(false);
  const [toastMessage, setToastMessage] = useState<string | null>(null);

  const showToast = (msg: string) => {
    setToastMessage(msg);
    setTimeout(() => setToastMessage(null), 3500);
  };

  const refreshCart = useCallback(async () => {
    try {
      const data = await fetchApi<Cart>("/cart/");
      setCart(data);
    } catch (err) {
      // If no items yet, cart may not be created on server yet
      setCart(null);
    }
  }, []);

  useEffect(() => {
    refreshCart();
  }, [refreshCart]);

  const addItem = async (variantId: number, quantity: number = 1) => {
    setLoading(true);
    try {
      const res = await fetchApi<{ message: string; cart: Cart }>("/cart/items/", {
        method: "POST",
        body: JSON.stringify({ variant_id: variantId, quantity }),
      });
      setCart(res.cart);
      showToast("✨ Added to your shopping bag!");
      setIsDrawerOpen(true);
    } catch (err: any) {
      const msg = err.data?.quantity || err.data?.variant_id || err.message || "Failed to add to cart";
      showToast(`⚠️ ${Array.isArray(msg) ? msg[0] : msg}`);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const updateQuantity = async (itemId: number, quantity: number) => {
    if (quantity < 1) {
      return removeItem(itemId);
    }
    setLoading(true);
    try {
      const updatedCart = await fetchApi<Cart>(`/cart/items/${itemId}/`, {
        method: "PATCH",
        body: JSON.stringify({ quantity }),
      });
      setCart(updatedCart);
    } catch (err: any) {
      const msg = err.data?.quantity || err.message || "Failed to update quantity";
      showToast(`⚠️ ${Array.isArray(msg) ? msg[0] : msg}`);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const removeItem = async (itemId: number) => {
    setLoading(true);
    try {
      const updatedCart = await fetchApi<Cart>(`/cart/items/${itemId}/`, {
        method: "DELETE",
      });
      setCart(updatedCart);
      showToast("Item removed from bag");
    } catch (err: any) {
      showToast("Failed to remove item");
    } finally {
      setLoading(false);
    }
  };

  const clearCart = async () => {
    setLoading(true);
    try {
      const updatedCart = await fetchApi<Cart>("/cart/clear/", {
        method: "DELETE",
      });
      setCart(updatedCart);
    } catch (err: any) {
      showToast("Failed to clear bag");
    } finally {
      setLoading(false);
    }
  };

  const itemCount = cart?.item_count || 0;

  return (
    <CartContext.Provider
      value={{
        cart,
        loading,
        itemCount,
        isDrawerOpen,
        setIsDrawerOpen,
        toastMessage,
        refreshCart,
        addItem,
        updateQuantity,
        removeItem,
        clearCart,
      }}
    >
      {children}
    </CartContext.Provider>
  );
}

export function useCart() {
  const context = useContext(CartContext);
  if (!context) {
    throw new Error("useCart must be used within a CartProvider");
  }
  return context;
}
