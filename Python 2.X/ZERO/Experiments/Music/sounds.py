import time
import winsound

################################################################################

class PIF:

    def __init__(self, data):
        data = data.split(' ')
        data = [data[index:index+3] for index in xrange(0, len(data), 3)]
        self.__data = [(float(secs), int(frequency), int(duration)) for secs, frequency, duration in data]

    def play(self):
        for secs, frequency, duration in self.__data:
            time.sleep(secs)
            winsound.Beep(frequency, duration)

################################################################################

class Template:

    def __init__(self):
        self.__data = []

    def __str__(self):
        return ' '.join(map(str, self.__data))

    def code(self):
        return '.'.join([self.__class__.__name__ + '()'] + ['add(%s, %s, %s)' % tuple(args) for args in (self.__data[index:index+3] for index in xrange(0, len(self.__data), 3))])

    def add(self, secs, frequency, duration):
        self.__data.extend([float(secs), int(frequency), int(duration)])
        return self

    def sub(self, count=1):
        count = int(count)
        if count < 0:
            self.__data = []
        else:
            self.__data = self.__data[:-3*count]
        return self

    def play(self):
        # Listen to the current PIF information.
        PIF(str(self)).play()
