str = input("\nEnter any word: ")
print(f"\n{str} is a palindrome\n" if str.lower() == str.lower()[::-1] else f"\n{str} is not a palindrome\n")