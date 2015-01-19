from winreg import *

def main():
    strings = []
    try:
        while True:
            strings.append(raw_input('Search? '))
    except EOFError:
        print
        search(strings)
    raw_input('====\nDONE\n====')

def search(strings):
    strings = map(str.lower, strings)
    name = dict(map(reversed, HKEY.__dict__.items()))
    for hive in Registry():
        sub_search(hive, strings, name[int(repr(hive)[4:-1])])

def sub_search(key, strings, sn):
    for name in key.values:
        for string in strings:
            if string in name.lower():
                print sn
                print name, '=', key.values[name]
                print
    for sub_key in key.keys:
        try:
            sub_search(key.keys[sub_key], strings, '%s\\%s' % (sn, sub_key))
        except:
            pass

if __name__ == '__main__':
    main()
