class Board:
    
    TABLE = ''.join([chr(i) for i in range(256)])
    NAME = ''.join([chr(i) for i in range(256) if len(repr(chr(i))) == 3 or i == ord('\\')])
    BOARD = '\n *_|'

    def __init__(self, name, board):
        self.__name = name
        self.__board = board
        self.__check()

    def name(self):
        return self.__name

    def board(self):
        return self.__board

    def __check(self):
        name_error = self.__name.translate(self.TABLE, self.NAME)
        board_error = self.__board.translate(self.TABLE, self.BOARD)
        assert self.__name and not name_error
        assert self.__board and not board_error
        self.__logic()

    def __logic(self):
        board = self.__board.splitlines()
        assert not board[0]
        columns = len(board[1])
        assert columns
        for row in board[2:]:
            assert len(row) == columns

################################################################################

first_try = Board('First Try', '''
                                                     
                                                     
                                                     
                                __*___|_             
                          |           |              
                          |           |              
                         _|__*________|______*___    
                          |           |              
                  ___*____|___________|_             
                          |           |              
                          |           |              
                          |           |              
    ____*_________________|___________|______*____   ''')

################################################################################

second_try = Board('Second Try', '''
                                                     
                                                     
                                                     
                                __*___|_             
    _|________*_____|_*___|___        |              
     |     |        |     |           |              
    _|_*_  |   __*__|_   _|__*________|______*_|_    
           |              |           |        |     
           |      ___*____|________|__|_   _*__|_    
           |              |        |  |              
           |     _|__*_   |   __*__|_ |              
           |      |       |           |              
    ____*__|______|_______|___________|______*____   ''')

################################################################################

boards = first_try, second_try
