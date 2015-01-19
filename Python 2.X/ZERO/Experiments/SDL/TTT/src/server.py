import socket
import thread

import time

import spots
import ttt_logic

################################################################################

class Syncronize:

    def __init__(self, obj):
        self.__obj = obj
        self.__lock = thread.allocate_lock()

    def __getattr__(self, name):
        return Wrapper(getattr(self.__obj, name), self.__lock)

class Wrapper:

    def __init__(self, method, lock):
        self.__method = method
        self.__lock = lock

    def __call__(self, *args, **kwargs):
        self.__lock.acquire()
        try:
            data = self.__method(*args, **kwargs)
        finally:
            self.__lock.release()
        return data

################################################################################

RUN_SERVER = True
LOCAL_MODE = False

def main(port=2536):
    server = socket.socket()
    server.bind(('', port))
    server.listen(5)
    while RUN_SERVER:
        thread.start_new_thread(game, (server.accept(), server.accept()))
    server.close()

def game(pri, sec):
    if RUN_SERVER:
        if LOCAL_MODE:
            assert pri[1][0] == '127.0.0.1' or \
                   sec[1][0] == '127.0.0.1', 'PRIVATE SERVER'
        # connect and get avatars
        c1 = spots.qri(pri[0])
        c2 = spots.qri(sec[0])
        a1 = c1.call(' ')
        a2 = c2.call(a1)
        c1.call(None)
        assert {'o': 'x', 'x': 'o'}[a1] == a2, 'INVALID REPLY'
        # setup game and create response engine
        ttt = ttt_logic.TL(a1)
        safe_ttt = Syncronize(ttt)
        pause = thread.allocate_lock()
        pause.acquire()
        thread.start_new_thread(processor, (c1, a1, c2, safe_ttt, pause))
        thread.start_new_thread(processor, (c2, a2, c1, safe_ttt, pause))
        # run socket cleanup
        pause.acquire()
        pause.release()
        pri[0].shutdown(socket.SHUT_RDWR)
        sec[0].shutdown(socket.SHUT_RDWR)
        pri[0].close()
        sec[0].close()

################################################################################

def processor(client, avatar, next, logic, run):
    # loop while running and get query
    while run.locked():
        try:
            ID, pos = get_query(client, run)
            time.sleep(.1)
        except SystemExit:
            raise
        except:
            continue
        # move and respond to errors
        try:
            data = getattr(logic, avatar)(*pos)
        except Exception, error:
            client.reply(ID, (False, error))
        else:
            # return status and notify next
            client.reply(ID, (True, data))
            call(next, pos)
            if data in list('ox'):
                call(next, (-1, -1))
                run.release()

def get_query(client, run):
    # loop while game is running
    while run.locked():
        try:
            return client.query(1)
        except Warning:
            pass
        except:
            thread.exit()
        
def call(next, pos):
    try:
        next.call(pos, .1)
    except Warning:
        pass
    except:
        thread.exit()
