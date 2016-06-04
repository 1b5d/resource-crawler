"""
module that contains parsers used by the crawler.
"""

from bs4 import BeautifulSoup
from link import Link


class Parser(object):
    """
    Class Parser that represents a parser to be used by the crawler class.
    """

    attrs = {
        'img': 'src',
        'script': 'src',
        'link': 'href',
        'video': 'src',
        'audio': 'src',
        'iframe': 'src',
        'embed': 'src',
        'object': 'data',
        'source': 'src',
    }

    @staticmethod
    def parse(content):
        """
        parse contents and extract different types of links in it.

        :param str content: content of the parsed page.
        :return: a generator of Link objects.
        """
        soup = BeautifulSoup(content)

        # extract `a` links
        for link in soup.find_all('a', href=True):
            yield Link(link['href'])

        for tag, attr in Parser.attrs.iteritems():
            for link in soup.find_all(tag, {attr: True}):
                yield Link(link[attr], Link.TYPE_RESOURCE, tag)
