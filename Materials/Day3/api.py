# Session 4 — REST API Example
# GET /api/products        — list all products
# GET /api/products/<id>   — get single product
# POST /api/products       — create new product
# DELETE /api/products/<id>— delete a product

from flask import Flask, request, jsonify

app = Flask(__name__)

products_db = [
    {"id": 1, "name": "T-Shirt",  "price": 20.0, "stock": 50, "category": "clothing"},
    {"id": 2, "name": "Jeans",    "price": 50.0, "stock": 30, "category": "clothing"},
    {"id": 3, "name": "Shoes",    "price": 40.0, "stock": 20, "category": "footwear"},
]


@app.route("/api/products", methods=["GET"])
def api_get_products():
    return jsonify(products_db)


@app.route("/api/products/<int:product_id>", methods=["GET"])
def api_get_product(product_id):
    product = None
    for p in products_db:
        if p["id"] == product_id:
            product = p
            break

    if product is None:
        return jsonify({"error": "Product not found"}), 404

    return jsonify(product)


@app.route("/api/products", methods=["POST"])
def api_create_product():
    data = request.get_json()

    if not data or "name" not in data or "price" not in data:
        return jsonify({"error": "name and price are required"}), 400

    max_id = 0
    for p in products_db:
        if p["id"] > max_id:
            max_id = p["id"]

    new_product = {
        "id": max_id + 1,
        "name": data["name"],
        "price": data["price"],
        "stock": data.get("stock", 0),
        "category": data.get("category", "general"),
    }
    products_db.append(new_product)
    return jsonify(new_product), 201


@app.route("/api/products/<int:product_id>", methods=["DELETE"])
def api_delete_product(product_id):
    global products_db

    found = False
    new_list = []
    for p in products_db:
        if p["id"] == product_id:
            found = True
            continue
        new_list.append(p)

    if not found:
        return jsonify({"error": "Product not found"}), 404

    products_db = new_list
    return jsonify({"message": "Product deleted"})


if __name__ == "__main__":
    app.run(debug=True)
