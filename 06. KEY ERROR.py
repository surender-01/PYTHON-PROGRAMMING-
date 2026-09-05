dict = {"name": "Alice", "age": 30}
try:
    key = input("Enter a key to access the dictionary: ")
    value = dict[key]
    print(f"The value for '{key}' is: {value}")
except KeyError:
    print(f"Error: Key '{key}' not found in the dictionary.")
finally:
    print("Execution completed.")