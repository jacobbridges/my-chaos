import os, time                 # Provide os.getsize() & time.time()
import spice_coding, spice_key  # Provide Core Functions

import random; random.seed()    # Initialize Random State

LIMIT_FLAG = True               # Limiting Is Active
LIMIT_SIZE = 1024 * 1024        # 1 MB Source On Encrypt

def main():
    print underline('Welcome to Spice')
    print
    while True:
        select = menu()
        if select == 1:
            create_key()
        elif select == 2:
            encrypt_file()
        elif select == 3:
            decrypt_file()
        else:
            print 'Good-bye!'
            break
        print 'Done.'
        print

def underline(string):
    return string + '\n' + '=' * len(string)

def menu():
    print underline('Menu')
    print '(1) Create Key'
    print '(2) Encrypt File'
    print '(3) Decrypt File'
    print '(4) Exit Program'
    while True:
        try:
            select = int(raw_input('Select: '))
            if 0 < select < 5:
                if select != 4:
                    print
                return select
        except:
            pass
        print 'ERROR: Selection must be between 1 and 4.'

def create_key():
    print underline('Create Key')
    major, minor = create_keys()
    major.write(spice_key.new_night_key(spice_key.new_major_key()))
    minor.write(spice_key.new_night_key(spice_key.new_minor_key()))
    major.close()
    minor.close()

def create_keys():
    while True:
        file_name = raw_input('Name: ')
        try:
            return open(file_name + '.major', 'wb', 0), \
                   open(file_name + '.minor', 'wb', 0)
        except:
            print 'ERROR: Name must be different.'

def encrypt_file():
    print underline('Encrypt File')
    source = get_source(False)
    destination = get_destination()
    major, minor = get_keys()
    source_size = len(source)                           # INFO CODE
    print 'Source Size:', source_size, 'Bytes'          # INFO CODE
    seconds = time.time()                               # INFO CODE
    destination.write(spice_coding.encode(major, minor, source))
    difference = time.time() - seconds                  # INFO CODE
    destination.close()
    print 'Encrypt Time:', int(difference), 'Seconds'   # INFO CODE
    if difference != 0:                                 # INFO CODE
        print int(source_size / difference), 'B/S'      # INFO CODE

def get_source(decrypt):
    global LIMIT_FLAG, LIMIT_SIZE
    while True:
        try:
            file_name = raw_input('Source: ')
            if decrypt:
                assert os.path.getsize(file_name) % 4 == 0
            elif LIMIT_FLAG:
                assert os.path.getsize(file_name) <= LIMIT_SIZE
            return file(file_name, 'rb', 0).read()
        except:
            print 'ERROR: Source must be different.'

def get_destination():
    while True:
        try:
            return open(raw_input('Destination: '), 'wb', 0)
        except:
            print 'ERROR: Destination must be different.'

def get_keys():
    while True:
        file_name = raw_input('Key: ')
        try:
            return spice_key.new_dream_key(file(file_name + '.major', 'rb', 0).read()), \
                   spice_key.new_dream_key(file(file_name + '.minor', 'rb', 0).read())
        except:
            print 'ERROR: Key must be different.'

def decrypt_file():
    print underline('Decrypt File')
    source = get_source(True)
    destination = get_destination()
    major, minor = get_keys()
    source_size = len(source)                           # INFO CODE
    print 'Source Size:', source_size, 'Bytes'          # INFO CODE
    seconds = time.time()                               # INFO CODE
    destination.write(spice_coding.decode(major, minor, source))
    difference = time.time() - seconds                  # INFO CODE
    destination.close()
    print 'Decrypt Time:', int(difference), 'Seconds'   # INFO CODE
    if difference != 0:                                 # INFO CODE
        print int(source_size / difference), 'B/S'      # INFO CODE

if __name__ == '__main__':
    main()
