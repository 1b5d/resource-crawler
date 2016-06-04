from crawler_exceptions import CrawlerException
from crawler import Crawler
from sitemap import Generator
import time
import codecs

if __name__ == '__main__':
    start = time.time()
    crawler = Crawler(['http://gocardless.com'], ['gocardless.com'], 20, verbose=True)
    try:
        crawler.start()
    except CrawlerException, e:
        print 'An error occurred while executing the crawler: %s' % e.message
    except Exception, e:
        print 'An error occurred while executing the crawler: %s' % e.message

    generator = Generator(crawler.links)
    with codecs.open('output.html', 'w', encoding='utf-8') as f:
        f.write(generator.get_html())
    f.close()

    print "Time: %.2f seconds" % (time.time() - start)
