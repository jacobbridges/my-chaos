import copy
from Zam import *

# NOTE 1:
# class struct needs to be "baked" into class page.
# visibile, x, & y will be properties of a page objects
# and will not be used by page objects, only windows
# will use these three attributes; otherwise, they can
# be ignored for other perposes.

# NOTE 2:
# When "struct" is baked into "page," there will need
# to be linking and unlinking functions added to "page"
# and "windows." Calls will be like so:
# page_obejct.link_to(page_object)
# page_obejct.un_link(<initialization information>)
# window_obejct.link_to(window_object)
# window_obejct.un_link(<initialization information>)
# Linking between pages will involve sharing self.__data
# (via a list containing self.__data). self.__data will
# become self.__data[0] and self.__data will be a list
# with one item. Linking between windows will be similar
# and will most likely share self.__data & self.__list
# (to become self.__page & self.__data currently).

# NOTE 3:
# Since self.__data (in page) is a matrix that is
# never re-created, when linking pages, self.__data
# is all that needs to be shared via the following:
# page_object.__data = self.__data

class struct: # VERSION 1.0 # Lose class struct; bake into class page.

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
        return self # ADDITION

    def set_x(self, x):
        self.__assert_type((int, x))
        self.__x = x
        return self # ADDITION

    def set_y(self, y):
        self.__assert_type((int, y))
        self.__y = y
        return self # ADDITION

    def set_value(self, value):
        self.__value = value
        return self # ADDITION
    
    def __assert_type(self, *tuples):
        for types, objects in tuples:
            if type(objects) is not types:
                raise TypeError

class page: # VERSION 1.1

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
        return self # ADDITION

    def set_row(self, row, value=''): # ADDITION
        self.__assert_type((int, row), (str, value))
        if value:
            self.__data[row] = value[0]
        else:
            self.__data[row] = ' '
        return self

    def set_column(self, column, value): # ADDITION
        self.__assert_type((int, column), (str, value))
        for row in self.__data:
            if value:
                row[column] = value[0]
            else:
                row[column] = ' '
        return self

    def data(self):
        return copy.deepcopy(self.__data)

    def __str__(self):
        return '\n'.join([''.join(row) for row in self.__data])

    def __repr__(self): # ADDITION
        return repr(self.__data)

    def __assert_type(self, *tuples):
        for types, objects in tuples:
            if type(objects) is not types:
                raise TypeError

# NOTE:
# __update should always be called, and its main body of code
# should always be executed in case objects were modified
# without the knowledge of the window object. Furthermore,
# self.__list accessors and mutators need to be looked at
# in closer detail to see that they function correctly.
# def option() & def size() may need to looked at in greater
# detail, and these classes may need better error checking
# systems built into them (array & matrix lack error checking.
# BTW, the returning of self in setitem and delitem appears to
# be incorrect and has been removed.

class window: # VERSION 1.5

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
        self.__draw = True   # Lose self.__draw
        self.__data = None   # Rename to self.__page
        self.__list = list() # Rename to self.__data

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

    def __repr__(self): # ADDITION
        self.__update()
        return repr(self.__data)
            
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
        # if self.__draw:
        # SUBSTITUTE
        if True:
            self.__draw = False
            self.__data = page(self.__height, self.__width, self.__background)
            for item in self.__list:
                if item.get_visible():
                    x = item.get_x()
                    y = item.get_y()
                    data = item.get_value().data()
                    # rows = len(data) / len(data[0])
                    # MODIFICATION
                    rows = len(data)
                    columns = len(data[0])
                    for row in range(rows):
                        for column in range(columns):
                            self.__data.mutate(row + x, column + y, data[row][column])
            if self.__border:
                # self.__data.mutate(0, 0, self.__border * self.__width)
                # self.__data.mutate(self.__height - 1, 0, self.__border * self.__width)
                # for row in range(1, self.__height - 1):
                #     self.__data.mutate(row, 0, self.__border)
                #     self.__data.mutate(row, self.__width - 1, self.__border)
                # SUBSTITUE
                self.__data.set_row(0, self.__border).set_row(self.__height - 1, self.__border) \
                                       .set_column(0, self.__border).set_column(self.__width - 1, self.__border)

    def __assert_type(self, *tuples):
        for types, objects in tuples:
            if type(objects) is not types:
                raise TypeError

# TEST CODE
it = window(10, 10)
print it
it.option('#')
print it
it.option(background='-')
print it
it += struct(True, 2, 2, page(1, 1, '%'))
print it
other = struct(True, 3, 3, page(2, 2, 'H'))
it += other
print it
it -= other
print it
del it[0]
print it
other = struct(True, 2, 2, page(2, 2, '%'))
it += other
other_2 = struct(True, 5, 2, other.get_value())
it += other_2
print it
other_2.get_value().mutate(0, 0, 'H')
# The next line should not be needed now.
# it.size(11, 11)
print it
it.option('', '')
print it
