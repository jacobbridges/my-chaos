import copy
from Zam import *

class struct:

    def __init__(self, visible, x, y, value):
        self.__assert_type((bool, visible), (int, x), (int, y))
        self.__visible = visible
        self.__x = x
        self.__y = y
        self.__value = value

    def get_visible(self):
        return self.__visible

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_value(self):
        return self.__value

    def set_visible(self, visible):
        self.__assert_type((bool, visible))
        self.__visible = visible

    def set_x(self, x):
        self.__assert_type((int, x))
        self.__x = x

    def set_y(self, y):
        self.__assert_type((int, y))
        self.__y = y

    def set_value(self, value):
        self.__value = value
    
    def __assert_type(self, *tuples):
        for types, objects in tuples:
            if type(objects) is not types:
                raise TypeError

class page:

    def __init__(self, rows, columns, value=''):
        self.__assert_type((int, rows), (int, columns), (str, value))
        if value:
            self.__data = matrix(rows, columns, value[0])
        else:
            self.__data = matrix(rows, columns, ' ')

    def access(self, row, column, length=1):
        self.__assert_type((int, row), (int, column), (int, length))
        string = str()
        for index in range(length):
            try:
                string += self.__data[row][column + index]
            except:
                pass
        return string

    def mutate(self, row, column, value):
        self.__assert_type((int, row), (int, column), (str, value))
        for index in range(len(value)):
            try:
                self.__data[row][column + index] = value[index]
            except:
                pass

    def data(self):
        return copy.deepcopy(self.__data)

    def __str__(self):
        return '\n'.join([''.join(row) for row in self.__data])

    def __assert_type(self, *tuples):
        for types, objects in tuples:
            if type(objects) is not types:
                raise TypeError

class window:

    def __init__(self, height, width, border='  ', background='  '):
        self.__assert_type((int, height), (int, width), (str, border), (str, background))
        self.__height = height
        self.__width = width
        if len(border) < 2:
            self.__border = border
        else:
            self.__border = ''
        if len(background) < 2:
            self.__background = background
        else:
            self.__background = ''
        self.__draw = True
        self.__data = None
        self.__list = list()

    def size(self, height=0, width=0):
        self.__assert_type((int, height), (int, width))
        if height != 0:
            self.__draw = True
            self.__height = height
        if width != 0:
            self.__draw = True
            self.__width = width
        return self.__height, self.__width

    def option(self, border='  ', background='  '):
        self.__assert_type((str, border), (str, background))
        if len(border) < 2:
            self.__draw = True
            self.__border = border
        if len(background) < 2:
            self.__draw = True
            self.__background = background
        return self.__border, self.__background

    def data(self):
        self.__update()
        return self.__data.data()

    def __str__(self):
        self.__update()
        return str(self.__data)
            
    def __len__(self):
        return len(self.__list)
    
    def __getitem__(self, key):
        self.__assert_type((int, key))
        self.__draw = True
        return self.__list[key]
    
    def __setitem__(self, key, value):
        self.__assert_type((int, key))
        self.__draw = True
        self.__list[key] = value
        
    def __delitem__(self, key):
        self.__assert_type((int, key))
        self.__draw = True
        del self.__list[key]
        
    def __iter__(self):
        self.__draw = True
        return iter(self.__list)
    
    def __contains__(self, value):
        return value in self.__list

    def __iadd__(self, value):
        self.__draw = True
        self.__list.append(value)
        return self

    def __isub__(self, value):
        self.__draw = True
        while value in self.__list:
            self.__list.remove(value)
        return self
    
    def __update(self):
        if self.__draw:
            self.__draw = False
            self.__data = page(self.__height, self.__width, self.__background)
            for item in self.__list:
                if item.get_visible():
                    x = item.get_x()
                    y = item.get_y()
                    data = item.get_value().data()
                    rows = len(data) / len(data[0])
                    columns = len(data[0])
                    for row in range(rows):
                        for column in range(columns):
                            self.__data.mutate(row + x, column + y, data[row][column])
            if self.__border:
                self.__data.mutate(0, 0, self.__border * self.__width)
                self.__data.mutate(self.__height - 1, 0, self.__border * self.__width)
                for row in range(1, self.__height - 1):
                    self.__data.mutate(row, 0, self.__border)
                    self.__data.mutate(row, self.__width - 1, self.__border)

    def __assert_type(self, *tuples):
        for types, objects in tuples:
            if type(objects) is not types:
                raise TypeError
