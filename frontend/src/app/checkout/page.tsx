"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { useQuery } from "@tanstack/react-query";
import {
  ShieldCheck, Truck, CreditCard, Smartphone, CheckCircle2,
  Lock, ArrowRight, Loader2, AlertCircle, Building2
} from "lucide-react";
import { DeliveryMethod, Coupon } from "@/types";
import { fetchApi } from "@/lib/api";
import { formatPrice } from "@/lib/formatters";
import { useCart } from "@/context/CartContext";
import { useAuth } from "@/context/AuthContext";

export default function CheckoutPage() {
  const router = useRouter();
  const { cart, refreshCart } = useCart();
  const { user } = useAuth();

  // Form State
  const [customerName, setCustomerName] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [streetAddress, setStreetAddress] = useState("");
  const [notes, setNotes] = useState("");
  const [selectedDeliveryMethodId, setSelectedDeliveryMethodId] = useState<number | null>(null);
  const [couponCode, setCouponCode] = useState("");
  const [discountAmount, setDiscountAmount] = useState<number>(0);
  const [paymentMethod, setPaymentMethod] = useState<"mtn_momo" | "airtel_money" | "card" | "cod">("mtn_momo");
  const [paymentPhone, setPaymentPhone] = useState("");

  // Submission & Modal State
  const [submitting, setSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  // Simulated Mobile Money USSD Prompt Modal
  const [paymentModalOpen, setPaymentModalOpen] = useState(false);
  const [activeOrderNumber, setActiveOrderNumber] = useState<string | null>(null);
  const [activePaymentRef, setActivePaymentRef] = useState<string | null>(null);
  const [verifyingPayment, setVerifyingPayment] = useState(false);
  const [simulatedPin, setSimulatedPin] = useState("1234");

  // Autofill user details if signed in
  useEffect(() => {
    if (user) {
      setCustomerName(`${user.first_name || ""} ${user.last_name || ""}`.trim() || user.username);
      setEmail(user.email);
      if (user.profile?.phone) {
        setPhone(user.profile.phone);
        setPaymentPhone(user.profile.phone);
      }
    }
  }, [user]);

  // Fetch Delivery Methods
  const { data: deliveryMethodsData } = useQuery<{ results: DeliveryMethod[] }>({
    queryKey: ["delivery-methods"],
    queryFn: () => fetchApi("/delivery-methods/"),
  });

  const deliveryMethods = deliveryMethodsData?.results || [];

  // Default to first delivery method
  useEffect(() => {
    if (deliveryMethods.length > 0 && selectedDeliveryMethodId === null) {
      setSelectedDeliveryMethodId(deliveryMethods[0].id);
    }
  }, [deliveryMethods, selectedDeliveryMethodId]);

  const selectedDelivery = deliveryMethods.find((d) => d.id === selectedDeliveryMethodId);
  const deliveryFee = selectedDelivery ? parseFloat(selectedDelivery.base_fee) : 0;
  const subtotal = cart?.subtotal ? parseFloat(cart.subtotal) : 0;
  const total = Math.max(0, subtotal + deliveryFee - discountAmount);

  const handleApplyCoupon = async () => {
    if (!couponCode.trim()) return;
    try {
      const res = await fetchApi<any>("/promotions/apply/", {
        method: "POST",
        body: JSON.stringify({ code: couponCode.trim(), subtotal }),
      });
      if (res.valid) {
        setDiscountAmount(parseFloat(res.discount_amount));
      }
    } catch (err: any) {
      setDiscountAmount(0);
      alert(err.message || "Invalid coupon");
    }
  };

  const handleCheckout = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!customerName || !email || !phone || !streetAddress) {
      setErrorMessage("Please fill in all required contact and delivery fields.");
      return;
    }

    setSubmitting(true);
    setErrorMessage(null);

    try {
      // 1. Create order
      const orderRes = await fetchApi<{ message: string; order: any }>("/checkout/", {
        method: "POST",
        body: JSON.stringify({
          customer_name: customerName,
          email,
          phone,
          delivery_address: streetAddress,
          delivery_method_id: selectedDeliveryMethodId,
          coupon_code: couponCode,
          payment_method: paymentMethod,
          notes,
        }),
      });

      const orderNumber = orderRes.order.order_number;
      setActiveOrderNumber(orderNumber);

      // 2. Initiate Payment
      const payRes = await fetchApi<any>("/payments/initiate/", {
        method: "POST",
        body: JSON.stringify({
          order_number: orderNumber,
          provider: paymentMethod,
          phone_number: paymentPhone || phone,
        }),
      });

      setActivePaymentRef(payRes.transaction_reference);
      await refreshCart();

      // Open Payment Simulation Modal for MoMo / Card
      if (paymentMethod === "cod") {
        router.push(`/orders/${orderNumber}`);
      } else {
        setPaymentModalOpen(true);
      }
    } catch (err: any) {
      setErrorMessage(err.data?.cart || err.message || "Failed to process checkout. Please try again.");
    } finally {
      setSubmitting(false);
    }
  };

  const handleSimulatePaymentApproval = async () => {
    if (!activePaymentRef || !activeOrderNumber) return;
    setVerifyingPayment(true);
    try {
      await fetchApi("/payments/verify/", {
        method: "POST",
        body: JSON.stringify({
          transaction_reference: activePaymentRef,
          simulated_pin: simulatedPin,
        }),
      });

      router.push(`/orders/${activeOrderNumber}?payment_success=true`);
    } catch (err: any) {
      alert("Payment verification failed");
    } finally {
      setVerifyingPayment(false);
    }
  };

  if (!cart || cart.items.length === 0) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-20 text-center">
        <h2 className="font-serif text-2xl font-bold mb-4">Your bag is empty</h2>
        <button
          onClick={() => router.push("/shop")}
          className="bg-brand-dark text-white text-xs px-6 py-3 rounded-full"
        >
          Return to Shop
        </button>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
      <div className="mb-8">
        <h1 className="font-serif text-2xl sm:text-3xl font-bold text-neutral-900">
          Secure Checkout
        </h1>
        <p className="text-xs text-neutral-500 mt-1">
          Complete your contact information and select a verified payment method.
        </p>
      </div>

      {errorMessage && (
        <div className="mb-6 p-4 bg-red-50 text-red-800 rounded-2xl border border-red-200 text-xs flex items-center gap-2">
          <AlertCircle className="w-4 h-4 shrink-0 text-red-600" />
          <span>{errorMessage}</span>
        </div>
      )}

      <form onSubmit={handleCheckout} className="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12">
        {/* Left Columns: Inputs */}
        <div className="lg:col-span-7 space-y-8">
          {/* 1. Customer Information */}
          <div className="bg-white p-6 rounded-3xl border border-neutral-200/80 shadow-sm space-y-4">
            <h2 className="font-serif text-lg font-bold text-neutral-900 flex items-center gap-2">
              <span className="w-6 h-6 bg-brand-dark text-white text-xs rounded-full flex items-center justify-center font-sans font-bold">1</span>
              Customer Contact Information
            </h2>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
              <div>
                <label className="block font-semibold text-neutral-700 mb-1">Full Name *</label>
                <input
                  type="text"
                  required
                  value={customerName}
                  onChange={(e) => setCustomerName(e.target.value)}
                  placeholder="e.g. Eva Nakato"
                  className="w-full bg-neutral-50 border border-neutral-200 rounded-xl px-3 py-2.5 text-neutral-900 focus:outline-none focus:border-brand-500"
                />
              </div>

              <div>
                <label className="block font-semibold text-neutral-700 mb-1">Email Address (for Receipt) *</label>
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="e.g. eva@example.com"
                  className="w-full bg-neutral-50 border border-neutral-200 rounded-xl px-3 py-2.5 text-neutral-900 focus:outline-none focus:border-brand-500"
                />
              </div>

              <div className="sm:col-span-2">
                <label className="block font-semibold text-neutral-700 mb-1">Mobile Telephone Number *</label>
                <input
                  type="tel"
                  required
                  value={phone}
                  onChange={(e) => {
                    setPhone(e.target.value);
                    if (!paymentPhone) setPaymentPhone(e.target.value);
                  }}
                  placeholder="e.g. +256 772 987 654 or 0700112233"
                  className="w-full bg-neutral-50 border border-neutral-200 rounded-xl px-3 py-2.5 text-neutral-900 focus:outline-none focus:border-brand-500"
                />
              </div>
            </div>
          </div>

          {/* 2. Delivery Address & Zone */}
          <div className="bg-white p-6 rounded-3xl border border-neutral-200/80 shadow-sm space-y-4">
            <h2 className="font-serif text-lg font-bold text-neutral-900 flex items-center gap-2">
              <span className="w-6 h-6 bg-brand-dark text-white text-xs rounded-full flex items-center justify-center font-sans font-bold">2</span>
              Delivery Address in Uganda
            </h2>

            <div className="space-y-4 text-xs">
              <div>
                <label className="block font-semibold text-neutral-700 mb-1">Physical Address / Street / Landmark *</label>
                <textarea
                  rows={2}
                  required
                  value={streetAddress}
                  onChange={(e) => setStreetAddress(e.target.value)}
                  placeholder="e.g. Plot 14 Acacia Avenue, Kololo (Near Acacia Mall), Kampala"
                  className="w-full bg-neutral-50 border border-neutral-200 rounded-xl px-3 py-2.5 text-neutral-900 focus:outline-none focus:border-brand-500"
                />
              </div>

              {/* Delivery Zone Options */}
              <div>
                <label className="block font-semibold text-neutral-700 mb-2">Select Delivery Zone & Speed *</label>
                <div className="space-y-2">
                  {deliveryMethods.map((dm) => (
                    <label
                      key={dm.id}
                      className={`flex items-center justify-between p-3.5 rounded-2xl border cursor-pointer transition ${
                        selectedDeliveryMethodId === dm.id
                          ? "border-brand-600 bg-brand-50/60 ring-1 ring-brand-500/20"
                          : "border-neutral-200 hover:border-neutral-300 bg-white"
                      }`}
                    >
                      <div className="flex items-center gap-3">
                        <input
                          type="radio"
                          name="delivery_method"
                          checked={selectedDeliveryMethodId === dm.id}
                          onChange={() => setSelectedDeliveryMethodId(dm.id)}
                          className="text-brand-600 focus:ring-brand-500"
                        />
                        <div>
                          <p className="font-bold text-neutral-900">{dm.name}</p>
                          <p className="text-[11px] text-neutral-500">{dm.estimated_delivery}</p>
                        </div>
                      </div>
                      <span className="font-extrabold text-neutral-900">
                        {parseFloat(dm.base_fee) === 0 ? "FREE" : formatPrice(dm.base_fee)}
                      </span>
                    </label>
                  ))}
                </div>
              </div>

              <div>
                <label className="block font-semibold text-neutral-700 mb-1">Special Delivery Instructions (Optional)</label>
                <input
                  type="text"
                  value={notes}
                  onChange={(e) => setNotes(e.target.value)}
                  placeholder="e.g. Call before dispatch or leave with reception"
                  className="w-full bg-neutral-50 border border-neutral-200 rounded-xl px-3 py-2 text-neutral-900 focus:outline-none focus:border-brand-500"
                />
              </div>
            </div>
          </div>

          {/* 3. Payment Method */}
          <div className="bg-white p-6 rounded-3xl border border-neutral-200/80 shadow-sm space-y-4">
            <h2 className="font-serif text-lg font-bold text-neutral-900 flex items-center gap-2">
              <span className="w-6 h-6 bg-brand-dark text-white text-xs rounded-full flex items-center justify-center font-sans font-bold">3</span>
              Payment Method
            </h2>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
              {/* MTN MoMo */}
              <label
                className={`p-4 rounded-2xl border cursor-pointer flex flex-col justify-between transition ${
                  paymentMethod === "mtn_momo" ? "border-yellow-500 bg-yellow-50/50 ring-1 ring-yellow-400" : "border-neutral-200 hover:border-neutral-300"
                }`}
              >
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-2">
                    <input
                      type="radio"
                      name="payment_method"
                      checked={paymentMethod === "mtn_momo"}
                      onChange={() => setPaymentMethod("mtn_momo")}
                      className="text-yellow-600 focus:ring-yellow-500"
                    />
                    <span className="font-bold text-neutral-900">MTN Mobile Money</span>
                  </div>
                  <Smartphone className="w-4 h-4 text-yellow-600" />
                </div>
                <p className="text-[11px] text-neutral-500">Instant USSD PIN prompt on your phone</p>
              </label>

              {/* Airtel Money */}
              <label
                className={`p-4 rounded-2xl border cursor-pointer flex flex-col justify-between transition ${
                  paymentMethod === "airtel_money" ? "border-red-500 bg-red-50/50 ring-1 ring-red-400" : "border-neutral-200 hover:border-neutral-300"
                }`}
              >
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-2">
                    <input
                      type="radio"
                      name="payment_method"
                      checked={paymentMethod === "airtel_money"}
                      onChange={() => setPaymentMethod("airtel_money")}
                      className="text-red-600 focus:ring-red-500"
                    />
                    <span className="font-bold text-neutral-900">Airtel Money</span>
                  </div>
                  <Smartphone className="w-4 h-4 text-red-600" />
                </div>
                <p className="text-[11px] text-neutral-500">Instant Airtel push prompt</p>
              </label>

              {/* Card */}
              <label
                className={`p-4 rounded-2xl border cursor-pointer flex flex-col justify-between transition ${
                  paymentMethod === "card" ? "border-blue-500 bg-blue-50/50 ring-1 ring-blue-400" : "border-neutral-200 hover:border-neutral-300"
                }`}
              >
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-2">
                    <input
                      type="radio"
                      name="payment_method"
                      checked={paymentMethod === "card"}
                      onChange={() => setPaymentMethod("card")}
                      className="text-blue-600 focus:ring-blue-500"
                    />
                    <span className="font-bold text-neutral-900">Credit / Debit Card</span>
                  </div>
                  <CreditCard className="w-4 h-4 text-blue-600" />
                </div>
                <p className="text-[11px] text-neutral-500">Visa, Mastercard, 3D-Secure</p>
              </label>

              {/* COD */}
              <label
                className={`p-4 rounded-2xl border cursor-pointer flex flex-col justify-between transition ${
                  paymentMethod === "cod" ? "border-brand-600 bg-brand-50/50 ring-1 ring-brand-400" : "border-neutral-200 hover:border-neutral-300"
                }`}
              >
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-2">
                    <input
                      type="radio"
                      name="payment_method"
                      checked={paymentMethod === "cod"}
                      onChange={() => setPaymentMethod("cod")}
                      className="text-brand-600 focus:ring-brand-500"
                    />
                    <span className="font-bold text-neutral-900">Cash On Delivery</span>
                  </div>
                  <Truck className="w-4 h-4 text-brand-600" />
                </div>
                <p className="text-[11px] text-neutral-500">Pay when your wig arrives (Kampala)</p>
              </label>
            </div>

            {(paymentMethod === "mtn_momo" || paymentMethod === "airtel_money") && (
              <div className="pt-2 text-xs">
                <label className="block font-semibold text-neutral-700 mb-1">
                  {paymentMethod === "mtn_momo" ? "MTN" : "Airtel"} Phone Number to Prompt *
                </label>
                <input
                  type="tel"
                  required
                  value={paymentPhone}
                  onChange={(e) => setPaymentPhone(e.target.value)}
                  placeholder="e.g. 0782112233"
                  className="w-full bg-neutral-50 border border-neutral-200 rounded-xl px-3 py-2 text-neutral-900 focus:outline-none focus:border-brand-500"
                />
              </div>
            )}
          </div>
        </div>

        {/* Right Column: Order Items & Summary */}
        <div className="lg:col-span-5 space-y-6">
          <div className="bg-neutral-50 p-6 rounded-3xl border border-neutral-200/80 space-y-5 sticky top-28">
            <h2 className="font-serif text-lg font-bold text-neutral-900">Bag Summary ({cart.item_count})</h2>

            {/* Items Mini List */}
            <div className="max-h-60 overflow-y-auto space-y-3 divide-y divide-neutral-200/60 pr-1">
              {cart.items.map((item) => (
                <div key={item.id} className="pt-3 flex gap-3 text-xs">
                  <div className="w-12 h-16 bg-neutral-200 rounded-lg overflow-hidden shrink-0">
                    <img
                      src={item.image?.image_url || "https://images.unsplash.com/photo-1595476108010-b4d1f102b1b1?auto=format&fit=crop&w=300&q=80"}
                      alt={item.product_name}
                      className="w-full h-full object-cover"
                    />
                  </div>
                  <div className="flex-1 min-w-0">
                    <h4 className="font-semibold text-neutral-900 line-clamp-1">{item.product_name}</h4>
                    <p className="text-[11px] text-neutral-500">
                      Qty: {item.quantity} • {item.variant_options.length_inches}" {item.variant_options.color}
                    </p>
                    <p className="font-bold text-neutral-900 mt-1">{formatPrice(item.line_total)}</p>
                  </div>
                </div>
              ))}
            </div>

            {/* Calculations Breakdown */}
            <div className="pt-4 border-t border-neutral-200 space-y-2.5 text-xs">
              <div className="flex justify-between text-neutral-600">
                <span>Items Subtotal:</span>
                <span className="font-semibold text-neutral-900">{formatPrice(subtotal)}</span>
              </div>

              {discountAmount > 0 && (
                <div className="flex justify-between text-emerald-700 font-semibold">
                  <span>Coupon Savings:</span>
                  <span>-{formatPrice(discountAmount)}</span>
                </div>
              )}

              <div className="flex justify-between text-neutral-600">
                <span>Delivery ({selectedDelivery?.zone || "Kampala"}):</span>
                <span className="font-semibold text-neutral-900">
                  {deliveryFee === 0 ? "FREE" : formatPrice(deliveryFee)}
                </span>
              </div>

              <div className="pt-3 border-t border-neutral-200 flex justify-between items-baseline">
                <span className="text-sm font-bold text-neutral-900">Grand Total:</span>
                <span className="font-serif text-2xl font-extrabold text-neutral-950">
                  {formatPrice(total)}
                </span>
              </div>
            </div>

            {/* Coupon Code Inline Input */}
            <div className="flex gap-2 text-xs">
              <input
                type="text"
                value={couponCode}
                onChange={(e) => setCouponCode(e.target.value.toUpperCase())}
                placeholder="PROMO CODE"
                className="flex-1 bg-white border border-neutral-200 rounded-xl px-3 py-2 text-neutral-900 focus:outline-none focus:border-brand-500 uppercase font-mono text-xs"
              />
              <button
                type="button"
                onClick={handleApplyCoupon}
                className="bg-neutral-800 text-white font-semibold px-3 py-2 rounded-xl"
              >
                Apply
              </button>
            </div>

            {/* Final Place Order Button */}
            <button
              type="submit"
              disabled={submitting}
              className="w-full bg-brand-dark hover:bg-neutral-800 text-white font-bold text-xs py-4 rounded-2xl transition flex items-center justify-center gap-2 shadow-xl shadow-neutral-900/10 disabled:opacity-50"
            >
              {submitting ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  <span>Processing Order & Payment...</span>
                </>
              ) : (
                <>
                  <Lock className="w-4 h-4" />
                  <span>PLACE ORDER & PAY ({formatPrice(total)})</span>
                </>
              )}
            </button>
          </div>
        </div>
      </form>

      {/* Simulated USSD Push / Mobile Money Verification Modal */}
      {paymentModalOpen && (
        <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white rounded-3xl max-w-md w-full p-6 sm:p-8 space-y-6 shadow-2xl animate-scale-up text-center">
            <div className="w-16 h-16 bg-yellow-100 text-yellow-800 rounded-full flex items-center justify-center mx-auto">
              <Smartphone className="w-8 h-8 animate-bounce" />
            </div>

            <div>
              <span className="text-[11px] font-bold uppercase tracking-widest text-brand-600">
                Sandbox Payment Simulator
              </span>
              <h3 className="font-serif text-xl sm:text-2xl font-bold text-neutral-900 mt-1">
                Approve Payment on Phone
              </h3>
              <p className="text-xs text-neutral-600 mt-2 leading-relaxed">
                A simulated USSD push prompt has been sent to <strong>{paymentPhone || phone}</strong> for{" "}
                <strong className="text-neutral-950 font-bold">{formatPrice(total)}</strong>.
              </p>
            </div>

            <div className="bg-neutral-100 p-4 rounded-2xl text-xs space-y-2 text-left font-mono">
              <p className="text-neutral-500 text-[11px]">Prompt Details:</p>
              <p className="font-bold text-neutral-800">Order: {activeOrderNumber}</p>
              <p className="font-bold text-neutral-800">Ref: {activePaymentRef}</p>
              <p className="font-bold text-neutral-800">Amount: {formatPrice(total)}</p>
            </div>

            <div className="space-y-3 pt-2">
              <button
                type="button"
                onClick={handleSimulatePaymentApproval}
                disabled={verifyingPayment}
                className="w-full bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs py-3.5 rounded-xl transition flex items-center justify-center gap-2 shadow-lg shadow-emerald-600/20"
              >
                {verifyingPayment ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin" />
                    <span>Verifying with Provider...</span>
                  </>
                ) : (
                  <>
                    <CheckCircle2 className="w-4 h-4" />
                    <span>Confirm & Authorize Payment</span>
                  </>
                )}
              </button>

              <button
                type="button"
                onClick={() => router.push(`/orders/${activeOrderNumber}`)}
                className="text-xs text-neutral-500 hover:text-neutral-800 underline block mx-auto"
              >
                View Order Pending Payment
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
