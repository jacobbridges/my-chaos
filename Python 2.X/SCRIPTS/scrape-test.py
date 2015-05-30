from __future__ import print_function
from BeautifulSoup import BeautifulSoup
from time import sleep
import threading
import requests

DOMAIN = 'http://www.usatoday.com'


def chunks(l, n):
    for i in xrange(0, len(l), n):
        yield l[i:i + n]


def get_href(a):
    try:
        return a['href']
    except KeyError:
        print(a)


def scrape_links(url):
    sleep(0.1)
    if url.startswith('http'):
        r = requests.get(url)
    else:
        r = requests.get(DOMAIN + url)
    soup = BeautifulSoup(r.text)
    return map(get_href, soup.findAll('a'))


def scrape_paragraphs(url):
    sleep(0.1)
    if url.startswith('http'):
        r = requests.get(url)
    else:
        r = requests.get(DOMAIN + url)
    soup = BeautifulSoup(r.text)
    return soup.findAll('p')


def scraper_worker(*urls):
    for url in urls:
        print("{} found {} paragraphs on {}".format(
            threading.currentThread().getName(),
            len(scrape_paragraphs(url)),
            url))


def get_top_story_links():
    return list(chunks(scrape_links('/feeds/live/news?count=40'), 10))


def main():
    links_to_scrape = get_top_story_links()
    print("Spawning {} threads".format(len(links_to_scrape)))
    for i in range(len(links_to_scrape)):
        t = threading.Thread(target=scraper_worker, args=(links_to_scrape[i]))
        t.start()

if __name__ == "__main__":
    main()
