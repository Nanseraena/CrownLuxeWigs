import Link from "next/link";
import { Sparkles, ArrowRight, Home, ShoppingBag } from "lucide-react";

export default function NotFound() {
  return (
    <div className="min-h-[70vh] flex items-center justify-center px-4 py-16 bg-[#FDFBF9]">
      <div className="max-w-md w-full text-center space-y-6">
        <div className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-brand-100 text-brand-600 mb-2">
          <Sparkles className="w-10 h-10" />
        </div>

        <div className="space-y-2">
          <p className="text-xs uppercase tracking-widest font-semibold text-brand-600">
            Page Not Found • 404
          </p>
          <h1 className="text-3xl font-serif font-bold text-neutral-900">
            Lost Your Crown?
          </h1>
          <p className="text-sm text-neutral-600 leading-relaxed">
            The page or luxury wig you are looking for has either been moved,
            sold out, or does not exist. Let us guide you back to our royal collection.
          </p>
        </div>

        <div className="flex flex-col sm:flex-row items-center justify-center gap-3 pt-2">
          <Link
            href="/shop"
            className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-6 py-3 rounded-full bg-neutral-900 text-white font-medium text-sm hover:bg-neutral-800 transition-all shadow-md"
          >
            <ShoppingBag className="w-4 h-4" />
            <span>Explore Boutique</span>
            <ArrowRight className="w-4 h-4" />
          </Link>
          <Link
            href="/"
            className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-6 py-3 rounded-full border border-neutral-300 text-neutral-700 font-medium text-sm hover:bg-neutral-50 transition-colors"
          >
            <Home className="w-4 h-4" />
            <span>Return Home</span>
          </Link>
        </div>
      </div>
    </div>
  );
}
