import thread, time
from sync import Sync

################################################################################

def main():
    share = [True, Sync(2), Sync(3)]
    thread.start_new_thread(get_input, (share,))
    thread.start_new_thread(do_output, (share,))
    time.sleep(60)
    share[0] = False
    share[2].sync()
    
def get_input(share):
    while share[0]:
        share.append(raw_input('Please say something.\n'))
        share[1].sync()
    share[2].sync()


def do_output(share):
    while share[0]:
        share[1].sync()
        print 'You said, "%s"' % share.pop()
    share[2].sync()

################################################################################

if __name__ == '__main__':
    main()
