import boards
import util
import time
import ttyWindows

################################################################################

class Player:

    def __init__(self, screen, row=0, column=9, face='^'):
        self.screen = screen
        self.row = row
        self.column = column
        self.face = face[0]
        self.direction = 0, 0

    def setDirection(self, key):
        if key == '\xE0H':
            self.direction = 0, -1
        elif key == '\xE0P':
            self.direction = 0, +1
        elif key == '\xE0K':
            self.direction = -1, 0
        elif key == '\xE0M':
            self.direction = +1, 0

    def move(self):
        character = self.screen.read(self.row, self.column)
        x, y = self.direction
        if character == '_' or character == '*':
            self.column += x
        elif character == '|':
            self.row += y
        elif character == ' ':
            if self.screen.read(self.row + 1, self.column) != '|' or y == 1:
                self.row += 1
            else:
                self.column += x
        self.screen.write(self.row, self.column, self.face)

################################################################################

def main():
    screen = util.Screen(boards.boards[0])
    screen.update()
    player = Player(screen)
    while screen.read(player.row, player.column):
        time.sleep(.1)
        key = ttyWindows.readLookAhead()
        player.setDirection(key)
        player.move()
        screen.update()
    time.sleep(2)

if __name__ == '__main__':
    main()
