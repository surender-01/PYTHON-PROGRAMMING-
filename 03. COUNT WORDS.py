with open('example.txt', 'r') as file:
    content = file.read()
    word_count = len(content.split())
    print("Total number of words:", word_count)