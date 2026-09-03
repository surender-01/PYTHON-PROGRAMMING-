def natural_sum(n):
    if n < 1:
        return 0
    else:
        return n + natural_sum(n - 1)

n = int(input("\nEnter a number to find the sum of natural numbers up to that number: "))
print(f"\nSum of natural numbers up to {n} is {natural_sum(n)}\n")