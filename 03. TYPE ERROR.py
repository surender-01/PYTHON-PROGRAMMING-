str = int(input("Enter a number: "))
try:
    result = 10 / str
    print(f"The result of division is: {result}")
except TypeError:
    print("Error: Invalid type for division.")
finally:
    print("Execution completed.")