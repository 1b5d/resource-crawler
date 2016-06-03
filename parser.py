from bs4 import BeautifulSoup


class Parser(object):
    def __init__(self):
        pass

    @staticmethod
    def parse(content):
        soup = BeautifulSoup(content)
        for link in soup.find_all('a', href=True):
            if link.has_attr('href'):
                yield link['href']
