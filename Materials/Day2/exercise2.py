# Exercise 2 — Simple Calculator
# Defines four functions: add, subtract, multiply, divide
# The divide function returns an error message if dividing by zero
# Asks the user for two numbers and an operator (+, -, *, /)
# Calls the correct function and prints the result

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return "Error: Cannot divide by zero"
    return a / b

print("Simple Calculator")
a = float(input("First number: "))
op = input("Operator (+, -, *, /): ")
b = float(input("Second number: "))

if op == "+":
    print(f"Result: {add(a, b)}")
elif op == "-":
    print(f"Result: {subtract(a, b)}")
elif op == "*":
    print(f"Result: {multiply(a, b)}")
elif op == "/":
    print(f"Result: {divide(a, b)}")
else:
    print("Invalid operator")
