# TASK 9
#
# Having done some research on encapsulation, think about the benefits.
#
# Think of some examples and in your own words write down some benefits and trade-offs of using encapsulation in classes:
#     Take BankAccount class as an example, the actual money balance is private, and users can only change or view it using safe methods like deposit(), withdraw(), and get_balance().
#     Benefits
#         Data Protection: Outside code cannot directly change internal variables, preventing accidental corruption.
#         Controlled Access: You can add validation rules inside methods, such as stopping a user from withdrawing more money than they actually have.
#         Flexibility: You can rewrite the internal logic of a class later without breaking any other parts of your program that rely on it.
#     Trade-offs
#         More Boilerplate Code: You have to write extra methods (like getters and setters) just to access or modify data.
#         Added Complexity: Too many layers of abstraction can make the code harder to read and trace for a beginner.
#         Slight Overhead: Calling extra methods instead of accessing variables directly can add a tiny bit of performance overhead in certain languages.

# STRETCH TASK 9.1
#
# In the following  class, make the name property private
# Add a `get_name()` method to allow read-only access.

class Person:
    def __init__(self, name: str, age: int):
        self.__name = name
        self.__age = age

    def get_name(self):
        return self.__name

    def is_adult(self):
      return self.__age >= 18

imran = Person("Imran", 22)
print(imran.get_name())
#print(imran.age) # fails
#print(imran.__age) # fails
print(imran.is_adult()) # works and prints True

eliza = Person("Eliza", 12)
print(eliza.get_name())
#print(eliza.age) # fails
#print(imran.__age) # fails
print(eliza.is_adult()) # works and prints False
