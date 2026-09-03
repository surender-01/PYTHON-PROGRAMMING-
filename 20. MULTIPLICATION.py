def multiplication(a):
    for i in range(1, 13):
        print(f"{a} x {i} = {a * i}")

a = int(input("\nEnter a number to print its multiplication table: "))
print(f"\nMultiplication table of {a}:\n")
multiplication(a)