# Project A — Shopping Cart Simulator
# Build this from scratch. The full reference implementation is below.

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

    # def total(self):
    #     return sum(
    #         item["product"].price * item["qty"]
    #         for item in self.items.values()
    #     )
    
    def total(self):
        total_value = 0
        for item in self.items.values():
            total_value += item["product"].price * item["qty"]
        return total_value

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


# Test it
catalog = [
    Product(1, "T-Shirt", 20.0, 50),
    Product(2, "Jeans",   50.0, 10),
    Product(3, "Shoes",   40.0, 0),
]

cart = ShoppingCart()
cart.add(catalog[0], 2)
cart.add(catalog[1], 1)
cart.add(catalog[2], 1)   # should warn — out of stock
cart.show()