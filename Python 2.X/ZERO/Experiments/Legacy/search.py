from httplib import HTTPConnection

def main():
    global search_key
    search_key = ('', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', \
                   'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', \
                   'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z')
    run_am()

def run_am():
    for a in search_key:
        for b in search_key:
            for c in search_key:
                for d in search_key:
                    for e in search_key:
                        for f in search_key:
                            for g in search_key:
                                for h in search_key:
                                    for i in search_key:
                                        for j in search_key:
                                            for k in search_key:
                                                for l in search_key:
                                                    for m in search_key:
                                                        run_nz('/' + a + b + c + d + e + f + g + h + i + j + k + l + m)



def run_nz(url):
    for n in search_key:
        for o in search_key:
            for p in search_key:
                for q in search_key:
                    for r in search_key:
                        for s in search_key:
                            for t in search_key:
                                for u in search_key:
                                    for v in search_key:
                                        for w in search_key:
                                            for x in search_key:
                                                for y in search_key:
                                                    for z in search_key:
                                                        test(url + n + o + p + q + r + s + t + u + v + w + x + y + z)

def test(url):
    connection = HTTPConnection('127.0.0.1')
    connection.request('GET', url)
    if connection.getresponse().status != 404:
        print url

if __name__ == '__main__':
    main()
