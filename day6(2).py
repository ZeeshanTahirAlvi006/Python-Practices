
# Scenario 1: Book issuing and returning simulation
# Create or overwrite the books.txt with pre defined data.
with open("books.txt", "w") as f:  # open books.txt in write mode and recreate it if necessary and close automatically
    f.write("Data Science\n")
    f.write("AI Basics\n")

# Ask the user which book to issue.
list = [input("Enter the name of book to issue: ")]

# Read the current inventory.
with open("books.txt", "r") as f:
    books = [line.strip() for line in f]

# Issue the requested book if it is available.
for i in list:
    if i in books:
        print(f"{i} issued successfully.")
        # Rewrite the books.txt file without the issued book.
        with open("books.txt", "w") as f:
            for book in books:
                if book != i:
                    f.write(book + "\n")
    else:
        print(f"{i} is not available.")

# Ask the user for a book to return and append it to the inventory file.
list = [input("Enter the name of book to return: ")]
with open("books.txt", "a") as f:
    f.write(f"{list[0]}\n")

#  Scenario 2: Student marks update from file
marks = []
# Write initial marks data to marks.txt.
with open("marks.txt", "w") as f:
    f.write("Ali: 70\n")
    f.write("Ahmed: 85\n")
    f.write("Sara: 90\n")

# Read the marks.txt back and print the list.
with open("marks.txt", "r") as f:
    marks = [line.strip() for line in f]
    print(marks)

# Parse each line into a dictionary with integer scores.
marks_dict = {}
for i in marks:
    name, mark = i.split(":")
    marks_dict[name] = int(mark)

# Update Ali's mark and show the updated dictionary.
marks_dict["Ali"] = 75
print(marks_dict)

# Convert the dictionary back into formatted lines and overwrite marks.txt.
list = [f"{name}: {mark}\n" for name, mark in marks_dict.items()]
with open("marks.txt", "w") as f:
    f.writelines(list)

# Scenario 3
list = ["2026-05-08: 5000\n","2026-05-08: 5000\n","2026-05-08: 7000\n","2026-05-08: 12000\n","2026-05-08: 8000\n"]
def addSale(sale):
    backup = ""
    # Open Sales.txt in read mode to create a backup of Sales.txt
    with open("Sales.txt","r") as f:
        backup = f.read()
    # Open Sales.txt in write mode to create a backup
    with open("Backup.txt","w") as f:
        f.write(backup)
    # Open Sales.txt in append mode to add new sales.
    with open("Sales.txt","a") as f:
        for i in list:
            f.write(i)
            sale = i.split(":")
            sale = int(sale[1])
            if sale > 10000:
                f.write("High Sales day\n")
                f.write(f"Today's Sale: {sale}\n")
    
addSale(list)