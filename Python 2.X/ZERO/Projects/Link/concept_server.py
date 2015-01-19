class Virtual:

    'Virtual(connection, name) -> Virtual'
    
    def __init__(self, link, name):
        'Initialize the Virtual object.'
        self.__link = link
        self.__name = name

    def __getattr__(self, name):
        'Extend the object call.'
        return Virtual(self.__link, '%s.%s' % (self.__name, name))

    def __call__(self, *args, **kwargs):
        'Call the object specified.'
        return self.__link(self.__name, *args, **kwargs)

################################################################################

class Server:

    'Server() -> Server'

    def __init__(self, callback):
        'Initialize the Server object.'
        self.__callback = callback
        # reference data
        self.__title = None         # server's title
        self.__name = None          # server's name
        self.__documentation = None # server's documentation
        self.__objects = {}         # installed objects
        # server thread data
        self.__active = False
        self.__thread = False
        self.__lock = thread.allocate_lock()
        # client argument data
        self.__with_client = []
        self.__wc_lock = thread.allocate_lock()

    # SERVER CONTROL METHODS

    def start(self, host, port):
        'Start the server.'
        self.__lock.acquire()
        self.__active = True
        if not self.__thread:
            self.__thread = True
            thread.start_new_thread(self.__server_thread, (host, port))
        self.__lock.release()

    def stop(self):
        'Stop the server.'
        self.__lock.acquire()
        self.__active = False
        self.__lock.release()

    def title(self, title):
        'Set the server\'s title.'
        self.__title = str(title)

    def name(self, name):
        'Set the server\'s name.'
        self.__name = str(name)

    def documentation(self, documentation):
        'Set the server\'s documentation.'
        self.__documentation = str(documentation)

    def install(self, name, obj):
        'Install an object.'
        check_name(name)
        self.__objects[str(name)] = obj

    def uninstall(self, name):
        'Uninstall an object.'
        check_name(name)
        del self.__objects[str(name)]

    def with_client(self, name):
        'Add client as first argument.'
        name = str(name)
        self.__wc_lock.acquire()
        if name not in self.__with_client:
            self.__with_client.append(name)
        self.__wc_lock.release()

    def rm_client(self, name):
        'Remove client from first argument.'
        name = str(name)
        self.__wc_lock.acquire()
        if name in self.__with_client:
            self.__with_client.remove(name)
        self.__wc_lock.release()

    # PRIVATE SERVER CODEs

    def __server_thread(self, host, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, port))
        server.listen(5)
        while True:
            client = server.accept()[0]
            self.__lock.acquire()
            if not self.__active:
                server.close()
                client.shutdown(socket.SHUT_RDWR)
                client.close()
                self.__thread = False
                self.__lock.release()
                break
            self.__lock.release()
            # create and register connection
            new_connection = Connection(self, client)
            self.__callback(new_connection)

################################################################################

class Connection:

    def __init__(self, server, client):
        self.__client()         # create client controls
        self.server = server    # create server controls
        self.__objects = server._Server__objects
        self.__socket = client
        self.__qri = spots.qri(client)
        self.__active = True
        thread.start_new_thread(self.__processor, ())
        # attributes for timeout control
        self.__thread_timeout = {}
        self.__tt_lock = thread.allocate_lock()
        # client argument data
        self.__with_client = server._Server__with_client
        self.__wc_lock = server._Server__wc_lock

    def __client(self):
        'Create client controls.'
        class client: pass
        client = client()
        # documentation controls
        client.title = self.__client_title
        client.name = self.__client_name
        client.documentation = self.__client_documentation
        # object controls
        client.objects = self.__client_objects
        client.signature = self.__client_signature
        client.help = self.__client_help
        # kill service
        client.end = self.__client_end
        # timeout controls
        client.timeout = self.__client_timeout
        client.clear = self.__client_clear
        # publish client controls
        self.client = client

    # CLIENT CONTROL METHODS

    def __client_title(self):
        'Get the client\'s title.'
        return self.__call(False, 'title')

    def __client_name(self):
        'Get the client\'s name.'
        return self.__call(False, 'name')

    def __client_documenation(self):
        'Get the client\'s documenation.'
        return self.__call(False, 'documentation')

    def __client_objects(self):
        'List the objects on the client.'
        return self.__call(False, 'objects')

    def __client_signature(self, name):
        'Get an object\'s signature.'
        return self.__call(False, 'signature', name)

    def __client_help(self, name):
        'Get an object\'s documentation.'
        return self.__call(False, 'help', name)

    def __client_end(self):
        # stop processing commands
        self.__active = False

    def __client_timeout(self, seconds):
        'Set this thread\'s timeout for calls.'
        if not isinstance(seconds, (float, int, long)):
            raise TypeError, 'timeout must be of type float, int, or long'
        if not seconds >= 0:
            raise ValueError, 'timeout must be greater than or equal to 0'
        self.__tt_lock.acquire()
        self.__thread_timeout[thread.get_ident()] = seconds
        self.__tt_lock.release()

    def __client_clear(self):
        'Clear timeouts for this thread.'
        ident = thread.get_ident()
        self.__tt_lock.acquire()
        if self.__thread_timeout.has_key(ident):
            del self.__thread_timeout[ident]
        self.__tt_lock.release()
        
    # FDR INTERFACE

    def __getattr__(self, name):
        'Get a virtual, callable object.'
        return Virtual(self, name)

    def __call__(self, name, *args, **kwargs):
        'Allow call of object.'
        return self.__call(True, name, args, kwargs)

    # PRIVATE METHODS

    def __call(self, *obj):
        'Make a call and handle errors.'
        assert self.__active, 'Client Is Not Active'
        ident = thread.get_ident()
        self.__tt_lock.acquire()
        if self.__thread_timeout.has_key(ident):
            timeout = self.__thread_timeout[ident]
            self.__tt_lock.release()
            no_error, data = self.__qri.call(obj, timeout)
        else:
            self.__tt_lock.release()
            no_error, data = self.__qri.call(obj)
        if no_error:
            return data
        raise data

    def __processor(self):
        while self.__active:
            try:
                ID, obj = self.__qri.query(5)
                if not self.__active:
                    self.__qri.reply(ID, (False, AssertionError('SERVER IS NOT ACTIVE')))
                    return
                thread.start_new_thread(self.__worker, (ID, obj))
            except Warning:
                pass
            except:
                self.__socket.shutdown(socket.SHUT_RDWR)
                self.__socket.close()
                raise

    def __worker(self, ID, obj):
        normal_query, name = obj[:2]
        if normal_query:
            exists, the_obj = self.__find(name)
            if exists:
                self.__exe(ID, the_obj, name, *obj[2:])
            else:
                self.__qri.reply(ID, (False, AttributeError(name)))
        else:
            # SECTION W2
            if name == 'title':
                self.__qri.reply(ID, (True, self.server._Server__title))
            elif name == 'name':
                self.__qri.reply(ID, (True, self.server._Server__name))
            elif name == 'documentation':
                self.__qri.reply(ID, (True, self.server._Server__documentation))
            elif name == 'objects':
                self.__qri.reply(ID, (True, sorted(self.__objects.keys())))
            elif name == 'signature':
                self.__reply_signature(ID, obj[2])
            elif name == 'help':
                self.__reply_help(ID, obj[2])
            else:
                self.__qri.reply(ID, (False, NotImplementedError(name)))
            
    def __exe(self, ID, obj, name, args, kwargs):
        args = list(args)
        self.__with_client_check(name, args)
        try:
            data = obj(*args, **kwargs)
            assert self.__active, 'SERVER IS NOT ACTIVE'
            self.__qri.reply(ID, (True, data))
        except Exception, error:
            self.__qri.reply(ID, (False, error))

    def __with_client_check(self, name, args):
        self.__wc_lock.acquire()
        with_client = self.__with_client[:]
        self.__wc_lock.release()
        for func in with_client:
            if name.startswith(func):
                if len(name) == len(func) or name[len(func)] == '.':
                    args.insert(0, self)
