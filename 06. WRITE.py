line = ["ONE", "PIECE", "IS", "REAL"]
with open('example.txt', 'a') as file:
    for item in line:
        file.write(item + "\n")
print("List of strings written to the file successfully.")