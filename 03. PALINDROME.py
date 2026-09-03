def palindrome(str):
    print(f"\nThe string '{str}' is a palindrome") if str.lower() == str.lower()[::-1] else print(f"\nThe string '{str}' is not a palindrome")

str = input("\nEnter a string to check if it is a palindrome: ")
palindrome(str)