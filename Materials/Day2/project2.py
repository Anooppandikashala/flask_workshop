# Project B — Product Search CLI
# Build this from scratch. The full reference implementation is below.

def main():
    products = [
        {"id": 1, "name": "T-Shirt",  "price": 20.0, "category": "clothing"},
        {"id": 2, "name": "Jeans",    "price": 50.0, "category": "clothing"},
        {"id": 3, "name": "Shoes",    "price": 40.0, "category": "footwear"},
        {"id": 4, "name": "Sneakers", "price": 60.0, "category": "footwear"},
        {"id": 5, "name": "Hat",      "price": 15.0, "category": "accessories"},
    ]

    def search_by_name(query):
        query = query.lower()
        result = []
        for p in products:
            if query in p["name"].lower():
                result.append(p)
        return result

    def filter_by_category(category):
        category = str(category).lower()
        result = []
        for p in products:
            if p["category"] == category:
                result.append(p)
        return result


    def filter_by_price(max_price):
        result = []
        for p in products:
            if p["price"] <= max_price:
                result.append(p)
        return result

    def display(items):
        if not items:
            print("No products found.")
            return
        for p in items:
            print(f"  [{p['id']}] {p['name']} — ${p['price']} ({p['category']})")

    while True:
        print("\n1. Search by name")
        print("2. Filter by category")
        print("3. Filter by max price")
        print("4. Show all")
        print("0. Exit")
        choice = input("Choose: ")

        if choice == "1":
            q = input("Search: ")
            display(search_by_name(q))
        elif choice == "2":
            cat = input("Category (clothing/footwear/accessories): ")
            display(filter_by_category(cat))
        elif choice == "3":
            max_p = float(input("Max price: $"))
            display(filter_by_price(max_p))
        elif choice == "4":
            display(products)
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice")
            
if __name__ == "__main__":
    main()