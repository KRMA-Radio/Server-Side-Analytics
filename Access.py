import json

__author__ = 'Isaac'


class Access:
    def __init__(self, ip, time, http_method, host, page, response_code, http_referer, user_agent, length):
        self.ip = ip
        self.time = time
        self.http_method = http_method
        self.host = host
        self.page = page
        self.response_code = response_code
        self.http_referer = http_referer
        self.user_agent = user_agent
        self.length = length

    # We compare by the date at which the event took place
    def __cmp__(self, other):
        return self.time.__comp__(other.time)

    def __str__(self):
        return json.dumps(self.__dict__)

    '''
     Parses a line like: 162.251.161.74 - admin [13/Sep/2015:18:45:09 -0400] "GET /admin/stats.xml?mount=/KRMARadio-LIVE HTTP/1.1" 200 3513 "-" "Mozilla/4.0 (StreamLicensing Directory Tester)" 0
     into a Access object like
     {
        ip: "162.251.161.74"
        time: "13/Sep/2015:18:45:09 -0400"
        host: host
        http_method: GET
        page: "/admin/stats.xml?mount=/KRMARadio-LIVE"
        response_code: 200
        http_referer: "-"
        user_agent: "Mozilla/4.0 (StreamLicensing Directory Tester)"
        length: 0
    }
    '''

    @classmethod
    def from_file(cls, file, host=""):
        log = []

        line = file.readline()
        while line != "":
            access = cls.from_line(line, host)
            log.append(access)
            line = file.readline()
        return log

    @classmethod
    def from_line(cls, line: str, host: str):
        ip, passed = cls.parse_token(line, " ")
        line = line[passed:]

        # we'll just throw this away as I'm not quite sure what it's for
        blank, passed = cls.parse_token(line, " ")
        if blank != '-':
            print(blank + " expected -")
        line = line[passed:]

        # we'll throwing this away too. It's important, but I don't know what to do with it
        user, passed = cls.parse_token(line, " ")
        line = line[passed:]

        time, passed = cls.parse_token(line, "[", "]")
        line = line[passed + 1:]

        # get the entire request looks something like:
        # GET /admin/stats.xml?mount=/KRMARadio-LIVE HTTP/1.1" 200 3513 "-" "Mozilla/4.0 (StreamLicensing Directory Tester)"
        request, passed = cls.parse_token(line, '"')
        line = line[passed:]

        http_method, passed = cls.parse_token(request, " ")
        request = request[passed:]
        page, passed = cls.parse_token(request, " ")

        response_code, passed = cls.parse_token(line, " ")
        response_code = int(response_code)
        line = line[passed:]

        # we'll just throw this away as I'm not quite sure what it's for TODO: figure out what this does
        blank, passed = cls.parse_token(line, " ")
        line = line[passed:]

        http_referer, passed = cls.parse_token(line, '"')
        line = line[passed+1:]

        user_agent, passed = cls.parse_token(line, '"')
        line = line[passed:]

        length, passed = cls.parse_token(line, " ", "\n")
        length = int(length)

        return Access(ip, time, http_method, host, page, response_code, http_referer, user_agent, length)



    # Access.parse_ip(string) returns the ip address which starts the supplied string
    # It assumes the ip is separated from the next element by space
    @classmethod
    def parse_token(cls, string: str, start: str, end: str = None):
        if end is None:
            end = start

        word = bytearray()

        in_word = False
        covered = 0
        for c in string:
            covered += 1
            if c != start and c != end:
                word.append(ord(c))
                in_word = True
            elif in_word:
                break
        return word.decode("utf-8"), covered
