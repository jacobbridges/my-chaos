import os
import sys
import thread
import traceback

MAX_RECORDS = 5

new_thread = []
cur_thread = []
del_thread = []
count = 0

var_lock = thread.allocate_lock()
out_lock = thread.allocate_lock()

def iThread(function, args, *kwargs):
    if len(kwargs) == 0:
        _thread(debugger, (function, args))
    elif len(kwargs) == 1:
        _thread(debugger, (function, args), kwargs[0])
    else:
        raise TypeError

def debugger(function, args, **kwargs):
    record = build_record(function, args, kwargs)
    add_new_thread(record)
    try:
        function(*args, **kwargs)
    except SystemExit:
        pass
    except:
        out_lock.acquire()
        raw_input(traceback.format_exc())
        out_lock.release()
    add_del_thread(record)

def build_record(function, args, kwargs):
    global count
    mod = function.__module__ if hasattr(function, '__module__') else '<MOD>'
    name = function.__name__ if hasattr(function, '__name__') else '<FUNC>'
    args = map(repr, args)
    kwargs = ['%s=%r' % (key, kwargs[key]) for key in kwargs.keys()]
    signature = '%s/%s(%s)' % (mod, name, ', '.join(args + kwargs))
    var_lock.acquire()
    count += 1
    ID = count
    var_lock.release()
    record = ID, signature
    return record

def add_new_thread(record):
    var_lock.acquire()
    new_thread.insert(0, record)
    if len(new_thread) > MAX_RECORDS:
        new_thread.pop()
    cur_thread.append(record)
    update_screen()

def add_del_thread(record):
    var_lock.acquire()
    del_thread.insert(0, record)
    if len(del_thread) > MAX_RECORDS:
        del_thread.pop()
    cur_thread.remove(record)
    update_screen()

def update_screen():
    new_record = new_thread[:]
    cur_record = cur_thread[:]
    del_record = del_thread[:]
    var_lock.release()
    cache = '\n'
    if new_record:
        cache += 'NEW THREADS\n===========\n'
        for record in new_record:
            cache += '%s: %s\n' % record
        cache += '\n'
    if cur_record:
        cache += 'CUR THREADS\n===========\n'
        for record in cur_record:
            cache += '%s: %s\n' % record
        cache += '\n'
    if del_record:
        cache += 'DEL THREADS\n===========\n'
        for record in del_record:
            cache += '%s: %s\n' % record
        cache += '\n'
    out_lock.acquire()
    os.system('cls')
    sys.stdout.write(cache)
    out_lock.release()

_thread = thread.start_new_thread
thread.start_new_thread = iThread
