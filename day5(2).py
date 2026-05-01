# index error - try catch
# try:
#     list1 = [1,2,3]
#     list1[10]
# except IndexError:
#     print("invalid index")

# reverse string without using .reverse()
# string = "Hello world"
# print(string[::-1])

# split sentence into words and count
# sent = "I am Zeeshan"
# li = sent.split(" ")
# print(len(li))
# print(li)

# Check if a password is at least 8 characters long and contains at least one digit.
# pw = "123helloworld@"
# print(len(pw))
# oneDigit = False
# for x in pw:
#     if x.isdigit:
#         oneDigit= True
#         break
# if oneDigit:
#     print("String has one digit")

# Create a list of squares for all even numbers between 1 and 20.
# sq = [x*x for x in range(21) ]
# for x in sq:
#     print(x, end= " ")

# list with duplicates and sets to remove them
# li = [1,1,2,3,3,4,5,6,7,7,8]
# s = set(li)
# print(s)

# student = {"Name":"Zeeshan",
#            "ID":123,
#            "Marks":99}
# for x,y in student.items():
#     print(y)

# def fact(n):
#     if n in (0,1):
#         return 1
#     return n*fact(n-1)
# print(fact(0))

# cubes = {x: x*x*x for x in range(6)}
# print(cubes)

# li = [1,2,3]
# li2 = [5,6]
# li.extend(li2)
# print(li)

# tup = (10,20,30,50,40)
# print(tup[-2])
# print(tup[-1])

# student = {"Name":"Zeeshan",
#         "ID":123,
#         "Marks":99}
# student["Grade"] = "A"
# print(student)

# add_num = lambda x: x+10
# print(add_num(5))

# li = [1,2,3]
# li2 = [3,4,5,6]
# print(list(set(li).union(li2)))
# print(list(set(li).intersection(li2)))

# classroom = {
#     "student1":{
#         "name":"Zeeshan",
#         "Age":19,
#     },
# "student2":{
#     "name":"Daniyal",
#     "Age":19,
# }
# }
# li = ["He","hell","helloworld","hello","1"]
# li.sort()
# print(li)

# name = "Zeeshan"
# def change_name():
#     global name
#     name = "hannan"
# change_name()
# print(name)


# import math as m
# def function(num1 ,num2):
#     return num1 + num2,num1 * num2
# print(function(1,2))

# data = [[1,2],[3,4]]
# li1= data[1]
# print(li1[1])

# student = {"Name":"Zeeshan",
#         "ID":123,
#         "Marks":99}
# print(student.keys())

# li = [10, 20, 50, 60, 60, 80]
# sqr = {x : x*x for x in li if x >50}
# print(sqr)


# class Student:
#     def __init__(self,name,marks):
#         self.name = name
#         self.marks = marks
#     def display(self):
#         print(f"""Name: {self.name}
# Marks: {self.marks} """)
#     def update_marks(self,marks):
#             self.marks = marks
# students = [Student("Zeeshan",100),Student("Hasaan",100)]
# for x in students:
#     x.update_marks(101)
#     x.display()
    

# class Person:
#     def __init__(self,name,age):
#         self.name = name
#         self.age = age  
#     @property
#     def name(self):
#         return self._name
#     @name.setter
#     def name(self,name):
#         self._name = name
#     def print_role(self):
#         print(f"Name: {self.name}- Age: {self.age}")
#     def save(self):
#         with open(f"{self.name}.txt","a") as s:
#             s.write(f"Name: {self.name}- Age: {self.age}")
#     def extract_from_file(self):
#         with open(f"{self.name}.txt","r")as s:
#             print(s.read())

# class Student(Person):
#     def __init__(self,name,age):
#         super().__init__(name,age)
#     def print_role(self):
#         print("--- Student ---")
#         print(f"Name: {self.name}- Age: {self.age}")
#     def __str__(self):
#         return f"Name: {self.name}- Age: {self.age}"
# s = Student("Zeeshan",19)
# # s.print_role()
# # s.name = "Hannan"
# # print(s.name)
# # print(Student("Zeeshan",19))
# s.save()
# s.extract_from_file()
# s.save()


# import abc as a
# class Shape:
#     def __init__(self):
#         pass
#     @a.abstractmethod
#     def area(self):
#         pass
# class Square(Shape):
#     def __init__(self,length):
#         self.__length = length
#     @property
#     def length(self):
#         return self.__length
#     @length.setter
#     def length(self,length):
#         self.__length = length
#     def area(self):
#         print(f"Area: {self.__length * self.__length}")
# sqr = Square(2)
# sqr.length= 3
# sqr.area()

with open("notes.txt","w") as n:
    n.write(""" Hello
            python
            python2
            not
            in 
            my 
            love""")
with open("notes.txt","r")as n:
    while True:
        line = n.readline()
        if line:
            if "python" in line:
                print(line.strip())
        else:
            break
