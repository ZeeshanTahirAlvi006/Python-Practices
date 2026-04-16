def check_login(username,password):
    if username == "admin" and password == "1234":
        print("Login successful!")
        return True
    else:
        print("Login failed!")
        return False
def login_system():
    while True:
        try:
            username = input("Enter username: ")
            password = input("Enter password: ")
            if(not username or not password):
                print("Username and password cannot be empty.")
                continue
            else:
                check = check_login(username,password)
                if check: 
                    return
        except ValueError:
            print("Invalid input. Please try again.")
# login_system()
def text_analyzer():
    while True:           
        sentence = input("Enter a sentence: ")
        count = 0
        count_vowels = 0
        count_words= 0
        vowels = "aeiouAEIOU"
        for c in sentence:
            count+=1
            if c in vowels:
                count_vowels+=1
            if c == " ":
                count_words+=1
        print(f"Number of characters: {count}")
        print(f"Number of vowels: {count_vowels}")
        print(f"Number of words: {count_words+1}")
        upper = sentence.upper()
        print(f"Uppercase: {upper}")
        reverse = sentence[::-1]
        print(f"Reversed: {reverse}")
        if "AI" in sentence:
            print("The sentence contains 'AI'.")
# text_analyzer()
def smart_number_analyzer():
    while True:
        try:
            num = int(input("Enter a number: "))
            if num > 0:
                print(f"Number is positive ({num})") 
            elif num < 0:
                print(f"Number is negative ({num})")
            else:
                print(f"Zero ({num})")
            if num % 2 == 0:
                print(f"Number is even ({num})")
            else:
                print(f"Number is odd ({num})")
            if num > 1:
                prime = True
                if num == 2:
                    prime = True
                else:
                    for i in range(2,num):
                        if(num % i == 0):
                            prime = False
                            break
                if prime:
                    print(f"Number is prime ({num})")
                else:
                    print(f"Number is not prime ({num})")
                for i in range(1,11):
                    print(f"{num} x {i} = {num*i}")

        except ValueError:
            print("Invalid Input! Try Again.")
# smart_number_analyzer()
def student_dictionary_system():
    while True:
        try:
            li = input("Enter ")

        except ValueError:
            print("Invalid Input! Try Again.")