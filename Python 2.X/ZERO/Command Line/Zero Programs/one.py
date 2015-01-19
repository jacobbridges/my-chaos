import zero

def one(path):
    size = zero.os.path.getsize(path)
    if size:
        data = open(path, 'wb')
        todo = size
        if todo >= 2 ** 20:
            buff = '\xFF' * 2 ** 20
            while todo >= 2 ** 20:
                data.write(buff)
                todo = size - data.tell()
        data.write('\xFF' * todo)
        data.close()

if __name__ == '__main__':
    zero.main(one)
