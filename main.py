from crawler import Crawler

if __name__ == '__main__':
    crawler = Crawler(['gocardless.com'], ['gocardless.com'])
    crawler.start()