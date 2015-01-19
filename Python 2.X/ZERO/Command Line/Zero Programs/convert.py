import zero

TABLE = ''.join(map(chr, range(256)))
DELETECHARS = ''.join(c for c in TABLE if len(repr(c)) != 6)

def convert(path):
    if not file(path, 'rb').read(2 ** 20).translate(TABLE, DELETECHARS):
        data = file(path, 'r').read()
        file(path, 'w').write(data)

if __name__ == '__main__':
    zero.main(convert)
