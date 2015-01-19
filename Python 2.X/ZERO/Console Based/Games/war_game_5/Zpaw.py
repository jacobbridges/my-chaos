import Zam

class page(object):

    def __init__(self, rows, columns, value=None):
        self.__assert_type((int, rows), (int, columns))
        if value:
            self.__assert_type((str, value))
            self.__data = Zam.matrix(rows, columns, value[0])
        else:
            self.__data = Zam.matrix(rows, columns, ' ')
        # These three are new variables (from class struct).
        self.__visible = True
        self.__x = 0
        self.__y = 0

    def __repr__(self):
        return repr(self.__data)

    def __str__(self):
        return '\n'.join([''.join(row) for row in self.__data])

    def size(self): # Return a tuple of matrix's size.
        return len(self.__data), len(self.__data[0])

    def access(self, row, column, length=None): # Get a string of length from row and column.
        self.__assert_type((int, row), (int, column))
        if length:
            self.__assert_type((int, length))
        else:
            length = 1
        string = str()
        for index in range(length):
            try:
                string += self.__data[row][column + index]
            except:
                pass
        return string
    
    def mutate(self, row, column, value): # Write a character or string where told.
        self.__assert_type((int, row), (int, column), (str, value))
        for index in range(len(value)):
            try:
                self.__data[row][column + index] = value[index]
            except:
                pass
        return self

    def set_row(self, row, value=None): # Set or clear a row to one character.
        self.__assert_type((int, row))
        if value:
            self.__assert_type((str, value))
            self.__data[row] = value[0]
        else:
            self.__data[row] = ' '
        return self

    def set_column(self, column, value=None): # Set or clear a column to one character.
        self.__assert_type((int, column))
        if value:
            self.__assert_type((str, value))
        else:
            value = ' '
        for row in self.__data:
            row[column] = value[0]
        return self

    def visible(self, value=None): # Get or set visible.
        if value is None:
            return self.__visible
        else:
            self.__assert_type((bool, value))
            self.__visible = value
            return self

    def x(self, value=None): # Get or set x.
        if value is None:
            return self.__x
        else:
            self.__assert_type((int, value))
            self.__x = value
            return self

    def y(self, value=None): # Get or set y.
        if value is None:
            return self.__y
        else:
            self.__assert_type((int, value))
            self.__y = value
            return self

    def project(self, value): # Copy value to self with offset.
        for row in range(value.size()[0]):
            for column in range(value.size()[1]):
                try:
                    self.__data \
                                [value.y() + row] \
                                [value.x() + column] = \
                                value.__data[row][column]
                except:
                    pass
        return self

    def page(self): # Casting statement.
        return self

    def link(self, value): # Use and share value's __data.
        if value.__class__ is page:
            self.__data = value.__data
            return self
        else:
            raise ValueError

    def unlink(self):
        temp = Zam.matrix(len(self.__data), len(self.__data[0])) # Create a new matrix.
        for row in range(len(self.__data)): # Copy all of the data to the new matrix.
            for column in range(len(self.__data[0])):
                temp[row][column] = self.__data[row][column]
        self.__data = temp # Finish the conversion.
        return self # Allow more work to be done.

    def __assert_type(self, *tuples):
        for types, objects in tuples:
            if type(objects) is not types:
                raise TypeError

class window(object):

    def __init__(self, height, width, border=None, background=None):
        self.__assert_type((int, height), (int, width))
        if border:
            self.__assert_type((str, border))
            self.__border = border[0]
        else:
            self.__border = ''
        if background:
            self.__assert_type((str, background))
            self.__background = background[0]
        else:
            self.__background = ' '
        self.__height = height
        self.__width = width
        self.__page = page(0, 0)
        self.__list = list()
        self.__refresh()

    def __repr__(self):
        self.__refresh()
        return repr(self.__page)

    def __str__(self):
        self.__refresh()
        return str(self.__page)

    def __len__(self):
        return len(self.__list)
    
    def __getitem__(self, key):
        self.__assert_type((int, key))
        return self.__list[key]
    
    def __setitem__(self, key, value):
        self.__assert_type((int, key))
        if value.__class__ is page or value.__class__ is window:
            self.__list[key] = value
        else:
            raise ValueError

    def __delitem__(self, key):
        self.__assert_type((int, key))
        del self.__list[key]

    def __iter__(self):
        return iter(self.__list)

    def __contains__(self, value): # value in self
        return value in self.__list

    def __iadd__(self, value): # self += page || window
        if value.__class__ is page or value.__class__ is window:
            self.__list.append(value)
            return self # this line is required
        else:
            raise ValueError

    def __isub__(self, value): # self -= page || window
        while value in self.__list:
            self.__list.remove(value)
        return self # this line may be required

    def size(self, height=None, width=None): # This needs to be divided into two functions.
        if height or width:
            if height:
                self.__assert_type((int, height))
                self.__height = height
            if width:
                self.__assert_type((int, width))
                self.__width = width
            return self
        return self.__height, self.__width

    def option(self, border=None, background=None): # This needs to be divided into two functions.
        if border is not None or background is not None:
            if border is not None:
                self.__assert_type((str, border))
                if border:
                    self.__border = border[0]
                else:
                    self.__border = border
            if background is not None:
                self.__assert_type((str, background))
                if background:
                    self.__background = background[0]
                else:
                    self.__background = background
            return self
        return self.__border, self.__background

    def visible(self, value=None): # Get or set visible.
        return self.__page.visible(value)

    def x(self, value=None): # Get or set x.
        return self.__page.x(value)

    def y(self, value=None): # Get or set y.
        return self.__page.y(value)

    def page(self): # This is like a casting statement.
        self.__refresh()
        return self.__page

    def __refresh(self):
        temp = page(self.__height, self.__width, self.__background) \
               .visible(self.__page.visible()).x(self.__page.x()).y(self.__page.y())
        self.__page = temp
        for item in self.__list: # Display Pages And Windows
            if item.visible():
                    self.__page.project(item.page())
        if self.__border: # Create Borders
            self.__page.set_row(0, self.__border).set_row(self.__height - 1, self.__border) \
                                   .set_column(0, self.__border).set_column(self.__width - 1, self.__border)

    def __assert_type(self, *tuples):
        for types, objects in tuples:
            if type(objects) is not types:
                raise TypeError

# TEST CODE
if __name__ == '__main__':
    it = window(10, 10)
    print it
    print it.option('#')
    print it.option(background='-')
    it += page(1, 1, '%').x(2).y(2)
    print it
    other = page(2, 2, 'H')
    it += other.x(3).y(3)
    print it
    it -= other
    print it
    del it[0]
    print it
    other = page(2, 2, '%')
    it += other.x(2).y(2)
    print it
    other_2 = page(0, 0)
    it += other_2.y(5).x(2).link(other)
    print it
    other_2.mutate(0, 0, 'H')
    print it
    print it.option('', '')
