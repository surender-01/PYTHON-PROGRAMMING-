n = int(input("\nEnter the number for which you want the factorial: "))

factorial = 1

while n > 0:
    factorial *= n
    n -= 1

print(f"\nFactorial of the number is {factorial}\n")    