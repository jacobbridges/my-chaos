from __future__ import print_function
from BeautifulSoup import BeautifulSoup
import time
import multiprocessing
import requests

DOMAIN = 'http://www.usatoday.com'


def chunks(l, n):
    for i in xrange(0, len(l), n):
        yield l[i:i + n]


def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print('%s function took %0.3f ms' % (f.func_name,
              (time2 - time1) * 1000.0))
        return ret
    return wrap


def get_href(a):
    try:
        return a['href']
    except KeyError:
        print(a)


def scrape_links(url):
    time.sleep(0.1)
    if url.startswith('http'):
        r = requests.get(url)
    else:
        r = requests.get(DOMAIN + url)
    soup = BeautifulSoup(r.text)
    return map(get_href, soup.findAll('a'))


def scrape_paragraphs(url):
    time.sleep(0.1)
    if url.startswith('http'):
        r = requests.get(url)
    else:
        r = requests.get(DOMAIN + url)
    soup = BeautifulSoup(r.text)
    return soup.findAll('p')


@timing
def scraper_worker(*urls):
    for url in urls:
        print("{} found {} paragraphs on {}".format(
            multiprocessing.current_process().name,
            len(scrape_paragraphs(url)),
            url))
    return


def get_top_story_links():
    return list(chunks(scrape_links('/feeds/live/news?count=40'), 10))


def main():
    links_to_scrape = get_top_story_links()
    print("Spawning {} processes".format(len(links_to_scrape)))
    for i in range(len(links_to_scrape)):
        p = multiprocessing.Process(
            target=scraper_worker, args=(links_to_scrape[i]))
        p.start()
    return

if __name__ == "__main__":
    main()
