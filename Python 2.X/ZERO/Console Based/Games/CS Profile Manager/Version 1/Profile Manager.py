import traceback
import os
import sha
import random
import spice
import cStringIO
import sys

TEST_FILE = 'Doukutsu.exe'
TEST_SHA = 'bb2d0441e073da9c584f23c2ad8c7ab8aac293bf'
SAVE_PATH = 'save'
MAJOR_KEY = 987659
MINOR_KEY = 977

VALID_COMMANDS = 'help', 'save', 'load', 'pax', 'delete'
STRING = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

def main():
    check_data()
    load_keys()
    load_profiles()
    command_line()
    save_profiles()
    
def check_data():
    if not os.path.isfile(TEST_FILE):
        raw_input('File not found: %s\n' % TEST_FILE)
        sys.exit(1)
    if not sha.new(file(TEST_FILE, 'rb').read()).hexdigest() == TEST_SHA:
        raw_input('Corrupt file found: %s\n' % TEST_FILE)
        sys.exit(2)
    if os.path.exists(SAVE_PATH):
        if not os.path.isdir(SAVE_PATH):
            raw_input('Reserved name taken: %s\n' % SAVE_PATH)
            sys.exit(3)
    else:
        os.makedirs(SAVE_PATH)

def load_keys():
    global MAJOR_KEY, MINOR_KEY
    random.seed(MAJOR_KEY)
    MAJOR_KEY = spice.major()
    random.seed(MINOR_KEY)
    MINOR_KEY = spice.minor()
    random.seed()

def load_profiles():
    global profiles
    profiles = dict()
    for name in os.listdir(SAVE_PATH):
        path = os.path.join(SAVE_PATH, name)
        if os.path.isfile(path):
            add_profile(path)
            os.remove(path)
        else:
            os.rmdir(path)

def add_profile(path):
    string = cStringIO.StringIO()
    spice.decode(open(path, 'rb'), string, MAJOR_KEY, MINOR_KEY)
    data = string.getvalue()
    profile = data[:1540]
    if not len(profile) == 1540:
        raw_input('Corrupt profile found: %s\n' % path)
        sys.exit(4)
    name = data[1540:]
    profiles[name] = profile

def command_line():
    print 'Profile Manager v1.0'
    print '===================='
    print
    while True:
        command = raw_input('>>> ').lower()
        if command not in VALID_COMMANDS:
            print 'UNKNOWN COMMAND: %r\n' % command
        else:
            try:
                globals()[command]()
                print
            except:
                break

def help():
    print 'Valid Commands:'
    print '  help: get this message'
    print '  save: store current profile'
    print '  load: get a saved profile'
    print '  pax: publish and exit'
    print '  delete: discard a profile'

def save():
    if not os.path.isfile('Profile.dat'):
        print 'PROFILE NOT FOUND'
    else:
        profile = file('Profile.dat', 'rb').read()
        name = raw_input('Save As: ')
        profiles[name] = profile

def load():
    names = profiles.keys()
    if not names:
        print 'PROFILES NOT FOUND'
    else:
        print 'Please select a profile:'
        for index, name in enumerate(names):
            print '(%s) - %r' % (index + 1, name)
        print
        while True:
            try:
                index = int(raw_input('Index: ')) - 1
                assert index > -1
                name = names[index]
                break
            except:
                print 'INDEX OUTSIDE RANGE'
        file('Profile.dat', 'wb').write(profiles[name])
                
def pax():
    raise Exception

def save_profiles():
    for name in profiles:
        source = cStringIO.StringIO(profiles[name] + name)
        ID = ''.join(random.sample(STRING, len(STRING)))
        path = os.path.join(SAVE_PATH, ID)
        spice.encode(source, open(path, 'wb'), MAJOR_KEY, MINOR_KEY)

def delete():
    names = profiles.keys()
    if not names:
        print 'PROFILES NOT FOUND'
    else:
        print 'Please select a profile:'
        for index, name in enumerate(names):
            print '(%s) - %r' % (index + 1, name)
        print
        while True:
            try:
                index = int(raw_input('Index: ')) - 1
                assert index > -1
                name = names[index]
                break
            except:
                print 'INDEX OUTSIDE RANGE'
        del profiles[names[index]]
        
if __name__ == '__main__':
    try:
        main()
    except Exception:
        raw_input(traceback.format_exc())
    except:
        pass
    
