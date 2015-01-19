import boards
import util
import time

def main():
    screen = util.Screen(boards.boards[0])
    screen.update()
    time.sleep(2)
    row, col = 1, 9
    while True:
        character = screen.read(row, col)
        if character == '_' or character == '*':
            col += 1
        elif character == '|':
            row -= 1
        elif character == ' ':
            if screen.read(row + 1, col) == '|':
                col += 1
            else:
                row += 1
        else:
            break
        screen.write(row, col, '^')
        screen.update()
        time.sleep(.1)
    screen.update()
    time.sleep(2)

if __name__ == '__main__':
    main()
