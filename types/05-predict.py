imran = {
  "name": "Imran",
  "age": 22,
  "preferred_operating_system": "Ubuntu",
}

eliza = {
  "name": "Eliza",
  "age": 34,
  "preferred_operating_system": "Arch Linux",
}


print(imran["name"])
print(imran["address"])

# TASK 5:
# This code contains some untyped objects.
# Try checking it with mypy before running the code and predict what you think will happen when you run the code.
#     Success: no issues found in 1 source file
# Prediction:
#     KeyError: 'address'
# Can you explain what actualy happens?
#     The "imran" dictionary does not have a key called "address"
