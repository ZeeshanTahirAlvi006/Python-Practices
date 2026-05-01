#Q1. Shopping Cart System
def shopping_cart():
    cart = [input("Enter item: ") for _ in range(5)]
    sum = 0
    for item in cart:
        print("Enter price for", item)
        while True:
            try:
                price = float(input())
                if price < 0:
                    print("Price cannot be negative. Please enter a valid price.")
                    continue
                sum += price
                break
            except ValueError:
                print("Invalid input! Please enter a numeric value.")
    print("Total cost of items in the cart:", sum)
    if sum > 2000:
        sum *= 0.9
        print("Total bill after 10% discount:", sum)
    else:
        print("Total bill (no discount):", sum)
#shopping_cart()

#Q2. Password Generator
import random as r
def password_gen():
    while True:
        username = input("Enter username: ")
        if not username:
            print("Username cannot be empty. Please enter a valid username.")
            continue
        password = ""
        for i in range(3):
            password += username[i]
        password += str(r.randint(1, 100))
        print("Generated password:", password)
        break
# password_gen()
def calculator():
    while True:
        try:
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            operator = input("Enter operator (+, -, *, /): ")
            if operator == '+':
                result = num1 + num2
            elif operator == '-':
                result = num1 - num2
            elif operator == '*':
                result = num1 * num2
            elif operator == '/':
                if num2 != 0:
                    result = num1 / num2
                else:
                    print("Division by zero is not allowed.")
                    continue
            else:
                print("Invalid operator! Please enter one of +, -, *, /.")
                continue
            print(f"Result: {num1} {operator} {num2} = {result}")
        except ValueError:
            print("Invalid input! Please enter valid numbers")
       
calculator()

