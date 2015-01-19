# This is a slightly modified version of the first
# class and in mainly an outline for other classes.

class window_v1a: # VERSION 1.1
    
    def __init__(self, x, y):
        try:
            self.data = []
            temp = []
            for count in range(x):
                temp.append(' ')
            for count in range(y):
                self.data.append(temp[:])
        except:
            raise Exception
    
    def set(self, data, x, y):
        try:
            if type(data) is not str or len(data) != 1:
                raise Exception
            self.data[y][x] = data
        except:
            raise Exception
    
    def get(self, x, y):
        try:
            return self.data[y][x]
        except:
            raise Exception
    
    def __str__(self):
        try:
            string = ''
            for y in range(len(self.data)):
                temp = ''
                for x in range(len(self.data[0])):
                    temp += self.data[y][x]
                string += temp + '\n'
            return string
        except:
            raise Exception

###########################################################

# This is the second version of WINDOW. It has
# extensive value checking to prevent errors.

class window_v2a: # VERSION 1.2

    def __init__(self, columns, rows):
        if type(columns) is not int or columns < 1 or type(rows) is not int or rows < 1:
            raise 'ERROR'
        self.__columns = columns
        self.__rows = rows
        self.__window = list()
        self.__windows = list()
        for index in range(self.__rows):
            self.__window.append(list(' ' * self.__columns))

    def mutate(self, column, row, data):
        if type(column) is int and 0 <= column < self.__columns and type(row) is int and 0 <= row < self.__rows and type(data) is str and len(data) is not 0:
            if len(data) is 1:
                self.__window[row][column] = data
            else:
                try:
                    for index in range(len(data)):
                        self.__window[row][column + index] = data[index]
                except:
                    pass

    def access(self, column, row, size = 1):
        if type(column) is int and 0 <= column < self.__columns and type(row) is int and 0 <= row < self.__rows and type(size) is int and size > 0:
            if data is 1:
                return self.__window[row][column]
            else:
                temp = str()
                try:
                    for index in range(size):
                        temp += self.__window[row][column + index]
                except:
                    pass
                return temp

    def window(self):
        temp = list()
        for row in self.__window:
            temp.append(row[:])
        return temp

    def append(self, data):
        if data.__class__ is self.__class__:
            self.__windows.append(data)

    def remove(self, data):
        if data.__class__ is self.__class__:
            self.__windows.remove(data)

    def __getitem__(self, index):
        if type(index) is int and 0 <= index < len(self.__windows):
            return self.__windows[index]
    
    def __str__(self):
        temp = str()
        for row in self.__window:
            for string in row:
                temp += string
            temp += '\n'
        return temp

###########################################################

# This is the third version of WINDOW. It does not
# have value checking but relies on try/except clauses.

# Note 1: Some value checking does need to be implemented (example: mutate).
# Note 2: There should be versions of window and __str__ that take windows
#         into account; otherwise, they should take windows into account.
# Note 3: The structure of windows still needs to be defined;
#         IDEAS: [[window, [x, y], visible], ...],
#                windows[0] is top-most window,
#                [x, y] is window position,
#                visible remembers if window can be seen.

class window_v3a: # VERSION 1.3

    def __init__(self, rows, columns):
        try:
            # Setup variables.
            self.__rows = rows
            self.__columns = columns
            self.__window = list()
            self.__windows = list()
            # Setup window.
            for index in range(self._rows):
                self.__window.append(list(' ' * self.__columns))
        except:
            raise 'Window Error'

    def mutate(self, row, column, string):
        try:
            # Save string to window.
            for index in range(len(string)):
                self.__window[row][column + index] = string[index]
        except:
            pass

    def access(self, row, column, size = 1):
        temp = str()
        try:
            # Load temp from window.
            for index in range(size):
                temp += self.__window[row][column + index]
        except:
            pass
        return temp

    def window(self):
        temp = list()
        # Copy window to temp.
        for row in self.__window:
            temp.append(row[:])
        return temp

    def append(self, instance):
        # Only append windows to windows.
        if instance.__class__ is self.__class__:
            self.__windows.append(instance)

    def remove(self, instance):
        # Try to remove instance.
        try:
            self.__windows.remove(instance)
        except:
            pass

    def __getitem__(self, index):
        # Try to return instance.
        try:
            return self.__windows[index]
        except:
            pass

    def __str__(self):
        # Return representation of self.
        temp = str()
        for row in self.__windows:
            for character in row:
                temp += character
        return temp

# WINDOW THEORY V1
# ================
# Windows should contain zero or more pages.
# Windows should contain zero or more windows.
# ----------------
# Pages should be buffers that cannot be resized once created.
# Pages should be in the form of 2D list.
# Pages should be editable.
# Pages should be able to return a plain representation of their contents (a copy of the 2D list).
# ----------------
# (INCOMPLETE)

# GENERAL THEORY V2
# =================
#
# Page Theory
# ===========
# A page is a buffer.
# A page is created with a size that cannot be changed.
# Internally, a page is a 2D list of length 1 strings.
# The contents of a page can be edited with length 1 strings.
# A page can be created with a default cell value;
#     otherwise, the value is a space.
# A copy of the internal buffer of a page can be returned.
# A string representation of a page can be returned;
#     there is to be no newline added to the last row of a page.
#
# Window Theory
# =============
# A window is created with a size, outline (which can be None etc. or a length 1 string), and background (a length 1 string [defaults to space]).
# A window can contain 0 or more pages and 0 or more windows.
# A window can have an outline (1 character); otherwise, it does not have an outline.
# A window can have a background character; otherwise, the background is a space.
# A window must have a size.
# Internally, besides outline, background, and size, a windows consists of a list of information (page(s) and window(s) etc.).
# The list consists of lists of the following information: position of the object, the object, and if the object is visible (displayed).
# The ordering of the list indicates what object is on top of another object; list[0] is the bottom-most object to be displayed.
# A look of a window can be returned as a 2D list (so that it has the same form as a page).
# A string representation of the window can be returned and does not have a newline tacked onto its end.
#
# =============
# Ultimately, windows should be able to be printed, along with all of the window's contents and sub-contents.
# Windows should not be reversible; pages might optionally be reversible to show only a second side.

# This is the first version of the page class.
class page_v1: # VERSION 1.0

    def __init__(self, rows, columns, default = None):
        # (page_v1, int, int, str)
        if default is None:
            default = ' '
        self.__page = list()
        for index in range(rows):
            self.__page.append(list(default[0] * columns))

    def mutate(self, row, column, string):
        # (page_v1, int, int, str)
        try:
            if row >= 0:
                for index in range(len(string)):
                    if column + index >= 0:
                        self.__page[row][column + index] = string[index]
        except:
            pass

    def access(self, row, column, length = 1):
        # (page_v1, int, int, int)
        string = str()
        try:
            for index in range(length):
                string += self.__page[row][column + index]
        except:
            pass
        return string

    def internal(self):
        # (page_v1)
        array = list()
        for row in self.__page:
            array.append(row[:])
        return array

    def __str__(self):
        # (page_v1)
        string = str()
        for row in self.__page:
            for character in row:
                string += character
            string += '\n'
        return string[:-1]

# This is the first version of a theoretical window.
class window_v1: # VERSION 1.4

    def __init__(self, height, width, border = None, background = None):
        # (window_v1, int, int, str, str)
        self.__height = height
        self.__width = width
        self.__border = border
        self.__background = background
        self.__draw = True
        self.__buffer = None
        self.__contents = list()

    def append(self, instance, position, visible = True, index = None):
        # (window_v1, page_v1 OR window_v1, [int, int], bool, int)
        self.__draw = True
        if index is None:
            self.__contents.append([instance, position, visible])
        else:
            self.__contents.insert(index, [instance, position, visible])

    def remove(self, instance):
        # (window_v1, page_v1 OR window_v1)
        for index in range(len(self.__contents)):
            if instance is self.__contents[index][0]:
                self.__draw = True
                del self.__contents[index]

    def __getitem__(self, index):
        # (window_v1, int)
        self.__draw = True
        return self.__contents[index]

    def __delitem__(self, index):
        # (window_v1, int)
        self.__draw = True
        del self.__contents[index]

    def size(self, height = None, width = None):
        # (window_v1, int, int)
        if height is not None:
            self.__draw = True
            self.__height = height
        if width is not None:
            self.__draw = True
            self.__width = width
        if height is None and width is None:
            return self.__height, self.__width

    def look(self, border = 0, background = 0):
        # (window_v1, str, str)
        if border is not 0:
            self.__draw = True
            self.__border = border
        if background is not 0:
            self.__draw = True
            self.__background = background
        if border is 0 and background is 0:
            return self.__border, self.__background

    def __update(self):
        # (window_v1)
        if self.__draw:
            self.__draw = False
            self.__buffer = page_v1(self.__height, self.__width, self.__background)
            for item in self.__contents:
                if item[2]:
                    internal = item[0].internal()
                    for row in range(len(internal)):
                        for column in range(len(internal[0])):
                            self.__buffer.mutate(row + item[1][0], column + item[1][1], internal[row][column])
            if self.__border is not None:
                self.__buffer.mutate(0, 0, self.__border[0] * self.__width)
                self.__buffer.mutate(self.__height - 1, 0, self.__border[0] * self.__width)
                for row in range(1, self.__height - 1):
                    self.__buffer.mutate(row, 0, self.__border[0])
                    self.__buffer.mutate(row, self.__width - 1, self.__border[0])

    def internal(self):
        # (window_v1)
        self.__update()
        return self.__buffer.internal()

    def __str__(self):
        # (window_v1)
        self.__update()
        return str(self.__buffer)
