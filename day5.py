class Account:
    def __init__(self,acc_no, balance):
        self.__acc_no = acc_no
        self.__balance  = balance
    def withdraw(self,amount):
        if amount <=0:
            print("Invalid amount")
        elif amount > self.__balance:
            print("Insufficient funds")
        else:
            self.__balance -= amount
            print(f"PKR {amount} deducted from account {self.__acc_no}. New balance {self.__balance}")
    def deposit(self,amount):
        if amount <= 0:
            print("Invalid amount")
        else:
            self.__balance += amount
            print(f"PKR {amount} deposited to account {self.__acc_no}. New balance {self.__balance}")

# acc1 = Account(123,123)
# acc1.deposit(100)
# acc1.deposit(0)
# acc1.deposit(-10)
# acc1.withdraw(-10)
# acc1.withdraw(0)
# acc1.withdraw(224)
# acc1.withdraw(223)

class Student:
    def __init__(self,name):
        self.name = name
        self.marks = {}
    def add_marks(self,subject,marks):
        if marks < 0:
            print("Invalid marks")
        else:
            self.marks[subject] = marks
    def calc_avg(self):
        if not self.marks:
            raise Exception("No value found")
        else:
            print(f"Average: {sum(self.marks.values())/len(self.marks)}")
# hassan = Student("hassan")
# hassan.add_marks("PFAI",100)
# hassan.add_marks("PFAI",90)
# hassan.add_marks("PFAI",80)
# hassan.add_marks("PFAI",70)
# hassan.add_marks("PFAI",60)
# hassan.calc_avg()

class Employee:
    def __init__(self,name,salary):
        self.name = name
        self.__salary = salary
    def get_sal(self):
        return self.__salary
# EmployeeList = [Employee("Zeeshan",100000),Employee("Daniyal",99000)]
# highest = max(EmployeeList ,key = lambda e : e.get_sal())
# print(highest.get_sal())

class Library:
    def __init__(self):
        self.books = {}
    def add_book(self,book_name):
        self.books[book_name] = True
    def issue_book(self,book_name):
        if not self.books.get(book_name,False):
            print("Book not available")
        else:
            self.books[book_name] = False
            print(f"{book_name} issued!")

# lib = Library()
# lib.add_book("Harry Potter")
# lib.issue_book("Harry Potter")
# lib.issue_book("Harry Potter")

