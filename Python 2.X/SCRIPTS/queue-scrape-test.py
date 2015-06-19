from __future__ import print_function
from BeautifulSoup import BeautifulSoup
import time
import threading
from Queue import Queue
import requests

DOMAIN = 'http://www.usatoday.com'


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


def scraper_worker(q):
    while not q.empty():
        url = q.get()
        print("{} found {} paragraphs on {}".format(
            threading.current_thread().name,
            len(scrape_paragraphs(url)),
            url))
        q.task_done()
    return


def get_top_story_links():
    return scrape_links('/feeds/live/news?count=40')


@timing
def main():
    links_to_scrape = get_top_story_links()
    q = Queue()
    for link in links_to_scrape:
        q.put(link)
    num_processes = len(links_to_scrape) / 10
    print("Spawning {} threads".format(num_processes))
    for i in range(num_processes):
        p = threading.Thread(
            target=scraper_worker, args=(q,))
        p.start()
    q.join()

if __name__ == "__main__":
    main()
