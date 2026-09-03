str = input("\nEnter any phrase: ")
n = input("Enter a character to count: ")
count = 0
for char in str:
    if char == n:
        count += 1
print(f"\nCount of {n} in {str} is {count}\n")