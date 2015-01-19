import socket

def main():
    print 'Loading Index ...',
    index = load_index('vintage_index.bin')
    print 'Done'
    print 'Starting Server ...',
    main_socket = socket.socket()
    main_socket.bind(('', 1337))
    main_socket.listen(10)
    print 'Done'
    while True:
        work_socket = main_socket.accept()
        print 'Port', work_socket[1][1], '...',
        if work_socket[1][0] == '127.0.0.1':
            query_string = get_all(work_socket[0])
            answer_string = get_answer(index, query_string)
            set_all(work_socket[0], answer_string)
            error = ''
        else:
            error = '(' + work_socket[1][0] + ')'
        work_socket[0].close()
        print 'Done', error

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
    

def get_all(work_socket):
    query_string = temp = work_socket.recv(1024)
    while len(query_string) < 1024 and '\n' not in query_string and temp != '':
        temp = work_socket.recv(1024)
        query_string += temp
    return query_string

def get_answer(index, query_string):
    try:
        return index[int(query_string[:query_string.index('\n')])]
    except:
        return 'ERROR'

def set_all(work_socket, answer_string):
    size = len(answer_string)
    fail = 0
    while len(answer_string) is not 0 and fail is not 10:
        answer_string = answer_string[work_socket.send(answer_string):]
        if len(answer_string) == size:
            fail += 1
        size = len(answer_string)

if __name__ == '__main__':
    main()
