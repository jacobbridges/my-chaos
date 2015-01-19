from winreg import *

def main():
    faults = []
    try:
        while True:
            faults.append(raw_input('Fault: '))
    except EOFError:
        engine(faults)
    raw_input('====\nDONE\n====')

def engine(faults):
    faults = map(str.lower, faults)
    name = dict(map(reversed, HKEY.__dict__.items()))
    for hive in Registry():
        SAD(faults, hive, name[int(repr(hive)[4:-1])], False)

def SAD(faults, key, name, prune):
    try:
        for value in key.values:
            for fault in faults:
                if prune or fault in value.lower():
                    del key.values[value]
                    print 'DEL VAL: %s\\%s' % (name, value)
                    break
                else:
                    try:
                        if fault in key.values[value].value:
                            del key.values[value]
                            print 'DEL VAL: %s\\%s' % (name, value)
                            break
                    except:
                        pass
        for subkey in key.keys:
            search = True
            newname = '%s\\%s' % (name, subkey)
            for fault in faults:
                if prune or fault in subkey.lower():
                    search = False
                    SAD(faults, key.keys[subkey], newname, True)
                    del key.keys[subkey]
                    print 'DEL KEY:', '%s\\%s' % (name, subkey)
                    break
            if search:
                SAD(faults, key.keys[subkey], newname, False)
    except:
        pass

if __name__ == '__main__':
    main()
