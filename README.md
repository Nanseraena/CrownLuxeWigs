# CrownLuxe Wigs & Hair — Full-Stack E-Commerce Platform

A production-ready, modern wig and hair extension e-commerce application inspired by SHEIN's product discovery engine and convenience-driven checkout flow. Designed with an original luxury brand identity tailored to African and international customers shopping for virgin human hair, HD swiss lace frontals, glueless bobs, and bundles.

---

## 1. System Architecture

```
Wig_Ecommerce/
├── Wig_Ecommerce_Backend/backend/     # Django REST Framework Monolith
│   ├── core/                          # Settings, URLs, WSGI/ASGI, OpenAPI
│   ├── catalog/                       # Categories, Products, Variants, Images, Reviews
│   ├── cart/                          # Guest & User Cart, CartItem, Merge logic
│   ├── orders/                        # Orders, OrderItems, Delivery Zones, Tracking
│   ├── payments/                      # MTN Mobile Money, Airtel Money, Card sandbox
│   ├── promotions/                    # Coupons & Discount calculation engine
│   ├── users/                         # User Profiles, Registration, Saved Addresses
│   ├── requirements.txt               # Python package dependencies
│   └── manage.py
│
├── frontend/                          # Next.js 14 App Router Storefront
│   ├── src/
│   │   ├── app/                       # App Router Pages
│   │   │   ├── page.tsx               # SHEIN-inspired High-Converting Homepage
│   │   │   ├── shop/page.tsx          # Multi-Faceted Filterable Catalog
│   │   │   ├── products/[slug]/       # Product Details, Gallery & Variant Picker
│   │   │   ├── cart/page.tsx          # Full Shopping Bag Page
│   │   │   ├── checkout/page.tsx      # Step-by-Step Checkout & MoMo Simulator
│   │   │   ├── orders/[order_number]/ # Order Confirmation & Live Timeline Tracking
│   │   │   ├── account/               # Auth, Orders History, Addresses
│   │   │   ├── wishlist/page.tsx      # Saved Favorites & 1-Click Move to Bag
│   │   │   └── admin-portal/page.tsx  # Store Owner KPI Dashboard & Fulfillment
│   │   ├── components/                # Reusable UI & Layout Components
│   │   ├── context/                   # Cart & Auth React Contexts
│   │   ├── lib/                       # API Fetcher & Currency Formatters
│   │   └── types/                     # TypeScript Model Definitions
│   ├── tailwind.config.js             # Luxury Blush, Gold & Dark Neutral Theme
│   └── package.json
```

---

## 2. Key Features

- **SHEIN-Inspired Product Discovery**: Sticky promotional announcement banner, story/category carousel, flash deals, tabbed Best Sellers / New Arrivals, and real customer reviews.
- **Dynamic Multi-Facet Filtering**: Filter catalog by Hair Type (Virgin Human, Synthetic, Blend), Texture (Bone Straight, Deep Wave, Body Wave, Kinky Curly, Bob), Length (10"–30"), Price, and In-Stock status.
- **Precision Variant Selector**: Choose length, color, texture, and lace type with live price adjustments and stock quantity availability guards.
- **Reliable Cart Workflow**: Persistent guest carts via `X-Cart-Token` UUID, server-side authoritative pricing, stock validation, and seamless automatic cart merging on customer login.
- **Ugandan Delivery Zones**: Configurable shipping fees (Kampala Central 10,000 UGX, Greater Kampala/Wakiso 15,000 UGX, Express 20,000 UGX, Upcountry 25,000 UGX, Free Boutique Pickup).
- **Payment Gateway Integration**: Official sandbox flow for **MTN Mobile Money**, **Airtel Money**, and **Debit/Credit Cards** with simulated USSD prompt verification and idempotent status transitions.
- **Order Tracking & Fulfillment**: Live progress timeline from Pending Payment to Delivered with customer receipt view.
- **Store Administrator Portal**: Executive analytics dashboard displaying revenue totals, order counts, low-stock inventory alerts, and quick fulfillment status updater.

---

## 3. Quick Start Guide

### Prerequisites
- Python 3.12+
- Node.js 18+ and npm

### Backend Setup

```bash
cd Wig_Ecommerce_Backend/backend

# 1. Activate Virtual Environment
source .venv/bin/activate   # or python3.12 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2. Run Database Migrations
python manage.py migrate

# 3. Seed Realistic Catalog & Accounts
python manage.py seed_catalog

# 4. Run Test Suite (All 17 Tests Pass)
python manage.py test

# 5. Start Development Server
python manage.py runserver 0.0.0.0:8000
```

### Frontend Setup

```bash
cd frontend

# 1. Install Dependencies
npm install

# 2. Build or Run Dev Server
npm run build
npm run dev -- -p 3000
```

Open `http://localhost:3000` to view the storefront!

---

## 4. Default Seed Accounts & Promo Codes

- **Admin User**: `admin` / `admin123456` (Access full Django admin at `http://127.0.0.1:8000/admin/` or `/admin-portal`)
- **Demo Customer**: `nakato_e` / `customer123`
- **Active Promo Coupons**:
  - `WELCOME10`: 10% Off First Purchase
  - `CROWN50K`: 50,000 UGX Flat Discount on orders over 450,000 UGX
  - `GLUELESS20`: 20% Off Glueless & HD Lace Frontal Wigs
  - `VIPCROWN`: 15% Off VIP Member Special

---

## 5. API Endpoints Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/health/` | API Health Check |
| `GET` | `/api/v1/categories/` | List Active Categories |
| `GET` | `/api/v1/products/` | Filterable Product Catalog |
| `GET` | `/api/v1/products/{slug}/` | Product Details & Variants |
| `POST` | `/api/v1/products/{slug}/reviews/` | Submit Customer Review |
| `GET` | `/api/v1/cart/` | Retrieve Cart (X-Cart-Token) |
| `POST` | `/api/v1/cart/items/` | Add Variant to Cart |
| `PATCH` | `/api/v1/cart/items/{id}/` | Update Quantity |
| `DELETE` | `/api/v1/cart/items/{id}/` | Remove Item |
| `POST` | `/api/v1/cart/merge/` | Merge Guest Cart on Login |
| `POST` | `/api/v1/promotions/apply/` | Validate & Calculate Coupon |
| `GET` | `/api/v1/delivery-methods/` | Active Delivery Zones & Fees |
| `POST` | `/api/v1/checkout/` | Server-Validated Order Creation |
| `POST` | `/api/v1/payments/initiate/` | Initiate Mobile Money / Card |
| `POST` | `/api/v1/payments/verify/` | Sandbox Verification Callback |
| `GET` | `/api/v1/orders/track/{order_number}/` | Public Order Tracking |
| `GET` | `/api/v1/admin/dashboard-stats/` | Store Owner KPI Metrics |
| `POST` | `/api/v1/auth/register/` | Customer Registration |
| `POST` | `/api/token/` | SimpleJWT Login Token |
