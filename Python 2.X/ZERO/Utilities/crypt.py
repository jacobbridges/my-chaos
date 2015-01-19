import pickle, random, time

def main():
    show_heading('Welcome to CRYPT')
    print
    exit = False
    while not exit:
        answer = menu()
        if answer is 1:
            create_key()
        elif answer is 2:
            encode_file()
        elif answer is 3:
            decode_file()
        elif answer is 4:
            exit = True
        else:
            raise Exception

def show_heading(heading):
    print heading
    underline = ''
    for line in range(len(heading)):
        underline += '-'
    print underline

def menu():
    show_menu()
    return get_answer()

def show_menu():
    show_heading('MENU')
    print '(1) Create Key'
    print '(2) Encode File'
    print '(3) Decode File'
    print '(4) Exit Program'
    print

def get_answer():
    while True:
        try:
            answer = int(raw_input('Please make a selection: '))
            if answer is 1 or answer is 2 or answer is 3 or answer is 4:
                print
                return answer
        except:
            pass
        print 'You must enter 1, 2, 3, or 4 as a selection.'

def create_key():
    show_heading('CREATE KEY')
    key_file = get_destination('What will be the name of the key file?')
    key_data = create_key_data()
    pickle.Pickler(key_file).dump(key_data)
    key_file.flush()
    key_file.close()
    print 'The key has been created at the location specified.'
    print

def get_destination(prompt):
    while True:
        try:
            key = file(raw_input(prompt + ' '), 'wb')
            return key
        except:
            print 'Please enter a different filename.'

def create_key_data():
    list_one = range(256)
    list_two = range(256)
    key = []
    random.seed(time.time())
    for index in range(256):
        index_one = random.randint(0, 255 - index)
        index_two = random.randint(0, 255 - index)
        key.append((list_one[index_one], list_two[index_two]))
        del list_one[index_one], list_two[index_two]
    return key

def encode_file():
    show_heading('ENCODE FILE')
    source = get_source('What is the name of the source file?')
    destination = get_destination('What will be the name of the destination file?')
    bad_key = True
    while bad_key:
        try:
            key = get_key()
            work_encode(source, destination, key)
            bad_key = False
        except:
            print 'Please enter a different filename.'
    print 'The encoded file has been created at the location specified.'
    print

def get_source(prompt):
    while True:
        try:
            source = file(raw_input(prompt + ' '), 'rb')
            return source
        except:
            pass
        print 'Please enter a different filename.'

def get_key():
    key_file = get_source('What is the name of the key file?')
    key = pickle.Unpickler(key_file).load()
    key_file.close()
    return key

def work_encode(source, destination, key):
    new_file = ''
    encode_key = range(256)
    for index in range(256):
        encode_key[key[index][0]] = key[index][1]
    for line in source:
        for byte in line:
            new_file += chr(encode_key[ord(byte)])
    destination.write(new_file)
    source.close()
    destination.flush()
    destination.close()

def decode_file():
    show_heading('DECODE FILE')
    source = get_source('What is the name of the source file?')
    destination = get_destination('What will be the name of the destination file?')
    bad_key = True
    while bad_key:
        try:
            key = get_key()
            work_decode(source, destination, key)
            bad_key = False
        except:
            print 'Please enter a different filename.'
    print 'The decoded file has been created at the location specified.'
    print

def work_decode(source, destination, key):
    new_file = ''
    decode_key = range(256)
    for index in range(256):
        decode_key[key[index][1]] = key[index][0]
    for line in source:
        for byte in line:
            new_file += chr(decode_key[ord(byte)])
    destination.write(new_file)
    source.close()
    destination.flush()
    destination.close()

if __name__ == '__main__':
    main()
