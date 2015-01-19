import html_help
import os
import sys
import time
import Zcgi

KEYS = 'description', 'start', 'end', 'sunday', 'monday', \
       'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'

class soft_dict:
    
    def __init__(self, dictionary, format):
        self.__dictionary = dictionary
        self.__format = format
        
    def __getitem__(self, key):
        try:
            if self.__dictionary[key]:
                return self.__format % self.__dictionary[key]
        except:
            pass
        return ''

class WeekError:

    def __init__(self, string):
        self.__string = string

    def __str__(self):
        return self.__string

def main():
    if Zcgi.dictionary is None:
        show_form()
    elif has_keys(Zcgi.dictionary, KEYS):
        show_table()
    else:
        show_form()

def show_form(error=''):
    if error:
        error = '\t\t<b>' + error + '</b>\n'
    values = soft_dict(Zcgi.dictionary, ' value="%s"')
    Zcgi.print_html('''<html>
\t<head>
\t\t<title>
\t\t\tSchedule Maker
\t\t</title>
\t</head>
\t<body>
%s\t\t<form action="%s">
\t\t\tDescription:<br>
\t\t\t<input type="text"%s name="description" size="25"><br>
\t\t\tStart Date:<br>
\t\t\t<input type="text"%s name="start" size="25"><br>
\t\t\tEnd Date:<br>
\t\t\t<input type="text"%s name="end" size="25"><br>
\t\t\tSunday:<br>
\t\t\t<input type="text"%s name="sunday" size="25"><br>
\t\t\tMonday:<br>
\t\t\t<input type="text"%s name="monday" size="25"><br>
\t\t\tTuesday:<br>
\t\t\t<input type="text"%s name="tuesday" size="25"><br>
\t\t\tWednesday:<br>
\t\t\t<input type="text"%s name="wednesday" size="25"><br>
\t\t\tThursday:<br>
\t\t\t<input type="text"%s name="thursday" size="25"><br>
\t\t\tFriday:<br>
\t\t\t<input type="text"%s name="friday" size="25"><br>
\t\t\tSaturday:<br>
\t\t\t<input type="text"%s name="saturday" size="25"><br>
\t\t\t<input type="submit" value="Create Schedule">
\t\t</form>
\t</body>
</html>''' % tuple([error, os.path.basename(sys.argv[0])] \
                   + unpack(values, KEYS)))

def has_keys(dictionary, keys):
    for key in keys:
        if not dictionary.has_key(key):
            return False
    return True

def show_table():
    values = Zcgi.dictionary
    if not values['description']:
        show_form('You must enter a description.')
    try:
        start = time.strptime(values['start'], '%m/%d/%y')
        end = time.strptime(values['end'], '%m/%d/%y')
    except:
        show_form('Dates must be in the MM/DD/YY format.')
    try:
        assert time.mktime(end) > time.mktime(start)
    except:
        show_form('The end date must come after the start date.')
    try:
        check_week(values, KEYS[3:])
    except WeekError, problem:
        show_form(str(problem))
    html = create_html(values['description'], start, end, unpack(values, KEYS[3:]))
    Zcgi.print_html(html)

def unpack(values, keys):
    unpacked = []
    for key in keys:
        unpacked.append(values[key])
    return unpacked

def check_week(dictionary, keys):
    for key in keys:
        try:
            if not dictionary[key]:
                continue
            hm = dictionary[key].split('-')
            assert len(hm) == 2
            first = time.strptime(hm[0].strip(), '%H:%M')
            second = time.strptime(hm[1].strip(), '%H:%M')
            dictionary[key] = hm[0].strip() + ' - ' + hm[1].strip()
        except:
            raise WeekError(key.capitalize() + ' should be in the HH:MM - HH:MM format.')
        try:
            assert second.tm_hour * 60 + second.tm_min > first.tm_hour * 60 + first.tm_min
        except:
            raise WeekError('Start time must come before end time on ' + key.capitalize() + '.')

def create_html(description, start, end, week):
    html = '''<html>
\t<head>
\t\t<title>
\t\t\tThe Schedule
\t\t</title>
\t</head>
\t<body>
\t\t<center>
'''
    start_month = start.tm_year * 12 + (start.tm_mon - 1)
    end_month = end.tm_year * 12 + (end.tm_mon - 1)
    for month in range(start_month, end_month + 1):
        html += html_help.html_table(1, 1, 3, '\t').mutate(0, 0, create_month_html(description, start, end, week, month)).html() + '\n'
        if month != end_month:
            html += '\t\t\t<hr>\n'
    return html + '\t\t</center>\n\t</body>\n</html>'

def create_month_html(description, start, end, week, month):
    start = time.mktime(start) - 43200
    end = time.mktime(end) + 43200
    now = time.strptime(str((month / 12) % 100).zfill(2) + ' ' +  str(month % 12 + 1) + ' 01', '%y %m %d')
    html = '<b>' + time.strftime('%B %Y', now) + '</b>\n'
    html_month = html_help.html_month((month / 12) % 100, month % 12 + 1, 0, '\t')
    html_month.table_option('border="1" width="800"').row_option('valign="top"').column_option('width="14%"')
    now_month = now.tm_mon
    while now.tm_mon == now_month:
        mktime = time.mktime(now)
        if start <= mktime <= end:
            week_day = (now.tm_wday + 1) % 7
            if week[week_day]:
                html_month.mutate(now.tm_mday, '<b>' + description + '</b><br>\n' + week[week_day])
        now = time.localtime(mktime + 86400)
    return html + html_month.html()

if __name__ == '__main__':
    Zcgi.execute(main, 'cgi')
