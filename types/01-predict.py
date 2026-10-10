def half(value):
    return value / 2

def double(value):
    return value * 2

def second(value):
    return value[1]

# TASK 1:
# 1. Predict what you think will happen with each of the following functions
# 2. Then, test it, and explain in your own words what is actually happening and why
# (feel free to comment out lines if you think they cause errors or crashes while testing)

print(half(22))
# Prediction:  11
# What actually happens and why:  11.0 : there is no integer division in python and division will be casted to float

print(half("22"))
# Prediction:  error
# What actually happens and why:  TypeError: unsupported operand type(s) for /: 'str' and 'int'

print(double(22))
# Prediction:  44
# What actually happens and why:  44 : there is integer multiplication in python

print(double("22"))
# Prediction:  2222
# What actually happens and why:  2222 : multiplication operator means repeat in string operations

print(second(22))
# Prediction:  error
# What actually happens and why:  TypeError: 'int' object is not subscriptable

print(second(0x16))
# Prediction:  error
# What actually happens and why:  TypeError: 'int' object is not subscriptable

print(second("22"))
# Prediction:  2
# What actually happens and why:  2 : index operater means the position of character in a string
