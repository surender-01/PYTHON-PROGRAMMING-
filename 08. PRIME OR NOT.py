def prime(n):
    if n == 0: print("Zero is neither prime nor composite number")
    if n > 1:
        for i in range(2, n):
            if n % i == 0:
                print(f"\n{n} is not a prime number\n")
                break
        else:
            print(f"\n{n} ia a prime number\n")
    else:
        print(f"\n{n} is not a prime number\n")

n = int(input("\nEnter a number to check if it is prime: "))
prime(n)