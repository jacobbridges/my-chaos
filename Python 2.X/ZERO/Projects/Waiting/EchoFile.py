class EchoWrite:

    def __init__(self, stream):
        self.__stream = stream

    def write(self, string):
        self.__stream.write(string)
        for byte in string:
            print '%02X' % ord(byte),

    def __getattr__(self, name):
        return getattr(self.__stream, name)

################################################################################

class EchoRead:

    def __init__(self, stream):
        self.__stream = stream

    def read(self, length):
        string = self.__stream.read(length)
        for byte in string:
            print '%02X' % ord(byte),
        return string

    def __getattr__(self, name):
        return getattr(self.__stream, name)
