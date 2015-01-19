import msvcrt

def readLookAhead():
    string = str()
    while msvcrt.kbhit():
        string += msvcrt.getch()
    return string
