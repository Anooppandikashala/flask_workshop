# Exercise 3 — Product Manager
# Build a product manager using a list of dictionaries and three functions:

# add_product(name, price, stock) — creates a product dict with an auto-incremented id and appends it to the list
# list_products() — prints all products; shows "In Stock" or "Sold Out" based on stock
# total_inventory_value() — returns the total value of all stock (price × stock summed)
# Then call all three functions to test them.

def main():
    products = []

    def add_product(name, price, stock):
        product = {
            "id": len(products) + 1,
            "name": name,
            "price": price,
            "stock": stock
        }
        products.append(product)
        print(f"Added: {name}")

    def list_products():
        if not products:
            print("No products.")
            return
        for p in products:
            status = "In Stock" if p["stock"] > 0 else "Sold Out"
            print(f"[{p['id']}] {p['name']} — ${p['price']} ({status})")

    def total_inventory_value():
        total = 0
        for p in products:
            total += p["price"] * p["stock"]
        return total

    add_product("T-Shirt", 20.0, 50)
    add_product("Jeans", 50.0, 0)
    add_product("Shoes", 40.0, 20)

    list_products()
    print(f"Inventory Value: ${total_inventory_value():.2f}")
    
if __name__ == "__main__":
    main()