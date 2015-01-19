import sys
import random
import parse

def main():
    while True:
        line = sys.stdin.readline()
        for data in parse.words(line):
            if isinstance(data, str):
                sys.stdout.write(data)
            else:
                if len(data) < 4:
                    sys.stdout.write(''.join(data))
                else:
                    sys.stdout.write(confuse(data))

def confuse(data):
    array = [data[0]]
    array.extend(random.sample(data[1:-1], len(data) - 2))
    array.append(data[-1])
    return ''.join(array)

if __name__ == '__main__':
    main()
