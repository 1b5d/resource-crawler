from crawler import Crawler

if __name__ == '__main__':
    crawler = Crawler(['https://gocardless.com/'], ['gocardless.com'])
    crawler.start()

    # from random import randrange
    # from time import sleep
    # from thread_pool import ThreadPool
    #
    # delays = [randrange(1, 10) for i in range(3)]
    #
    # def wait_delay(d):
    #     print 'sleeping for (%d)sec' % d
    #     sleep(d)
    #     delays = [randrange(1, 10) for i in range(3)]
    #     for i, d in enumerate(delays):
    #         pool.add_task(wait_delay, d)
    #
    #
    # pool = ThreadPool(20)
    #
    # for i, d in enumerate(delays):
    #     pool.add_task(wait_delay, d)
    #
    # pool.wait_completion()
