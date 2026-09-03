list = [2, 4, 4, 4, 6, 6, 6, 6, 6]
n = int(input("\nEnter the element to be removed from the list: "))
print(f"\nList before removing occurrences of {n}: {list}\n")
list = [i for i in list if i != n]
print(f"List after removing all the occurrences of element {n} is : {list}\n")