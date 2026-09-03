def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

a, b = map(int, input("\nEnter two numbers separated by space to find the GCD: ").split())
print(f"\nGCD of {a} and {b} is {gcd(a, b)}\n")