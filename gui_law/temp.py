from jsonHandler import *
from itertools import chain

string = r"\u00b2"
test = string.encode()
test = test[0:len(string)]
print(test.decode())
