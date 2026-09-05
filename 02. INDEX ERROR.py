str = input("Enter a string: ")
index = int(input("Enter an index: "))

try:
    print(f"The character at index {index} is: '{str[index]}'")
except IndexError:
    print("Error: Index out of range.")
finally:
    print("Execution completed.")