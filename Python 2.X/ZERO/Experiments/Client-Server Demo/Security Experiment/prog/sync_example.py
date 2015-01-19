from sync import Sync
import thread
import sys
import random
import time
import os

def write(*args):
    sys.stdout.write(' '.join(map(str, args)) + '\n')

def example_1():
    from time import sleep
    def get_input(share):
        while share[0]:
            share[1] = raw_input('Please say something.\n')
            share[2].sync()
        share[3].sync()
    def do_output(share):
        while share[0]:
            share[2].sync()
            write('You said, "%s"' % share[1])
        share[3].sync()
    share = [True, None, Sync(2), Sync(3)]
    thread.start_new_thread(get_input, (share,))
    thread.start_new_thread(do_output, (share,))
    sleep(60)
    share[0] = False
    share[3].sync()

def example_2():
    from os import name, system
    from random import randint
    SLOTS = 10
    def writer(slots, select, stop):
        while True:
            if not random.randint(0, 10 ** 5):
                stop.sync()
                time.sleep(5)
            slots[select] = (slots[select] + 1) % 10
    def reader(slots):
        while True:
            if os.name == 'nt':
                os.system('cls')
            elif os.name == 'posix':
                os.system('clear')
            for slot in slots:
                print slot,
    slots = [0] * SLOTS
    stop = Sync(SLOTS)
    thread.start_new_thread(reader, (slots,))
    for select in range(SLOTS):
        thread.start_new_thread(writer, (slots, select, stop))
    Sync(2).sync()

################################################################################

if __name__ == '__main__':
    example_1()
