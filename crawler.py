from chess_exceptions import ParserNotSetException
from parser import Parser
from thread_pool import ThreadPool
from link import Link
from threading import Thread
import urllib2
import urlparse


class Crawler(Thread):
    def __init__(self, seed_urls, domains, parser=Parser()):
        super(Crawler, self).__init__()
        self.seed_urls = seed_urls
        self.domains = domains
        self.parser = parser
        self.links = {}
        self.pool = ThreadPool(4)

        for seed_url in seed_urls:
            self.links[seed_url] = Link(seed_url)

    @staticmethod
    def fetch_page(link):
        print 'Downloading URL: ' + link.link
        url = link.link
        if link is None or link.link is None:
            return None
        if len(link.link.strip()) == 0:
            return None
        try:
            response = urllib2.urlopen(url)
        except Exception, e:
            return None
        return response.read()

    def parse_page(self, link, content):
        if self.parser is None:
            raise ParserNotSetException
        content_links = self.parser.parse(content)
        for content_link in content_links:
            url = urlparse.urljoin(link.link, content_link)
            if not url.startswith('http'):
                url = 'http://' + url
            parsed_url = urlparse.urlparse(url)
            if parsed_url.netloc not in self.domains:
                continue
            if self.links.get(url) is not None:
                continue
            self.links[url] = Link(url, link)
            # self.pool.add_task(self.process_page, Link(url, link))
            self.process_page(Link(url, link))

    def process_page(self, link):
        print 'Processing URL: ' + link.link
        content = self.fetch_page(link)
        if content is None:
            return
        self.parse_page(link, content)
        return

    def run(self):
        for link in self.links.values():
            # self.pool.add_task(self.process_page, link)
            self.process_page(link)
        self.pool.wait_completion()
        return

