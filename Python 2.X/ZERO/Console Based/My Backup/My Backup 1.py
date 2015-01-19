import os
from aens_time import *

################################################################################

# DIRECTORIES
GET = 'C:\\Documents and Settings\\Zero\\My Documents'
SET = 'F:\\BACKUP'

# CONFIGURATION
BAD = 'db', 'pyc'
ERR = []

################################################################################

# PRIMARY WITH CLEANUP

def main():
    patch_bookmarks() # NEW
    remove(GET)
    rmdir(GET)
    destination = os.path.join(SET, format(seconds()))
    copy_dir(GET, destination)
    raw_input('\n====\nDONE\n====')
    handle_errors()

def handle_errors():
    if ERR:
        print
        for source_name in ERR:
            print 'ERROR: ', source_name
        raw_input('\n====\nWARN\n====')

################################################################################

BM_GET = 'C:\\Documents and Settings\\Zero\\Application Data\\Mozilla\\Firefox\\Profiles'
BM_SET = 'C:\\Documents and Settings\\Zero\\My Documents\\My Archive\\Other'

BM_OLD = 'bookmarks.html'
BM_NEW = 'My Bookmarks.html'

def patch_bookmarks():
    try:
        dir_list = os.listdir(BM_GET)
        assert len(dir_list) == 1, 'THERE MUST BE ONE PROFILE'
        bookmarks = os.path.join(BM_GET, dir_list[0], BM_OLD)
        data = file(bookmarks, 'rb').read()
        bookmarks = os.path.join(BM_SET, BM_NEW)
        file(bookmarks, 'wb').write(data)
        print 'PATCHED BOOKMARKS'
    except:
        import sys, traceback
        raw_input(traceback.format_exc())
        sys.exit(1)

################################################################################

# DELETE JUNK FILES

def remove(top):
    for root, dirs, files in os.walk(top):
        for name in files:
            if os.path.splitext(name)[1][1:].lower() in BAD:
                path = os.path.join(root, name)
                os.remove(path)
                print 'REMOVE:', path

################################################################################

# REMOVE EMPTY FOLDERS

def rmdir(top):
    for root, dirs, files in os.walk(top, False):
        for name in dirs:
            path = os.path.join(root, name)
            if empty(path):
                os.rmdir(path)
                print 'RMDIR: ', path

def empty(path):
    for name in os.listdir(path):
        path_name = os.path.join(path, name)
        if os.path.isdir(path_name):
            if not empty(path_name):
                return False
        elif os.path.isfile(path_name):
            return False
    return True

################################################################################

# MAIN BACKUP PROCEDURES

def copy_dir(source, destination):
    dir_list = os.listdir(source)
    os.mkdir(destination)
    print 'MKDIR: ', destination
    for name in dir_list:
        source_name = os.path.join(source, name)
        destination_name = os.path.join(destination, name)
        try:
            if os.path.isdir(source_name):
                copy_dir(source_name, destination_name)
            elif os.path.isfile(source_name):
                copy_file(source_name, destination_name)
        except:
            ERR.append(source_name)

def copy_file(source, destination):
    sour = open(source, 'rb')
    dest = open(destination, 'wb')
    print 'FILE:  ', destination
    buff = sour.read(2 ** 20)
    while buff:
        dest.write(buff)
        buff = sour.read(2 ** 20)
    sour.close()
    dest.close()

################################################################################

if __name__ == '__main__':
    main()
