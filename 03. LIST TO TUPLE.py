list = ["list", 67, 3.14, True, ("tuple", 67), {"set"}, {"dict": 67}]
print(f"\n LIST : {list}\nData Type of the list before convertion : {type(list).__name__}")
tuple = tuple(list)
print(f"\nData Type of the list after explicit type convertion: {type(tuple).__name__}")
print(f" TUPLE : {tuple}\n ")