from dataclasses import dataclass

@dataclass(frozen=True)
class Person:
    name: str
    age: int
    preferred_car_brand: str

    def is_adult(self) -> bool:
        return self.age >= 18

    def greet(self) -> str:
        return "Hello "+self.name+"!"

def drivers_license_check(person: Person) -> str:
  if person.is_adult():
    return 'Valid drivers license'

  return 'This person is underage!'

imran = Person("Imran", 22, "Mercedes")
print(imran) # should print out all fields
print(drivers_license_check(imran)) # should return 'Valid drivers license'


# TASK 10.1:
# Convert the above `Person` class into a value type using `@dataclass`
# so you can print the class (and see it's type and properties)
# and compare class instances that are identical.
# Make sure your `is_adult` method and `drivers_license_check` free function both work.

# TASK 10.2:
# Make a new method on your Person class - `greet()` which should return `"Hello <person name>!"` when used.

# TASK 10.3:
# Read the @dataclass documentation here: https://docs.python.org/3/library/dataclasses.html
# Explain what `frozen=True` does to the class?
# What other options could you play around with and explore? Offer suggestions for any that would be useful here.
#     frozen=true emulates read-only frozen instances and assigns to fields will generate an exception.
#     order=true generates __lt__(), __le__(), __gt__(), and __ge__() methods and compare the class as if it were a tuple of its fields in order.
