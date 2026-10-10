class Parent:
    def __init__(self, first_name: str, last_name: str):
        self.first_name = first_name
        self.last_name = last_name

    def get_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Child(Parent):
    def __init__(self, first_name: str, last_name: str):
        super().__init__(first_name, last_name)
        self.previous_last_names = []

    def change_last_name(self, last_name) -> None:
        self.previous_last_names.append(self.last_name)
        self.last_name = last_name

    def get_full_name(self) -> str:
        suffix = ""
        if len(self.previous_last_names) > 0:
            suffix = f" (née {self.previous_last_names[0]})"
        return f"{self.first_name} {self.last_name}{suffix}"

# TASK 16:
# Play computer with this code
# Describe what is happening and why on each line below here
# If any lines cause errors, comment out the line and explain why the error happens

person1 = Child("Elizaveta", "Alekseeva")   # initiate a `Child` object
print(person1.get_name())                   # call Child's get_name() method inherited from `Parent` class and print "Elizaveta Alekseeva"
print(person1.get_full_name())              # call Child's get_full_name() method and print "Elizaveta Alekseeva"
person1.change_last_name("Tyurina")         # call Child's change_last_name() method and updated its last name with old one stored
print(person1.get_name())                   # call Child's get_name() method inherited from `Parent` class and print "Elizaveta Tyurina"
print(person1.get_full_name())              # call Child's get_full_name() method and print "Elizaveta Tyurina (née Alekseeva)"

person2 = Parent("Elizaveta", "Alekseeva")  # initiate a `Parent` object
print(person2.get_name())                   # call Parent's get_name() method and print "Elizaveta Alekseeva"
#print(person2.get_full_name())             # call Parent's get_full_name() method which does not exist
#person2.change_last_name("Tyurina")        # call Parent's change_last_name() method which does not exist
print(person2.get_name())                   # call Parent's get_name() method and print "Elizaveta Alekseeva"
#print(person2.get_full_name())             # call Parent's get_full_name() method which does not exist
