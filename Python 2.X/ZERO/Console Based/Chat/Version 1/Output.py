import z_service, time

def main():
    name = raw_input('Name: ')
    client = z_service.Client(raw_input('Host: '), 9000)
    ticket = 0
    while True:
        temp_ticket, messages = client('query', name, ticket)
        if temp_ticket:
            ticket = temp_ticket
            for message in messages:
                print message
        time.sleep(5)

if __name__ == '__main__':
    main()
