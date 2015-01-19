import zero
import random

STRING = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

def ident(path):
    d, b = zero.os.path.split(path)
    zero.os.rename(path, zero.os.path.join(d, ''.join(random.sample(STRING, len(STRING))) + zero.os.path.splitext(b)[1]))

if __name__ == '__main__':
    zero.main(ident)
