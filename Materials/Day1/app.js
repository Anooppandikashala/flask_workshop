// The product name we want to show in the alert
const productName = "Classic T-Shirt";

// Track the current quantity
let quantity = 1;

// Get references to the HTML elements we need to control
const display   = document.getElementById("quantity-display");
const plusBtn   = document.getElementById("plus-btn");
const minusBtn  = document.getElementById("minus-btn");
const cartBtn   = document.getElementById("cart-btn");

// Clicking + increases quantity
plusBtn.addEventListener("click", function () {
  quantity++;
  display.textContent = quantity;
});

// Clicking − decreases quantity, but never goes below 1
minusBtn.addEventListener("click", function () {
  if (quantity > 1) {
    quantity--;
    display.textContent = quantity;
  }
});

// Clicking "Add to Cart" shows a confirmation alert
cartBtn.addEventListener("click", function () {
  alert("Added to cart: " + productName + " × " + quantity);
});