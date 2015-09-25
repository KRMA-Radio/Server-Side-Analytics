"""
test.py is intended to run tests of mostly Access.py to try to make sure it is working
Currently it is being used for manual tests as needed
"""
from Access import Access
from GoogleAnalyticsMeasurementProtocol import hit

f = open("access.log")

log = Access.from_file(f, "test.com")




def test(access):
    return hit.hit_from_access(access, "UA-67487168-1")


futures = []
for access in log[:100]:
    futures.append(test(access))

for future in futures:
    response = future.result()
    print(response.text)

