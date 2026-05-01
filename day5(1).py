class BillingSystem:
    def __init__(self,name):
        self.name = name
        self.items = {}
        self.total = 0
    def add_item(self):
        while True:
            print("Enter E to exit")
            try:
                item_name = input("Enter the name of item: ")
                if not item_name:
                    continue
                if item_name == "E":
                    break
                price = int(input("Enter the price: "))
                if price < 1:
                    print("Invalid amount")
                self.items[item_name] = price
                self.total += price
            except ValueError:
                print("Invalid number")
        if self.total > 1000:
            self.total -= self.total * 0.10
            print("10% discount applied for bills above 1000")
    def print_bill(self):
        if not self.items:
            print("No bill to display")
        else:
            for key,value in self.items.items():
                print(f"{key}: {value}")
            print("Total:",self.total)

# b1 = BillingSystem("Zeeshan")
# b1.add_item()
# b1.print_bill()

class Employee:
    def __init__(self,name,salary):
        self.name = name
        self.__salary = salary
    def get_salary(self):
        return self.__salary
    
# Employees = [Employee("Zeeshan",100000),Employee("Daniyal",100000),Employee("Hasaan",99000),Employee("Zarak",98000)]
# filter = [x for x in Employees if x.get_salary() > 98000]
# average = 0
# for x in filter:
#     average += x.get_salary()
# average /= len(filter)
# highest = max(Employees , key = lambda e: e.get_salary())
# highest = highest.get_salary()
# bonus = [x for x in filter if x.get_salary() > 99000]
# print("Report")
# print(f"Average Salary: {int(average)}")
# print(f"Highest Salary: {highest}")
# print("Employees Eligible for bonus")
# for x in bonus:
#     print(x.name)

class Library:
    def __init__(self):
        self.books = {}
    def add_books(self):
        while True:
            print("Enter E/e to exit")
            try:
                title = input("Enter the title of book: ")
                if not title:
                    continue
                if title in ["E","e"]:
                    break
                copies = int(input("Enter available copies: "))
                if copies < 1:
                    print("Invalid value")
                    continue
                self.books[title] = copies
            except ValueError:
                print("invalid value")
    def show_books(self):
        if not self.books:
            print("No available books in catalogue")
        for key,value in self.books.items():
            print(f"{value}: {key}")
    def issue_book(self,title):
        if not title:
            print("No title entered")
            return
        for title in self.books:
            if self.books[title]>0:
                self.books[title] -= 1
                print(f"{title} issued!")
                return
            else:
                print(f"{title} not available")
                return
# Lib = Library()
# Lib.add_books()
# Lib.issue_book("harry potter")
# Lib.issue_book("harry potter")

class user:
    def __init__ (self, name,age):
        self.name = name
        self.age = age
    def display_user(self):
        print(f"Name: {self.name}")
        print(f"Age: {self.age}")

class Student(user):
    def __init__(self,name,age,roll_no):
        super().__init__(name,age)
        self.roll_no = roll_no
    def display_user(self):
        print(f"Name: {self.name}")
        print(f"Age: {self.age}")
        print(f"Roll #: {self.roll_no}")
class Employee(user):
    def __init__(self,name,age,employee_id):
        super().__init__(name,age)
        self.employee_id = employee_id
    def display_user(self):
        print(f"Name: {self.name}")
        print(f"Age: {self.age}")
        print(f"Employee #: {self.employee_id}")
users = [Student("Zeeshan",19,"F2024376279"),Employee("Daniayl",19,"F2024376281")]
# for x in users:
#     x.display_user()

class Shape:
    def __init__ (self):
        pass
    def area(self):
        pass
class Circle(Shape):
    def __init__(self,radius):
        self.radius = radius
    def area(self):
        print(f"Area of Circle: {int(3.14*self.radius*self.radius)}")
class Rectangle(Shape):
    def __init__(self,length,breadth):
        self.length = length 
        self.breadth = breadth
    def area(self):
        print(f"Area of Rectangle: {int(self.length * self.breadth)}")
shapes = [Circle(2),Rectangle(2,4),Circle(3),Rectangle(3,6)]
for x in shapes:
    x.area()
    