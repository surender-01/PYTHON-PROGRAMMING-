def odd_even(n):
    print(f"\nThe number {n} is an even number") if n % 2 == 0 else print(f"\nThe number {n} is an odd number\n")

n = int(input("\nEnter a number to check if it is odd or even: "))
odd_even(n)