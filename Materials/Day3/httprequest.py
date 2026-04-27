from flask import Flask
from flask import request
from flask import redirect, url_for

app = Flask(__name__)

@app.route("/")
def home():
    return "Home Page"

@app.route("/old-page")
def old_page():
    return redirect(url_for("home"))    # redirect to the home() function

@app.route("/about")
def about():
    return "About Page"

@app.route("/products")
def products():
    return "Products Page"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Form was submitted — process data
        username = request.form.get("username")
        password = request.form.get("password")
        return f"Logged in as: {username}"
    else:
        # Browser visiting the page — show the form
        return "Show login form here"

if __name__ == "__main__":
    app.run(debug=True)