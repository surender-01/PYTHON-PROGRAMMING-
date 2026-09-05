with open('example.txt', 'r') as file:
    with open('example_copy.txt', 'w+') as copy_file:
        content = file.read()
        copy_file.write(content)

        copy_file.seek(0)  
        print("Content of the copied file: ", copy_file.read())