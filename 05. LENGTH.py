str = input("\nEnter the sentence: ")
_str_ = str.split()
print(f"Length of the longest word in '{str}' is {max(_str_, key=len)}")