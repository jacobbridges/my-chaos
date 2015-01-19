import matrix

# START BUG FIX
# =============
# "assert" is faulty on compile.

def assert_(condition, reason):
    if not condition:
        raise Exception(reason)

# END BUG FIX
# ===========

class TL:

    def __init__(self, start):
        assert_(start in list('ox'), 'start must be in "ox"')
        self.__go = start
        self.__play = True
        self.__grid = matrix.Matrix(3, 3, ' ')

    def __repr__(self):
        return repr(self.__grid)

    def __str__(self):
        ttt = matrix.Matrix(5, 5)
        for y in range(3):
            for x in range(2):
                ttt[y * 2][x * 2 + 1] = '|'
        for y in range(2):
            for x, s in enumerate('-+-+-'):
                ttt[y * 2 + 1][x] = s
        for y, r in enumerate(self.__grid):
            for x, s in enumerate(r):
                ttt[y * 2][x * 2] = s.upper()
        return '\n'.join(''.join(row) for row in ttt)

    def o(self, x, y):
        assert_(self.__play, 'GAME OVER')
        assert_(self.__go == 'o', 'call "x" first')
        assert_(self.__grid[y][x] == ' ', '(%s, %s) is taken' % (x, y))
        self.__grid[y][x] = 'o'
        self.__go = 'x'
        return self.win()

    def x(self, x, y):
        assert_(self.__play, 'GAME OVER')
        assert_(self.__go == 'x', 'call "o" first')
        assert_(self.__grid[y][x] == ' ', '(%s, %s) is taken' % (x, y))
        self.__grid[y][x] = 'x'
        self.__go = 'o'
        return self.win()

    def win(self):
        self.__play = False
        # check rows
        for y in range(3):
            test = self.__grid[y][1]
            if test in list('ox') and self.__grid[y][0] == test == self.__grid[y][2]:
                return test
        # check columns
        for x in range(3):
            test = self.__grid[1][x]
            if test in list('ox') and self.__grid[0][x] == test == self.__grid[2][x]:
                return test
        # check diagonals
        test = self.__grid[1][1]
        if test in list('ox'):
            if self.__grid[0][0] == test == self.__grid[2][2]:
                return test
            if self.__grid[2][0] == test == self.__grid[0][2]:
                return test
        # still playing
        self.__play = True
        return ' '
