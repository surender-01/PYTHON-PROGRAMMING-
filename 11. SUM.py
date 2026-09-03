def Sum(list):
    sum = 0
    for i in list:
        sum += i
    return sum

list = [1, 10, 100, 1000, 10000, 100000]
print(f"Sum of the elements in the list is {Sum(list)}")