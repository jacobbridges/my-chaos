import os
import random
import sys

def main():
    for line in file(name()):
        for data in parse(line):
            sys.stdout.write(''.join(data if isinstance(data, list) or len(data) < 4 else [data[0]] + random.sample(data[1:-1], len(data) - 2) + [data[-1]]))
    raw_input('\n====\nDONE\n====')

def name():
    while True:
        path = raw_input('What is the filename? ')
        if os.path.isfile(path):
            return path
        print 'ERROR: "%s" is not a file.\n' % path

def parse(line):
    data = []
    buff = ''
    code = 'A' <= line[0] <= 'Z' or 'a' <= line[0] <= 'z'
    for character in line:
        if code == ('A' <= character <= 'Z' or 'a' <= character <= 'z'):
            buff += character
        else:
            data.append(tuple(buff) if code else list(buff))
            buff = character
            code = not code
    data.append(tuple(buff) if code else list(buff))
    return data

if __name__ == '__main__':
    main()
