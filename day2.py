print("""Name: Zeeshan Tahir
      Roll Number: F2024376279
      Section: A9""")
print("""Q8: Write a program that takes a number from user and check either the give number
is positive/negative/zero. Also check the given number is even/odd, and lastly check
the given number is prime or not. Output and input are clearly mentioned below. You
have followed all the program statement instructions.""")
num = int(input("Enter a number: "))
positive = False
negative = False
zero = False
even = False
odd = False
prime = True

if num > 0:
    positive = True 
elif num < 0:
    negative = True
else:
    zero = True
if num % 2 == 0:
    even = True
else:
    odd = True
if num > 1:
    prime = True
    if num == 2:
        prime = True
    else:
        for i in range(2,num):
            if(num % i == 0):
                prime = False
                break

if zero:
    print(f"{num} is Zero")        
elif (positive  and even and prime):
    print(f"{num} is Positive Even and Prime Number")
elif(positive and even and not prime):
    print(f"{num} is Positive Even and Not Prime Number")
elif(positive and odd and prime):
    print(f"{num} is Positive Odd and Prime Number")
elif(positive and odd and not prime):
    print(f"{num} is Positive Odd and Not Prime Number")
elif(negative and even and prime):
    print(f"{num} is Negative Even and Prime Number")
elif(negative and even and not prime):
    print(f"{num} is Negative Even and Not Prime Number")
elif(negative and odd and prime):

    print(f"{num} is Negative Odd and Prime Number")
elif(negative and odd and not prime):
    print(f"{num} is Negative Odd and Not Prime Number")



# print(""" Write a program that takes string input and a character from user and count
# occurrences of a character in a string.""")
# sentence = input("Enter a string: ")
# char = input("Enter a character to count: ")
# count = 0
# for c in sentence:
#     if c == char:
#         count += 1
# print(f"The character '{char}' occurs {count} times in the string.")
# print("""Q6: Write a program that prompts the size of number triangle from user. Print
# number pattern using nested loops. Output and input are clearly mentioned below.
# You have followed all the program statement instructions.
# """)
# size = int(input("Enter the size of the number triangle: "))
# for i in range(1, size+1):
#     for j in range(1, i+1):
#         print(j, end=" ")
#     print()
# print("""Q5. Write a program that takes a number from use and calculate sum of digits of that
# integer""")
# num  = int(input("Enter an integer: "))
# sum = None
# if num < 0:
#     print("Negative numbers are not allowed.")
# else:
#     sum = 0
#     while num > 0:
#         digit = num % 10
#         sum += digit
#         num //= 10
#     print(f"Sum of digits: {sum}")
# print("""Q4. Write a program that takes a paragraph from user and check whether a
# paragraph is palindrome or not?""")
# para = input("Enter a paragraph: ")
# reverse = ""
# length = 0
# for c in para:
#     length += 1
# for i in range(length -1,-1,-1):
#     reverse += para[i]
# print(reverse)
# if para == reverse:
#     print("The paragraph is a palindrome.")
# else:
#     print("The paragraph is not a palindrome.")
# print("""Q3. Write a program that take a paragraph from user. you task is to reverse that
# paragraph without slicing or built-in functions?""")
# para = input("Enter a paragraph: ")
# reverse = ""
# length = 0
# for c in para:
#     length += 1
# for i in range(length -1,-1,-1):
#     reverse += para[i]
# print(f"Reversed Paragraph: {reverse}")
#print("""Q2. Write a program that takes 5 integers from user and find the largest and smallest
# numbers. Don’t use any built-in function?""")
# largest = None
# smallest = None
# li = [int(input(f"Enter integer{i+1}: ")) for i in range(5)]
# for num in li:
#     if largest is None or num > largest:
#         largest = num
#     if smallest is None or num < smallest:
#         smallest = num
# print(f"Largest number: {largest}")
# print(f"Smallest number: {smallest}")

"""Q1. Write a program that takes string from user. Your task is to find the length of that
string prompted by user and calculate its length manually using loop. Don’t use any
built-in methods?
"""
# sentence = input("Enter a string:")
# length = 0
# for c in sentence:
#     length += 1
# print(f"The length of the string is: {length}")