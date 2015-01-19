import zero

def kaos(path):
    size = zero.os.path.getsize(path)
    if size:
        data = open(path, 'wb')
        todo = size
        while todo:
            data.write(zero.os.urandom(min(todo, 2 ** 20)))
            todo = size - data.tell()
        data.close()

if __name__ == '__main__':
    zero.main(kaos)
