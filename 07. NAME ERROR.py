try:
    x = int(input("Enter a number: "))
    y = int(input("Enter another number: "))
    print(y , z)
except NameError:
    print("Prevented the program from crashing due to a NameError.")
finally:
    print("Execution completed.")