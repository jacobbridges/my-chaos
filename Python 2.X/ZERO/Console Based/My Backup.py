SOUR = 'C:\\Documents and Settings\\Zero\\My Documents'
DEST = 'F:\\'

BAD_EXT = 'db', 'ini', 'pyc'

import os
import aens_time

# DELETE UN-NEEDED FILES
# DELETE EMPYT FOLDERS
# CREATE DESTINATION FOLDER
# COPY SOURCE TO DESTINATION

def prune_files(top):
    for root, dirs, files in os.walk(top):
        for name in files:
            if os.path.splitext(name)[1][1:].lower() in BAD_EXT:
                path = os.path.join(root, name)
                os.remove(path)
                print 'REMOVE:', path

########################################

def prune_folders(path):
    if sum(map(prune_folders, filter(os.path.isdir, map(lambda name: os.path.join(path, name), os.listdir(path))))) == 0 and len(filter(os.path.isfile, map(lambda name: os.path.join(path, name), os.listdir(path)))) == 0:
        os.rmdir(path)
        print 'RMDIR:', path
        return False
    return True

def empty(path): # CONCEPT ALGORITHM
    for name in os.listdir(path):
        path_name = os.path.join(path, name)
        if os.path.isdir(path_name):
            if not empty(path_name):
                return False
        elif os.path.isfile(path_name):
            return False
    return True

########################################

def get_destination(root):
    new = aens_time.format(aens_time.seconds())
    path = os.path.join(root, new)
    print 'MKDIR:', path
    return path

########################################

def copy(source, destination, ignore=None, errors=None):
    # Check recursion level.
    if ignore is None and errors is None:
        root = True
        ignore = destination
        errors = list()
    else:
        root = False
    # Copy everything from the source to the destination.
    directory = os.listdir(source)
    os.mkdir(destination)
    for name in directory:
        source_name = os.path.join(source, name)
        destination_name = os.path.join(destination, name)
        try:
            if source_name == ignore:
                continue
            elif os.path.isdir(source_name):
                copy(source_name, destination_name, ignore, errors)
            elif os.path.isfile(source_name):
                copy_file(source_name, destination_name)
        except:
            errors.append('%s\n%s' % (source_name, destination_name))
    # Write error log if needed.
    if root and errors:
        file(os.path.join(os.path.dirname(sys.argv[0]), 'error.log'), 'w').write('\n\n'.join(errors))

def copy_file(source, destination):
    s = open(source, 'rb')
    d = open(destination, 'wb')
    buff = s.read(2 ** 20)
    while buff:
        d.write(buff)
        buff = s.read(2 ** 20)
    s.close()
    d.close()

########################################

if __name__ == '__main__':
    prune_files(SOUR)
    prune_folders(SOUR)
    dest = get_destination(DEST)
    copy(SOUR, dest)
    raw_input('\nDone.')
