import getpass, os
import para_time

################################################################################

# SOURCE AND DESTINATION
GET = 'C:\\Documents and Settings\\' + getpass.getuser()
SET = 'G:\\BACKUP'

# BOOKMARK NAME SETTINGS
OLD_NAME = 'bookmarks.html'
NEW_NAME = 'Favorites.html'

# JUNK DATA KEYS
BAD_FILE = 'Thumbs.db', 'Desktop.ini'
BAD_EXT = 'pyc', 'pyo'

################################################################################

def main():
    patch_bookmarks()
    prune_junk()
    prune_dirs()
    build_sink()
    write_dirs(GET, SINK)
    print_last()

def print_last():
    raw_input('\n====\nDONE\n====\n')
    if ERR:
        for source_name in ERR:
            print 'ERROR:   ', source_name
        raw_input('\n====\nWARN\n====\n')

################################################################################

BM_GET = GET + '\\Application Data\\Mozilla\\Firefox\\Profiles'
BM_SET = GET + '\\My Documents\\Favorites'

def patch_bookmarks():
    try:
        dir_list = os.listdir(BM_GET)
        assert len(dir_list) == 1, 'THERE MUST BE (1) PROFILE'
        bookmarks = os.path.join(BM_GET, dir_list[0], OLD_NAME)
        data = file(bookmarks, 'rb').read()
        bookmarks = os.path.join(BM_SET, NEW_NAME)
        file(bookmarks, 'wb').write(data)
        print 'PATCHED BOOKMARKS'
    except Exception, error:
        raw_input(error.message)
        raise SystemExit

################################################################################

BAD_FILE = [name.lower() for name in BAD_FILE]
BAD_EXT = [name.lower() for name in BAD_EXT]

def prune_junk():
    for root, dirs, files in os.walk(GET):
        for name in files:
            path = name.lower()
            if path in BAD_FILE or os.path.splitext(path)[1][1:] in BAD_EXT:
                path = os.path.join(root, name)
                os.remove(path)
                print 'REMOVE:  ', path

################################################################################

def prune_dirs():
    for root, dirs, files in os.walk(GET, False):
        for name in dirs:
            path = os.path.join(root, name)
            if empty(path):
                os.rmdir(path)
                print 'RMDIR:   ', path

def empty(path):
    for name in os.listdir(path):
        path_name = os.path.join(path, name)
        if os.path.isdir(path_name) and not empty(path_name):
            return False
        elif os.path.isfile(path_name):
            return False
        return True

################################################################################

GET = os.path.join(GET, 'My Documents')
ERR = []

def build_sink():
    global SINK
    try:
        os.makedirs(SET)
    except:
        pass
    else:
        print 'MAKEDIRS:', SET
    SINK = os.path.join(SET, para_time.format(para_time.seconds()))

################################################################################

def write_dirs(source, destination):
    dir_list = os.listdir(source)
    os.mkdir(destination)
    print 'MKDIR:   ', destination
    for name in dir_list:
        source_name = os.path.join(source, name)
        destination_name = os.path.join(destination, name)
        try:
            if os.path.isdir(source_name):
                write_dirs(source_name, destination_name)
            elif os.path.isfile(source_name):
                write_file(source_name, destination_name)
        except:
            ERR.append(source_name)

def write_file(source, destination):
    sour = open(source, 'rb')
    dest = open(destination, 'wb')
    print 'OPEN:    ', destination
    buff = sour.read(2 ** 20)
    while buff:
        dest.write(buff)
        buff = sour.read(2 ** 20)
    sour.close()
    dest.close()

################################################################################

if __name__ == '__main__':
    main()
