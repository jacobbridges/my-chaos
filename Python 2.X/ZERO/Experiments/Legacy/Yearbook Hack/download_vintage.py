import httplib

def main():
    vintage_index = load_index('vintage_index.bin')
    total = vintage_index.count('1')
    count = 0
    for index in range(10000):
        if vintage_index[index] == '1':
            count += 1
            print 'Saving picture', count, 'of', total
            save_picture(index)

def load_index(name):
    string = file(name, 'rb', 0).read()
    index = str()
    for byte in string:
        index += convert(ord(byte)).zfill(8)
    return index

def convert(byte):
    string = str()
    while byte is not 0:
        string = str(byte % 2) + string
        byte = byte >> 1
    return string

def save_picture(index):
    picture = get_picture(index)
    file('.\\vintage_images\\stu_ed%s.jpg' % index, 'wb', 0).write(picture)

def get_picture(index):
    connection = httplib.HTTPSConnection('home.bju.edu')
    connection.request('GET', '/vintage_images/stu_ed%s.jpg' % index)
    return connection.getresponse().read()

if __name__ == '__main__':
    main()
