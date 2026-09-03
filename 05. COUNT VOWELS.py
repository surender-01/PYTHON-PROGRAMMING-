def count_vowels(str):
    c = 0
    for i in str.lower():
        if i in "aeiou":
            c += 1
    return c

str = input("\nEnter a string to count the number of vowels in it: ")
print(f"The number of vowels in the string '{str}' is {count_vowels(str)}\n")