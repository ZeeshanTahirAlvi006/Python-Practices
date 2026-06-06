import pandas as pd
"""
Task 1
Create a Series containing marks of 5 students.
Requirements:
•	Display the Series
•	Display highest marks
•	Display average marks
"""
# marks = pd.Series([85,90,78,92,100])
# print("Series: ",marks)
# print("Highest marks: ",marks.max())
# print("Average Marks: ",marks.mean())

"""
Task 2
Create a DataFrame containing:
•	Name
•	Age
•	Department
•	GPA
Display:
•	First 3 rows
•	Information about DataFrame
•	Statistical summary
"""
# student_data = {
#     "Name":["Zeeshan","Daniyal","Hasaan","Zarak"],
#     "Age":[19,20,20,20],
#     "Department":["AI","AI","AI","AI"],
#     "GPA" : [3.75,3.50,3.70,3.90]
# }
# df = pd.DataFrame(student_data)
# print(df.head(3))
# print(df.info())
# print(df.describe()) 
"""
Task 3
Create a DataFrame of employee records.
Perform:
•	Filter employees with salary > 50000
•	Sort data by salary
•	Add a new bonus column
"""
# employee_data = {
#     "Name":["Zeeshan","Daniyal","Hasaan","Zarak"],
#     "Salary":[50000,60000,70000,80000],
# }
# emp_df = pd.DataFrame(employee_data)
# print(emp_df[emp_df["Salary"]>50000])
# print(emp_df.sort_values("Salary"))
# emp_df["Bonus"] = emp_df["Salary"]*0.10
# print(emp_df)
"""
Task 4
Load a CSV file and:
•	Display first 5 rows
•	Check missing values
•	Replace missing values with 0
"""
# df.to_csv("Students.csv",index = False)
# csvdf = pd.read_csv("Students.csv")
# csvdf.loc[4,"Name"] = "Hassan"
# print(csvdf.head(5))
# print(csvdf.isnull())
# print(csvdf.fillna(0))
"""
Task 5
Create a student grading system.
Requirements:
•	Store names and marks
•	Calculate average marks
•	Assign grades using conditions
•	Save output into CSV file
"""
# names =["Zeeshan","Daniyal","Hasaan","Zarak"]
# marks = []
# for i in names:
#     marks.append(int(input(f"Enter marks of {i} ")))
# grades = []
# for i in marks:
#     if i >= 90:
#         grades.append("A")
#     elif i >= 80:
#         grades.append("B")
#     elif i >= 70:
#         grades.append("C")
#     else:
#         grades.append("F")
# df = pd.DataFrame({"Names":names,"Marks":marks,"Grades":grades})
# df.to_csv("Students_data.csv",index = False)
# print(pd.read_csv("Students_data.csv"))
"""
Challenge Task 1
Design a hospital patient management system using Pandas.
Requirements:
•	Patient ID
•	Name
•	Age
•	Disease
•	Bill Amount
Perform:
•	Filtering
•	Sorting
•	Statistical analysis
•	CSV export
"""
# patient_data = {
#     "Name": [],
#     "Age": [],
#     "Disease": [],
#     "Bill Amount": []
# }
# while True:
#     try:
#         print("Choose from the menu: ")
#         print("1. Add patient")
#         print("2. Display Data")
#         print("3. Filter Data")
#         print("4. Statistical Analysis")
#         print("5. Sort Data")
#         print("6. Save Data")
#         print("7. Exit")
#         choice = int(input("Enter your choice: "))
#         if choice == 1:
#             patient = {
#                 "Name":input("Enter the name of the patient: "),
#                 "Age":int(input("Enter the age of the patient: ")),
#                 "Disease": input("Enter the name of disease: "),
#                 "Bill Amount": int(input("Enter the amount of bill:"))
#             }
#             patient_data["Name"].append(patient["Name"])
#             patient_data["Age"].append(patient["Age"])
#             patient_data["Disease"].append(patient["Disease"])
#             patient_data["Bill Amount"].append(patient["Bill Amount"])
#             df = pd.DataFrame(patient_data)
#             df.to_csv("patient_data.csv",index = False) 
#         elif choice == 2:
#             print(pd.read_csv("patient_data.csv"))
#         elif choice == 3:
#             while True:
#                 print("1. Filter by bill amount greater than")
#                 print("2. Filter by bill amount less than")
#                 print("3. Filter by Age greater than")
#                 print("4. Filter by Age less than")
#                 print("5. Filter by bill amount greater than")
#                 print("6. Filter by bill amount less than")
#                 print("7. Filter by patient name")
#                 print("8. Filter by disease")
#                 print("9. Exit")
#                 filter_choice = int(input("Enter your choice: "))
#                 if filter_choice == 1:
#                     print(df[df["Bill Amount"]>int(input("Enter the amount of bill: "))])
#                 elif filter_choice == 2:
#                     print(df[df["Bill Amount"]<int(input("Enter the amount of bill: "))])
#                 elif filter_choice == 3:
#                     print(df[df["Age"]>int(input("Enter the age: "))])
#                 elif filter_choice == 4:
#                     print(df[df["Age"]<int(input("Enter the age: "))])
#                 elif filter_choice == 5:
#                     print(df[df["Bill Amount"]>int(input("Enter the amount of bill: "))])
#                 elif filter_choice == 6:
#                     print(df[df["Bill Amount"]<int(input("Enter the amount of bill: "))])
#                 elif filter_choice == 7:
#                     print(df[df["Name"]==input("Enter the name: ")])
#                 elif filter_choice == 8:
#                     print(df[df["Disease"]==input("Enter the disease: ")])
#                 elif filter_choice == 9:
#                     break
#         elif  choice == 4:
#             print(df.describe())
#         elif  choice == 5:
#             while True:
#                 print("1. Sort by Name")
#                 print("2. Sort by Age")
#                 print("3. Sort by Disease")
#                 print("4. Sort by Bill Amount")
#                 print("5. Exit")
#                 sort_choice = int(input("Enter your choice: "))
#                 if sort_choice == 1:
#                     print(df.sort_values("Name"))
#                 elif sort_choice == 2:
#                     print(df.sort_values("Age"))
#                 elif sort_choice == 3:
#                     print(df.sort_values("Disease"))
#                 elif sort_choice == 4:
#                     print(df.sort_values("Bill Amount"))
#                 elif sort_choice == 5:
#                     break
#         elif  choice == 6:
#             df.to_csv("patient_data.csv",index = False)
#         elif choice == 7:
#             break

#     except ValueError:
#         print("Invalid value entered!")
#     finally:
#         print("Patient data added.")


"""
Challenge Task 2
Develop a sales analysis dashboard dataset using Pandas.
Requirements:
•	Product Name
•	Category
•	Quantity
•	Revenue
Perform:
•	Grouping
•	Revenue analysis
•	Top-selling product identification
"""

product_data = {
    "Product Name": [],
    "Category": [],
    "Quantity": [],
    "Revenue": []
}

while True:
    try:
        print("\nMenu:")
        print("1. Add Product")
        print("2. Display Data")
        print("3. Filter Data")
        print("4. Grouping")
        print("5. Revenue Analysis")
        print("6. Top-selling Product")
        print("7. Save Data")
        print("8. Exit")
        
        choice = int(input("Enter your choice: "))
        
        if choice == 1:
            product = {
                "Product Name": input("Enter product name: "),
                "Category": input("Enter product category: "),
                "Quantity": int(input("Enter quantity sold: ")),
                "Revenue": float(input("Enter revenue generated: "))
            }
            product_data["Product Name"].append(product["Product Name"])
            product_data["Category"].append(product["Category"])
            product_data["Quantity"].append(product["Quantity"])
            product_data["Revenue"].append(product["Revenue"])
            df = pd.DataFrame(product_data)
            df.to_csv("sales_data.csv", index=False)
            print("Product added successfully!")
            
        elif choice == 2:
            print(pd.read_csv("sales_data.csv"))
            
        elif choice == 3:
            print("\nFilter Options:")
            print("1. By Revenue (>)")
            print("2. By Revenue (<)")
            print("3. By Quantity (>)")
            print("4. By Quantity (<)")
            print("5. By Product Name")
            print("6. By Category")
            print("7. Exit Filter")
            
            filter_choice = int(input("Enter filter choice: "))
            
            if filter_choice == 1:
                print(df[df["Revenue"] > float(input("Enter revenue threshold: "))])
            elif filter_choice == 2:
                print(df[df["Revenue"] < float(input("Enter revenue threshold: "))])
            elif filter_choice == 3:
                print(df[df["Quantity"] > int(input("Enter quantity threshold: "))])
            elif filter_choice == 4:
                print(df[df["Quantity"] < int(input("Enter quantity threshold: "))])
            elif filter_choice == 5:
                print(df[df["Product Name"] == input("Enter product name: ")])
            elif filter_choice == 6:
                print(df[df["Category"] == input("Enter category name: ")])
            elif filter_choice == 7:
                continue
            else:
                print("Invalid filter choice.")
            
        elif choice == 4:
            print("\nGrouped by Category:")
            print(df.groupby("Category").sum())
            
        elif choice == 5:
            print("\nRevenue Analysis:")
            print(f"Total Revenue: {df['Revenue'].sum():.2f}")
            print(f"Average Revenue: {df['Revenue'].mean():.2f}")
            print(f"Max Revenue: {df['Revenue'].max():.2f}")
            print(f"Min Revenue: {df['Revenue'].min():.2f}")
            
        elif choice == 6:
            print("\nTop-selling Products:")
            print(df.nlargest(3, 'Revenue'))
            
        elif choice == 7:
            df.to_csv("sales_data.csv", index=False)
            print("Data saved successfully!")
            
        elif choice == 8:
            break
            
        else:
            print("Invalid choice. Please try again.")
            
    except ValueError:
        print("Invalid value entered. Please enter a valid number.")
    except Exception as e:
        print(f"An error occurred: {e}")
