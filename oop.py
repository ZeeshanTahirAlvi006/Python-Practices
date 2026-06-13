#Task 1 : Student Management System
class Student:
    dep = "AI"
    def __init__(self,studentID,name,cgpa):
        self.studentId = studentID
        self.name =name
        self.cgpa = cgpa
    def display(self):
        if self.cgpa >= 3.5:
            print(f"{self.name} qualifies for Dean's List")
        else:
            print(f"{self.name} does not qualify for Dean's List")
        print(f"""Student Details\nName:{self.name}\nStudentID:{self.studentId}\nDepartment:{Student.dep}\nCGPA:{self.cgpa}""")

# students = {
#     "name" :["Zeeshan","Abdullah","Saad"],
#     "StudentID": ["F2024376279","F2024376297","F2024376257"],
#     "CGPA":[3.75,3.91,3.70]
# }
# obj =[]
# for i in range(len(students["name"])):
#     obj.append(Student(students["StudentID"][i],students["name"][i],students["CGPA"][i]))
# for o in obj:
#     print("------------")
#     o.display()

#Task 2 : Bank Account Management System
class BankAccount:
    def __init__(self,accNum,name,initialBalance):
        self.accNum = accNum
        self.name = name
        self.__balance = initialBalance
    def deposit(self,amount):
        if amount > 0:
            self.__balance += amount
            print(f"Deposited: {amount}")
    def withdraw(self,amount):
        if amount > self.__balance:
            print("Insufficient Balance!")
        else:
            self.__balance -= amount
            print(f"Withdrawn: {amount}")
    def checkBalance(self):
        print(f"Account Details\nAccountHolder:{self.name}\nAccountNumber:{self.accNum}\nBalance:{self.__balance}")

# acc = BankAccount("1002345","Zeeshan",5000)
# print("------------")
# acc.checkBalance()
# acc.deposit(1500)
# acc.withdraw(2000)
# acc.withdraw(6000)
# acc.checkBalance()

#Task 3 : Employee Salary System
class Employee:
    compName = "TechCorp"
    def __init__(self,empID,name,salary):
        self.empId = empID
        self.name = name
        self.salary = salary
    def calculateAnnualSalary(self):
        return self.salary * 12
    def display(self):
        print(f"""Employee Details\nCompany:{Employee.compName}\nEmployeeID:{self.empId}\nName:{self.name}\nMonthlySalary:{self.salary}\nAnnualSalary:{self.calculateAnnualSalary()}""")

employees = {
    "empID": ["E001","E002","E003"],
    "name": ["Zeeshan","Abdullah","Saad"],
    "salary": [45000,55000,60000]
}
# empObj = []
# for i in range(len(employees["empID"])):
#     empObj.append(Employee(employees["empID"][i],employees["name"][i],employees["salary"][i]))
# for e in empObj:
#     print("------------")
#     e.display()

#Task 4 : Library Management System
class Book:
    def __init__(self,bookID,title,author):
        self.bookId = bookID
        self.title = title
        self.author = author
        self.available = True
    def issueBook(self):
        if self.available:
            self.available = False
            print(f"Issued '{self.title}' successfully.")
        else:
            print(f"'{self.title}' is already issued.")
    def returnBook(self):
        if not self.available:
            self.available = True
            print(f"Returned '{self.title}' successfully.")
        else:
            print(f"'{self.title}' is already available.")
    def display(self):
        status = "Available" if self.available else "Issued"
        print(f"Book Details\nBookID:{self.bookId}\nTitle:{self.title}\nAuthor:{self.author}\nStatus:{status}")

booksData = {
    "bookID": ["B01","B02","B03","B04","B05"],
    "title": ["Python Programming","Machine Learning","Deep Learning","Data Structures","Discrete Math"],
    "author": ["John Doe","Jane Smith","Ian Goodfellow","G. Karumanchi","Kenneth Rosen"]
}
# books = []
# for i in range(len(booksData["bookID"])):
#     books.append(Book(booksData["bookID"][i],booksData["title"][i],booksData["author"][i]))
# print("------------")
# print("Initial Library Status:")
# for b in books:
#     print("------------")
#     b.display()
# print("------------")
# books[1].issueBook()
# books[1].returnBook()
# print("------------")
# print("Updated Library Status:")
# for b in books:
#     print("------------")
#     b.display()

#Task 5 : University Management System
class Person:
    def __init__(self,name,age):
        self.name = name
        self.age = age
    def display(self):
        print(f"Name:{self.name}\nAge:{self.age}")

class Student(Person):
    def __init__(self,name,age,rollNum,dep):
        super().__init__(name,age)
        self.rollNum = rollNum
        self.dep = dep
    def display(self):
        super().display()
        print(f"RollNum:{self.rollNum}\nDepartment:{self.dep}")

class Teacher(Person):
    def __init__(self,name,age,empID,subject):
        super().__init__(name,age)
        self.empId = empID
        self.subject = subject
    def display(self):
        super().display()
        print(f"EmployeeID:{self.empId}\nSubject:{self.subject}")

# s = Student("Daniyal",20,"F2024376200","AI")
# t = Teacher("Dr. Hasaan",45,"T5001","Computer Science")
# print("------------")
# s.display()
# print("------------")
# t.display()

#Task 6 : Hospital Management System
class Person:
    def __init__(self,name,age):
        self.name = name
        self.age = age
    def display(self):
        print(f"Name:{self.name}\nAge:{self.age}")

class Patient(Person):
    def __init__(self,name,age,patientID,disease):
        super().__init__(name,age)
        self.patientId = patientID
        self.disease = disease
    def display(self):
        super().display()
        print(f"PatientID:{self.patientId}\nDisease:{self.disease}")

class IndoorPatient(Patient):
    def __init__(self,name,age,patientID,disease,roomNum,admDate):
        super().__init__(name,age,patientID,disease)
        self.roomNum = roomNum
        self.admDate = admDate
    def display(self):
        super().display()
        print(f"RoomNum:{self.roomNum}\nAdmissionDate:{self.admDate}")

# ip = IndoorPatient("Zarak",35,"P302","Flu","Room 105","12-06-2026")
# print("------------")
# ip.display()

#Task 7 : Online Payment System
class Payment:
    def pay(self,amount):
        print(f"Processing payment of {amount}")

class CreditCardPayment(Payment):
    def pay(self,amount):
        print(f"Paid {amount} using Credit Card")

class JazzCashPayment(Payment):
    def pay(self,amount):
        print(f"Paid {amount} using JazzCash")

class BankTransferPayment(Payment):
    def pay(self,amount):
        print(f"Paid {amount} using Bank Transfer")

# payments = [
#     CreditCardPayment(),
#     JazzCashPayment(),
#     BankTransferPayment()
# ]
# for p in payments:
#     print("------------")
#     p.pay(5000)

#Task 8 : AI Model Evaluation System
from abc import ABC, abstractmethod

class AIModel(ABC):
    @abstractmethod
    def evaluate(self):
        pass

class ClassificationModel(AIModel):
    def __init__(self,accuracy):
        self.accuracy = accuracy
    def evaluate(self):
        print(f"Classification Evaluation\nAccuracy:{self.accuracy}")

class RegressionModel(AIModel):
    def __init__(self,rmse):
        self.rmse = rmse
    def evaluate(self):
        print(f"Regression Evaluation\nRMSE:{self.rmse}")

# cModel = ClassificationModel(0.92)
# rModel = RegressionModel(2.5)
# print("------------")
# cModel.evaluate()
# print("------------")
# rModel.evaluate()

#Task 9 : University Information System
class University:
    uniName = "FAST NUCES"
    @classmethod
    def changeUniName(cls,newName):
        cls.uniName = newName
    def display(self):
        print(f"UniversityName: {University.uniName}")

class StudentRecord:
    def __init__(self,name,rollNum):
        self.name = name
        self.rollNum = rollNum
    def display(self):
        print(f"Student Record\nName:{self.name}\nRollNum:{self.rollNum}\nUniversity:{University.uniName}")

# studentsList = [
#     StudentRecord("Zeeshan","F2024376279"),
#     StudentRecord("Abdullah","F2024376297")
# ]
# print("------------")
# print("Before University Name Change:")
# for s in studentsList:
#     print("------------")
#     s.display()
# University.changeUniName("ITU Lahore")
# print("------------")
# print("After University Name Change:")
# for s in studentsList:
#     print("------------")
#     s.display()

#Task 10 : AI Research Repository
class ResearchProject:
    def __init__(self,title,area,accuracy):
        self.title = title
        self.area = area
        self.teamMembers = []
        self.accuracy = accuracy
    def addTeamMember(self,name):
        self.teamMembers.append(name)
    def determineStatus(self):
        if self.accuracy >= 90:
            return "Excellent"
        elif self.accuracy >= 75:
            return "Good"
        else:
            return "Needs Improvement"
    def display(self):
        members = ", ".join(self.teamMembers)
        print(f"Project Details\nTitle:{self.title}\nArea:{self.area}\nMembers:{members}\nAccuracy:{self.accuracy}%\nStatus:{self.determineStatus()}")

p1 = ResearchProject("Autonomous Driving","Computer Vision",92)
p1.addTeamMember("Zeeshan")
p1.addTeamMember("Abdullah")
p2 = ResearchProject("Medical Chatbot","NLP",84)
p2.addTeamMember("Saad")
p2.addTeamMember("Daniyal")
p3 = ResearchProject("Stock Predictor","Time Series",68)
p3.addTeamMember("Zarak")
p3.addTeamMember("Hasaan")
projects = [p1,p2,p3]
for p in projects:
    print("------------")
    p.display()
