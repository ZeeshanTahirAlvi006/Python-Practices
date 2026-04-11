balance = 1000.0

def deposit(amount):
    global balance
    if amount > 0:
        balance += amount
        print(f"Successfully deposited ${amount}")
    else:
        print("Error: Deposit amount must be positive.")
def withdraw(amount):
    global balance
    if amount > balance:
        print("Error: Insufficient funds!")
    elif amount <= 0:
        print("Error: Withdrawal amount must be positive.")
    else:
        balance -= amount
        print(f"Successfully withdrew ${amount}")
def check_balance():
    print(f"Current Balance: ${balance}")

def start_banking():
    print("Zeeshan's Bank - Welcome!")
    
    while True:
        print("\nOptions: 1. Deposit  2. Withdraw  3. Check Balance  4. Exit")
        choice = input("Enter choice (1-4): ")

        if choice == '4':
            print("Thank you for using our bank. Goodbye!")
            break

        try:
            if choice == '1':
                amt = float(input("Enter amount to deposit: "))
                deposit(amt)
            elif choice == '2':
                amt = float(input("Enter amount to withdraw: "))
                withdraw(amt)
            elif choice == '3':
                check_balance()
            else:
                print("Invalid choice! Please select 1-4.")
        except ValueError:
            print("Invalid input! Please enter a numeric value.")
        print(f"Updated Balance: ${balance}")
def get_grade(average):
    if average >= 85:
        return "A"
    elif average >= 70:
        return "B"
    elif average >= 50:
        return "C"
    else:
        return "F"

def analyze_performance():
    marks_list = []
    subject_count = 5
    
    print(f"--- Student Grade Analyzer (Input {subject_count} Subjects) ---")
    
    i = 1
    while len(marks_list) < subject_count:
        try:
            mark = float(input(f"Enter marks for Subject {i} (0-100): "))
            
            if 0 <= mark <= 100:
                marks_list.append(mark)
                i += 1
            else:
                print("Error: Marks must be between 0 and 100.")
        except ValueError:
            print("Invalid input! Please enter a number.")

    average_marks = sum(marks_list) / subject_count
    
    final_grade = get_grade(average_marks)

    format_score = lambda x: round(x, 2)

    print("\nResults")
    print(f"Average Marks: {format_score(average_marks)}")
    print(f"Final Grade: {final_grade}")

start_banking()
analyze_performance()
