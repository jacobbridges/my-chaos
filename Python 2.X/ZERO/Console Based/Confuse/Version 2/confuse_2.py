import os, random, sys
import parse

def main():
    filename = name()
    output = file('%s_confused%s' % os.path.splitext(filename), 'w')
    for line in file(filename):
        for data in parse.words(line):
            if isinstance(data, str):
                output.write(data)
            else:
                if len(data) < 4:
                    output.write(''.join(data))
                else:
                    output.write(confuse(data))

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
