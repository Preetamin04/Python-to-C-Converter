# Ultimate Master Test Case for Python-to-C Converter

def square(x):
    return x * x

def calculate_complex_sum(a, b):
    # Function calling another function
    s1 = square(a)
    s2 = square(b)
    return s1 + s2

def factorial(n):
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

def outer_function(x):
    def inner_function(y):
        return y * 10
    
    res = inner_function(x) + 5
    return res

# Main Logic
print("--- Ultimate Master Test ---")

# 1. Math and Floor Division
a = 15
b = 4
floor_res = a // b
power_res = 2 ** 5
print("Floor division of 15 // 4 is:", floor_res)
print("2 power 5 is:", power_res)

# 2. Boolean Logic
x = 10
y = 20
if x < y and not x == 0 or y == 100:
    print("Complex boolean logic passed")

# 3. Functions calling Functions
val = calculate_complex_sum(3, 4)
print("Sum of squares (3^2 + 4^2):", val)

# 4. Nested Loops (Multiplication Table snippet)
print("Multiplication Table (2x2):")
for i in range(1, 3):
    for j in range(1, 3):
        res = i * j
        print(i, "*", j, "=", res)

# 5. List Iteration
items = [10, 20, 30]
for item in items:
    if item > 15:
        print("Item", item, "is large")
