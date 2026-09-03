str = input("\nEnter any numbers: ")
print(f"Data Type of Input: {type(str).__name__}")
float = float(str)
print(f"Data Type of Input after explicit type convertion: {type(float).__name__}\n")