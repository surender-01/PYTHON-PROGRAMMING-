with open('example.txt', 'r') as file:
    content = file.read()
    char_count = len(content)
    print("Total number of characters:", char_count)