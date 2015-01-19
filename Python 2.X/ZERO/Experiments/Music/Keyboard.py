import msvcrt
import random
import time
import winsound

# CONSTANTS
KEYS = 'zsxcfvgbnjmk,l./\'q2we4r5t6yu8i9op-[=]'
A4 = 440
AUTHOR = '.\',zb'
NEW_SONG = ('vm',
            'zv',
            'cn',
            'vm',
            'xb',
            'cn',
            'zv')

# CONFIGURATION
NS_SP = 1
SPEED = 5
HOLD_RATIO = 0.95
TRANSPOSE = 0
PAUSE_TIME = 2
SHOW_FREQU = False

# RANDOM
NEIGHBOR_RATIO = 0.9
ODD_RATIO = 0.05
SWITCH_RATIO = 0.01
WHITE_KEYS = 'zxcvbnm,./qwertyuiop[]'
BLACK_KEYS = 'sfgjkl\'245689-='

I_WORSHIP_THEE = [('c', 1),
                  ('c', 2),
                  ('c', 1),
                  ('c', 1),
                  ('v', 1),
                  ('b', 1),
                  ('n', 2),
                  ('n', 1),
                  ('b', 2),
                  ('c', 1),
                  (',', 2),
                  (',', 1),
                  ('m', 2),
                  ('b', 1),
                  ('v', 5),
                  ('c', 1),
                  (',', 2),
                  (',', 1),
                  ('.', 1),
                  ('/', 1),
                  ('\'+', 1),
                  ('m', 2),
                  ('m', 1),
                  ('b', 2),
                  ('b', 1),
                  ('n', 2),
                  ('b', 1),
                  ('v', 1),
                  ('c', 1),
                  ('v', 1),
                  ('c', 5)]

I_WILL_FOLLOW = [('m', 2),
                 ('m', 1),
                 ('m', 2),
                 ('/', 1),
                 ('n', 2),
                 ('m', 1),
                 ('n', 1),
                 ('b', 1.5),
                 ('v', 0.5),
                 ('b', 2),
                 ('b', 1),
                 ('b', 1),
                 ('v', 1),
                 ('c', 1),
                 ('v', 6),
                 ('m', 2),
                 ('m', 1),
                 ('m', 2),
                 ('/', 1),
                 ('n', 2),
                 ('m', 1),
                 ('n', 1),
                 ('b', 1.5),
                 ('v', 0.5),
                 ('b', 2),
                 ('b', 1),
                 ('v', 1),
                 ('c', 1),
                 ('v', 1),
                 ('c', 5),
                 ('c', 1),
                 (',', 2),
                 (',', 1),
                 ('.', 3),
                 ('.', 2),
                 ('\'+', 1),
                 ('/', 2),
                 ('/', 1),
                 ('/', 2),
                 ('/', 1),
                 ('\'+++', 1),
                 ('\'+', 1),
                 ('/', 1),
                 ('m', 6),
                 ('m', 2),
                 ('m', 1),
                 ('m', 2),
                 ('/', 1),
                 ('n', 2),
                 ('m', 1),
                 ('n', 1),
                 ('b', 1.5),
                 ('v', 0.5),
                 ('b', 2),
                 ('b', 1),
                 ('v', 1),
                 ('c', 1),
                 ('v', 1),
                 ('c', 6)]

LISTEN_TO_THE_PEOPLE = [(' ', 1),
                        ('c', 0.5),
                        ('v', 0.5),
                        ('b', 0.5),
                        ('n', 0.5),
                        ('m', 1),
                        ('/', 3),
                        ('/', 0.5),
                        ('.', 0.5),
                        (',', 0.5),
                        ('.', 0.5),
                        ('m', 3),
                        (' ', 1),
                        (',', 0.5),
                        ('m', 0.5),
                        ('n', 0.5),
                        (',', 0.5),
                        ('m', 1),
                        ('c', 3),
                        ('v', 0.5),
                        ('b', 0.5),
                        ('n', 0.5),
                        ('b', 0.5),
                        ('v', 3),
                        (' ', 1),
                        ('c', 0.5),
                        ('v', 0.5),
                        ('b', 0.5),
                        ('n', 0.5),
                        ('m', 1),
                        ('/', 3),
                        ('/', 0.5),
                        ('.', 0.5),
                        (',', 0.5),
                        ('.', 0.5),
                        ('m', 3),
                        (' ', 1),
                        (',', 0.5),
                        ('m', 0.5),
                        ('n', 0.5),
                        (',', 0.5),
                        ('m', 1),
                        ('c', 2.5),
                        ('c', 0.5),
                        ('n', 0.5),
                        ('b', 0.5),
                        ('v', 0.5),
                        ('b', 0.5),
                        ('c', 3),
                        ('s', 0.5),
                        ('c', 0.5),
                        ('v', 0.5),
                        ('b', 0.5),
                        ('n', 0.5),
                        ('m', 0.5),
                        (',', 1),
                        ('/', 0.5),
                        ('.', 0.5),
                        (',', 0.5),
                        ('.', 0.5),
                        ('/', 1),
                        (',', 2),
                        (' ', 1),
                        ('.', 0.5),
                        (',', 0.5),
                        ('m', 0.5),
                        (',', 0.5),
                        ('.', 3),
                        (' ', 1),
                        (',', 0.5),
                        ('m', 0.5),
                        ('n', 0.5),
                        ('m', 0.5),
                        (',', 1),
                        ('n', 2),
                        (' ', 1),
                        ('m', 0.5),
                        ('n', 0.5),
                        ('b', 0.5),
                        ('n', 0.5),
                        ('m', 3),
                        (' ', 1),
                        ('/', 0.5),
                        ('.', 0.5),
                        (',', 0.5),
                        ('.', 0.5),
                        ('/', 1),
                        (',', 2),
                        ('\'+', 0.5),
                        ('/', 0.5),
                        ('.', 0.5),
                        ('/', 0.5),
                        ('m', 3),
                        (' ', 1),
                        ('\'+', 0.5),
                        ('/', 0.5),
                        ('.', 0.5),
                        ('/', 0.5),
                        ('m', 3),
                        (' ', 1),
                        (',', 0.5),
                        ('m', 0.5),
                        ('n', 0.5),
                        (',', 0.5),
                        ('m', 1),
                        ('c', 2),
                        (' ', 1),
                        ('n', 0.5),
                        ('b', 0.5),
                        ('v', 0.5),
                        ('b', 0.5),
                        ('c', 3)]

AT_CALVARY = [('m', 1.5),
              ('m', 0.5),
              ('m', 0.75),
              ('n', 0.25),
              ('b', 0.75),
              ('n', 0.25),
              ('m', 1),
              (',', 1),
              ('m', 2),
              ('.', 1.5),
              ('.', 0.5),
              ('.', 0.75),
              (',', 0.25),
              ('m', 0.75),
              ('n', 0.25),
              ('b', 1),
              (',', 1),
              ('m', 2),
              ('m', 1.5),
              ('m', 0.5),
              ('m', 0.75),
              ('n', 0.25),
              ('b', 0.75),
              ('n', 0.25),
              ('m', 1),
              (',', 1),
              ('m', 1),
              ('/', 1),
              ('\'+', 2),
              ('.', 2),
              ('/', 4),
              ('/', 1.5),
              ('.', 0.5),
              ('/', 0.75),
              ('.', 0.25),
              ('/', 0.75),
              (',', 0.25),
              (',', 1),
              ('m', 1),
              ('m', 2),
              ('.', 1.5),
              (',', 0.5),
              ('.', 0.75),
              (',', 0.25),
              ('.', 0.75),
              (',', 0.25),
              ('m', 1),
              ('/', 1),
              ('/', 2),
              ('/', 1.5),
              ('.', 0.5),
              ('/', 0.75),
              ('.', 0.25),
              ('/', 0.75),
              (',', 0.25),
              (',', 1),
              ('m', 1),
              ('m', 1),
              ('/', 1),
              ('\'+', 2),
              ('.', 2),
              ('/', 4)]

MY_GOD_IS_GOOD = [('b', 0.5),
                  ('b', 0.5),
                  ('b', 0.5),
                  ('b', 0.5),
                  ('n', 0.5),
                  ('n', 0.5),
                  ('n', 0.5),
                  ('b', 0.5),
                  ('v', 0.5),
                  ('v', 0.5),
                  ('m', 0.5),
                  ('v', 0.5),
                  ('b', 2),
                  ('n', 0.5),
                  ('n', 0.5),
                  ('m', 0.5),
                  (',', 0.5),
                  ('m', 0.5),
                  ('c', 0.5),
                  ('n', 0.5),
                  ('b', 0.5),
                  ('v', 4),
                  ('b', 0.5),
                  ('b', 0.5),
                  ('b', 0.5),
                  ('b', 0.5),
                  ('n', 0.5),
                  ('b', 0.5),
                  ('b', 0.5),
                  ('b', 0.5),
                  (',', 0.5),
                  (',', 0.5),
                  ('.', 0.5),
                  (',', 0.5),
                  ('b', 1),
                  ('b', 1),
                  ('n', 0.5),
                  ('n', 0.5),
                  ('m', 0.5),
                  (',', 0.5),
                  ('m', 0.5),
                  ('c', 0.5),
                  ('n', 0.5),
                  ('b', 0.5),
                  ('v', 5),
                  ('m', 1),
                  (',', 1),
                  ('.', 1),
                  ('.', 0.5),
                  ('/', 0.5),
                  ('/', 0.5),
                  ('m', 0.5),
                  ('m', 1.5),
                  ('b', 0.5),
                  ('n', 0.5),
                  ('b', 0.5),
                  ('c', 0.5),
                  ('v', 0.5),
                  ('b', 1.5),
                  ('b', 0.5),
                  ('n', 0.5),
                  ('n', 0.5),
                  ('m', 0.5),
                  (',', 0.5),
                  ('m', 0.5),
                  ('/', 0.5),
                  ('/', 0.5),
                  ('.', 0.5),
                  (',', 0.5),
                  (',', 0.5),
                  ('.', 0.5),
                  ('/', 0.5),
                  ('\'+', 1.5),
                  ('\'+', 0.5),
                  ('\'+++', 0.5),
                  ('\'+++', 0.5),
                  ('\'+++', 0.5),
                  ('\'+', 0.5),
                  ('\'+', 0.5),
                  ('/', 0.5),
                  ('.', 0.5),
                  ('/', 0.5),
                  (',', 0.5),
                  (',', 0.5),
                  (',', 0.5),
                  ('m', 0.5),
                  ('n', 1.5),
                  ('v', 0.5),
                  ('b', 0.5),
                  ('m', 0.5),
                  ('m', 0.5),
                  ('b', 0.5),
                  ('n', 0.5),
                  (',', 0.5),
                  (',', 0.5),
                  ('m', 0.5),
                  (',', 2),
                  ('.', 2),
                  ('/', 4)]

ALL_THE_WAY = [('m', 2),
               (',', 1),
               ('m', 2),
               ('m', 1),
               ('n', 2),
               ('b', 1),
               ('n', 0.5),
               ('b', 0.5),
               ('v', 2),
               ('b', 2),
               ('m', 1),
               ('/', 2),
               ('m', 1),
               ('n', 2),
               ('v', 1),
               ('m', 3),
               ('m', 2),
               (',', 1),
               ('m', 2),
               ('m', 1),
               (',', 2),
               ('.', 1),
               ('/', 1),
               (',', 2),
               ('m', 2),
               ('b', 1),
               ('c', 2),
               ('b', 1),
               ('v', 2),
               ('c', 1),
               ('c', 3),
               ('/', 2),
               ('\'+', 1),
               ('/', 2),
               ('.', 1),
               ('/', 2),
               ('\'+', 1),
               ('/', 1),
               (',', 2),
               ('m', 2),
               ('/', 1),
               ('\'+++', 2),
               ('/', 1),
               ('\'+', 2),
               (',', 1),
               ('m', 3),
               ('m', 1),
               (',', 1),
               ('.', 1),
               ('/', 2),
               ('.', 1),
               (',', 2),
               ('m', 1),
               ('m', 1),
               ('b', 2),
               ('b', 2),
               ('m', 1),
               ('c', 2),
               ('b', 1),
               ('v', 2),
               ('c', 1),
               ('c', 3)]

# KNOWN MUSIC
SONGS = I_WORSHIP_THEE, \
        I_WILL_FOLLOW, \
        LISTEN_TO_THE_PEOPLE, \
        AT_CALVARY, \
        MY_GOD_IS_GOOD, \
        ALL_THE_WAY

def main():
    print '''
MENU
====
(R)andom
(S)huffle
(P)lay
(K)eyboard
(A)uthor
(N)ew Song'''
    while True:
        key = msvcrt.getch()
        if key in 'rspk': print
        if key == 'r': menu_help(random.random)
        if key == 's': menu_help(random.shuffle)
        if key == 'p': select_song()
        if key == 'k': menu_help()
        if key == 'a': author()
        if key == 'n': new_song()

def new_song():
    while True:
        sig = 0
        for notes in NEW_SONG:
            sig *= 2
            for note in random.sample(notes, 2):
                try:
                    winsound.Beep(get_frequency(note), int(100 / float(NS_SP)))
                except:
                    pass
            if notes[1] == note:
                sig += 1
            time.sleep((1.0 / 30) / NS_SP)
        if not SHOW_FREQU:
            print sig + 1

def select_song():
    songs = (('I_WORSHIP_THEE', I_WORSHIP_THEE),
             ('I_WILL_FOLLOW', I_WILL_FOLLOW),
             ('LISTEN_TO_THE_PEOPLE', LISTEN_TO_THE_PEOPLE),
             ('AT_CALVARY', AT_CALVARY),
             ('MY_GOD_IS_GOOD', MY_GOD_IS_GOOD),
             ('ALL_THE_WAY', ALL_THE_WAY))
    for index, data in enumerate(songs):
        print '(%s) %s' % (index + 1, data[0].replace('_', ' ').lower().title())
    while True:
        try:
            index = int(raw_input('\nSelect: '))
            assert 0 < index <= len(songs)
            play(songs[index - 1][1])
        except:
            pass

def menu_help(score=None):
    if isinstance(score, list):
        play(score)
    elif score is random.random:
        play_random()
    elif score is random.shuffle:
        play_songs()
    keyboard()

def play(score):
    for key, duration in score:
        duration /= float(SPEED)
        bd = int(duration * HOLD_RATIO * 1000)
        sd = duration * (1 - HOLD_RATIO)
        try:
            winsound.Beep(get_frequency(key), bd)
        except:
            time.sleep(duration * HOLD_RATIO)
        time.sleep(sd)

def keyboard():
    while msvcrt.kbhit():
        msvcrt.getch()
    while True:
        try:
            winsound.Beep(get_frequency(msvcrt.getch()), 100)
        except:
            pass

def get_frequency(key):
    assert key[0] in KEYS
    if SHOW_FREQU:
        frequ = int((A4 * 2 ** ((KEYS.find(key[0]) + key.count('+') - (0 if key[0] == '-' else key.count('-')) + TRANSPOSE) / 12.0)) + 0.5)
        print frequ
        return frequ
    else:
        print key,
        return int((A4 * 2 ** ((KEYS.find(key[0]) + key.count('+') - (0 if key[0] == '-' else key.count('-')) + TRANSPOSE) / 12.0)) + 0.5)

def play_random():
    key = 'c'
    RANDOM_KEYS = WHITE_KEYS
    while not msvcrt.kbhit():
        if random.random() < SWITCH_RATIO:
            if RANDOM_KEYS is WHITE_KEYS:
                RANDOM_KEYS = BLACK_KEYS
            else:
                RANDOM_KEYS = WHITE_KEYS
            key = RANDOM_KEYS[random.randrange(len(RANDOM_KEYS))]
        if random.random() < NEIGHBOR_RATIO:
            index = RANDOM_KEYS.index(key[0]) + key.count('+') - key.count('-') + random.randrange(2) * 2 - 1
            if index < 0:
                key = RANDOM_KEYS[0] + '-' * (index * -1)
            elif index >= len(RANDOM_KEYS):
                key = RANDOM_KEYS[-1] + '+' * (index - len(RANDOM_KEYS) + 1)
            else:
                key = RANDOM_KEYS[index]
        else:
            key = RANDOM_KEYS[random.randrange(len(RANDOM_KEYS))]
        if random.random() < ODD_RATIO:
            if random.randrange(2):
                key += '+'
            else:
                key += '-'
        neg = key.count('-')
        pos = key.count('+')
        trans = pos - neg
        if trans > 0:
            key = key[0] + '+' * trans
        elif trans < 0:
            key = key[0] + '-' * (trans * -1)
        else:
            key = key[0]
        winsound.Beep(get_frequency(key), 100)

def play_songs():
    songs = list(SONGS)
    while True:
        random.shuffle(songs)
        for song in songs:
            play(song)
            time.sleep(PAUSE_TIME)

def author():
    for note in AUTHOR:
        winsound.Beep(get_frequency(note), 1000)
    time.sleep(1)
    while msvcrt.kbhit():
        msvcrt.getch()
    author = random.sample(AUTHOR, len(AUTHOR))
    while not msvcrt.kbhit():
        for note in author:
            winsound.Beep(get_frequency(note), 100)
        last_note = author[-1]
        author = random.sample(AUTHOR, len(AUTHOR))
        while author[0] == last_note:
            author = random.sample(AUTHOR, len(AUTHOR))

if __name__ == '__main__':
    main()
