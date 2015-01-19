import os, random, thread, time
from sync import Sync

################################################################################

SLOTS = 10

################################################################################

def main():
    slots = [0] * SLOTS
    stop = Sync(SLOTS)
    for index in xrange(SLOTS):
        thread.start_new_thread(writer, (slots, index, stop))
    reader(slots)

def writer(slots, index, stop):
    while True:
        if not random.randint(0, 65535):
            stop.sync()
            time.sleep(5)
        slots[index] = (slots[index] + 1) % 10

def reader(slots):
    while True:
        if os.name == 'nt':
            os.system('cls')
        elif os.name == 'posix':
            os.system('clear')
        print ' '.join(map(str, slots))

################################################################################

if __name__ == '__main__':
    main()
