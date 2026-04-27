# Exercise 1 — Product Info Collector
# Write a program that:
# 1. Asks the user to enter a product name
# 2. Asks for the price
# 3. Asks for the quantity
# 4. Prints: Total for [name]: $[price * quantity]

name = input("Product name: ")
price = float(input("Price: $"))
qty = int(input("Quantity: "))
total = price * qty
print(f"Total for {name}: ${total:.2f}")
