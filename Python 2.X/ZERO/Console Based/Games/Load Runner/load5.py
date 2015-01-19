import boards
import random
import time
import ttyWindows
import util

################################################################################

class Player:

    def __init__(self, screen, face, row=1, column=10):
        self.screen = screen
        self.face = face
        self.row = row
        self.column = column
        self.vector = 0, 0

    def move(self):
        global playing, you, players
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
        if self.screen.read(self.row, self.column) is None:
            if self is you:
                playing = False
            else:
                players.remove(self)

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

    def __init__(self, screen, face, row=1, column=10):
        Player.__init__(self, screen, face, row, column)
        self.move_count = 0

    def move(self):
        if self.screen.read(self.row, self.column) == ' ':
            Player.move(self)
        else:
            self.move_count += 1
            if self.move_count % 2:
                Player.move(self)
            else:
                self.screen.write(self.row, self.column, self.face)

    def setDirection(self, key):
        global playing, you
        if you.row == self.row and you.column == self.column:
            playing = False
        if self.column > you.column:
            self.vector = -1, 0
        elif self.column < you.column:
            self.vector = +1, 0
        if self.row != you.row:
            context = self.screen.read(self.row, self.column)
            if context == '|':
                if self.row > you.row:
                    self.vector = 0, -1
                elif self.row < you.row:
                    self.vector = 0, +1

################################################################################

SELECT = 1

def main():
    global playing, you, players
    screen = util.Screen2(boards.boards[SELECT])
    you = You(screen, '^')
    screen.update()
    players = [you]
    clock = 0
    playing = True
    time.sleep(2)
    while playing:
        clock += 1
        if clock > 40 and len(players) < 3:
            players.append(Robot(screen, '&', column=random.randrange(len(boards.boards[SELECT].board().splitlines()[1]))))
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
