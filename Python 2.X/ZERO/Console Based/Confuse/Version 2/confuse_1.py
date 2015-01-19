import os, random, sys
import parse

def main():
    for line in file(name()):
        for data in parse.words(line):
            if isinstance(data, str):
                sys.stdout.write(data)
            else:
                if len(data) < 4:
                    sys.stdout.write(''.join(data))
                else:
                    sys.stdout.write(confuse(data))
    raw_input('\n====\nDONE\n====')

def name():
    while True:
        try:
            path = raw_input('What is the filename? ')
        except:
            sys.exit()
        if os.path.isfile(path):
            return path
        print 'ERROR: "%s" is not a file.\n' % path

def confuse(data):
    array = [data[0]]
    array.extend(random.sample(data[1:-1], len(data) - 2))
    array.append(data[-1])
    return ''.join(array)

if __name__ == '__main__':
    main()
