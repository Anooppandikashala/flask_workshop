from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
import json

app = Flask(__name__)
app.secret_key = "quickshop-secret-2025"


def load_products():
    with open("data/products.json", "r") as f:
        return json.load(f)


# --- Page Routes ---

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/products")
def products():
    all_products = load_products()
    category = request.args.get("category")

    if category:
        filtered = []
        for p in all_products:
            if p["category"] == category:
                filtered.append(p)
        all_products = filtered

    categories_set = set()
    for p in load_products():
        categories_set.add(p["category"])

    categories = []
    for c in categories_set:
        categories.append(c)

    return render_template(
        "products.html",
        products=all_products,
        categories=categories,
        selected_category=category
    )


@app.route("/product/<int:product_id>")
def product_detail(product_id):
    all_products = load_products()

    product = None
    for p in all_products:
        if p["id"] == product_id:
            product = p
            break

    if product is None:
        return "Product not found", 404

    return render_template("single_product.html", product=product)

@app.route("/cart/add/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    all_products = load_products()

    product = None
    for p in all_products:
        if p["id"] == product_id:
            product = p
            break

    if product is None or product["stock"] == 0:
        flash("Product unavailable.", "danger")
        return redirect(url_for("products"))

    qty = int(request.form.get("qty", 1))

    cart = session.get("cart", {})
    pid = str(product_id)

    if pid in cart:
        cart[pid]["qty"] += qty
    else:
        cart[pid] = {
            "id": product["id"],
            "name": product["name"],
            "price": product["price"],
            "qty": qty
        }

    session["cart"] = cart
    flash(f"'{product['name']}' added to cart!", "success")
    return redirect(url_for("products"))


if __name__ == "__main__":
    app.run(debug=True)
