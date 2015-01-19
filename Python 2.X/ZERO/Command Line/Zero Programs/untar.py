import zero
import tarfile

if __name__ == '__main__':
    zero.main(lambda path: tarfile.open(path).extractall(zero.os.path.dirname(path)))
