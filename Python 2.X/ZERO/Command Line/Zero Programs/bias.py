import zero

def bias(path):
    root, ext = zero.os.path.splitext(path)
    if not ext[1:]:
        zero.os.rename(path, root + '.txt')

if __name__ == '__main__':
    zero.main(bias)
