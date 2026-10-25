import type { Metadata } from "next";
import "@/styles/globals.css";
import { AuthProvider } from "@/context/AuthContext";
import { CartProvider } from "@/context/CartContext";
import AnnouncementBar from "@/components/layout/AnnouncementBar";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import MobileNav from "@/components/layout/MobileNav";
import CartDrawer from "@/components/cart/CartDrawer";
import Providers from "./providers";

export const metadata: Metadata = {
  title: "CrownLuxe Wigs & Hair Uganda | Luxury Virgin Human Hair Wigs",
  description: "Shop premier 100% Virgin Human Hair Wigs, HD Melted Lace Frontals, Bone Straight Wigs, and Glueless Bobs. Same-day delivery in Kampala with MTN MoMo & Airtel Money.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="min-h-screen flex flex-col bg-white text-neutral-900 antialiased selection:bg-brand-100 selection:text-brand-900">
        <Providers>
          <AuthProvider>
            <CartProvider>
              <AnnouncementBar />
              <Navbar />
              <main className="flex-1 pb-20 lg:pb-0">{children}</main>
              <Footer />
              <MobileNav />
              <CartDrawer />
            </CartProvider>
          </AuthProvider>
        </Providers>
      </body>
    </html>
  );
}
