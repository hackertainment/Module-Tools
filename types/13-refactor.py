from dataclasses import dataclass

@dataclass(frozen=True)
class Person:
    name: str
    age: int
    preferred_operating_systems: list[str]


@dataclass(frozen=True)
class Laptop:
    id: int
    manufacturer: str
    model: str
    screen_size_in_inches: float
    operating_system: str


def find_possible_laptops(laptops: list[Laptop], person: Person) -> list[Laptop]:
    possible_laptops = []
    for laptop in laptops:
        if laptop.operating_system in person.preferred_operating_systems:
            possible_laptops.append(laptop)
    return possible_laptops


people = [
    Person(name="Imran", age=22, preferred_operating_systems=["Ubuntu"]),
    Person(name="Eliza", age=34, preferred_operating_systems=["Arch Linux"]),
]

laptops = [
    Laptop(id=1, manufacturer="Dell", model="XPS", screen_size_in_inches=13, operating_system="Arch Linux"),
    Laptop(id=2, manufacturer="Dell", model="XPS", screen_size_in_inches=15, operating_system="Ubuntu"),
    Laptop(id=3, manufacturer="Dell", model="XPS", screen_size_in_inches=15, operating_system="ubuntu"),
    Laptop(id=4, manufacturer="Apple", model="macBook", screen_size_in_inches=13, operating_system="macOS"),
]

for person in people:
    possible_laptops = find_possible_laptops(laptops, person)
    print(f"Possible laptops for {person.name}: {possible_laptops}")

# Task 13
# Change the type annotation of `Person.preferred_operating_system` from `str` to `list[str]`.
# Run mypy on the code.
# It tells us different places that our code is now wrong. Fix it to remove any errors.

# Now we changed the types, we probably also want to _rename_ our field to something appropriate.
# Run mypy again.

# Fix all of the places that mypy tells you need changing.
# Then, make sure the program works as you'd expect.
