import boards
import util
import time
import ttyWindows

################################################################################

class Player:

    def __init__(self, screen, face, row=1, column=10):
        self.screen = screen
        self.face = face
        self.row = row
        self.column = column
        self.vector = 0, 0

    def move(self):
        global playing, you
        context = self.screen.read(self.row, self.column)
        left = self.screen.read(self.row, self.column - 1)
        right = self.screen.read(self.row, self.column + 1)
        x, y = self.vector
        x_move = False
        if context == '_':
            self.column += x
            x_move = True
        elif context == '|':
            self.row += y
        elif context == ' ':
            if self.screen.read(self.row + 1, self.column) != '|' or y == 1:
                self.row += 1
            else:
                self.column += x
        if not x_move and context != ' ':
            if left == '_' and x == -1:
                self.column -= 1
            elif right == '_' and x == 1:
                self.column += 1
        self.screen.write(self.row, self.column, self.face)
        if self is you and self.screen.read(self.row, self.column) is None:
            playing = False

################################################################################

class You(Player):

    def __init__(self, screen, face, row=1, column=10):
        Player.__init__(self, screen, face, row, column)
        self.score = 0

    def setDirection(self, key):
        context = self.screen.read(self.row, self.column)
        if context == '*':
            self.score += 10
            self.screen.cache_write(self.row, self.column, '_')
        if key == '\xE0H':
            self.vector = 0, -1
        elif key == '\xE0P':
            self.vector = 0, +1
        elif key == '\xE0K':
            self.vector = -1, 0
        elif key == '\xE0M':
            self.vector = +1, 0
        elif key == 'a':
            self.screen.cache_write(self.row, self.column - 1, ' ')
        elif key == 'd':
            self.screen.cache_write(self.row, self.column + 1, ' ')

class Robot(Player):

    def setDirection(self, key):
        global playing, you
        if you.row == self.row and you.column == self.column:
            playing = False
        if self.row == you.row:
            if self.column > you.column:
                self.vector = -1, 0
            else:
                self.vector = +1, 0
        else:
            context = self.screen.read(self.row, self.column)
            if context == '|':
                if self.row > you.row:
                    self.vector = 0, -1
                elif self.row < you.row:
                    self.vector = 0, +1

################################################################################

def main():
    global playing, you
    screen = util.Screen2(boards.boards[0])
    you = You(screen, '^')
    screen.update()
    players = [you]
    clock = 0
    playing = True
    time.sleep(2)
    while playing:
        clock += 1
        if clock == 90:
            players.append(Robot(screen, '&'))
        time.sleep(.1)
        key = ttyWindows.readLookAhead()
        for player in players:
            player.setDirection(key)
            player.move()
        screen.update()
        print 'Score: %s' % you.score
    screen.update()
    print 'Score: %s' % you.score
    time.sleep(2)

if __name__ == '__main__':
    main()
