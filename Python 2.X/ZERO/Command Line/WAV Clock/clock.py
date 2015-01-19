try:
    import os, sys, time, msvcrt, winsound
    import random, StringIO, dfs
except Exception, error:
    sys.stderr.write('%s: %s' % (error.__class__.__name__, error))
    sys.exit(1)

def main():
    try:
        load_sounds()
        try:
            arg = time.strptime(sys.argv[1], '%H:%M')
            arg_sec = (arg.tm_hour * 60 + arg.tm_min) * 60
            now = time.localtime()
            now_sec = (now.tm_hour * 60 + now.tm_min) * 60 + now.tm_sec
            alarm(arg_sec - now_sec + (86400 if arg_sec <= now_sec else 0))
        except:
            sys.stdout.write('Usage: %s HH:MM' % os.path.basename(sys.argv[0]))
    except Exception, error:
        sys.stderr.write('%s: %s' % (error.__class__.__name__, error))

def load_sounds():
    global sounds
    sounds = []
    hack_dfs()
    dfs.Release(file('sounds.bin', 'rb')).release('')

def hack_dfs():
    os.path.exists = lambda path: 1
    os.path.isfile = lambda path: 0
    class File(StringIO.StringIO):
        def __init__(self, *args):
            StringIO.StringIO.__init__(self)
        def close(self):
            sounds.append(self.getvalue())
            StringIO.StringIO.close(self)
    __builtins__.open = File

def alarm(seconds):
    time.sleep(seconds)
    while msvcrt.kbhit():
        msvcrt.getch()
    while not msvcrt.kbhit():
        winsound.PlaySound(random.choice(sounds), winsound.SND_MEMORY)

if __name__ == '__main__':
    main()
