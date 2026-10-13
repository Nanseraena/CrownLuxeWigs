# API examples

## 1. Browse published products

`GET /api/v1/products/?search=curly&hair_type=human&ordering=-created_at`

## 2. Add selected variant to cart

For a guest, create a UUID in the frontend once per guest session and send it as `X-Cart-Token` on every cart request.

```http
POST /api/v1/cart/items/
Content-Type: application/json
X-Cart-Token: 9c4e6db6-95c4-4b36-b1b4-8f74c65ac9b7

{"variant_id": 12, "quantity": 1}
```

The response includes `cart.token`, `cart.items`, `cart.item_count`, and `cart.subtotal`. Use the returned token if a new cart was created. The server controls price and validates stock.

## 3. Change quantity

```http
PATCH /api/v1/cart/items/42/
Content-Type: application/json
X-Cart-Token: 9c4e6db6-95c4-4b36-b1b4-8f74c65ac9b7

{"quantity": 2}
```

## 4. Remove cart line

`DELETE /api/v1/cart/items/42/` with the same cart token header.

## 5. Checkout

`POST /api/v1/checkout/` with `customer_name`, `email`, `phone`, and `delivery_address`. Checkout creates an order with pending payment, snapshots line prices, decrements stock within a database transaction, and clears the cart. Do not expose a customer-facing “payment successful” state until a verified provider callback updates payment status.
