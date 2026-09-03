n = int(input("\nEnter how many terms of the Fibonacci sequence you want: "))

a, b = 0, 1

while n > 0:
    print(a, end=" ")
    a, b = b, a + b
    n -= 1