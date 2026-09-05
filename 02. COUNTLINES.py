with open('example.txt', 'r') as file:
    line_count = file.readlines()
    print("Total number of lines:", len(line_count))
