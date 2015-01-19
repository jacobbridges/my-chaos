import httplib, random

def main():
    random.seed()
    number = random.randint(1311, 7366)
    while not check_URL('home.bju.edu', '/vintage_images/stu_ed%s.jpg' % number):
        number = random.randint(1311, 7366)
    print '''Content-Type: text/html

<html>
\t<head>
\t\t<title>
\t\t\tVintage Pictures
\t\t</title>
\t\t<meta http-equiv="refresh" content="5">
\t</head>
\t<body>
\t\t<table height="100%%" width="100%%">
\t\t\t<tr>
\t\t\t\t<td align="center">
\t\t\t\t\t<img src="https://home.bju.edu/vintage_images/stu_ed%s.jpg">
\t\t\t\t</td>
\t\t\t</tr>
\t\t</table>
\t</body>
</html>''' % number

def check_URL(host, url):
    connection = httplib.HTTPSConnection(host)
    connection.request('HEAD', url)
    return connection.getresponse().status == 200

if __name__ == '__main__':
    main()
