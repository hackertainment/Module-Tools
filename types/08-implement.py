from datetime import date
import math

class Person:
    def __init__(self, name: str, date_of_birth: date, preferred_car_brand: str):
        self.name = name
        self.date_of_birth = date_of_birth
        self.preferred_car_brand = preferred_car_brand

    def is_adult(self) -> bool:
        today = date.today()
        age = math.floor((today-self.date_of_birth).days/365.25)
        return age>=18

def drivers_license_check(person: Person) -> str:
  if person.is_adult():
    return 'Valid drivers license'

  return 'This person is underage!'

imran = Person("Imran", date(2004, 1, 1), "Mercedes")
print(drivers_license_check(imran)) # should return 'Valid drivers license'

# TASK 8:
#
# Add an `is_adult` method into the class, and make sure your code gives the expected output.
#
# Change the `Person` class to take a date of birth using
# the standard library's `datetime.date` class
# https://docs.python.org/3/library/datetime.html#datetime.date))
# and store the `date of birth` instead of `age`.
#
# Try to run your code now and observe how this change breaks your code.
# What kind of error do you get? Is it helpful in identifying where your next change needs to be?
#
# Now update only the `is_adult` method to fix the error and check everything works correctly.
