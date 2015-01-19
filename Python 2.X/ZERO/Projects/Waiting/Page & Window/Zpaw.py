import Zam

class ClassError(StandardError): # VERSION 1.0
    pass

class page(object): # VERSION 1.5
    
    def __init__(self, height, width, value=None):
        self.__assert_type((int, height), (int, width))
        if value is None:
            value = ''
        else:
            self.__assert_type((str, value))
        if default:
            self.__matrix = Zam.matrix(height, width, value[0])
        else:
            self.__matrix = Zam.matrix(height, width, ' ')
        self.__visible = True
        self.__x = 0
        self.__y = 0

    def __repr__(self):
        return repr(self.__matrix)

    def __str__(self):
        return '\n'.join([''.join(row) for row in self.__matrix])

    def mutate(self, column, row, value):
        self.__assert_type((int, column), (int, row), (str, value))
        for index in range(len(value)):
            try:
                self.__matrix[row][column + index] = value[index]
            except:
                pass
        return self

    def access(self, column, row, value=None):
        self.__assert_type((int, column), (int, row))
        if value is None:
            value = 1
        else:
            self.__assert_type((int, value))
        string = str()
        for index in range(value):
            try:
                string += self.__matrix[row][column + index]
            except:
                pass
        return string

    def visible(self, value=None):
        if value is None:
            return self.__visible
        else:
            self.__assert_type((bool, flag))
            self.__visible = value
            return self

    def x(self, value=None):
        if value is None:
            return self.__x
        else:
            self.__assert_type((int, column))
            self.__x = value
            return self

    def y(self, value=None):
        if value is None:
            return self.__y
        else:
            self.__assert_type((int, row))
            self.__y = value
            return self

    def set_column(self, column, value=None):
        self.__assert_type((int, column))
        if value is None:
            value=''
        else:
            self.__assert_type((str, value))
        for row in self.__matrix:
            if value:
                row[column] = value[0]
            else:
                row[column] = ' '
        return self
