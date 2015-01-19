from winreg import *

def main():
    subkey = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall'
    uninstall = Key(HKEY.LOCAL_MACHINE, subkey)
    names = search(uninstall, 'DisplayName', [])
    for name in sorted(names):
        print name

def search(key, value, cache):
    if value in key.values:
        cache.append(key.values[value].value)
    for name in key.keys:
        search(key.keys[name], value, cache)
    return cache

if __name__ == '__main__':
    main()
