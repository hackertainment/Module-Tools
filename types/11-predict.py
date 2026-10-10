from dataclasses import dataclass

@dataclass(frozen=True)
class Animal:
    name: str
    species: str

@dataclass(frozen=True)
class Person:
    name: str
    age: int

@dataclass(frozen=True)
class FamilyTree:
    parent: Person
    members: list

pet = Animal(name="Gromit", species="Dog")
fatma = Person(name="Fatma", age=4)
aisha = Person(name="Aisha", age=6)
imran = Person(name="Imran", age=30)

family = FamilyTree(parent=imran, members=[fatma, aisha, pet])

def print_family_tree(family: FamilyTree):
    print(family.parent.name)
    for child in family.members:
        print(f"{child.name} ({child.age} years old)")

print_family_tree(family)

# TASK 11
# There is a bug in this code. Can you spot it?
#     AttributeError: 'Animal' object has no attribute 'age'
# Run your code through mypy. Does mypy spot it?
#     11-predict.py:16: error: Missing type parameters for generic type "list"  [type-arg]
# Offer an explanation for what is happening.
#     `FamilyTree.members` is a list, but mypy doesn't know what type of thing is in the list. It doesn't even know that everything in the list has the same type = `["hello", 7, True]` is a legal list in Python. Many people would consider a pet to be a member of the family, so it seems correct, but due to the different types, this code breaks down and mypy can't spot the problem.
