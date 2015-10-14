"""
write-to-file-threaded.py

Write to a file "asynchronously" by spawning a new thread for every write process
"""
from threading import Thread, Lock
from toolz import curry


@curry
def write(file_obj, lock, string):
    def run():
        lock.acquire()
        file_obj.write(string)
        lock.release()
    Thread(target=run).start()


def main():
    writer = write(open('test.secret', 'w'), Lock())
    writer('Something 1\n')
    writer('Something 2\n')
    writer('Something 3\n')
    Thread(target=(lambda: writer('Something Threaded 1\n'))).start()
    Thread(target=(lambda: writer('Something Threaded 2\n'))).start()
    Thread(target=(lambda: writer('Something Threaded 3\n'))).start()


if __name__ == '__main__':
    main()
