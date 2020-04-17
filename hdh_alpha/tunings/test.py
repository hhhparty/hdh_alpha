import os

a = os.path.split(os.path.realpath(__file__))[0]
print(a)
print(os.getcwd())