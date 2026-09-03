def num_digit_sum(n):
    sum = 0
    for i in str(n):
        sum += int(i)
    return sum
n = int(input("\nEnter a number to find the sum of its digits: "))
print(f"\nSum of the digits in {n} is {num_digit_sum(n)}\n")