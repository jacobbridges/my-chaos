import zero

def lower(path):
    root, ext = zero.os.path.splitext(path)
    lower = ext.lower()
    if ext != lower:
        zero.os.rename(path, root + lower)

if __name__ == '__main__':
    zero.main(lower)
