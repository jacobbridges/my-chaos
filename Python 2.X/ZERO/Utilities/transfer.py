def main():
    try:
        from os import mkdir
        from os.path import basename, isdir
        while True:
            from_path = raw_input('Copy From: ')
            to_path = raw_input('Copy To: ')
            if not isdir(to_path):
                mkdir(to_path)
            paste_dir(copy_dir(from_path), to_path)
    except:
        pass

def copy_file(path):
    '''copy_file(str)

    Import all needed functions.
    Assert that path is valid.
    Return  the filename and data.'''
    from os.path import basename, isfile
    assert isfile(path)
    return (basename(path), file(path, 'rb', 0).read())

def paste_file(file_object, path):
    '''paste_file(tuple, str)

    Import all needed functions.
    Assert that path is valid.
    Create a file from file_object.'''
    from os.path import isdir, join
    assert isdir(path)
    file(join(path, file_object[0]), 'wb', 0).write(file_object[1])

def copy_dir(path):
    '''copy_dir(str)

    Import all needed functions.
    Assert that path is valid.
    Create a storage variable.
    Store all valid data.
    Return all valid data.'''
    from os import listdir
    from os.path import basename, isdir, isfile, join
    assert isdir(path)
    dir_object = (basename(path), list())
    for name in listdir(path):
        next_path = join(path, name)
        try:
            if isdir(next_path):
                dir_object[1].append(copy_dir(next_path))
            elif isfile(next_path):
                dir_object[1].append(copy_file(next_path))
        except:
            print 'ERROR:', next_path
    return dir_object

def paste_dir(dir_object, path):
    '''paste_dir(tuple, str)

    Import all needed functions.
    Assert that path is valid.
    Modify path and create a directory if needed.
    Write all stored data.'''
    from os import mkdir
    from os.path import isdir, join
    assert isdir(path)
    if dir_object[0] is not '':
        path = join(path, dir_object[0])
        mkdir(path)
    for object in dir_object[1]:
        try:
            if type(object[1]) is list:
                paste_dir(object, path)
            else:
                paste_file(object, path)
        except:
            print 'ERROR:', join(path, object[0])

if __name__ == '__main__':
    main()
