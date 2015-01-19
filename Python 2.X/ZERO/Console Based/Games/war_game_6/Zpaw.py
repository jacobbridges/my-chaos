import Zam

class ClassError(StandardError): # VERSION 1.0
    pass # This class is just for exceptions.

class page(object): # VERSION 1.3

    def __init__(self, width, height, value=None):
        self.__assert_type((int, height), (int, width))
        if value is None:
            value = ''
        else:
            self.__assert_type((str, value))
        if value:
            self.__data = Zam.matrix(height, width, value[0])
        else:
            self.__data = Zam.matrix(height, width, ' ')
        self.__visible = True
        self.__x = 0
        self.__y = 0

    def __repr__(self):
        return repr(self.__data)

    def __str__(self):
        return '\n'.join([''.join(row) for row in self.__data])

    def width(self):
        return len(self.__data[0])

    def height(self):
        return len(self.__data)

    def access(self, row, column, length=None):
        self.__assert_type((int, row), (int, column))
        if length is None:
            length = 1
        else:
            self.__assert_type((int, length))
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
        return self

    def set_row(self, row, value=None):
        self.__assert_type((int, row))
        if value is None:
            value = ''
        else:
            self.__assert_type((str, value))
        if value:
            self.__data[row] = value[0]
        else:
            self.__data[row] = ' '
        return self

    def set_column(self, column, value=None):
        self.__assert_type((int, column))
        if value is None:
            value = ''
        else:
            self.__assert_type((str, value))
        for row in self.__data:
            if value:
                row[column] = value[0]
            else:
                row[column] = ' '
        return self

    def visible(self, value=None):
        if value is None:
            return self.__visible
        else:
            self.__assert_type((bool, value))
            self.__visible = value
            return self

    def x(self, value=None):
        if value is None:
            return self.__x
        else:
            self.__assert_type((int, value))
            self.__x = value
            return self

    def y(self, value=None):
        if value is None:
            return self.__y
        else:
            self.__assert_type((int, value))
            self.__y = value
            return self

    def page(self, ids=None): # ids=None is for recursion bug fix.
        return self

    def _page(self): # This functions is for recursion bug fix.
        return self

    def project(self, value): # Does not respect value.visible().
        self.__assert_class((page, value))
        for row in range(value.height()):
            for column in range(value.width()):
                try:
                    self.__data \
                                [row + value.y()] \
                                [column + value.x()] = \
                                value.__data[row][column]
                except:
                    pass
        return self

    def link(self, value): # Loses current matrix and uses value's.
        self.__assert_class((page, value))
        self.__data = value.__data
        return self

    def unlink(self): # Copies and unlinks current matrix.
        temp = Zam.matrix(self.height(), self.width())
        for row in range(self.height()):
            for column in range(self.width()):
                temp[row][column] = self.__data[row][column]
        self.__data = temp
        return self

    def __assert_class(self, *tuples):
        for classes, objects in tuples:
            if objects.__class__ is not classes:
                raise ClassError(str(objects.__class__) + ' is not ' + str(classes))

    def __assert_type(self, *tuples):
        for types, objects in tuples:
            if type(objects) is not types:
                raise TypeError

class window(object): # VERSION 1.7

    def __init__(self, width, height, border=None, background=None):
        self.__assert_type((int, width), (int, height))
        if border is None:
            border = ''
        else:
            self.__assert_type((str, border))
        if background is None:
            background = ''
        else:
            self.__assert_type((str, background))
        self.__width = width
        self.__height = height
        if border:
            self.__border = border[0]
        else:
            self.__border = None
        if background:
            self.__background = background[0]
        else:
            self.__background = ' '
        self.__list = list()
        # __page must exist for __refresh.
        self.__page = page(0, 0)
        self.__refresh()
            

    def __repr__(self):
        self.__refresh()
        return repr(self.__page)

    def __str__(self):
        self.__refresh()
        return str(self.__page)

    def width(self, value=None):
        if value is None:
            return self.__width
        else:
            self.__assert_type((int, value))
            self.__width = value
            return self

    def height(self, value=None):
        if value is None:
            return self.__height
        else:
            self.__assert_type((int, value))
            self.__height = value
            return self

    def border(self, value=None):
        if value is None:
            return self.__border
        else:
            self.__assert_type((str, value))
            if value:
                self.__border = value[0]
            else:
                self.__border = None
            return self

    def background(self, value=None):
        if value is None:
            return self.__background
        else:
            self.__assert_type((str, value))
            if value:
                self.__background = value[0]
            else:
                self.__background = ' '
            return self

    def __len__(self):
        return len(self.__list)

    def __getitem__(self, key):
        self.__assert_type((int, key))
        return self.__list[key]

    def __setitem__(self, key, value):
        self.__assert_type((int, key))
        self.__assert_class((page, window, value))
        self.__list[key] = value

    def __delitem__(self, key):
        self.__assert_type((int, key))
        del self.__list[key]

    def __iter__(self):
        return iter(self.__list)

    def __contains__(self, value):
        self.__assert_class((page, window, value))
        return value in self.__list

    def __iadd__(self, value):
        self.__assert_class((page, window, value))
        self.__list.append(value)
        return self # Must return self.

    def __isub__(self, value):
        self.__assert_class((page, window, value))
        while value in self.__list:
            self.__list.remove(value)
        return self # Must return self.

    def visible(self, value=None):
        if value is None:
            return self.__page.visible()
        else:
            # Check type here and return self.
            self.__assert_type((bool, value))
            self.__page.visible(value)
            return self

    def x(self, value=None):
        if value is None:
            return self.__page.x()
        else:
            # Check type here and return self.
            self.__assert_type((int, value))
            self.__page.x(value)
            return self

    def y(self, value=None):
        if value is None:
            return self.__page.y()
        else:
            # Check type here and return self.
            self.__assert_type((int, value))
            self.__page.y(value)
            return self

    def page(self, ids=None):
        # ids=None helps prevent too much recursion.
        if ids is not None:
            self.__assert_type((list, ids))
        self.__refresh(ids)
        return self.__page

    def _page(self): # Don't refresh __page.
        return self.__page

    def __refresh(self, ids=None):
        if ids is None:
            ids = list()
        # region: should not be executed if id(self) in ids.
        temp = page(self.__width, self.__height, self.__background) \
               .visible(self.__page.visible()).x(self.__page.x()).y(self.__page.y())
        self.__page = temp
        for item in self.__list:
            if item.visible():
                # This needs to be fixed.
                if id(item) in ids:
                    self.__page.project(item._page())
                else:
                    ids.append(id(item))
                    self.__page.project(item.page(ids))
        # endregion
        # The border still needs to finished.
        # Border needs be finished for caller and projection.
        if self.__border:
            self.__page \
                        .set_row(0, self.__border).set_row(self.__height - 1, self.__border) \
                        .set_column(0, self.__border).set_column(self.__width - 1, self.__border)

    def __assert_class(self, *tuples):
        # This function allows checking against several classes.
        # Note: self.__assert_class((class, ..., object), ...)
        for objects in tuples:
            for classes in objects[:-1]:
                if objects[-1].__class__ is classes:
                    break
            if objects[-1].__class__ is not classes:
                raise ClassError

    def __assert_type(self, *tuples):
        # Allows checking against only one type per object.
        # Note: self.__assert_type((type, object), ...)
        for types, objects in tuples:
            if type(objects) is not types:
                raise TypeError

# TEST CODE

def main():
    # PART 1
    print 'PART 1'
    it = window(10, 10)
    print it
    print it.border('#')
    print it.background('-')
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
    print it.border('').background('')
    # PART 2
    print 'PART 2'
    test = window(40, 20, '#', '.')
    print test
    copy = page(0, 0).link(test.page())
    test += page(5, 5).mutate(0, 0, '+---+').mutate(1, 0, '|   |')
    print test
    test += page(0, 0).link(test[0].x(3).y(2)).x(3).y(11)
    print test
    test[1].mutate(2, 0, '| A |').mutate(3, 0, test[0].access(1, 0, 5))
    print test
    test[0].mutate(4, 0, test[1].access(0, 0, 5))
    print test
    test[0].visible(False)
    print test
    test[0].mutate(2, 2, 'B')
    print test
    test[0].visible(True)
    test[1].visible(False)
    print test
    test.height(10).width(20)[1] =  page(3, 3, 'X').x(6).y(5)
    print test
    print copy
    # PART 3 - recursion depth fix
    print 'PART 3'
    try:
        test += test
        print test
        print test.x(5).y(5)
        # NOTE: border cannot be shown with recusion
    except RuntimeError, bug:
        print 'TEST FAILED:', bug

if __name__ == '__main__':
    main()
