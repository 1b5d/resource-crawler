from crawler_exceptions import ParserNotSetException, CrawlerRuntimeError
from parser import Parser
from link import Link
from Queue import Queue, Empty
import utils
import urllib3
import workerpool

urllib3.disable_warnings()


class Crawler(object):
    def __init__(self, seed_urls, domains, num_threads=8, parser=Parser(), verbose=False):
        super(Crawler, self).__init__()
        self.seed_urls = seed_urls
        self.verbose = verbose
        self.domains = domains
        self.parser = parser
        self.links = {}
        self.queue = Queue()
        self.pool = workerpool.WorkerPool(size=num_threads)
        self.connection_pool = urllib3.PoolManager(
            maxsize=max(int(num_threads * 0.9), 1)
        )

    def fetch_page(self, link):
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
        content = self.fetch_page(link)
        if content is None:
            return
        self.parse_page(link, content)
        return

    def consume_pages(self, worker_num):
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

