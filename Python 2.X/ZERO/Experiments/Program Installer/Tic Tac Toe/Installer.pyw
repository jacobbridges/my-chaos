import dfs
import sys

def main():
    source = file(sys.argv[0], 'rb')
    source.seek(17920)
    files = dfs.Release(source)
    while not files.EOF():
        files.release('C:\\')
    source.close()

if __name__ == '__main__':
    main()
