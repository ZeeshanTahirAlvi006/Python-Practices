#Scenario 1
# with open ("books.txt","w") as f:
#     f.write("Data Science\n")
#     f.write("AI Basics\n")
# list = [ input("Enter the name of book to issue: ") ]
# with open("books.txt","r") as f:
#     books = [line.strip() for line in f]
# for i in list:
#     if i in books:
#         print(f"{i} issued successfully.")
#         with open("books.txt","w")as f:
#             for book in books:
#                 if book != i:
#                     f.write(book + "\n")        
#     else:
#         print(f"{i} is not available.")
# list = [ input("Enter the name of book to return: ") ]
# with open("books.txt","a") as f:
#     f.write(f"{list[0]}\n")

#Scenario 2
# marks = []
# with open("marks.txt","w") as f:
#     f.write("Ali: 70\n")
#     f.write("Ahmed: 85\n")
#     f.write("Sara: 90\n")
# with open("marks.txt","r") as f:
#     marks = [ line.strip() for line in f]
#     print(marks)
# marks_dict = {}
# for i in marks:
#     name,mark = i.split(":")
#     marks_dict[name]= int(mark)
# marks_dict["Ali"] = 75
# print(marks_dict)
# list = [f"{name}: {mark}\n" for name,mark in marks_dict.items()]
# with open( "marks.txt","w") as f:
#     f.writelines(list)

# Scenario 3
list = ["2026-05-08: 5000\n","2026-05-08: 5000\n","2026-05-08: 7000\n","2026-05-08: 12000\n","2026-05-08: 8000\n"]
def addSale(sale):
    backup = ""
    with open("Sales.txt","r") as f:
        backup = f.read()
    with open("Backup.txt","w") as f:
        f.write(backup)
    with open("Sales.txt","a") as f:
        for i in list:
            f.write(i)
            sale = i.split(":")
            sale = int(sale[1])
            if sale > 10000:
                f.write("High Sales day\n")
                f.write(f"Today's Sale: {sale}\n")
    
addSale(list)