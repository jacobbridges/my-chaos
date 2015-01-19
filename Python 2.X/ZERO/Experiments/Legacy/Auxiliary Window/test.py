from window import aux_win
from time import time, sleep

test = aux_win()
sec = time()
while time() - sec < 30:
    string = raw_input('Enter: ')
    if string == 'clear':
        test.clear()
    elif string == 'end':
        test.close()
        break
    else:
        test.write(string + '\n')
sleep(sec - time() + 30)
