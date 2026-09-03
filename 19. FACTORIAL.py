def factorial(n):
    fact = 1
    for i in range(1, n + 1):
        fact *= i
    return fact

a = int(input("\nEnter a number to find its factorial: "))
print(f"\nFactorial of {a} is {factorial(a)}\n")