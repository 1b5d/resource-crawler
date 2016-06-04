"""
Module that contains the main Crawler class.
"""

from crawler_exceptions import ParserNotSetException, CrawlerRuntimeError
from parser import Parser
from link import Link
from Queue import Queue, Empty
import utils
import urllib3
import workerpool

urllib3.disable_warnings()


class Crawler(object):
    """
    Class Crawler crawls a website to get all the links and resources.
    """
    def __init__(self, seed_urls, domains, num_threads=8,
                 parser=Parser(), verbose=False):
        """
        initializes the Crawler class with necessary arguments

        :param List seed_urls: a list of starting points of the crawler.
        :param List domains: a list of domains to restrict the crawling to.
        :param int num_threads: number of workers to crawl the website in parallel.
        By default, the crawler is set with 8 threads.
        :param Parser parser: the parser object that is used in the crawler.
        By default, an object of the parser.Parser class is used.
        :param bool verbose: whether to output execution updates to the console.
        :return: None.
        """
        super(Crawler, self).__init__()
        self.seed_urls = seed_urls
        self.verbose = verbose
        self.domains = domains
        self.parser = parser
        self.links = {}
        self.queue = Queue()
        self.pool = workerpool.WorkerPool(size=num_threads)

        # initialize a connection pool to be used to make concurrent
        # requests to fetch pages' contents
        # the number of connection pool sockets will be 90% of the number of thread
        # to make some availability for page processing like parsing ...etc.
        self.connection_pool = urllib3.PoolManager(
            maxsize=max(int(num_threads * 0.9), 1)
        )

    def fetch_page(self, link):
        """
        requests a page by URL and returns its content.

        :param Link link: a link object that contains the URL to be requested
        :return: str the content of the page requested.
        """
        if link is None or link.link is None:
            return None
        if len(link.link.strip()) == 0:
            return None

        content = None

        try:
            r = self.connection_pool.request('GET', link.link)
            content = r.data
        except Exception:
            if self.verbose:
                print 'Link %s was broken' % link.link
        return content

    def parse_page(self, link, content):
        """
        parses a content of a page and adds its links to the processing queue.

        :param Link link: a link object that contains the URL of the parsed page.
        :param str content: the content to be parsed
        :return: None.
        """
        if self.parser is None:
            raise ParserNotSetException()
        content_links = self.parser.parse(content)
        for content_link in content_links:
            content_link.parent = link

            if utils.get_url_domain(content_link.link) not in self.domains:
                continue

            key_url = utils.strip_http(content_link.link)
            # check if the link has already been crawled
            if self.links.get(key_url) is not None:
                continue
            self.links[key_url] = content_link

            # add the link to the queue
            if content_link.link_type == Link.TYPE_HYPERLINK:
                self.queue.put(content_link)

    def process_page(self, link):
        """
        crawls a link off the processing queue.

        :param Link link: a link object that has the URL of the page to be processed.
        :return: None.
        """
        content = self.fetch_page(link)
        if content is None:
            return
        self.parse_page(link, content)
        return

    def consume_pages(self, worker_num):
        """
        processes the links off the processing queue,
        this method represents a worker and can work in parallel.

        :param worker_num: number of the worker.
        :return: None.
        """
        while True:
            try:
                # give 10 seconds to wait for new links to come in the queue
                # otherwise exit the worker
                link = self.queue.get(block=True, timeout=10)
            except Empty:
                return
            if self.verbose:
                print 'Got URL: %s' % link.link
            try:
                self.process_page(link)
            except Exception, e:
                raise CrawlerRuntimeError(
                    'An error occurred while processing page %s,'
                    ' inner error: [%s]' % (link.link, e.message))

    def start(self):
        """
        starts the crawler.
        this method will initialize a pool of workers
        to be crawling the website in parallel.

        :return: None.
        """
        self.links = {}
        # add seed urls to the processing queue
        for seed_url in self.seed_urls:
            key_url = utils.strip_http(seed_url)
            self.links[key_url] = Link(seed_url)
            self.queue.put(self.links[key_url])

        self.pool.map(self.consume_pages, range(1, self.pool.size() + 1))
        self.pool.join()
        self.pool.shutdown()
        return

