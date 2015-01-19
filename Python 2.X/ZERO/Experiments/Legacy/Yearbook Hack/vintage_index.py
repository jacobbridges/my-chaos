import httplib

def main():
    print 'Creating Index ...'
    index_list = create_index(10000)
    print 'Creating Binary ...'
    binary_list = create_binary(index_list)
    print 'Creating Number ...'
    number_list = create_number(binary_list)
    print 'Creating Character ...'
    character_list = create_character(number_list)
    print 'Creating String ...'
    string = create_string(character_list)
    print 'Writing File ...'
    file('vintage_index.bin', 'wb', 0).write(string)

def create_index(size):
    index_list = list()
    for index in range((size / 8) * 8):
        print 'Checking File', index, '...'
        index_list.append(check_URL('home.bju.edu', '/vintage_images/stu_ed%s.jpg' % index))
    return index_list

def check_URL(host, url):
    connection = httplib.HTTPSConnection(host)
    connection.request('HEAD', url)
    return connection.getresponse().status == 200

def create_binary(index_list):
    binary_list = list()
    for index in range(len(index_list) / 8):
        string = str()
        for digit in range(8):
            if index_list[index * 8 + digit]:
                string += '1'
            else:
                string += '0'
        binary_list.append(string)
    return binary_list

def create_number(binary_list):
    number_list = list()
    for binary in binary_list:
        number_list.append(int(binary, 2))
    return number_list

def create_character(number_list):
    character_list = list()
    for number in number_list:
        character_list.append(chr(number))
    return character_list

def create_string(character_list):
    string = str()
    for character in character_list:
        string += character
    return string

if __name__ == '__main__':
    main()
