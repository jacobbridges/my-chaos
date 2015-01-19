import time
import Zam

class html_table:

    def __init__(self, rows, columns, indent, style):
        self.__matrix = Zam.matrix(rows, columns, '')
        self.__indent = indent
        self.__style = style
        self.__table_option = ''
        self.__row_option = ''
        self.__column_option = ''

    def mutate(self, row, column, text):
        assert type(text) is str
        self.__matrix[row][column] = text
        return self

    def access(self, row, column):
        return self.__matrix[row][column]

    def table_option(self, string):
        assert type(string) is str
        self.__table_option = string
        return self

    def row_option(self, string):
        assert type(string) is str
        self.__row_option = string
        return self

    def column_option(self, string):
        assert type(string) is str
        self.__column_option = string
        return self

    def html(self):
        html = self.__style * self.__indent + '<table'
        if self.__table_option:
            html += ' ' + self.__table_option
        html += '>\n'
        for row in self.__matrix:
            html += self.__style * (self.__indent + 1) + '<tr'
            if self.__row_option:
                html += ' ' + self.__row_option
            html += '>\n'
            for item in row:
                html += self.__style * (self.__indent + 2) + '<td'
                if self.__column_option:
                    html += ' ' + self.__column_option
                html += '>\n'
                html += ''.join([self.__style * (self.__indent  + 3) + line + '\n' for line in item.splitlines()])
                html += self.__style * (self.__indent + 2) + '</td>\n'
            html += self.__style * (self.__indent + 1) + '</tr>\n'
        return html + self.__style * self.__indent + '</table>'

class html_month:

    def __init__(self, year, month, indent, style):
        matrix = self.__make_matrix(year, month)
        self.__table = html_table(len(matrix) + 1, 7, indent, style)
        for index, item in enumerate(('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday')):
            self.__table.mutate(0, index, '<b>' + item + '</b>')
        for row in range(len(matrix)):
            for column in range(7):
                if matrix[row][column]:
                    self.__table.mutate(row + 1, column, '<b>' + str(matrix[row][column]).zfill(2) + '</b>\n<hr>\n')

    def __make_matrix(self, year, month):
        rows = [Zam.array(7, 0)]
        row = 0
        now = time.localtime(time.mktime(time.strptime(str(year).zfill(2) + ' ' + str(month).zfill(2) + ' 01', '%y %m %d')) + 14400)
        self.__first_day = (now.tm_wday + 1) % 7
        once = False
        while now.tm_mon == month:
            if once:
                if now.tm_wday == 6:
                    rows.append(Zam.array(7, 0))
                    row += 1
            else:
                once = True
            rows[row][(now.tm_wday + 1) % 7] = now.tm_mday
            self.__days_in_month = now.tm_mday
            now = time.localtime(time.mktime(now) + 86400)
        return rows

    def mutate(self, day, text):
        row, column = self.__get_pos(day)
        self.__table.mutate(row, column, self.__table.access(row, column)[:15] + text)
        return self

    def access(self, day):
        row, column = self.__get_pos(day)
        return self.__table.access(row, column)[15:]

    def __get_pos(self, day):
        assert 1 <= day <= self.__days_in_month
        pos = self.__first_day - 1 + day
        return pos / 7 + 1, pos % 7

    def table_option(self, string):
        self.__table.table_option(string)
        return self

    def row_option(self, string):
        self.__table.row_option(string)
        return self

    def column_option(self, string):
        self.__table.column_option(string)
        return self

    def html(self):
        return self.__table.html()
