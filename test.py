"""
test.py is intended to run tests of mostly Access.py to try to make sure it is working
Currently it is being used for manual tests as needed
"""
from Access import Access


f = open("access.log", "r")

log = Access.from_file(f, "")

for entry in log:
    print(entry)
