def remove(_list_):
    return list(set(_list_))

_list_ = [2, 4, 4, 4, 6, 6, 6, 6, 6]
print(f"\nList before removing duplicates : {_list_}\n\nList after removing duplicate elements: {remove(_list_)}\n")