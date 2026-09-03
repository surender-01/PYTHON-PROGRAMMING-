def lcm(a, b):
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    return (a * b) // gcd(a, b)

a, b = map(int, input("\nEnter two numbers separated by space to find the LCM: ").split())
print(f"\nLCM of {a} and {b} is {lcm(a, b)}\n")