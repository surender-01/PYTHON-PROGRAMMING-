try: 
    print(10 / 0)
    list = []
    print(list[1])
    print(int("abc"))
    with open("non_existent_file.txt", 'r') as file:
        print(file.read())
    dict = {}
    print(dict["ace"])
    print(undefined_variable)

except Exception as e:
    print(f"Error Occured due to {e}")
finally:
    print("Prevented the system from crashing")