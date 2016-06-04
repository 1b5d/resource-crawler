from crawler_exceptions import CrawlerException
from crawler import Crawler

if __name__ == '__main__':
    crawler = Crawler(['https://qordoba.com'], ['qordoba.com'], 20)
    try:
        crawler.start()
    except CrawlerException, e:
        print 'An error occurred while executing the crawler: %s' % e.message
    except Exception, e:
        print 'An error occurred while executing the crawler: %s' % e.message
