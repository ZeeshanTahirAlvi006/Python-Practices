class staff:
    def __init__(self,staff_id,Dept_id,name,role,contact):
        self.staff_id = staff_id
        self.Dep_id = Dept_id
        self.name = name
        self.role = role
        self.contact = contact
    def display(self):
        print(f"Staff ID: {self.staff_id}")
        print(f"Department ID: {self.Dep_id}")
        print(f"Name: {self.name}")
        print(f"Role: {self.role}")
        print(f"Contact: {self.contact}")