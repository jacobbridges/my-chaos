import cgitb; cgitb.enable()

from xml_stream import *
import xml.sax.xmlreader
import xml.sax.saxutils
import StringIO
import getpass
import z_html
import z_cgi
import sys
import os

################################################################################

FIRST_FORM = '''\
<html>
    <head>
        <title>
            Calendar Maker
        </title>
    </head>
        <center>%s
            <table>
                <tr>
                    <td>
                        <form method="post" action="%s">
                            <table>
                                <tr>
                                    <td>
                                        Month:
                                    </td>
                                    <td>
                                        <input type="text" name="month">
                                    </td>
                                </tr>
                                <tr>
                                    <td>
                                        Year:
                                    </td>
                                    <td>
                                        <input type="text" name="year">
                                    </td>
                                </tr>
                                <tr>
                                    <td>
                                        <input type="submit" value="New" name="select">
                                    </td>
                                    <td>
                                    </td>
                                </tr>
                            </table>
                            <hr>
                            <table>
                                <tr>
                                    <td>
                                        File:
                                    </td>
                                    <td>
                                        <input type="file" name="filename">
                                    </td>
                                </tr>
                                <tr>
                                    <td>
                                        <input type="submit" value="Load" name="select">
                                    </td>
                                    <td>
                                    </td>
                                </tr>
                            </table>
                        </form>
                        <hr>
                        <a href="http://127.0.0.1:8080/"><b><font color="red">Shutdown</font></b></a>
                    </td>
                </tr>
            </table>
        </center>
    </body>
</html>'''

################################################################################

SECOND_FORM = '''\
<html>
    <head>
        <title>%s</title>
    </head>
    <body>
        <form method="post" action="%s">
            <input type="hidden" name="month" value="%s">
            <input type="hidden" name="year" value="%s">
%s
%s
        </form>
    </body>
</html>'''

################################################################################

THIRD_FORM = '''\
<html>
    <head>
        <title>
            %s
        </title>
    </head>
    <body>
%s
    </body>
</html>'''

################################################################################

def main():
    if z_cgi.dictionary.has_key('select'):
        try:
            show_month()
        except Exception, error:
            if isinstance(error, SystemExit): raise
            show_first('\n            <h1><font color="red"><u>ERROR</u></font></h1>')
    elif z_cgi.dictionary.has_key('month'):
        show_print()
    else:
        show_first()

def show_first(error=''):
    z_cgi.print_html(FIRST_FORM % (error, os.path.basename(sys.argv[0])))

def show_month():
    # region V2
    try:
        error = True
        try:
            month = int(z_cgi.dictionary['month'])
            error = False
        except:
            m = z_cgi.dictionary['month'].lower()
            for month, name in enumerate(z_html.calendar.month_name):
                if name.lower().startswith(m):
                    error = False
                    break
        assert not error
        year = int(z_cgi.dictionary['year'])
        create_month_form(year, month)
    except Exception, error:
        if isinstance(error, SystemExit): raise
        assert z_cgi.dictionary['select'] == 'Load'
        create_month_form()
    # endregion

# region V2
class MonthParser:

    def __init__(self):
        self.days = {}
        self.__month = False
        self.__year = False
        self.__textarea = None

    def __getattr__(self, name):
        return Event

    def startElement(self, name, attrs):
        if name == 'Month':
            self.__month = True
        elif name == 'Year':
            self.__year = True
        elif name == 'TextArea':
            self.__textarea = attrs.getValue('day')

    def characters(self, content):
        if self.__month:
            self.__month = False
            self.month = int(content)
        elif self.__year:
            self.__year = False
            self.year = int(content)
        elif self.__textarea is not None:
            self.days[int(self.__textarea)] = str(content)
            self.__textarea = None
# endregion

def create_month_form(year=None, month=None):
    # region V2
    if z_cgi.dictionary['select'] == 'Load':
        load = True
        filename = os.path.join('C:\\Documents and Settings\\%s\\Desktop' % getpass.getuser(), z_cgi.dictionary['filename'])
        s = Stream(filename)
        s.minimize()
        parser = MonthParser()
        s.parse(parser)
        year = parser.year
        month = parser.month
    else:
        load = False
    # endregion
    m_a_y = '%s %s' % (z_html.calendar.month_name[month], year)
    h_month = z_html.HTML_Month(month, year, 0, '    ')
    h_month.set_month(height='100%', width='100%', border=1)
    h_month.set_week(valign='top')
    h_month.set_day(width='14%')
    for x in range(z_html.calendar.monthrange(year, month)[1]):
        # region V2
        if load:
            try:
                h_month.mutate(x + 1, '<textarea name="ta%s">%s</textarea>' % (x, parser.days[x]))
                h_month.special(x + 1, True)
            except:
                h_month.mutate(x + 1, '<textarea name="ta%s"></textarea>' % x)
        else:
            h_month.mutate(x + 1, '<textarea name="ta%s"></textarea>' % x)
        # endregion
    h_table = z_html.HTML_Table(1, 1, 3, '    ')
    if load:
        h_table.special(0, 0, True)
    h_table.mutate(0, 0, '<b>%s</b>\n%s' % (m_a_y, h_month.html()))
    h_table.set_table(width='100%', height='100%')
    # region V2
    controls = z_html.HTML_Table(2, 3, 3, '    ')
    controls.mutate(0, 0, 'HTML:')
    controls.mutate(0, 1, '<input type="text" name="filename" value="%s.htm">' % m_a_y)
    controls.mutate(0, 2, '<input type="submit" value="Create" name="action">')
    controls.mutate(1, 0, 'XML:')
    controls.mutate(1, 1, '<input type="text" name="xml", value="%s.xml">' % m_a_y)
    controls.mutate(1, 2, '<input type="submit" value="Save" name="action">')
    # endregion
    data = SECOND_FORM % (m_a_y,
                          os.path.basename(sys.argv[0]),
                          month,
                          year,
                          h_table.html(),
                          controls.html())
    z_cgi.print_html(data)

def show_print():
    month = int(z_cgi.dictionary['month'])
    year = int(z_cgi.dictionary['year'])
    create_print(month, year)

def create_print(month, year):
    # region V2
    if z_cgi.dictionary['action'] == 'Save':
        save = True
        stream = [startDocument(),
                  startElement('Calendar', xml.sax.xmlreader.AttributesImpl({})),
                  startElement('Date', xml.sax.xmlreader.AttributesImpl({})),
                  startElement('Month', xml.sax.xmlreader.AttributesImpl({})),
                  characters(str(month)),
                  endElement('Month'),
                  startElement('Year', xml.sax.xmlreader.AttributesImpl({})),
                  characters(str(year)),
                  endElement('Year'),
                  endElement('Date'),
                  startElement('Days', xml.sax.xmlreader.AttributesImpl({}))]
    else:
        save = False
    # endregion
    m_a_y = '%s %s' % (z_html.calendar.month_name[month], year)
    h_month = z_html.HTML_Month(month, year, 0, '    ')
    h_month.set_month(height='100%', width='100%', border=1)
    h_month.set_week(valign='top')
    h_month.set_day(width='14%')
    for x in range(z_html.calendar.monthrange(year, month)[1]):
        h_month.mutate(x + 1, '<br>'.join(z_cgi.dictionary['ta%s' % x].splitlines()))
        # region V2
        if save and z_cgi.dictionary['ta%s' % x]:
            stream.extend([startElement('TextArea', xml.sax.xmlreader.AttributesImpl({'day': str(x)})),
                           characters(z_cgi.dictionary['ta%s' % x]),
                           endElement('TextArea')])
        # endregion
    h_table = z_html.HTML_Table(1, 1, 2, '    ')
    h_table.mutate(0, 0, '<b>%s</b>\n%s' % (m_a_y, h_month.html()))
    h_table.set_table(width='100%', height='100%')
    # region V2
    name = 'C:\\Documents and Settings\\%s\\Desktop' % getpass.getuser()
    if save:
        stream.extend([endElement('Days'),
                       endElement('Calendar'),
                       endDocument()])
        data = StringIO.StringIO()
        xml_gen = xml.sax.saxutils.XMLGenerator(data)
        for event in stream:
            event(xml_gen)
        stream = Stream(data.getvalue())
        stream.maximize('    ')
        stream.parse(xml.sax.saxutils.XMLGenerator(file(os.path.join(name, z_cgi.dictionary['xml']), 'w')))
    # endregion
    data = THIRD_FORM % (m_a_y, h_table.html())
    # region V2
    if z_cgi.dictionary['action'] == 'Create':
        file(os.path.join(name, z_cgi.dictionary['filename']), 'w').write(data)
    # endregion
    z_cgi.print_html(data)

if __name__ == '__main__':
    z_cgi.execute(main, 'code')
