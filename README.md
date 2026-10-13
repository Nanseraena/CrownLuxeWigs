# CrownLuxe Wigs & Hair — Full-Stack E-Commerce Platform

A production-ready, modern wig and hair extension e-commerce application inspired by SHEIN's product discovery engine and convenience-driven checkout flow. Designed with an original luxury brand identity tailored to African and international customers shopping for virgin human hair, HD swiss lace frontals, glueless bobs, and bundles.

---

## 1. System Architecture

```
Wig_Ecommerce/
├── backend/                           # Django REST Framework Monolith
│   ├── core/                          # Settings, URLs, WSGI/ASGI, OpenAPI
│   ├── catalog/                       # Categories, Collections, Products, Variants, Images, Reviews
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
│   │   │   ├── page.tsx               # SHEIN-inspired Visual Homepage (Categories Carousel, Color & Length Discovery)
│   │   │   ├── shop/page.tsx          # Multi-Faceted Filterable Catalog & Active Chips
│   │   │   ├── products/[slug]/       # Product Details, Hair Specs, Gallery & Variant Picker
│   │   │   ├── cart/page.tsx          # Full Shopping Bag Page
│   │   │   ├── checkout/page.tsx      # Step-by-Step Checkout & MoMo Simulator
│   │   │   ├── orders/[order_number]/ # Order Confirmation & Live Timeline Tracking
│   │   │   ├── account/               # Auth, Orders History, Addresses
│   │   │   ├── wishlist/page.tsx      # Saved Favorites & 1-Click Move to Bag
│   │   │   └── admin-portal/page.tsx  # Store Owner KPI Dashboard & Fulfillment
│   │   ├── components/                # Reusable UI & Layout Components (FilterSidebar, ProductCard, etc.)
│   │   ├── context/                   # Cart & Auth React Contexts
│   │   ├── lib/                       # API Fetcher & Currency Formatters
│   │   └── types/                     # TypeScript Model Definitions (Product, Category, Collection, HairOrigin)
│   ├── tailwind.config.js             # Luxury Blush, Gold & Dark Neutral Theme
│   └── package.json
```

---

## 2. Key Features

- **SHEIN-Inspired Product Discovery**: Sticky promotional announcement banner, round story/category circle carousel, curated visual collections ("Best Sellers", "Under 350K UGX", "Beginner Friendly", "HD Melt", "Ready to Wear"), visual color cards, and length discovery grids.
- **Dynamic Multi-Facet Filtering**:
  - **Color**: Visual swatch pills (Natural Black `#1B1B1B`, Jet Black `#0A0A0A`, Dark Brown `#4A3728`, Chocolate Brown `#3B2219`, Honey Blonde `#D4A359`, 613 Blonde `#E8DFB8`, Burgundy `#5B1426`, Copper Red `#B25329`, Ginger `#C45E32`, Piano Highlights, Ombre).
  - **Length**: Grouped quick-filters (Short 10–14", Medium 16–20", Long 22–26", Extra Long 28–36") and individual inch selection pills (10" through 36").
  - **Hair Origin**: Confirmed origin attribute (*Brazilian, Peruvian, Malaysian, Indian, Vietnamese, Cambodian, Other, Unspecified*).
  - **Categories & Subcategories**: Hierarchical browsing across 9 major wig categories and 33 subcategories.
  - **Hair Material & Texture**: Virgin Human Hair, Remy Hair, Raw Hair, HD Synthetic, Heat-Resistant Synthetic across Bone Straight, Body Wave, Deep Wave, Water Wave, Kinky Curly, Afro Kinky, and Loose Wave.
  - **Lace Types**: 13x4 Lace Front, 13x6 Lace Front, 4x4 Closure, 5x5 Closure, HD Swiss Lace, Transparent Lace, Headband / No Lace.
  - **In-Stock Guard & Sorting**: Live price ascending/descending, newest arrivals, highest rating, and instant stock filtering.
- **Precision Variant Selector**: Choose length, color, density, and cap size with live price adjustments and stock quantity availability guards.
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
cd backend

# 1. Activate Virtual Environment
source .venv/bin/activate
pip install -r requirements.txt

# 2. Run Database Migrations
python manage.py migrate

# 3. Seed Realistic Catalog & Accounts (34 distinct products across 9 categories)
python manage.py seed_catalog

# 4. Run Test Suite (All 26 Tests Pass)
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

## 4. Catalog Structure & Categories

### 9 Main Categories & 33 Subcategories:
1. **Lace Front Wigs** (`lace-front-wigs`): 13x4 Lace Front, 13x6 Lace Front, HD Lace Front, Transparent Lace Front, Pre-plucked Lace Front
2. **Closure Wigs** (`closure-wigs`): 4x4 Closure, 5x5 Closure, 2x6 Closure, 2x4 Closure
3. **Glueless Wigs** (`glueless-wigs`): Glueless Lace Front, Wear & Go Pre-cut Lace, Headband Wigs, V-Part Wigs, U-Part Wigs
4. **Bob Wigs** (`bob-wigs`): Blunt Cut Bob, Asymmetrical Bob, Pixie Bob, Curly Bob, Layered Bob
5. **Human Hair Wigs** (`human-hair-wigs`): Virgin Human Hair, Raw Hair, Remy Hair
6. **Colored Wigs** (`colored-wigs`): 613 Blonde, Honey Blonde, Ginger / Copper, Burgundy / 99J, Ombre & Highlights
7. **Textured & Curly Wigs** (`textured-curly-wigs`): Deep Wave, Water Wave, Kinky Curly, Afro Kinky, Body Wave
8. **Synthetic & Budget Wigs** (`synthetic-budget-wigs`): Heat-resistant Synthetic, Everyday Budget Wigs
9. **Braided Wigs** (`braided-wigs`): Knotless Braids Wigs, Box Braids Wigs, Cornrow Wigs

### Curated Collections:
- `best-sellers`: Crown Best Sellers
- `under-350k`: Premium Under 350K UGX
- `beginner-friendly`: Beginner Friendly & Wear-and-Go
- `hd-lace-melt`: HD Lace Melt Collection
- `ready-to-wear`: Ready-to-Wear Glueless
- `blonde-and-copper`: Blonde & Copper Luxe
- `human-hair-essentials`: Virgin Hair Essentials
- `curly-coily-luxe`: Textured & Curly Luxe
- `bob-collection`: Chic Bob Collection
- `braided-glam`: Hand-Braided Glam
- `budget-glam`: Affordable Everyday Glam

---

## 5. API Endpoints Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/health/` | API Health Check |
| `GET` | `/api/v1/categories/` | List Root Categories with Subcategories |
| `GET` | `/api/v1/categories/all_categories/` | List Flat Categories & Subcategories |
| `GET` | `/api/v1/collections/` | Curated Promotional Collections |
| `GET` | `/api/v1/products/` | Filterable Product Catalog |
| `GET` | `/api/v1/products/filter-options/` | Available Filter Facets & Options |
| `GET` | `/api/v1/products/{slug}/` | Product Details, Variants & Specs |
| `POST` | `/api/v1/products/{slug}/reviews/` | Submit Customer Review |
| `GET` | `/api/v1/cart/` | Retrieve Cart (X-Cart-Token) |
| `POST` | `/api/v1/cart/items/` | Add Variant to Cart |
| `PATCH` | `/api/v1/cart/items/{id}/` | Update Quantity |
| `DELETE` | `/api/v1/cart/items/{id}/` | Remove Item |
| `POST` | `/api/v1/cart/merge/` | Merge Guest Cart on Login |
| `POST` | `/api/v1/promotions/apply/` | Validate & Calculate Coupon |
| `GET` | `/api/v1/delivery-methods/` | Active Delivery Zones & Fees |
| `POST` | `/api/checkout/` or `/api/v1/checkout/` | Server-Validated Order Creation |
| `POST` | `/api/v1/payments/initiate/` | Initiate Mobile Money / Card |
| `POST` | `/api/v1/payments/verify/` | Sandbox Verification Callback |
| `GET` | `/api/v1/orders/track/{order_number}/` | Public Order Tracking |
| `GET` | `/api/v1/admin/dashboard-stats/` | Store Owner KPI Metrics |
| `POST` | `/api/v1/auth/register/` | Customer Registration |
| `POST` | `/api/token/` | SimpleJWT Login Token |

### Product Filter Parameters (`/api/v1/products/`):
- `category`: Category slug (e.g. `lace-front-wigs`, `bob-wigs`)
- `subcategory`: Subcategory slug (e.g. `hd-lace-front`, `blunt-cut-bob`)
- `collection`: Collection slug (e.g. `best-sellers`, `under-350k`)
- `color`: Comma-separated colors (e.g. `Natural Black,613 Blonde,Honey Blonde`)
- `length_inches`: Comma-separated inch lengths (e.g. `12,14,24`)
- `length_group`: Comma-separated length tiers (`short`, `medium`, `long`, `extra_long`)
- `hair_origin`: Comma-separated origins (`brazilian`, `peruvian`, `malaysian`, `indian`, `vietnamese`, `cambodian`, `other`, `unspecified`)
- `hair_material`: Material choice (`virgin_human`, `remy_human`, `raw_human`, `synthetic_hd`, `synthetic_heat_resistant`)
- `texture`: Texture choice (`bone_straight`, `body_wave`, `deep_wave`, `water_wave`, `kinky_curly`, `afro_kinky`, `loose_wave`)
- `min_price` & `max_price`: Numerical UGX pricing boundaries
- `in_stock`: `true` to filter items with remaining quantity > 0
- `ordering`: `price_asc`, `price_desc`, `rating`, `newest`, `featured`

---

## 6. Default Seed Accounts & Promo Codes

- **Admin User**: `admin` / `admin123456` (Access full Django admin at `http://127.0.0.1:8000/admin/` or `/admin-portal`)
- **Demo Customer**: `nakato_e` / `customer123`
- **Active Promo Coupons**:
  - `WELCOME10`: 10% Off First Purchase
  - `CROWN50K`: 50,000 UGX Flat Discount on orders over 450,000 UGX
  - `GLUELESS20`: 20% Off Glueless & HD Lace Frontal Wigs
  - `VIPCROWN`: 15% Off VIP Member Special
