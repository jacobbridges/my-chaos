import os

################################################################################

class Screen:

    def __init__(self, board):
        self.__cache = [tuple(row) for row in board.board().splitlines()[1:]]
        self.__board()

    def write(self, row, column, character):
        try:
            self.__temp[row][column] = character[0]
        except:
            pass

    def read(self, row, column):
        try:
            return self.__temp[row][column]
        except:
            pass

    def update(self):
        self.__clear()
        self.__print()
        self.__board()

    def __clear(self):
        if os.name == 'nt':
            os.system('cls')
        elif os.name == 'posix' or os.name == 'mac':
            os.system('clear')
        else:
            raise OSError, 'not supported'

    def __print(self):
        print '\n'.join([''.join(row) for row in self.__temp])

    def __board(self):
        self.__temp = [list(row) for row in self.__cache]

################################################################################

class Screen2:

    def __init__(self, board):
        self.__cache = [list(row) for row in board.board().splitlines()[1:]]
        self.__board()

    def cache_write(self, row, column, character):
        try:
            self.__cache[row][column] = character[0]
            self.write(row, column, character)
        except:
            pass

    def write(self, row, column, character):
        try:
            self.__temp[row][column] = character[0]
        except:
            pass

    def read(self, row, column):
        try:
            return self.__temp[row][column]
        except:
            pass

    def update(self):
        self.__clear()
        self.__print()
        self.__board()

    def __clear(self):
        if os.name == 'nt':
            os.system('cls')
        elif os.name == 'posix' or os.name == 'mac':
            os.system('clear')
        else:
            raise OSError, 'not supported'

    def __print(self):
        print '\n'.join([''.join(row) for row in self.__temp])

    def __board(self):
        self.__temp = [list(row) for row in self.__cache]

