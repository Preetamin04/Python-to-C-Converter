# Master Test Case for Python-to-C Converter

def factorial(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n - 1)

def check_even_odd(num):
    if num % 2 == 0:
        return "Even"
    else:
        return "Odd"

# Main Logic
print("--- Master Test Case ---")

# 1. User Input and Types
val = int(input("Enter a number for factorial: "))
res = factorial(val)
print("Factorial is:", res)

# 2. Lists and Loops
numbers = [1, 2, 3, 4, 5]
total = 0
for x in numbers:
    total += x
print("Sum of list:", total)

# 3. Nested Conditionals and Math
limit = 10
for i in range(1, limit):
    if i % 3 == 0:
        print(i, "is divisible by 3")
    elif i % 2 == 0:
        print(i, "is even")
    else:
        pass

# 4. Complex Math
power_val = 2 ** 3
print("2 power 3 is:", power_val)
