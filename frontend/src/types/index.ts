export interface Category {
  id: number;
  name: string;
  slug: string;
  description: string;
  image_url?: string;
  sort_order: number;
}

export interface ProductImage {
  id: number;
  image_url: string;
  alt_text: string;
  is_primary: boolean;
  sort_order: number;
}

export interface ProductVariant {
  id: number;
  sku: string;
  length_inches: number | null;
  color: string;
  texture: string;
  lace_type: string;
  density: string;
  cap_size: string;
  price: string;
  compare_at_price: string | null;
  stock_quantity: number;
  in_stock: boolean;
}

export interface Review {
  id: number;
  product: number;
  reviewer_name: string;
  rating: number;
  title: string;
  comment: string;
  is_verified_purchase: boolean;
  created_at: string;
}

export interface Product {
  id: number;
  name: string;
  slug: string;
  description: string;
  category: Category;
  hair_type: "human" | "synthetic" | "blend";
  texture: string;
  default_length_inches: number | null;
  default_color: string;
  default_lace_type: string;
  min_price: string | null;
  compare_at_price: string | null;
  primary_image: ProductImage | null;
  average_rating: number;
  review_count: number;
  is_featured: boolean;
  is_new_arrival: boolean;
  is_best_seller: boolean;
  created_at: string;
  images?: ProductImage[];
  variants?: ProductVariant[];
  reviews?: Review[];
}

export interface CartItem {
  id: number;
  product_id: number;
  product_name: string;
  product_slug: string;
  variant_id: number;
  sku: string;
  variant_options: {
    length_inches: number | null;
    color: string;
    texture: string;
    lace_type: string;
    density: string;
    cap_size: string;
  };
  unit_price: string;
  quantity: number;
  line_total: string;
  image: ProductImage | null;
  added_at: string;
}

export interface Cart {
  token: string;
  items: CartItem[];
  item_count: number;
  subtotal: string;
  created_at: string;
  updated_at: string;
}

export interface DeliveryMethod {
  id: number;
  name: string;
  zone: string;
  base_fee: string;
  estimated_delivery: string;
  is_active: boolean;
  sort_order: number;
}

export interface OrderItem {
  id: number;
  product_name: string;
  sku: string;
  variant_description: Record<string, any>;
  unit_price: string;
  quantity: number;
  line_total: string;
}

export interface Order {
  id: number;
  order_number: string;
  customer_name: string;
  email: string;
  phone: string;
  delivery_address: string;
  delivery_method: DeliveryMethod | null;
  currency: string;
  subtotal: string;
  delivery_fee: string;
  discount_amount: string;
  coupon_code: string;
  total: string;
  status: "pending" | "processing" | "dispatched" | "delivered" | "cancelled";
  payment_method: "mtn_momo" | "airtel_money" | "card" | "cod";
  payment_status: "pending" | "processing" | "paid" | "failed" | "refunded";
  payment_reference: string;
  tracking_number: string;
  notes: string;
  created_at: string;
  updated_at: string;
  items: OrderItem[];
}

export interface Coupon {
  id: number;
  code: string;
  description: string;
  discount_type: "percentage" | "fixed";
  value: string;
  min_order_amount: string;
  max_discount: string | null;
  expiry_date: string | null;
  is_active: boolean;
}

export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  is_staff: boolean;
  profile?: {
    phone: string;
    avatar_url: string;
  };
}

export interface Address {
  id: number;
  full_name: string;
  phone: string;
  street_address: string;
  city_or_zone: string;
  country: string;
  is_default: boolean;
  created_at: string;
}
