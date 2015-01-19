import sys
from winreg import *

################################################################################

THRESHOLD = 2048

################################################################################

def main():
    global report
    report = file('large_values.txt', 'w', 0)
    name = dict(map(reversed, HKEY.__dict__.items()))
    for hive in Registry():
        search(hive, name[int(repr(hive)[4:-1])])
    

def search(key, name):
    for v in key.values:
        try:
            value = key.values[v]
            l = len(value.value)
            if l > THRESHOLD:
                report.write('\n%s\n%s == len(%s %s)\n' % (name, l, value.__class__.__name__, repr(v) if v else '(Default)'))
        except:
            pass
    for k in key.keys:
        try:
            search(key.keys[k], '%s\\%s' % (name, k))
        except:
            pass

################################################################################

if __name__ == '__main__':
    main()
