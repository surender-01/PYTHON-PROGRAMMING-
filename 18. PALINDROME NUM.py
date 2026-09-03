def palindrome(num):
    return str(num) == str(num)[::-1]

num = int(input("\nEnter a number to check if it is a palindrome: "))
if palindrome(num):
    print(f"\n{num} is a palindrome number.\n")
else:
    print(f"\n{num} is not a palindrome number.\n")