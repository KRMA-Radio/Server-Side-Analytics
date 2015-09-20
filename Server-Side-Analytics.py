
import sys
from Access import Access


def LogParser(file, host, tracking_id):
    f = open(file)
    log = Access.from_file(f, host)


LogParser(sys.argv[1], sys.argv[2], sys.argv[3])