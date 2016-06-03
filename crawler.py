from chess_exceptions import ParserNotSetException
from parser import Parser
from link import Link
import urllib2
import urlparse
from Queue import Queue
from multiprocessing.dummy import Pool as ThreadPool
import threading


class Crawler(threading.Thread):
    def __init__(self, seed_urls, domains, parser=Parser()):
        super(Crawler, self).__init__()

        self.seed_urls = seed_urls
        self.domains = domains
        self.parser = parser
        self.links = []
        self.pool = ThreadPool(4)

        for seed_url in seed_urls:
            self.links.append(Link(seed_url))

    @staticmethod
    def fetch_page(link):
        url = link.link
        if link is None or link.link is None:
            return None
        if len(link.link.strip()) == 0:
            return None
        if link.parent is not None:
            url = urlparse.urljoin(link.parent, url)
        if not url.startswith('http'):
            url = 'http://' + url
        try:
            response = urllib2.urlopen(url)
        except Exception, e:
            print "ERROR: " + e.message
            return None
        return response.read()

    def parse_page(self, link, content):
        if self.parser is None:
            raise ParserNotSetException
        content_links = self.parser.parse(content)
        for content_link in content_links:
            if content_link in self.links:
                continue
            print "added link " + content_link
            self.links.append(Link(content_link, link))

    def process_page(self, link):
        print "fetching page " + link.link
        content = self.fetch_page(link)
        if content is None:
            return
        print "got page " + link.link
        self.parse_page(link, content)

    def run(self):
        self.pool.map(self.process_page, self.links, None)
        self.pool.close()
        self.pool.join()
        return
