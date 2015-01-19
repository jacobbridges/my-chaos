##import Zam
##
##class ClassError(StandardError): # VERSION 1.0
##    pass
##
##class page(object): # VERSION 1.4
##
##    #def __init__(self, width, height, value=None):
##        self.__assert_type((int, width), (int, height))
##        if value is None:
##            value = ''
##        else:
##            self.__assert_type((str, value))
##        if value:
##            self.__matrix = Zam.matrix(height, width, value[0])
##        else:
##            self.__matrix = Zam.matrix(height, width, ' ')
##        self.__visible = True
##        self.__x = 0
##        self.__y = 0
##
##    #def __repr__(self):
##        return repr(self.__matrix)
##
##    #def __str__(self):
##        return '\n'.join([''.join(row) for row in self.__matrix])
##
##    def width(self):
##        return len(self.__matrix[0])
##
##    def height(self):
##        return len(self.__matrix)
##
##    #def access(self, row, column, length=None):
##        self.__assert_type((int, row), (int, column))
##        if length is None:
##            lenght = 1
##        else:
##            self.__assert_type((int, lenght))
##        string = str()
##        for index in range(length):
##            try:
##                string += self.__matrix[row][column + index]
##            except:
##                pass
##        return string
##
##    #def mutate(self, row, column, value):
##        self.__assert_type((int, row), (int, column), (str, value))
##        for index in range(len(value)):
##            try:
##                self.__matrix[row][column + index] = value[index]
##            except:
##                pass
##        return self
##
##    def set_row(self, row, value=None):
##        self.__assert_type((int, row))
##        if value is None:
##            value = ''
##        else:
##            self.__assert_type((str, value))
##        if value:
##            self.__matrix[row] = value[0]
##        else:
##            self.__matrix = ' '
##        return self
##
##    def set_column(self, column, value=None):
##        self.__assert_type((int, column))
##        if value is None:
##            value = ''
##        else:
##            self.__assert_type((str, value))
##        for row in self.__matrix:
##            if value:
##                row[column] = value[0]
##            else:
##                row[column] = ' '
##        return self
##
##    #def visible(self, value=None):
##        if value is None:
##            return self.__visible
##        else:
##            self.__assert_type((bool, value))
##            self.__visible = value
##            return self
##
##    #def x(self, value=None):
##        if value is None:
##            return self.__x
##        else:
##            self.__assert_type((int, value))
##            self.__x = value
##            return self
##        
##    #def y(self, value=None):
##        if value is None:
##            return self.__y
##        else:
##            self.__assert_type((int, value))
##            self.__y = value
##            return self
##
##    def project(self, value):
##        self.__assert_class((page, value))
##        for row in range(len(value.__matrix)):
##            for column in range(len(value.__matrix[0])):
##                try:
##                    self.__matrix \
##                                  [value.__y + row] \
##                                  [calue.__x + column] \
##                                  = value.__matrix[row][column]
##                except:
##                    pass
##        return self
##
##    def link(self, value):
##        self.__assert_class((page, value))
##        self.__matrix = value.__matrix
##        return self
##        
##
##    def unlink(self):
##        temp = Zam.matrix(len(self.__matrix), len(self.__matrix[0]))
##        for row in range(len(self.__matrix)):
##            for column in range(len(self.__matrix[0])):
##                temp[row][column] = self.__matrix[row][column]
##        self.__matrix = temp
##        return self
##
##    def copy(self, value):
##        self.__assert_class((page, value))
##        self.__matrix = Zam.matrix(len(value.__matrix), len(value.__matrix[0]))
##        for row in range(len(value.__matrix)):
##            for column in range(len(value.matrix[0])):
##                self.__matrix[row][column] = value.__matrix[row][column]
##        return self
##
##    def __assert_class(self, *tuples):
##        for classes, objects in tuples:
##            if objects.__class__ is not classes:
##                raise ClassError(str(objects.__class__) + ' is not ' + str(classes))
##
##    def __assert_type(self, *tuples):
##        for types, objects in tuples:
##            if type(objects) is not types:
##                raise TypeError(str(type(objects)) + ' is not ' + str(types))
