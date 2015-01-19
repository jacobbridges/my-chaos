import z_service

def main():
    name = raw_input('Name: ')
    client = z_service.Client(raw_input('Host: '), 9000)
    while True:
        client('add', name, raw_input('Say: '))

if __name__ == '__main__':
    main()
