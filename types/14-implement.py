from dataclasses import dataclass
from enum import Enum

class OperatingSystem(Enum):
    MACOS = "macOS"
    ARCH = "Arch Linux"
    UBUNTU = "Ubuntu"

@dataclass(frozen=True)
class Person:
    name: str
    age: int
    preferred_operating_system: OperatingSystem


@dataclass(frozen=True)
class Laptop:
    id: int
    manufacturer: str
    model: str
    screen_size_in_inches: float
    operating_system: OperatingSystem


def find_possible_laptops(laptops: list[Laptop], person: Person) -> list[Laptop]:
    possible_laptops = []
    for laptop in laptops:
        if laptop.operating_system == person.preferred_operating_system:
            possible_laptops.append(laptop)
    return possible_laptops


people = [
    Person(name="Imran", age=22, preferred_operating_system=OperatingSystem.UBUNTU),
    Person(name="Eliza", age=34, preferred_operating_system=OperatingSystem.ARCH),
]

laptops = [
    Laptop(id=1, manufacturer="Dell", model="XPS", screen_size_in_inches=13, operating_system=OperatingSystem.ARCH),
    Laptop(id=2, manufacturer="Dell", model="XPS", screen_size_in_inches=15, operating_system=OperatingSystem.UBUNTU),
    Laptop(id=3, manufacturer="Dell", model="XPS", screen_size_in_inches=15, operating_system=OperatingSystem.UBUNTU),
    Laptop(id=4, manufacturer="Apple", model="macBook", screen_size_in_inches=13, operating_system=OperatingSystem.MACOS),
]

name = ""
while name=="":
    name = input("Enter your name: ").strip()
age = 0
while age<=0:
    try:
        age = int(input("Enter your age: ").strip())
    except ValueError:
        print("Invalid age, please enter an integer!")
print("1.", OperatingSystem.MACOS)
print("2.", OperatingSystem.ARCH)
print("3.", OperatingSystem.UBUNTU)
print("0.", "None of the above")
os = ""
while os!="0" and os!="1" and os!="2" and os!="3":
    os = input("Enter your preferred OS (0-3): ").strip()
if os=="1":
    preferred_os = OperatingSystem.MACOS
if os=="2":
    preferred_os = OperatingSystem.ARCH
if os=="3":
    preferred_os = OperatingSystem.UBUNTU
if os=="0":
    print(f"No laptop available for {name}!")
else:
    person = Person(name=name, age=age, preferred_operating_system=preferred_os)
    people.append(person)

for person in people:
    possible_laptops = find_possible_laptops(laptops, person)
    print(f"Possible laptops for {person.name}: {possible_laptops}")

# TASK 14
# The above code currently handles operating systems as strings.
#
# Refactor the code to use enums for operating systems.
#
# Check with mypy and test it to ensure the program still works correctly.
#
# Use the `input` function
# https://docs.python.org/3/library/functions.html#input
# to read a person's name, age, and preferred operating system,
# then add them to the list of people.
#
# Make sure your implementation has a good user experience, and properly validates the inputs, mapping an OS to one of the enum values.
#
# If an operating system can't be matched at all, your script should handle it appropriately and not crash.
