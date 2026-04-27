# Exercise 1 — Routes Practice
# Add these routes to app.py:
# 1. /           — returns "Welcome to QuickShop!"
# 2. /products   — returns "All Products"
# 3. /product/<int:id>  — returns "Product ID: {id}"
# 4. /api/hello  — returns JSON {"message": "Hello from Flask!"}

from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to QuickShop!"

@app.route("/products")
def products():
    return "All Products"

@app.route("/product/<int:id>")
def product_detail(id):
    return f"Product ID: {id}"

@app.route("/api/hello")
def api_hello():
    return jsonify({"message": "Hello from Flask!"})

if __name__ == "__main__":
    app.run(debug=True)
