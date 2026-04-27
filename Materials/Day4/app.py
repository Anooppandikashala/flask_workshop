from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
from functools import wraps
import json

from helpers import (
    register_user, verify_user, find_user_by_id,
    create_order, get_user_orders, load_orders, load_users
)

app = Flask(__name__)
app.secret_key = "quickshop-secret-2025"


# --- Decorators ---

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            flash("Please login to continue.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            flash("Please login.", "warning")
            return redirect(url_for("login"))
        user = find_user_by_id(session["user_id"])
        if not user or not user.get("is_admin"):
            flash("Admin access required.", "danger")
            return redirect(url_for("home"))
        return f(*args, **kwargs)
    return decorated


# --- Data ---

def load_products():
    with open("data/products.json", "r") as f:
        return json.load(f)


# --- Page Routes ---

@app.route("/")
def home():
    all_products = load_products()

    featured = []
    for p in all_products:
        if p["stock"] > 0:
            featured.append(p)
            if len(featured) == 3:
                break

    return render_template("index.html", featured=featured)


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

    return render_template("product.html", product=product)


# --- Cart Routes ---

@app.route("/cart")
def cart():
    cart = session.get("cart", {})

    total = 0
    for key in cart:
        item = cart[key]
        total += item["price"] * item["qty"]

    return render_template("cart.html", cart=cart, total=total)


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


@app.route("/cart/remove/<int:product_id>", methods=["POST"])
def remove_from_cart(product_id):
    cart = session.get("cart", {})
    pid = str(product_id)

    if pid in cart:
        name = cart[pid]["name"]
        del cart[pid]
        session["cart"] = cart
        flash(f"'{name}' removed.", "info")

    return redirect(url_for("cart"))


@app.route("/cart/clear", methods=["POST"])
def clear_cart():
    session.pop("cart", None)
    flash("Cart cleared.", "info")
    return redirect(url_for("cart"))


# --- Auth Routes ---

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")

        if not name or not email or not password:
            flash("All fields are required.", "danger")
            return redirect(url_for("register"))

        if password != confirm:
            flash("Passwords do not match.", "danger")
            return redirect(url_for("register"))

        if len(password) < 6:
            flash("Password must be at least 6 characters.", "danger")
            return redirect(url_for("register"))

        user, error = register_user(name, email, password)
        if error:
            flash(error, "danger")
            return redirect(url_for("register"))

        session["user_id"] = user["id"]
        flash(f"Welcome, {user['name']}! Account created.", "success")
        return redirect(url_for("home"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = verify_user(email, password)
        if user:
            session["user_id"] = user["id"]
            flash(f"Welcome back, {user['name']}!", "success")
            return redirect(url_for("home"))
        else:
            flash("Invalid email or password.", "danger")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("home"))


# --- Checkout & Orders ---

@app.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    cart = session.get("cart", {})
    if not cart:
        flash("Your cart is empty.", "warning")
        return redirect(url_for("cart"))

    total = 0
    for item in cart.values():
        total += item["price"] * item["qty"]

    if request.method == "POST":
        address = {
            "full_name": request.form.get("full_name"),
            "address":   request.form.get("address"),
            "city":      request.form.get("city"),
            "zip_code":  request.form.get("zip_code"),
        }
        if not all(address.values()):
            flash("Please fill in all address fields.", "danger")
            return redirect(url_for("checkout"))

        order = create_order(session["user_id"], cart, address)
        session.pop("cart", None)
        flash(f"Order #{order['id']} placed successfully!", "success")
        return redirect(url_for("order_confirmation", order_id=order["id"]))

    return render_template("checkout.html", cart=cart, total=total)


@app.route("/order/confirmation/<int:order_id>")
@login_required
def order_confirmation(order_id):
    order = None
    for o in load_orders():
        if o["id"] == order_id:
            order = o
            break

    if not order or order["user_id"] != session["user_id"]:
        return "Order not found", 404
    return render_template("order_confirmation.html", order=order)


@app.route("/orders")
@login_required
def orders():
    user_orders = get_user_orders(session["user_id"])
    user_orders.sort(key=lambda o: o["id"], reverse=True)
    return render_template("orders.html", orders=user_orders)


# --- Admin Routes ---

@app.route("/admin")
@admin_required
def admin_dashboard():
    all_products = load_products()
    all_orders = load_orders()
    all_users = load_users()

    total_revenue = 0
    for o in all_orders:
        total_revenue += o["total"]

    return render_template(
        "admin/dashboard.html",
        products=all_products,
        orders=all_orders,
        users=all_users,
        total_revenue=total_revenue
    )


@app.route("/admin/products/add", methods=["GET", "POST"])
@admin_required
def admin_add_product():
    if request.method == "POST":
        products = load_products()
        max_id = 0
        for p in products:
            if p["id"] > max_id:
                max_id = p["id"]
        new_product = {
            "id": max_id + 1,
            "name": request.form.get("name"),
            "price": float(request.form.get("price")),
            "stock": int(request.form.get("stock")),
            "category": request.form.get("category"),
            "description": request.form.get("description"),
            "image": request.form.get("image", "https://placehold.co/300x200")
        }
        products.append(new_product)
        with open("data/products.json", "w") as f:
            json.dump(products, f, indent=2)
        flash(f"Product '{new_product['name']}' added.", "success")
        return redirect(url_for("admin_dashboard"))
    return render_template("admin/add_product.html")


# --- API Routes ---

@app.route("/api/products")
def api_products():
    return jsonify(load_products())


@app.route("/api/products/<int:product_id>")
def api_product(product_id):
    all_products = load_products()

    product = None
    for p in all_products:
        if p["id"] == product_id:
            product = p
            break

    if product is None:
        return jsonify({"error": "Not found"}), 404

    return jsonify(product)


if __name__ == "__main__":
    app.run(debug=True)
