import z_service, time

def main():
    log = file(raw_input('Filename: '), 'w')
    client = z_service.Client(raw_input('Host: '), 9000)
    ticket = 0
    while True:
        temp_ticket, messages = client('query', None, ticket)
        if temp_ticket:
            ticket = temp_ticket
            for message in messages:
                log.write(message + '\n')
        time.sleep(60 * 4)

if __name__ == '__main__':
    main()
