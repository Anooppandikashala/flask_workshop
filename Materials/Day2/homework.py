# Homework — Shopping Cart with Save/Load and Discount
# Extends project1.py (ShoppingCart):
# 1. Save the cart to cart.json when the program ends
# 2. Load the cart from cart.json when the program starts
# 3. apply_discount(percent) method that discounts all items in the cart

import json
import os

CART_FILE = "cart.json"


class Product:
    def __init__(self, id, name, price, stock):
        self.id = id
        self.name = name
        self.price = price
        self.stock = stock

    def __str__(self):
        return f"{self.name} — ${self.price:.2f}"


class ShoppingCart:
    def __init__(self):
        self.items = {}   # {product_id: {"product": Product, "qty": int}}

    def add(self, product, qty=1):
        if product.stock < qty:
            print(f"Not enough stock for {product.name}")
            return
        if product.id in self.items:
            self.items[product.id]["qty"] += qty
        else:
            self.items[product.id] = {"product": product, "qty": qty}
        print(f"Added {qty}x {product.name} to cart")

    def remove(self, product_id):
        if product_id in self.items:
            del self.items[product_id]
            print("Item removed")
        else:
            print("Item not in cart")

    def total(self):
        total_value = 0
        for item in self.items.values():
            total_value += item["product"].price * item["qty"]
        return total_value

    def apply_discount(self, percent):
        if not 0 < percent < 100:
            print("Discount must be between 1 and 99 percent.")
            return
        for item in self.items.values():
            item["product"].price = round(item["product"].price * (1 - percent / 100), 2)
        print(f"{percent}% discount applied to all items.")

    def show(self):
        if not self.items:
            print("Your cart is empty.")
            return
        print("\n--- Your Cart ---")
        for item in self.items.values():
            p = item["product"]
            q = item["qty"]
            print(f"  {p.name} x{q}  = ${p.price * q:.2f}")
        print(f"  TOTAL: ${self.total():.2f}")
        print("-----------------\n")


def save_cart(cart):
    serializable = {}
    for pid, data in cart.items.items():
        serializable[str(pid)] = {
            "id": data["product"].id,
            "name": data["product"].name,
            "price": data["product"].price,
            "qty": data["qty"]
        }
    with open(CART_FILE, "w") as f:
        json.dump(serializable, f, indent=2)
    print("Cart saved.")


def load_cart(cart, catalog):
    if not os.path.exists(CART_FILE):
        return
    with open(CART_FILE, "r") as f:
        saved = json.load(f)
    for pid_str, item in saved.items():
        product = None
        for p in catalog:
            if p.id == item["id"]:
                product = p
                break
        if product:
            cart.items[product.id] = {"product": product, "qty": item["qty"]}
    print("Cart loaded from previous session.")


catalog = [
    Product(1, "T-Shirt", 20.0, 50),
    Product(2, "Jeans",   50.0, 10),
    Product(3, "Shoes",   40.0, 5),
]

cart = ShoppingCart()
load_cart(cart, catalog)

cart.add(catalog[0], 2)
cart.add(catalog[1], 1)
cart.show()

cart.apply_discount(10)
cart.show()

save_cart(cart)
