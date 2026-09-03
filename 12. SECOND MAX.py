def sec_max(_list_):
    rm_occurance =  list(set(_list_))
    sorted(_list_, reverse=True)
    return _list_[1]

_list_ = [2, 4, 4, 4, 6, 6, 6, 6, 6]
print(f"Second largest number in the list is {sec_max(_list_)}")