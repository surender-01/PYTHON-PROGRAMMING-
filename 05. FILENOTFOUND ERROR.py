try:
    x = open(input("Enter the file name to open: "), 'r')
    txt = x.read()
    print(txt)
except FileNotFoundError:
    print("Error: File not found. Please check the file name and try again.")
finally:
    print("Execution completed.")