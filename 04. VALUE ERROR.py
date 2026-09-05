try:
    a = int(input("Enter your age: "))
except ValueError:
    print("Error: Invalid input. Please enter a valid integer for age.")
    a = int(input("Enter your age: "))
finally:
    print("Eligible for voting." if a >= 18 else "Not eligible for voting.")
    print("Execution completed.")