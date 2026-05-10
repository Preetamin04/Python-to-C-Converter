def is_even(n):
    if n % 2 == 0:
        return True
    else:
        return False

num = int(input("Enter a number: "))

result = is_even(num)

if result == True:
    print("Even number")
else:
    print("Odd number")