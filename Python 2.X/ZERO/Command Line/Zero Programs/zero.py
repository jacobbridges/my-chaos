import os
import sys

ERROR = False

def main(function):
    try:
        arguments = sys.argv[1:]
        assert arguments
        for path in arguments:
            assert os.path.isdir(path)
        for path in arguments:
            engine(path, function)
    except:
        sys.stdout.write('Usage: %s <directory>' % os.path.basename(sys.argv[0]))

def engine(path, function):
    global ERROR
    for root, dirs, files in os.walk(path):
        for name in files:
            path = os.path.join(root, name)
            try:
                function(path)
            except:
                sys.stderr.write('%sError: %s' % (ERROR and '\n' or '', path))
                ERROR = True

def zero(path):
    size = os.path.getsize(path)
    if size:
        data = open(path, 'wb')
        todo = size
        if todo >= 2 ** 20:
            buff = '\x00' * 2 ** 20
            while todo >= 2 ** 20:
                data.write(buff)
                todo = size - data.tell()
        data.write('\x00' * todo)
        data.close()

if __name__ == '__main__':
    main(zero)
