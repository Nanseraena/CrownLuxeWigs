export function formatPrice(amount: string | number | null | undefined, currency: string = "UGX"): string {
  if (amount === null || amount === undefined) return "UGX 0";
  const num = typeof amount === "string" ? parseFloat(amount) : amount;
  if (isNaN(num)) return "UGX 0";

  return new Intl.NumberFormat("en-UG", {
    style: "currency",
    currency: currency,
    maximumFractionDigits: 0,
  }).format(num);
}

export function calculateDiscountPercent(original: string | number | null | undefined, current: string | number | null | undefined): number | null {
  if (!original || !current) return null;
  const orig = typeof original === "string" ? parseFloat(original) : original;
  const curr = typeof current === "string" ? parseFloat(current) : current;
  if (isNaN(orig) || isNaN(curr) || orig <= curr) return null;
  return Math.round(((orig - curr) / orig) * 100);
}

export function formatDate(dateString: string): string {
  try {
    const d = new Date(dateString);
    return d.toLocaleDateString("en-UG", {
      year: "numeric",
      month: "short",
      day: "numeric",
    });
  } catch {
    return dateString;
  }
}
