import zero

def upper(path):
    root, ext = zero.os.path.splitext(path)
    upper = ext.upper()
    if ext != upper:
        zero.os.rename(path, root + upper)

if __name__ == '__main__':
    zero.main(upper)
