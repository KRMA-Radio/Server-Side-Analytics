
import sys
from Access import Access


USAGE = "python Server-Side-Analytics.py [logfile] [hostname] [google analytics tracking id]"


def server_side_analytics(f, host: str, tracking_id: str):
    log = Access.from_file(f, host)

    for entry in log:
        print(entry)


if len(sys.argv) < 4:
    print("Error: not enough arguments")
    print("Usage: " + USAGE)
    exit(-1)

try:
    file = open(sys.argv[1])
    server_side_analytics(file, sys.argv[2], sys.argv[3])
except IOError:
    print("Error: log file can't be opened")
    print("Usage: " + USAGE)
    exit(-2)
